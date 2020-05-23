# Effective C++读书笔记(27): 少用cast

**守则27: 尽量避免类型转换**

> "Minimizing casting"

------

***本篇关键词: C风格类型转换，C++风格类型转换(static, dynamic, const, reinterpret)，继承层次指针***

------

C++的语法是被设计成类型安全的，因此如果程序顺利通过了编译并且没有发出任何警告，理论上你的代码不会包含类型不安全的操作。但是类型转换(type casting)的出现给C++安全的型别系统(type  system)带来了挑战，不像Java或者C#，类型转换十分必要而且风险更小，是一个十分神圣的存在。在C++里，转换类型时的稍不注意便有可能带来麻烦。

我们首先从类型转换的语法开始。C++的类型转换有3种方式，C风格，函数风格和C++风格:

```text
(T)expression  //C风格
T(expression) //函数风格
```

以上这两种写法没有明显区别，都可以叫做"老式"类型转换。下面我们看所谓的"新式"类型转换，可以看到明显的风格不同:

```text
//C++风格
static_cast<T>(expression)
dynamic_cast<T>(expression) //T必须是指向多态类型的指针或引用
const_cast<T>(expression) //T必须是指针或引用
reinterpret_cast<T>(expression) //T必须是指针或引用
```

上面的每一个cast都服务于不同目的:

- **static_cast**是最常用最好理解的C++风格类型转换，其实就相当于C++风格的显式转换，例如把int转为double，把无类型(void)指针转换为有类型指针，继承层次中的转换，把non-const对象转为const，但是不可以把const对象转为non-const(这是const_cast的功能)，也不能转换两个完全不兼容的类型:

```text
//double转为int:
double d = 1.3;
int a = (int)d; //C风格转换
int b = static_cast<int> d; //C++风格转换

//non-const转为const:
int a = 3;
const int b = (const int)a; //C风格转换
const int c = static_cast<const int>(a); //C++风格转换
```

- **dynamic_cast**，名字里带个"dynamic"，就说明它是动态的，发生在运行时，而上面静态的static_cast则发生在编译时。像动态绑定(dynamic binding)一样，dynamic_cast需要RTTI(runtime type  identification)信息做出运行时类型检测，所以它是最吃性能的cast。功能上不同于static_cast的是，它只能用在继承层级中，而且只支持**指向多态类型的指针或引用**，即继承层次的子类或有虚函数的基类。

```text
class Animal{
  public:
    virtual void doSomething(); //要作为多态基类
};
class Dog : public Animal{...}; //继承类
...
Dog* dog = new Dog();
Aminal* animal = new Animal();

//向上转型，转为父类
Animal* newAnimal = dynamic_cast<Animal*>(dog); //编译通过
//↑但要注意如果基类没有虚函数，目标类型就不是多态类型，就不能通过编译

//向下转型，转为子类
Dog* newDog = dynamic_cast<Dog*>(animal); //编译通过，但是返回空指针
```

dynamic_cast的一大用途就是检测当前指针指向的是父类还是子类。如果返回了空指针，当前指针就指向父类，如果返回了有效的指针，指向的就是子类，在文章下面会有例子。

- **const_cast**用来抹除对象的常量性(constness)，即去掉const限定符，它是唯一能去掉变量限定符的cast，也可以用来去掉volatile限定符。不过既然一个变量被定义为了const，我们当然不希望改变它，因此这种cast最有用的地方体现在函数传值里:

```text
//需要非常量参数
void doSomething(int* n){
...
}
...
const int a = 22;
doSomething(&a); //报错，不能把const int转为int
doSomething(const_cast<int*>(&a)); //正确
```

- **reinterpret_cast**用来把指针转换为任何类型的指针。既然叫做"reinterpret"，它的用途就是把相同的内存数据以不同的方式表示出来，因此不生成任何额外的CPU代码，常见于底层的应用。同时它也是一个十分危险的cast，再加上比较特殊的用途，所以比较少用:

```text
int a = 0x76; //字母v的ASCII
int* ap = &a; //获取指针
char* c = reinterpret_cast<char*>(ap); //输出v

float a = 2.76f; //尝试用reinterpret_cast把float转为int
float* ap = &a;
int* b = reinterpret_cast<int*>(ap); //只是按照比特位输出0xffffcbec
```

------

讲了这么多C++风格cast，意思就是最好还是多用这些新式转换。首先从代码字面显然新式类型转换更容易发现，所有关于类型的问题也能被快速定位。其次4种新式转换各服务于一个独特目的，因此编译器能更好诊断问题，例如你要去掉const限定符，不使用const_cast是无法编译的。最后功能上C++风格的类型转换完全能取代C风格类型转换，例如显式构造函数:

```text
class Widget{
  public:
    explicit Widget(int size);
  ...
};

void doSomething(const Widget& w);
doSomething(Widget(15)); //更像构造临时对象，但也可以理解为函数风格类型转换
doSomething(static_cast<Widget>(15)); //C++风格类型转换
//二者没有功能上的差异，都会把15转换为临时的Widget对象来传进函数
//如果要突出创建对象，用函数风格，如果要突出类型转换，用C++风格
```

许多人会认为类型转换无非就是告诉编译器要用另一种类型的方式处理这个对象。其实任何类型转换，包括隐式和显式，几乎都会造成更多的机器码:

```text
int x,y;
double d = static_cast<double>(x)/y;
```

显然这行转换产生了更多的机器码，因为int与double的储存和表现方式是不同的。可能这点几乎是常识了，那来看下面的例子，类型转换带来的意外结果:

```text
class Base{...};
class Derived : public Base{...};
Derived d;
Base* pb = &d; //derived*隐式转换为base*
```

看起来OK，我们只是希望做一个隐式转换，但这段代码可能会带来一个问题，即C++的基类和子类指针不一定相同，就会导致Derived对象会同时有两个地址。其它语言的内存分布可能会更规则，可是在C++里，不要随便做出这样的假设，更不要基于这样的假设执行任何操作。而且就算你知道这两个地址存在一个固定的偏移量，在一个平台上偏移量是这么多，不代表另一个平台上的编译器生成的偏移量也是这么多。

------

类型转换另一个有趣的现象是，你很容易写出来看起来对其实错了的代码。假如我们在写一个窗口应用，把Window作为基类，SpecialWindow作为继承类，两个都定义了onResize虚函数，而且其中SpecialWindow的onResize需要先调用Window的onResize才能执行其它操作:

```text
class Window{
  public:
    virtual void onResize(){...}
  ...
};

class SpecialWindow : public Window{
  public:
    virtual void onResize(){
      static_cast<Window>(*this).onResize();//想要把*this转换为Window再调用它的虚函数
      ... //执行其它操作
    }
};
```

如你所想，*this当然会被转换为Window对象并且调用Window::onResize()，但这全都是在生成的拷贝上完成的，并不是真正的*this！因为这行类型转换会生成一个基类部分的本地拷贝，所以我们只是用这份拷贝调用了onResize。

再加上onResize函数并没有加const限定符，它就有可能改变对象的状态，就会导致*this本体的基类部分并没有改变状态(改变的只是拷贝)，而后面的其它操作则会直接改变*this本体子类部分的状态，整体的*this就无意义了。

解决方法是不要用类型转换，直接告诉编译器你想用哪个函数:

```text
class SpecialWindow : public Window{
  public:
    virtual void onResize(){
      Window::onResize(); //明白说我要Window的onResize
      ...
    }
  ...
};
```

------

上面这个例子说明了在你想当然地要用类型转换时，错误可能就这么出现了，尤其是对于dynamic_cast。在讲例子之前，值得先注意的是dynamic_cast可能会非常慢，因为有些类型检测的实现是基于字符串对比。假如你在一个4层的继承层次里给一个对象做dynamic_cast，就会导致最多调用4次strcmp，不用说更深的或者多重继承层次了。所以在对类型转换保持谨慎的同时，更要尤其照顾dynamic_cast，如果你的程序很看重性能。

dynamic_cast的用途在于当你想对子类执行操作时，但你不知道手头上的指针或者引用指向的到底是父类还是子类，因为运行时的情况是不固定的。想要避免使用耗费性能的dynamic_cast，有两种方法:

第一种方法，使用容器储存**直接指向子类**的指针(经常是智能指针，见[第13章](https://zhuanlan.zhihu.com/p/70415131))，不再需要通过基类接口来操作子类了。还比如在我们的Window和SpecialWindow的层次里，如果只有SpecialWindow能闪烁，我们可以把以下代码:

```text
class Window{...};
class SpecialWindow : public Window{
  public:
    void blink(); //这种方法不用虚函数，下一种方法会用虚函数
  ...
};
typedef std::vector<std::shared_ptr<Window>> VPW; //智能指针见第13章
VPW winPtrs; //通过基类指针操作子类
...
for(VPW::iterator iter = winPtrs.begin(); iter != winPtrs.end(); ++iter){
  //如果当前对象是一个子类，if条件里就不是null，就能调用blink()
  if(SpecialWindow* psw = dynamic_cast<SpecialWindow*>(iter->get()))
    psw->blink(); //但是条件里用了慢的dynamic_cast
}
```

代替为:

```text
typedef std::vector<std::shared_ptr<SpecialWindow>> VPSW;
VPSW winPtrs; //现在直接使用子类指针
...
for(VPSW::iterator = winPtrs.begin(); iter != winPtrs.end(); ++iter){
  (*iter)->blink();
} //更好的代码，不用dynamic_cast
```

当然这种方法不能让你在同一个容器里储存继承层次里所有类型的对象，因为容器里储存的是子类对象不是基类。所以如果想要保管多种类型，会需要多个这样的容器。



第二种方法，通过基类接口操作所有子类，即通过虚函数实现你想要的功能。还看我们Window的例子，我们可以在基类中声明这个虚函数，给一个空的默认实现:

```text
class Window{
  public:
    virtual void blink(){}  //声明为虚函数，空操作作为默认实现
    ...
};
class SpecialWindow : public Window{
  public:
    virtual void blink(){...}  //子类这里做真正的实现
    ...
};
typedef std::vector<std::shared_ptr<Window>> VPW;
VPW winPtrs; //容器包含基类指针，通过它操作所有子类
...
for(VPW::iterator iter = winPtrs.begin(); iter != winPtrs.end(); ++iter){
  (*iter) ->blink(); //注意这里也没有dynamic_cast
}
```

虽然这两种方法，使用包含子类指针的容器，和使用包含多态基类指针的容器，可能并不能适用于百分之百的场合，但它们确实能有效代替缓慢的dynamic_cast，所以当可以用的时候就要尽量用。

还有一种你一定想要避免的糟糕代码，就是串联起来的dynamic_cast，比如这样:

```text
class Window{...};
class SpecialWindow1 : public Window{...};
class SpecialWindow2 : public Window{...};
... //其它子类

typedef std::vector<std::shared_ptr<Window>> VPW;
VPW winPtrs;
...

for(VPW::iterator iter = winPtrs.begin(); iter != winPtrs.end(); ++iter){
  //串联起来的dynamic_cast
  if(SpecialWindow1* psw1 = dynamic_cast<SpecialWindow1*>(iter->get())){...}
  else if(SpeciaWindow2* psw2 = dynamic_cast<SpecialWindow2*>(iter->get())){...}
  else if(SpeciaWindow3* psw3 = dynamic_cast<SpecialWindow3*>(iter->get())){...}
  ...
}
```

这会导致生成大量又缓慢的机器代码，而且这样的代码及其脆弱，因为每在继承层次里增加或者去掉某个类，这段代码就要被维护一遍。永远要用基于虚函数的实现替代这种代码。

好的C++代码会尽量少用类型转换，但完全不用显然也是不实际的。而且类型转换要尽量被隔离，以免给其它代码带来不可预见的影响，例如隐藏在函数中，把里面见不得人的过程从用户眼下完全藏在接口之下。

**总结:**

- 如果可以就要避免类型转换，尤其是在侧重性能代码中的dynamic_cast。如果有些设计需要类型转换，尽量用其它方案代替
- 如果类型转换是必要的，就把它隐藏在函数里。这样用户就只能调用接口而自己的代码里就不会出现类型转换
- 要多用C++风格的类型转换，少用C风格类型转换。它们更容易被发现，各自服务的功能也更具体