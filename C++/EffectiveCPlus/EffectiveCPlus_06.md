# Effective C++读书笔记(6): 自动生成的函数有时并不需要

**守则06: 明确告诉编译器你不需要某些函数**

> "Explicitly disallow the use of compiler-generated functions you do not want"

------

***本篇关键词: Uncopyable类***

------

试想如下情形，某个房地产商所拥有的房子都是不同的，同时你在为这个公司设计程序，而你不想将一座房子的信息拷贝给另一座房子，这就需要**禁止使用**拷贝构造函数(copy constructor)和拷贝赋值运算符(copy assignment operator)。

```text
class House{...};

House h1;
House h2;
House h3(h2);        //禁止执行
h1=2;                //也要禁止执行
```

如果是其他功能，不想使用的话不声明即可。但是对于以上这两个功能，像上一章讲过的，即使你不声明不定义，编译器是会为该类自动生成的。

**解决方法：**因为编译器为类自动生成的函数都是共有(public)的，我们就可以把这些函数声明为私有(private)，这样它的对象就无权调用。其次，只声明不定义，因为如果有定义，本类和友元函数(friend functions)还是可以调用它们。

```text
class House{
  public:
    ....
  private:
    House(const House&);               //只有声明，不要定义
    House& operator=(const House&);    //因为不会被用到，就不必再给参数想一个名字了
};
```

这样，当你在代码中试图拷贝对象，编译器就会报错。如果你不小心在该类的成员或者友元函数中调用了，因为找不到定义，链接器则会出错。但把所有报错提前到编译器不是更好吗？

**更好的解决方案**：上一章也讲到过，当一个父类将拷贝函数声明为私有时，编译器会拒绝为它的子类生成拷贝函数。因此我们可以专门使用一个父类，在其中声明拷贝操作为私有，并让我们的类继承自它。

```text
class Uncopyable{
  protected:
    Uncopyable();
    ~Uncopyable();
  private:
    Uncopyable(const Uncopyable&);               //将拷贝函数转移至此
    Uncopyable& operator=(const Uncopyable&);
};

class House:public Uncopyable{...};              //公有继承
```

这样所有关于拷贝的操作都会提前在编译时报错。

**总结：**

- 当不想让编译器为类自动生成某些函数时，把这些不想要的函数声明在此类的私有成员中，或者更好使用像如上例子的一个父类，并让我们的类公有继承。