# Effective C++读书笔记(29): 写异常安全的代码

**守则29: 要坚持写异常安全的代码**

> "Strive for exception-safe code"

------

***本篇关键词: 异常安全\***

------

假如我们在给一个GUI写一个可更换背景的菜单类。这个类要在多线程环境里跑，所以我们使用Mutex来上锁:

```text
class PrettyMenu{
  public:
    ...
    void changeBackground(std::istream& imgSrc);
  private:
    Mutex mutex;
    Image* bgImg;  //当前背景图片
    int imgChange; //背景被更改的次数
};
```

考虑以下换壁纸函数的可行方案:

```text
void PrettyMenu::changeBackground(std::istream& imgSrc){
  lock(&mutex);  //上锁
  delete bgImg;  //去掉老背景
  ++imgChange;   //更新计数器
  bgImg = new Image(imgSrc); //装上新背景
  unlock(&mutex); //解锁
}
```

可是从异常安全的角度出发，上面的实现是很危险的。异常安全有两点要求，上面的代码都不能做到。当异常被抛出时，异常安全的函数:

- **不泄露任何资源**。如果上面new这行抛出了异常，unlock的调用就永远不会触发，这个mutex便永远不会解锁。
- **不会让数据结构损坏**。如果还是new这行抛出了异常，bgImg将会指向一个已删除的对象，而且即使没有加上任何新背景，计数器也被更新了。

解决第一个问题相对简单，[第13章](https://zhuanlan.zhihu.com/p/70415131)讲过要用对象管理资源，[第14章](https://zhuanlan.zhihu.com/p/71805363)也介绍了安全管理Mutex的Lock类，那么解决第一个问题的解决方案如下:

```text
void PrettyMenu::changeBackground(std::istream& imgSrc){
  Lock ml(&mutex); //安全的Lock类详见第14章
  delete bgImg;
  ++imgChange;
  bgImg = new Image(imgSrc);
}
```

要解决第二个问题，我们要先了解一下异常安全的级别。函数的异常安全性有如下三种级别:

- 提供**基本保证**(basic  guarantee)的函数可以保证即使抛出了异常，函数也能在有效的状态下运行，没有对象或数据损坏，所有对象也保持内部一致，依然满足类不变量(class  invariant)，但是程序本身则可能处于不确定状态。例如用户使用我们changeBackground方法时抛出了异常，PrettyMenu对象可能依然持有原来的背景，或者持有默认的背景，但具体哪个则是不确定的。



- 提供**强保证**(strong  guarantee)的函数可以保证如果函数抛出了异常，程序的状态不会改变。这就意味着对强保证函数的调用是原子性的(atomic)，如果成功了就成功了，如果失败了就像什么都没有发生一样。强保证函数比基本保证函数更容易使用，因为强保证函数只能导致两种状态，成功或者不变，而基本保证的函数可能引向任何状态。



- 提供**不抛出保证**(nothrow guarantee)的函数保证永远不会抛出异常。例如所有对于基本类型(int，指针等等)的操作都提供不抛出保证。它是异常安全代码的基础。

------

对于异常抛出，可能许多人有这样的一点困惑: 如果我们不给函数规定抛出什么异常，即写一个空的异常规范(exception specification)，那它不就能提供最安全的不抛出保证了吗? 

```text
int doSomething() throw(); //空的异常规范
```

实际上这不是说它不会抛出任何异常，而是如果它抛出了异常，就是一个严重错误，然后触发unexpected()函数，而unexpected()函数默认会触发terminate()，所以它不能提供任何异常安全保证。要记住**异常安全取决于函数的具体实现，而非函数的声明**。

异常安全的代码必须满足上面三条标准中的一条。除非要用到异常不安全的老代码，否则一定要照顾到代码的异常安全性。但当然盲目追求最好也是不切实际的。不抛异常虽完美但显然很难做到。任何用到动态分配内存的动作，例如STL容器，都会在内存不足时抛出bad_alloc异常。所以可行的时候提供不抛出保证，大多数情况下还是要在基本和强保证中做出选择。

至于我们的changeBackground方法，要做到强保证几乎不难。首先把bgImg从裸指针改为智能指针，见[第13章](https://zhuanlan.zhihu.com/p/70415131)，这样就不至于指向一个已删除的无意义的对象，结果就可控了。然后把语句重新排一下，只有正确更新背景后才增加计数器。记住**要在对象保证被改变状态后再更新它所带来的影响**，其实这也和[第26章](https://zhuanlan.zhihu.com/p/84362023)的"推迟变量定义"第有异曲同工之妙:

```text
class PrettyMenu{
  ...
  std::shared_ptr<Image> bgImg; //使用shared_ptr
};
void PrettyMenu::changeBackground(std::istream& imgSrc){
  Lock ml(&mutex);
  bgImage.reset(new Image(imgSrc)); //替换新图片
  ++imgChange; //完成后再更新计数器
};
```

使用了智能指针，我们就不用操心手动delete了。而且shared_ptr::reset函数只有在它包含的"new  Image(imgSrc)"操作成功执行后，原指针才会被删除，新指针才能替代老指针，所以即使new失败了，依然能保证背景还是一样的。而且看我们使用的Lock和std::shared_ptr这两个资源管理类还让代码长度大大减少。越短的代码总体上出错几率越小，也越容易维护。

可我们毕竟说的是上面做到强保证"几乎"不难，那美中不足的是什么?  是imgSrc参数。如果istream&类型的它突然变得不可读了，Image类的构造函数则可能会抛出异常，这种情况我们还没有照顾到，所以在最坏的情况下我们的changeBackground只提供基本保证。

其实这个问题也容易修复，例如把istream类型直接变成包含文件名的字符串，然后在函数本地打开。但像这样**补东补西的方法并不具备普适性**，每个场景都要具体分析，较难应用于实际，这可怎么办呢?

还记得我们在[第25章](https://zhuanlan.zhihu.com/p/83968490)讨论的swap吗?这个方法就叫"copy and swap"。它的原理非常简单: 拷贝你想要改变的对象，然后对拷贝执行操作，如果其中任何一步抛出异常，对象本体不会变。当成功执行完所有操作时，将拷贝和本体调换。

[第25章](https://zhuanlan.zhihu.com/p/83968490)也介绍了pimpl手法(the "pimpl" idiom)作为一种实现基础，即把类包含的数据对象从它本身移除，单独作为另一个类，然后通过指针访问。现在给我们的PrettyMenu使用pimpl:

```text
struct PMImpl{ //PrettyMenuImplementation
  std::shared_ptr<Image> bgImage;
  int imgChange;
};

class PrettyMenu{
  ...
  private:
    Mutex mutex;
    std::shared_ptr<PMImpl> pImpl;
};

void PrettyMenu::changeBackground(std::istream& imgSrc){
  using std::swap;   //这句见第25章
  Lock ml(&mutex);   //使用第14章安全管理mutex的Lock类，上锁
  std::shared_ptr<PMImpl> pNew(new PMImpl(*pImpl)); //生成数据的临时拷贝
  pNew->bgImg.reset(new Image(imgSrc)); //在拷贝上执行操作，用std::shared_ptr::reset替换图片
  ++pNew->imgChange;
  swap(pImpl,pNew); //调换回去
}//解锁
```

为什么我们封装数据要用成员默认公有的struct? 因为它的封装性可以被PrettyMenu的私有接口保证，要接触到其中的数据首先要通过PrettyMenu的私有接口。当然使用class也可以，但可能会不方便一点。

------

copy and swap的方法是实现强异常安全的有效方法，即原子性操作(atomicity)——成功操作或者不做任何操作，但这种方法也有局限性，看下面的代码:

```text
void copySwapDoSomething(){
  ...//生成拷贝
  f1();
  f2();
  ...//拷贝回去
}
```

函数的异常安全性遵循**木桶原理**，即函数的异常安全性取决于它所调用操作的最弱异常安全性。假如f1不能提供强保证，那这个函数最多则只能提供基本保证。如果硬要保证它的强安全性，我们需要在调用f1之前把程序的状态存档，抓住f1抛出的所有异常，然后恢复程序原来的运行状态，显然非常麻烦不太实际。

假如f2根本不能保证异常安全，函数就也不能保证任何异常安全。因为如果f2抛出了异常，损坏了数据结构，整个程序就有可能因此崩溃。

可是就算f1和f2能提供强保证，doSomething也需要额外跟踪它们的操作来实现自己的强安全性。设想假如f1操作成功，f2操作失败，并且f1改变了某个全局变量，这种情况下我们就需要把f1所做的改动也撤回。可是有些改动则是根本不能撤回的，例如对数据库已提交的(committed)改动，用户早就已经看到了。而且swap and copy本身也有效率问题，因为要生成拷贝，对拷贝执行操作，再替换原来的对象，本来就是一个费时费空间的操作。

因此对于强保证，也不能盲目追求，最好的不一定是最合适的，要结合程序对性能和稳定性的需求，函数本身的功能，使用频率，异常安全实现难度和可行性等因素，在**以基本保证作为底线**的情况下追求强保证。当然有条件做到不抛出的话最好。

小结一下，要设计异常安全的系统，第一步要先从堵住资源泄漏开始，使用[资源管理类](https://zhuanlan.zhihu.com/p/70415131)，然后在这三种异常安全性中做出符合实际的选择，只有在使用异常不安全的老代码让你无路可走时才考虑零保证，最后记录下你的决定和原因，为用户和以后的维护考虑。

**总结:**

- 异常安全的函数即使在抛出异常时也不会泄露资源，损坏数据结构。这种安全性有三种级别，基本保证，强保证和不抛出保证
- copy and swap是实现强保证的有效方法，但给所有的函数加上强保证显然也不是实际的选择
- 函数的异常安全性遵循木桶原理，函数的最强安全性取决于它所调用操作的最弱安全性