# C++可变参数

VA_LIST 是在

[C语言](https://baike.baidu.com/item/C%E8%AF%AD%E8%A8%80)中解决变参问题的一组宏，所在头文件：#include <stdarg.h>，用于获取不确定个数的参数。

 

VA_LIST 是在[C语言](https://baike.baidu.com/item/C%E8%AF%AD%E8%A8%80)中解决变参问题的一组宏，所在头文件：#include <stdarg.h>

成员

变量

\#ifdef _M_ALPHA

typedef struct {

char *a0; /* pointer to first homed integer argument */

int offset; /* byte offset of next parameter */

} va_list;

\#else

typedef char * va_list;

\#endif

_M_ALPHA是指DEC ALPHA（Alpha AXP）架构。所以一般情况下va_list所定义变量为字符指针。

宏

**INTSIZEOF** **宏**,获取类型占用的空间长度，最小占用长度为int的整数倍：

\#define _INTSIZEOF(n) ( (sizeof(n) + sizeof(int) - 1) & ~(sizeof(int) - 1) )

**VA_START****宏**，获取可变参数列表的第一个参数的地址（ap是类型为va_list的指针，v是可变参数最左边的参数）：

\#define va_start(ap,v) ( ap = (va_list)&v + _INTSIZEOF(v) )

**VA_ARG****宏**，获取可变参数的当前参数，返回指定类型并将指针指向下一参数（t参数描述了当前参数的类型）：

\#define va_arg(ap,t) ( *(t *)((ap += _INTSIZEOF(t)) - _INTSIZEOF(t)) )

**VA_END****宏**，清空va_list可变参数列表：

\#define va_end(ap) ( ap = (va_list)0 )

用法

（1）首先在函数里定义一具VA_LIST型的变量，这个变量是指向参数的指针；

（2）然后用VA_START宏初始化刚定义的VA_LIST变量；

（3）然后用VA_ARG返回可变的参数，VA_ARG的第二个参数是你要返回的参数的类型（如果函数有多个可变参数的，依次调用VA_ARG获取各个参数）；

（4）最后用VA_END宏结束可变参数的获取。

注意问题

（1）可变参数的类型和个数完全由程序代码控制,它并不能智能地识别不同参数的个数和类型；

（2）如果我们不需要一一详解每个参数，只需要将可变列表拷贝至某个缓冲，可用vsprintf函数；

（3）因为编译器对可变参数的函数的原型检查不够严格,对编程查错不利.不利于我们写出高质量的代码；

 

来自 <<https://baike.baidu.com/item/va_list>> 

 

 

 

[对C语言中va_list，va_start，va_arg和va_end的一点理解](https://www.cnblogs.com/bwangel23/p/4700496.html)

这几个函数和变量是针对可变参数函数的，什么是可变参数函数呢，最经典的莫过于printf和scanf，这两个函数的声明如下：

1 int printf(const char *format, ...);
 2 
 3 int scanf(const char *format, ...);

这两个函数声明中省略号(...)表示的就是任意个数的参数，可变参数函数就是输入的参数的个数是可变的，那么这个具体是怎么实现的呢？

 

要了解这个是怎么实现，首先我们就要先理解一点，参数是如何传递给函数的。众所周知，函数的数据是存放于栈中的，那么给一个函数传递传递参数的过程就是将函数的参数从右向左逐次压栈，例如：

func(int i, char c, doube d)

这个函数传递参数的过程就是将d，c，i逐次压到函数的栈中，由于栈是从高地址向低地址扩展的，所以d的地址最高，i的地址最低。

 

理解了函数传递参数的过程，再来说一下va_list的原理，通常，可变参数的代码是这么写的：

 

 void func(char *fmt, ...)
  {
 	va_list ap;
	 va_start(ap, fmt);
	va_arg(ap, int);
 	va_end(va);      
  }

 

这里ap其实就是一个指针，指向了参数的地址。

va_start()所做的就是让ap指向函数的最后一个确定的参数（声明程序中是fmt）的下一个参数的地址。

va_arg()所做的就是根据ap指向的地址，和第二个参数所确定的类型，将这个参数的中的数据提取出来，作为返回值，同时让ap指向下一个参数。

va_end()所做的就是让ap这个指针指向0。

 

关于这三个参数实现的宏可以参看下面的实现：

 

1 // 使ap指向第一个可变参数的地址
 2 #define  va_start(ap,v)     ( ap = (va_list)&v + _INTSIZEOF(v) )
 3 
 4 // 使ap指向下一个可变参数，同时将目前ap所指向的参数提取出来并返回
 5 #define  va_arg(ap,t)       ( *(t *)((ap += _INTSIZEOF(t)) - _INTSIZEOF(t)) )
 6 
 7 //  销毁ap 
 8 #define  va_end(ap)         ( ap = (va_list)0 ) 

 

 

参考文章：

\1. [详解 C语言可变参数 va_list和_vsnprintf及printf实现](http://wenku.baidu.com/view/ecb33901de80d4d8d15a4fe3.html)

 

来自 <<https://www.cnblogs.com/bwangel23/p/4700496.html>> 

 

 
