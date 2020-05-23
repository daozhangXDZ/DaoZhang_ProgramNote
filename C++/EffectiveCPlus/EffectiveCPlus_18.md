# Effective C++读书笔记(18): 让你的接口好用对，难用错

***本篇关键词: 接口，用户端问题，智能指针***

------

现在我们来到软件设计的话题中。软件设计就是让软件做你想做的事，软件设计一定需要**接口**(interface)设计，最后用C++实现。我们今天讨论可能是其中最重要的一条守则，把你的接口设计得容易用对，不容易用错。讨论完这一条，会引出更多关于软件设计的话题，比如效率(efficiency)，封装(encapsulation)，可维护性(maintainability)和一些惯例(convention)。

所谓接口就是你提供给用户使用你代码的途径。C++到处都充满了接口的概念，比如函数接口，类接口，模板接口。理想条件下，如果我们用错了接口，编译器会报错，而如果编译器没有报错，那么我们用的接口就是对的。

要把接口设计得好用对，难用错，就需要考虑用户可能犯的各种错误。假如你在设计一个表示日期的类:

```text
class Date{
  public:
    Date(int month, int day, int year);  //美式标准
    ...
};
```

至少第一眼看起来是没问题的，但用户可能会出现这样的错误:

- 有个英国人输入了错误的格式:

```text
Date d(30, 3, 1995);  //规定输入美式标准的月，日，年
```

- 有个美国人打错了字，输入了非法日期:

```text
Date d(3, 40, 1995); //把3打成了4
```

对于这样的问题，我们可以定义新的类型，使用简单的包装类(wrapper class)，让编译器对错误的类型报错:

```text
//3个包装类
struct Day{
  explicit Day(int d):val(d){}
  int val;
};

struct Month{
  explicit Month(int m):val(m){}
  int val;
};

struct Year{
  explicit Year(int y):val(y){}
  int val;
};

//现在开始使用
class Date{
  public:
    Date(const Month& m, const Day& d, const Year& y);
    ...
};

Date d(30, 3, 1995); //int类型不正确报错
Date d(Day(30), Month(3), Year(1995)); //格式错误报错
Date d(Month(3), Day(30), Year(1995)); //正确
```

我们保证了格式的正确，下一步就是要对取值做出规范，例如月份只能有1到12。使用enum可以满足功能上的要求，但enum不是类型安全的(type safe)，因为[第2章](https://zhuanlan.zhihu.com/p/63515998)展示过enum可以被用来当作int类型使用。我们需要定义包含所有月份的集合:

```text
class Month{
  public:
    static Month Jan(){return Month(1);}  //见下文为什么使用函数，不使用对象
    static Month Feb(){return Month(2);}
    ...
    static Month Dec(){return Month(12);} 
    ...
  private:
    explicit Month(int m);  //explicit禁止参数隐式转换，private禁止用户生成自定义的月份
    ...
};

Date d(Month::Mar(), Day(30), Year(1995)); //正确
```

这种方法虽然略显繁琐，但保证了数据的正确性，并且在提升网页脚本安全性的实践中，这是一种常用的防止恶意用户注入代码的思路。

------

第二点是要把接口设计得**一致**。C++STL容器接口相比其它语言可以说是达到了高度一致性，因此这些接口也相比更加易用，例如每一个STL容器类都有一个成员函数size()来返回容器当前包含的对象数量。

不像Java，对于数组要使用*length属性*，对于字符串要使用*length方法*，对于List要使用*size方法*，总之各种各样的接口。在.NET中，对于数组要使用Length属性，对于ArrayList又要使用Count属性。可能有些开发者会认为，使用了IDE，这些不一致性就显得不那么重要，但不一致的接口依然会带来心理上的困难感，因为明显你需要记住更多东西，这是IDE不能弥补的。

这里的一致也有另外一层意思，是行为上的一致性，就是要把功能做得与原始类型或是其它标准类型的逻辑一致。[第3章](https://zhuanlan.zhihu.com/p/63609476)展示了*运算符用const修饰返回值来避免打错字带来的无意义赋值:

```text
if(a*b = c)...//应该是a*b == c
```

这样的错误难以察觉，我们当然希望这样的错误在编译时就被指正。要做到这样的一致性，我们只需要跟着原始类型的逻辑走，例如不允许给右值赋值，来防止可能造成的一系列误用。原作者的话就是:

> "When in doubt, do as the ints do"。

------

第三点就是，任何要求用户记住东西的接口都更容易造成误用，因为用户也不是电脑，只要是人类就会忘掉东西，例如动态分配了一个资源，要求用户以某种特定的方式释放资源。[第13章](https://zhuanlan.zhihu.com/p/70415131)引入了一个工厂函数(factory function):

```text
Investment* createInvestment();
```

为了防止资源泄漏，这个动态分配的资源必须在使用完后删除，但要求用户这样做可能会产生两种情景:

- 用户忘记了删除
- 多次删除同一个指针

[第13章](https://zhuanlan.zhihu.com/p/70415131)的解决方法是使用智能指针自动管理资源，但如果用户忘记把这个函数的返回值封装在智能指针内呢?所以我们最好让这个函数直接返回一个智能指针对象:

```text
std::shared_ptr<Investment> createInvestment();
```

实际上，返回一个智能指针还解决了一系列用户端资源泄漏的问题，[第14章](https://zhuanlan.zhihu.com/p/71805363)讲到，如果默认的删除器不好用，我们可以给shared_ptr绑定一个自定义的删除器(deleter)来自动实现我们想要的析构功能。不仅仅是内存资源，通过绑定删除器，我们还可以管理更多种类的资源，例如同样是[14章](https://zhuanlan.zhihu.com/p/71805363)里的Mutex锁。

假如我们规定，如果用户从这个工厂函数得到了一个Investment*对象，在释放时要用另一个getRidOfInvestment()函数来释放资源，而不是单独使用delete，这就可能会导致用户忘记而使用了错误的释放机制。要防止这种错误，我们把getRidOfInvestment()绑定到shared_ptr的删除器，这样shared_ptr就会在使用完成后自动帮用户调用释放函数。

绑定删除器还有另一大好处，就是避免了**DLL交叉问题**(cross-DLL  problem)。这个问题是当一个对象从一个DLL中生成，在另一个DLL中释放时，在许多平台上就会导致运行时的问题，因为不同DLL的new和delete可能会被链接到不同代码。shared_ptr的删除器则是固定绑定在创建它的DLL中，这就例如，我们有Stock类继承自Investment:

```text
std::shared_ptr<Investment> createInvestment(){
  return std::shared_ptr<Investment>(new Stock);
}
```

工厂函数返回的Stock类型智能指针就能在各个DLL中传递，智能指针会在构造时就固定好当引用计数为零时调用哪一个DLL的删除器，因此不必担心DLL交叉问题。

------

这一章不仅仅是关于shared_ptr，而是关于要把接口做得对于用户易用，但shared_ptr实在是十分优雅地解决了一系列用户资源管理的问题。虽然可能比裸指针占更多内存，可能会更慢，但在许多应用上是可以忽略不计的，可是用户端错误造成的问题就不是那么忽略不计了。

**总结:**

- 好的接口要容易用对，难用错。在所有接口设计中都应该秉行这条准则。
- 让接口更容易用对，就要把接口做得一致，易于记忆，逻辑上也要与原始类型和标准类型保持一致。
- 要防止错误，就定义新的包装类型，限制运算符操作，限制取值范围，不要让用户负责管理资源。
- shared_ptr支持自定义的删除器，实现我们想要的析构机制，还能防止DLL交叉问题，而且也能被用来管理其它资源例如Mutex锁。