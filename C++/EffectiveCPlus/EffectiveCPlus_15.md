# Effective C++读书笔记(15): 让原始资源可接触

**守则15: 让资源管理类的原始资源可向外界接触**

> "Provide access to raw resources in resource managing classes"

------

***本篇关键词: 智能指针，裸指针，二者之间的转换\***

------

到现在我们一直在一个完美的世界里，资源管理类会帮你完成对资源的所有操作，自己不用关心资源管理类里面的原始资源。但现实是残酷的，有时我们依然需要直接接触资源管理类所封装的原始资源。

我们继续[第13章](https://zhuanlan.zhihu.com/p/70415131)的投资管理的栗子，我们在为不同类型的投资写函数库:

```text
std::shared_ptr<Investment> pInv(createInvestment()); //某个Investment的智能指针对象
```

现有函数:

```text
int daysHeld(const Investment* pi); //返回某个Investment对象的持有时间
```

如果你直接把智能指针对象传入上面的函数中:

```text
int days = daysHeld(pInv);
```

这样编译器会报错，因为函数需要裸指针类型的参数，而你传入的是智能指针类型。你需要做的也很简单，把智能指针转换为裸指针，使用**隐式转换**或者**显式转换**。

shared_ptr和auto_ptr都有一个成员函数get()，用来执行显式转换，返回智能指针对象所包含的裸指针:

```text
int days = daysHeld(pInv.get());
```

shared_ptr和auto_ptr也重载了指针的解引用运算符，即->和*，这意味着我们可以通过它们来实现隐式转换:

```text
class Investment{  //定义Investment继承层次的基类
  public:
    boos isTaxFree() const;
  ...
};

Investment* createInvestment(); //用来返回指向Investment对象的指针

std::shared_ptr<Investment> pi1(createInvestment()); //使用shared_ptr管理资源
bool taxable1 = !(pi1->isTaxFree());  //使用->操作符接触资源

std::auto_ptr<Investment> pi2(createInvestment());  //使用auto_ptr来管理资源
bool taxable2 = !((*pi2).isTaxFree());  //使用*操作符接触资源
```

------

有时我们需要把RAII资源管理对象所封装的原始资源拿出来，我们可以定义一个转换函数，将资源管理类隐式或显式转换为原始资源。例如要实现对C API中的字体类型(font)的资源管理:

```text
FontHandle getFont(); //C API定义的分配字体函数
void releaseFont(FontHandle fh);  //C API定义的释放字体函数
```

现在我们定义自己的RAII资源管理类:

```text
class Font{
  public:
    explicit Font(FontHandle fh): //C只能使用值传递
    f(fh) {} //构造时获取资源
    ~Font() {releaseFont(f);}  //析构时释放资源
    ...
  private:
    FontHandle f;
};
```

如果我们要使用某些C API只能使用FontHandle类型，我们就需要把Font类型**显式转换**为FontHandle类型，因此我们定义一个显式转换的函数get():

```text
class Font{
  public:
  ...
  FontHandle get() const {return f;}  //显式转换函数
  ...
};
```

但是这样显式转换的缺点就是每次使用都要调用get()函数，比较麻烦:

```text
void changeFontSize(FontHandle f, int newSize); //改变字体大小的C API
Font f(getFont());
int newFontSize;
...
changeFontSize(f.get(), newFontSize);  //需要使用get()来显式转换
```

另外一个缺点就是，我们既然写了RAII资源管理类，为什么还要每次只使用它的原始资源，这不是跟我们希望避免资源泄漏的初衷背道而驰吗？我们下面来看看**隐式转换**:

```text
class Font{
  public:
    ...
    operator FontHandle() const  //隐式转换函数
    {return f;}
    ...
};
```

这样调用API就会简单很多:

```text
Font f(getFont());
int newFontSize;
...
changeFontSize(f, newFontSize); //隐式转换
```

但是隐式转换也有缺点，某些类型错误就不会被编译器探测到了:

```text
Font f1(getFont());
...
FontHandle f2=f1;
```

我们希望把一个Font对象拷贝进另一个Font对象，但比如某个人的辣鸡IDE把打进去的Font变成了FontHandle，这样就把我们的资源管理对象变成了原始资源对象，编译器也不会报错。

结果就是，程序有一个FontHandle对象被f1封装和管理，但这个FontHandle通过上面的操作被拷贝进了f2，这样f1和f2同时控制着一个FontHandle。如果f1被释放，这个FontHandle也将被释放，就会导致f2的字体被损坏。

------

至于具体使用隐式转换还是显式转换还是要根据不同的需要来决定，要保证代码的正确性，显式转换的get()函数可能是更好的选择，如果想要代码自然易懂，隐式转换可能更好，两者各有优缺点。

可能你会问，提取RAII资源管理类的原始资源会不会破坏资源管理类的封装？是的，但是资源管理类不是用来封装某些东西的，而是用来**保证某些必要的操作被执行**，例如释放资源，当然如果需要，封装也可以成为在这之上的另一种功能。资源管理类的典范，会把用户不需要的功能隐藏起来，给用户需要的东西留下简单易用的出入口，例如shared_ptr，把引用计数的机制完全封装起来，但用户会时不时需要使用裸指针，因此它提供了能直接返回裸指针的函数。

**总结：**

- API通常需要使用原始资源作为参数，因此我们的RAII资源管理类要保证它所封装的资源是对外界可接触的。
- 可以通过隐式转换或显式转换来实现对外接触。显式转换总体上更安全，隐式转换则对用户更加方便。