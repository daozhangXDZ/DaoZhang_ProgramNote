# Effective C++读书笔记(20): 多用常量引用传递

**守则20: 多用常量引用传递，少用值传递**

> "Prefer pass-by-reference-to-const to pass-by-value"

------

***本章关键词: 常量引用传递，值传递，拷贝，对象切割\***

------

C++继承了C默认传递方式为值传递的特性，那么对于一个值传递的函数，它的参数是被传进来变量的**拷贝**初始化的。拷贝是由拷贝构造函数生成的，而拷贝多是一个不经济的操作，至于为什么我们来看下面的例子。我们定义一个继承层次:

```text
class Person{
  public:
    Person();
    virtual ~Person();  //见第7章为什么使用虚函数
    ....
  private:
    std::string name;
    std::string address;
};

class Student : public Person{
  public:
    Student();
    virtual ~Student();
    ...
  private:
    std::string schoolName;
    std::string schoolAddress;
};
```

现有如下函数使用值传递:

```text
bool validateStudent(Student s);  //值传递
Student plato;
bool platoOK = validateStudent(plato);
```

来看当我们使用值传递时会发生什么:

- Student类的拷贝构造函数调用，用来初始化参数s
- 本地参数s在函数返回时被销毁

现在我们再往细节分析一下，Student类含有两个std::string对象，它又是继承自Person类，又有两个std::string对象。这就意味着，Student对象使用值传递会带来:

- 调用一次Student类的拷贝构造函数
- 调用一次Person类的拷贝构造函数
- 调用4次std::string类的拷贝构造函数
- 同样过程适用于返回时的析构过程

一共是6次拷贝构造函数，同时也对应了6次析构函数，成本果然很大吧！

我们当然希望函数的本地参数被安全地初始化和销毁，但我们同样希望避免这些不必要的开销，那么答案就是使用**常量引用传递**:

```text
bool validateStudent(const Student& s);
```

使用引用意味着直接在变量本身上进行读写，从而不用产生拷贝，那么如上繁杂的构造和析构过程也就省略掉了。如果我们不希望对它本身进行修改，就需要加const修饰符，让这个参数只读。

------

使用常量引用传递也巧妙避免了**对象切割问题**(object slicing  problem)。如果有一个函数的参数类型是父类，这时一个子类对象被值传递进这个函数时，参数初始化所调用的构造函数是父类的，子类所衍生的特性就全部被"切割"掉了，在这个函数里你就只剩下一个父类对象，惊喜不惊喜? 我们举一个例子:

```text
class Window{  //定义一个图形操作界面的窗口类
  public:
    ...
    std::string name() const;  //返回当前窗口名称
    virtual void display() const; //显示窗口和内容
};

class WindowWithScrollBar : public Window{
  public:
    ...
    virtual void display() const;
};
```

display()函数是虚函数，这就意味着两个类对于这个函数有不同的实现。如果你要写一个函数，先打印出窗口的名字，然后显示窗口，下面就是错误的写法:

```text
void printNameAndDisplay(Window w){  //值传递
  std::cout<<w.name();
  w.display();
}
```

这样使用值传递就会导致对象被"切割"，所以函数里所调用的display函数将永远是父类Window的display函数，不管传递进的是Window类还是WindowWithScrollBar类:

```text
WindowWithScrollBar wwsb;
printNameAndDisplay(wwsb);  //调用的永远是Window::display()
```

解决方法:

```text
void printNameAndDisplay(const Window& w){ //常量引用传递
  std::cout<<w.name();
  w.display();
}
```

------

*但引用传递并不是百分之百能替代值传递*

一般来讲，C++编译器会把引用作为指针来实现，所以引用传递本质上其实就是指针传递。因此，对于例如int的原始类型，直接用值传递还是比引用传递要高效，对于STL的迭代器和STL函数对象(function object / functor)，即提供至少一个operator()的实现的某类对象，值传递同样也比引用传递高效。

见[第1章](https://zhuanlan.zhihu.com/p/63515998)，C++由不同的"子语言"组成，每种"子语言"都有自己的高效编程守则，那么在STL和传统的C中，值传递是传递参数更高效的方法。为了遵循这一惯例，迭代器和函数对象，它们都被设计成值传递更高效，也不用我们去担心对象切割问题。

------

*使用值传递还是引用传递与大小无关*

有些人可能会讲，因为原始类型体积小，所以体积小的对象使用值传递会更高效。这句话并不准确，假如我们定义一个容器类只有一个指针，但这个指针装了许多许多的对象，那么拷贝这个类的对象就意味着也要拷贝它的指针包含的所有对象，成本也是非常高。

第二，在有些编译器中，原始类型和用户定义类型是被分开处理的。假如你定义一个类，里面只含有一个double数据成员，编译器可能不会把它放在寄存器里，但编译器会把同样大小的单个double放进寄存器里，这就会影响速度。如果你不确定编译器到底会怎么做，就把使用引用传递，因为引用传递即指针传递，编译器一定会把指针放在寄存器里。

最后，作为用户定义的类，就算现在它的体积再小，在项目后期也可能被修改，例如增加更多数据成员，那时可能就会后悔当时用了值传递。甚至对于标准类型，例如std::string，取决于使用不同的实现，对象的体积也是大小不一。

总体来讲，***只有\***对于原始类型，STL迭代器，STL函数对象来讲，你才可以认为值传递更高效。对于其它的一切，还是要遵循这一章的守则，多用常量引用传递，少用值传递。

**总结:**

- 多用常量引用传递，少用值传递。引用传递通常更高效，也能避免对象切割问题。
- 但是作为惯例，对于原始类型，STL迭代器，STL函数对象，值传递还是更加高效，这是仅有的例外。