# Effective C++读书笔记(5): 类中自动生成的函数

**守则05: 要知道C++自己生成了什么函数**

> "Know what functions C++ silently writes and calls"

------

***本篇关键词: 构造函数，拷贝构造函数，赋值运算符，析构函数\***

------

**①C++会为类生成默认的关键函数**

像上一章讲过的，如果在C++的类中不声明任何成员，C++会自动为你生成默认的构造函数(constructor)，拷贝赋值运算符(copy assignment constructor，即 '=')，拷贝构造函数(copy  constructor)以及析构函数(destructor)。例如:

```text
class Empty {};             

//假定以下功能都会被调用，此定义等价于：
class Empty{
  public:
    Empty(){....}                                //构造函数
    Empty(const Empty& empty){.....}             //拷贝构造函数
    ~Empty(){....}                               //析构函数
    Empty& operator=(const Empty& empty){....}   //拷贝赋值运算符
};
```

但是这些函数只有在被需要调用的时候才会生成，因此这4种功能不是保证都存在的。

**②但是这样的生成是有条件的！**

赋值运算符是为了将一个对象的成员数据拷贝进另一个对象中。对于赋值运算符，只有当代码合法而且有意义时，编译器才会自动生成。如下代码就不满足该条件：

```text
template<typename T>
class A{
  public:
    A(std::string& _name, const T& value);
  private:
    std::string& name;
    const T value;
};
```

对于如上的类，现在执行如下操作：

```text
std::string s1("hello");
std::string s2("hi");

A<int> a1(s1,3);
A<int> a2(s2,6);
a1=a2;
```

现在有问题了！C++规定引用是专一的，不允许引用被初始化后再指向另一个对象(〃'▽'〃)

而这样的操作就相当于：

```text
int  a=3;
int& b=a;
int  c=7;
int& d=c;
b=d;           //编译器在此当然会报错
```

因此给a1对象的成员name的再赋值会导致编译出错。同样，C++也不允许为常量再赋值，因此对成员value赋值也会编译出错。

**解决方法：**定义自己的赋值运算符！

此外，当基类有将赋值运算符声明为私有时，编译器也会拒绝为它的子类生成赋值运算符，因为在子类赋值过程中，它所包含的基类也应当被赋值。但是既然被声明为基类的私有成员，子类将不能调用。

**总结：**

- 如果自己不声明，编译器将会自动生成默认的构造函数，拷贝构造函数，拷贝赋值运算符和析构函数。