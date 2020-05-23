## [Effective *C++* 读书笔记(1), (2): *C++*与全局变量](https://zhuanlan.zhihu.com/p/63515998)

***本篇关键词: 全局变量，宏(#define)\***

------

**守则01：把C++看做一个语言的集合，而不是单一的语言**

> "C++ is a federation of languages"

早期的C++只是叫"C with classes"，但发展到今天已经成为一个多重泛型编程语言(Multi-paradigm programming language)，它具有4种“子语言”:

- C
- 面向对象的C++
- 模板C++
- STL

**高效的C++编程守则取决于你所使用的“子语言”**

例如**:**

- 在C中，一般使用值传递 (Pass by value)
- 在面向对象的C++和模板C++中，使用常量引用传递 (Pass by const reference)更加高效
- 对于STL，因为迭代器是基于指针构造而成，直接使用值传递即可

在不同的"子语言"中需要你用不同的策略，而非自始至终单一的方法，记住这一点对于理解学习C++这样功能强大的语言十分有帮助

------

**守则02：尽量使用const, enum, inline, 减少宏变量#define的使用**

**①或者说，尽量多用编译器，少用预处理器**

> "Prefer the compiler to the preprocessor"

例如:

```text
#define A 1.653   
```

在上面这个语句中，字符串'A'是不会被编译器看到的，而编译器看到的是'1.653'，这就会导致在调试过程中，编译器的错误信息只显示'1.653'而不是'A'，让你不知从何下手。

解决方法：定义全局常量

```text
const double A = 1.653;
```

使用全局常量还有一个好处：预处理器只会把每次对'A'的引用变成'1.653'而不管其是否已经存在，这就导致多次引用'A'会造成多个重复对象出现在目标代码中(Object code)，造成资源浪费。



**②当定义或声明全局变量时，常数指针和类的常数需要另加考虑**

- **对于指针**

对于指针要把指针本身和它指向的数据都定义为const，例如

```text
const char* const myWord = "Hello";
```

在C++中可以更方便地使用std::string这样基于char*类型的推广，例如

```text
const std::string myWord("Hello");
```

- **对于类的常数**

声明为类的私有静态成员，这样既保证变量只能被这个类的对象接触到，又不会生成多个拷贝

```text
class Player{
  private:
    static const int numPlayer = 5;
........
```

**注意**，因为此处是类的成员声明范围内，所以上面只是变量的声明和初始化，而并非定义，因此如果想获取变量的地址，需要在别处另加定义。这个定义不能有任何赋值语句，因为在类内已经规定为const:

```text
const int Player::numPlayer;
```



**③枚举技巧**(the enum hack):

试想当你在一个类内声明某变量，但你的编译器不允许在声明时赋值初始化，同时接下来的某个语句却需要用到这个变量的具体数值，例如:

```text
int noPlayer;
int scores[noPlayer];
```

此时编译器便会报错，需要在编译期间noPlayer有具体数值，这个时候就需要使用如下技巧:

```text
enum {noPlayer = 5};
int scores[noPlayer];
```

这样编译器就能顺利通过，因为enum可以被当成int类型来使用

但注意enum类型在内存中没有实体，无法取得enum类型的地址，因此这个方法更相当于取一个本地的#define数值



**④对于#define的宏函数，尽量使用inline修饰的函数来代替#define**

inline关键字用来建议编译器把某频繁调用的函数当做内联函数，即在每次函数调用时，直接把函数代码放在函数调用语句的地址，减少堆栈浪费。

如果为了减少堆栈资源的使用，把某个频繁调用的函数规定为宏，例如用a和b的最大值来调用某函数f:

```text
#define CALL_MAX(a,b) f((a) > (b) ? (a) : (b))
```

但这样的做法其实相当不好，因为第一需要把所有参数用小括号扩起来，这样的代码相当不雅观，而且也会导致未知的结果:

```text
int a=5, b=0;
CALL_MAX(++a, b);              //a增加了一次
CALL_MAX(++a, b+10);           //a增加了两次 
```

解决方法：

```text
template<typename T>
inline void callMax(const T& a, const T& b){
    f(a>b ? a:b);
}
```

这样既保证了堆栈不会枯竭，又让代码更加美观



**总结：宏常量用全局的const或者enum来替换，宏函数用inline修饰的函数来替换**