# Effective C++读书笔记(24): 需要参数类型转换的函数不能是成员

**守则24: 如果所有参数都需要类型转换，它就要作为非成员函数**

> "Declare non-member fuctions when type conversions should apply to all parameters"

------

***本篇关键词: 隐式转换，类型转换，成员函数\***

------



虽然在[第15章](https://zhuanlan.zhihu.com/p/73563364)讨论过隐式转换总体上会给程序带来隐患，因为如果出现了类型错误，编译器是不会报错的。但当我们在设计跟数字相关的类时，比如用一个类代表有理数，支持int的隐式转换是完全合理的。此外C++自己的自有类型也支持多种隐式转换，例如从int到double，那么我们也可以这样写这个有理数类:

```text
class Rational{
  public:
    Rational(int numerator = 0, int denominator = 1);
    //构造函数专门不声明为explicit来允许从int到Rational的隐式转换
    int numerator() const;
    int denominator() const;
  ...
};
```

作为一个有理数，我们当然也需要定义各种算术运算符，例如加减乘除，但它们到底要作为成员函数还是非成员函数? 可能直觉会告诉我们：迷的话按照面向对象那一套来就行了。既然我们的operator*是给Rational类用的，那么它就应该是个成员函数！

不过还记得[第23章](https://zhuanlan.zhihu.com/p/81361540)解释的，随意把函数作为成员函数的话，反而会破坏封装，违反面向对象准则吗? 先不管这些，我们现在就先看如果operator*是一个成员函数会怎么样:

```text
class Rational{
  public:
    ...
    const Rational operator*(const Rational& lhs) const;
  ...
};
```

(见[第3章](https://zhuanlan.zhihu.com/p/63609476)为什么要返回const，[第20章](https://zhuanlan.zhihu.com/p/77753938)为什么要使用引用传递，[第21章](https://zhuanlan.zhihu.com/p/79502926)为什么不返回引用)

这个设计可以让你把任何两个Rational对象相乘:

```text
Rational oneEighth(1,8);
Rational oneHalf(1,2);
Rational result = oneEighth * oneHalf; //编译通过
result = result * oneEighth; //编译通过
```

但还不能太满足，作为一个有理数，我们还希望它能与自带类型比如int进行互动，毕竟它们都是一个数，只不过就是类型不一样。现在看如下操作:

```text
result = oneHalf * 2; //编译通过
result = 2 * oneHalf; //编译错误
```

具体错误是如何产生的，我们把以上两行代码用它们等价的函数重写一下:

```text
result = oneHalf.operator*(2); //编译通过
result = 2.operator*(oneHalf); //错误
```

2作为一个整型当然没有成员函数operator*，但编译器可能也会去看非成员函数，例如在全局或者名空间作用域下声明的operator*，如果找到了就会这么调用:

```text
result = operator*(2, oneHalf);
```

如果都没有搜索到的话，编译器就只能报错了。

但我们看第一个成功的语句是不是也有一些疑问? 为什么我们定义的运算符要输入Rational参数，但传进去整型2也可以编译? 其实这就是隐式转换(implicit  conversion)。编译器用我们传进去的2隐式地调用了Rational的构造函数，因此真正发生的是下面这样:

```text
const Rational tmp(2);
result = oneHalf * tmp;
```

但编译器会这样做也是因为我们没有把构造函数声明为explicit，否则两行语句都不能编译:

```text
result = oneHalf * 2; //如果构造函数声明为explicit，int便不能转换为Rational
result = 2 * oneHalf; //这行还是上面的原因
```

------

要记住**只有在参数表里出现的参数才可以进行隐式转换**。我们这里的operator*作为成员函数，只能对乘号右边的参数即rhs进行隐式转换。而不在参数表里的参数，即调用成员函数的对象，也就是this指向的，是*不可能*被隐式转换的，所以整型2在乘号左边是不可能被隐式转换为Rational的，因此上面第一行的代码可以通过编译，第二行则不可以。

```text
(*this).someFunction(someThing1, someThing2); 
//*this是不可能被隐式转换的，只有someThing1，someThing2才可能被隐式转换
```

但我们归根结底还是希望oneHalf*2和2*oneHalf都可以编译，毕竟乘法交换律，否则我们的运算符就是有局限性的，而且只有2在右边的时候才能编译还显得格外别扭。那么如何实现呢? 可能答案现在已经清楚了，就是把operator*作为一个**非成员函数**，那么参数列表就可以包含乘号两边的参数，两个参数也都能进行隐式转换了:

```text
class Rational{...};
const Rational operator*(const Rational& lhs, const Rational& rhs){
  return Rational(lhs.numerator() * rhs.numerator(),
                  lhs.denominator() * rhs.denominator())
}//作为非成员函数
Rational oneFourth(1,4);
Rational result;
result = oneFourth * 2; //可以编译
result = 2 * oneFourth; //可以编译
```

这当然是个大好结局，但你刚刚是不是突然闪过了一个念头，既然不能成为一部分，那可不可以做朋友? 答案是No。(;´༎ຶД༎ຶ`)

因为我们从Rational类的公有接口就已经可以实现想要的功能了，不再需要额外的特殊接口。其实这是很多学习C++的人都会有的一个**误区**: 如果某个函数跟某个类相关，并且不能作为成员函数，那么它就是友元函数。这个例子证明这个想法是不必要的，而且要能不用友元函数就不用，还记得[上一章](https://zhuanlan.zhihu.com/p/81361540)讲到友元函数也是对封装有影响的吗? 

用作者的原话就是:

> "Whenever you can avoid friend function, you should, much as in real life, friends are often more trouble than they worth."

彳亍口巴。总之就是要记着如果某函数跟某类相关，并且不能作为成员函数，它并不一定要成为友元函数。

最后就是这一章只是放在面向对象C++的环境下讨论，[第1章](https://zhuanlan.zhihu.com/p/63515998)讲过C++是多种"子语言"的集合。如果要放在模板C++的环境下，比如我们要把Rational类写作一个模板类，那么就会有新规则适用，具体如何会在以后的章节里讲到。

**总结:**

- 如果所有的参数都可能需要隐式转换，这个函数必须要作为非成员函数