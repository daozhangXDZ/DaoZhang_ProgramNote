# Effective C++读书笔记(13): 用对象来管理资源

**守则13: 用对象来管理资源**

> “Use objects to manage resources”

我们在学习编程时，经常能听到"资源"这个词。资源可能是一个很宽泛的概念，但总体来讲，资源是我们可以用来使用，并且使用完之后要返还给系统的东西。在C++中，资源多数是指动态分配的内存。如果你只用new来分配内存却不在使用完后delete掉，将会导致内存泄漏。

其他资源比如文件描述符(file  descriptor)，Mutex锁，GUI中的字体(font)和画刷(brush)，网络接口(socket)，但不论资源是什么，我们一定要保证在使用过后要及时释放，否则就会造成资源泄露。当我们的代码变得越来越复杂，比如增加了异常抛出，函数不同的返回路径，手动管理资源将会变得费时费力，因此我们需要用对象来管理资源。

假设我们在为不同类型的投资写一个库:

```text
class Investment{...};            //Investment继承层级的基类
Investment* createInvestment();   //返回一个动态分配的Investment层级对象指针
```

返回一个指针就说明我们要负责在用毕后及时释放资源:

```text
void f(){
  Intestment* pInv = createInvestment(); //分配
  ...                                    //使用
  delete pInv;                           //释放
}
```

看起来是可以的，使用完后马上释放掉分配的内存，但这个函数仍然会失效！如果中间部分存在并触发了一个return语句，最后的delete语句便会被跳过。如果用在循环里，中间存在并触发了break或goto语句，delete也不会被执行。同样如果中间的代码抛出了异常，这个指针也不会被删除掉。如果这个动态分配的对象没有被清理掉，不仅仅是它占用的内存资源泄露，它所占有的**所有资源**也将泄露。

即使代码写得再小心，避免了以上的种种情况，但当项目被不同的人接手时，别人对某一部分的改动也可能让原来自己苦心制作的手动管理机制失效，导致资源泄露，所以手动管理费时费力，最后效果也不好。

------

**解决方法1:**

我们可以利用C++的对象析构函数自动调用机制，把资源封装在对象里面，这样当对象完成了它的使用周期，资源就会保证被释放。使用标准库的模板智能指针**auto_ptr**，它的析构函数会自动调用delete来释放它所指向的对象，十分方便。

```text
void f(){
  std::auto_ptr<Investment> pInv(createInvestment());
  ...   //使用
}       //无需手动释放
```

这个简单的例子阐明了用对象管理资源的两个关键概念：

1. 获得资源后要立即传递给资源管理对象用来初始化。在这里我们通过createInvestment()函数获得的资源被传递给了auto_ptr的构造函数。这就是C++重要的**RAII**概念，Resource Acquisition Is Initialisation，意为"资源获取即初始化"。
2. 资源管理类要利用析构函数来释放资源。当对象超出了它的作用域(scope)时，它的析构函数会自动调用，所以用析构函数来释放资源是保证安全的。但如[第8章](https://zhuanlan.zhihu.com/p/65454580)所讲，我们要防止在对象析构过程中抛出异常。

**注意！**因为auto_ptr会在使用周期后自动删除资源，所以不要使用多个auto_ptr指向同一个对象，否则同一个对象会被释放两次，是一个非法操作。为了防止这种操作，标准库给auto_ptr定义了一个奇怪的特性: 拷贝旧指针到一个新指针，旧指针会被设为NULL:

```text
std::auto_ptr<Investment> pInv1(createInvestment()); 
std::auto_ptr<Investment> pInv2(pInv1); //通过构造函数来拷贝，pInv1现在是NULL
pInv1 = pInv2;                          //通过赋值运算符来拷贝，pInv2现在是NULL
```

这个特性意味着auto_ptr不能被用在STL容器中，也就说明它不是管理资源最好的方法。STL容器要求它的元素拥有"正常的"拷贝特性，因为当使用STL容器的算法功能时将会使用赋值传递，这就会导致在函数生成本地拷贝的同时，容器原有的元素被设为NULL，所以装有auto_ptr的STL容器是不被允许的，会在编译时报出FBI(划掉)Warning。

**解决方法2:**

使用引用计数的智能指针(Reference-Counting Smart Pointer, RCSP)，它在运行时会统计有多少对象指向当前的资源，然后当没有任何对象指向当前资源时便会自动释放。C++标准库所追加TR1的**shared_ptr**就是这种智能指针的一个栗子:

```text
void f(){
  std::tr1::shared_ptr<Investment> pInv(createInvestment());
  ...
}  //同样无需手动释放
```

代码看起来和上面是差不多的，但shared_ptr可以在STL容器中使用，成为一个更好的选择，因为shared_ptr没有auto_ptr自动把原对象设为NULL的拷贝特性，也因为当使用容器的算法功能生成本地拷贝时，此时有两个对象指向了这个资源。即使拷贝的析构函数被调用了，原有的对象依然在指向这个资源，该资源便不会被提前释放。

```text
std::tr1::shared_ptr<Investment> pInv1(createInvestment());
std::tr1::shared_ptr<investment> pInv2(pInv1);  //pInv1保持不变
pInv1 = pInv2;                                  //pInv2保持不变
```

------

使用智能指针只是用对象管理资源的方法之一，而且也存在着局限性。例如我们不能使用标准库的智能指针来指向一个动态分配的数组，因为析构函数调用的是delete而不是delete []，虽然这样做依然可以通过编译。

```text
std::auto_ptr<std::string> aps(new std::string[10]);
std::tr1::shared_ptr<int> spi(new int[10]);
//析构函数并不会调用delete []
```

实际上在标准库中并没有数组版本的智能指针，因为强大的STL容器可以替代几乎所有数组的用途。如果真的需要数组版本的智能指针，可以使用boost，例如boost::scoped_array和boost::shared_array。

以上例子显示出智能指针并不能100%解决所有需要，更具普适性的解决方案是我们写自己的资源管理类，会在下面的章节中讲到。

**总结：**

- 防止资源泄露，从RAII做起。获取资源在构造过程中，释放资源在析构过程中。
- tr1::shared_ptr和auto_ptr是两个常用的RAII类。一般情况下tr1::shared_ptr是更好的选择，因为它的拷贝不会影响到其它对象，并且支持STL容器。