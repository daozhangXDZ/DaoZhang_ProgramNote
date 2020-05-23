# Effective C++读书笔记(3): 多用const

**守则03: 尽可能使用const关键字**

> "Use const whenever possible"

------

***本篇关键词：const变量, const函数, const T\*, T\* const\***

------

**①指针与const:**

如果要定义某指针或数据为常量不允许改变:

```objective-c++
const char* p;              //数据是const,数据不允许被改变
char* const p;              //指针是const,指针不允许被改变
const char* const p;        //数据与指针都是const,数据与指针都不可以被改变
```

记忆法: const在星号左边修饰数据，const在星号右边修饰指针

以及如下两个语句的功能是相同的，不需要对此产生困惑:

```text
const char* pw;             //都表示指向常量char的指针
char const* pw;
```

**②迭代器与const**

迭代器在功能上相当于指向某类型T的指针 T*

因此，如果想定义某迭代器指向一个常数，使用const iterator是不可以的，这样只相当于定义一个迭代器为一个常量(T* const)，例如:

```text
const std::vector<int>::iterator it = v.begin(); //注意，此声明只表示迭代器本身是常量        
*it = 10;                                        //编译通过，迭代器是常量，但数据可以被修改
++it;                                            //编译失败！因为const迭代器不允许被改变！
```

解决方法，使用const_iterator:

```text
std::vector<int>::const_iterator it = v.begin();  //使用了const_iterator类型
*it = 10;                                         //编译失败，数据不允许被改变！
++it;                                             //编译通过，迭代器本身可以被改变
```

**③尽量使用const可以帮助调试**

试想如下情形:

```text
class Rational{....};
Rational operator*(const Rational& lhs, const Rational& rhs){...}
```

在某处使用此乘法操作符时，误把比较操作符"=="打成了赋值操作符"="：

```text
Rational a,b,c;
if(a*b = c){......}                       
```

但编译器在此并不会报错，因为只有当a,b,c是C++自有类型(比如int)才会报错，对于用户自定义的类，编译器会认为此操作是将一个Rational赋值给另一个Rational

这就会导致不正确的结果却没有任何编译器错误信息，给调试增加麻烦

解决方法: 将该操作符定义为返回const，这样对其赋值将会是非法操作

```text
const Rational operator*(const Rational& lhs, const Rational& rhs){...}
```

**④类的成员函数与const**

给成员函数使用const关键字是非常重要的，它可以让接口更加直观，直接告诉用户这个函数是不是只读(Read only)，会不会改变某变量。

更重要的是，用const修饰的对象只能调用const修饰的成员函数，因为不被const修饰的成员函数可能会修改其他成员数据，打破const关键字的限制。

因此，需要同时声明有const和没有const的成员函数，例如:

```text
const char& operator[](size_t pos) const;
char& operator[](size_t pos);
```

对于某自定义的类Text:

```text
Text t("Hello");
const Text ct("Hello");

std::cout<<t[0];            //调用了不加const修饰的索引操作符
std::cout<<ct[0];           //调用了const版本, 但如果只有不加const的操作符，将会报错discard qualifier
t[0] = 'x';                 //成立，但注意此索引操作符必须声明为引用才可以支持赋值操作
ct[0] = 'x';                //错误！常量不能被修改
```

**⑤成员函数的常量性(Constness)**

C++标准对成员函数"常量性"的规定是数据常量性(bitwise constness)，即不允许常量对象的成员数据被修改。C++编译器对此的检测也十分简单粗暴，只检查该成员函数有没有给成员数据的赋值操作。

但如下情形，即使修改了某个数据，也可以通过编译器的检测：

```text
const Text ct("Hello");        //构造某常量对象
char* pc = &ct[0];             //取其指针
*pc = 'K';                     //通过指针修改常量对象，编译不会报错，结果为"Kello"
```

数据常量性还有另一个局限性，例如:

```text
class Text{
  public:
    std::sizt_t length() const;
  private:
    char* pText;
    std::size_t length;
    bool lengthValid;
....
};

std::size_t Text::length() const{
  if(!lengthValid){                      //做某些错误检测
    length = std::strlen(pText);         
    lengthValid = true;                   
  }

  return length;                         //这行才是代码核心
}
```

在这段代码中，length()函数要做某些错误检测，因此可能会修改成员数据。即使真正的功能核心只是返回字符长度，编译器依然认为你可能会修改某些成员数据而报错。

因此，更好的方法是**逻辑常量性**(Logical constness)，即允许某些数据被修改，只要这些改动不会反映在外，例如，以上问题可以用mutable关键字来解决:

```text
mutable std::size_t length;
mutable bool lengthValid;
```

这样成员函数length()就可以顺利通过编译。

**此外注意**，除mutable之外，静态成员(static)也可以被const成员函数修改。

**⑥在定义常量与非常量成员函数时，避免代码重复**

可能大家会有所困惑，既然两个版本的成员函数都要有，为什么又要避免重复?

其实在这里指的是函数的实现要避免重复。试想某函数既要检查边界范围，又要记录读取历史，还要检查数据完整性，这样的代码复制一遍，既不显得美观，又增加了代码维护的难度和编译时间。因此，我们可以使用非常量的函数来调用常量函数。

```text
const char& operator[](std::size_t pos) const{....}
char& operator[](std::size_t pos){
  return
    const_cast<char&>(                              //const_cast去掉const关键字，并转换为char&
      static_cast<const Text&>(*this)[position];    //给当前变量加上const关键字，才可以调用const操作符
  );
}
```

为了避免无限递归调用当前非常量的操作符，我们需要将(*this)转换为const Text&类型才能保证安全调用const的操作符，最后去掉const关键字再将其返回，巧妙避免了代码的大段复制。

但注意，如果使用相反的方法，用const函数来调用non-const函数，就可能会有未知结果，因为这样相当于non-const函数接触到了const对象的数据，就可能导致常量数据被改变。

**总结:** 

- 指针，迭代器，引用，本地变量，全局变量，成员函数，返回值都可以使用const来实现数据只读的目的，const是C++一个非常强大的特性。
- 除此之外，它还能帮助加快调试过程
- 即使编译器使用数据常量性的标准，我们编程的时候应该采用逻辑常量性，对相关不可避免更改的成员数据加上mutable关键字来修饰
- 当有大段复制代码出现在const和non-const的成员函数中，可以使用non-const函数来调用const函数来避免复制