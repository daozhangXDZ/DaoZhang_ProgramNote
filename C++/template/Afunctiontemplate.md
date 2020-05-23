# 函数模板

 

[ C++](https://zh.cppreference.com/w/cpp)

 

[C++ 语言](https://zh.cppreference.com/w/cpp/language)

 

[模板](https://zh.cppreference.com/w/cpp/language/templates)

 

函数模板定义一族函数。 

###  语法

|                                                              |      |            |
| ------------------------------------------------------------ | ---- | ---------- |
| `**template**` `**<**` 形参列表 `**>**` 函数声明             | (1)  |            |
|                                                              |      |            |
| `**template**` `**<**` 形参列表 `**>**` `**requires**` 制约 函数声明 | (2)  | (C++20 起) |
|                                                              |      |            |
| 带占位符函数声明                                             | (3)  | (C++20 起) |
|                                                              |      |            |
| `**export**` `**template**` `**<**` 形参列表 `**>**` 函数声明 | (4)  | (C++11 前) |
|                                                              |      |            |

###  解释

| 形参列表                | -    | 非空的[模板形参](https://zh.cppreference.com/w/cpp/language/template_parameters)的逗号分隔列表，每项是[非类型形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E9.9D.9E.E7.B1.BB.E5.9E.8B.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)、[类型形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E7.B1.BB.E5.9E.8B.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)、[模板形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E6.A8.A1.E6.9D.BF.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)或这些的[形参包](https://zh.cppreference.com/w/cpp/language/parameter_pack)之一。与任何模板一样，形参可以[有制约](https://zh.cppreference.com/w/cpp/language/template_parameters#.E6.9C.89.E5.88.B6.E7.BA.A6.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)。 (C++20 起) |
| ----------------------- | ---- | ------------------------------------------------------------ |
| 函数声明                | -    | [函数声明](https://zh.cppreference.com/w/cpp/language/function)。所声明的函数名成为模板名。 |
| 制约(C++20)             | -    | [制约表达式](https://zh.cppreference.com/w/cpp/language/constraints)，它限制此函数模板接受的模板形参。 |
| 带占位符函数声明(C++20) | -    | [函数声明](https://zh.cppreference.com/w/cpp/language/function)，其中至少一个形参的类型使用了占位符 [`auto`](https://zh.cppreference.com/w/cpp/language/auto) 或 Concept auto：模板形参列表将对每个占位符拥有一个虚设形参。（见下文“简写函数模板”） |

| `export` 是可选的修饰符，声明模板*被导出*（用于类模板时，它声明所有成员被导出）。对被导出模板进行实例化的文件不需要包含其定义：声明就足够了。`export` 的实现稀少而且在细节上互不一致。 | (C++11 前) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

| 简写函数模板 当函数声明或函数模板声明的形参列表中出现占位符类型（`auto` 或 [Concept auto](https://zh.cppreference.com/w/cpp/concepts)）时，该声明声明一个函数模板，并且为每个占位符向模板形参列表追加一个虚设的模板形参  `void f1(auto); // 与 template<class T> void f(T) 相同 void f2(C1 auto); // 若 C1 是概念，则与 template<C1 T> void f2(T) 相同 void f3(C2 auto...); // 若 C2 是概念，则与 template<C2... Ts> void f3(Ts...) 相同 void f4(const C3 auto*, C4 auto&); // 与 template<C3 T, C4 U> void f4(const T*, U&); 相同 template <class T, C U> void g(T x, U y, C auto z); // 与 template<class T, C U, C W> void g(T x, U y, W z); 相同` 简写函数模板可以和所有函数模板一样进行特化。  `template<> void f4<int>(const int*, const double&); // f4<int, const double> 的特化` | (C++20 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

###  函数模板实例化

函数模板自身并不是类型、函数或任何实体。从仅包含模板定义的源文件不生成任何代码。为使得代码出现必须实例化模板：必须确定各模板实参，以令编译器能生成一个实际的函数（或从类模板生成类）。 

####  显式实例化

|                                                              |      |            |
| ------------------------------------------------------------ | ---- | ---------- |
| `**template**` 返回类型 名字 `**<**`  实参列表 `**>**` `**(**` 形参列表 `**)**` `**;**` | (1)  |            |
|                                                              |      |            |
| `**template**` 返回类型 名字 `**(**` 形参列表 `**)**` `**;**` | (2)  |            |
|                                                              |      |            |
| `**extern**` `**template**` 返回类型 名字 `**<**` 实参列表 `**>**` `**(**` 形参列表 `**)**` `**;**` | (3)  | (C++11 起) |
|                                                              |      |            |
| `**extern**` `**template**` 返回类型 名字 `**(**` 形参列表 `**)**` `**;**` | (4)  | (C++11 起) |
|                                                              |      |            |

1) 显式实例化定义（当每个无默认值模板形参都被显式指定时，无[模板实参推导](https://zh.cppreference.com/w/cpp/language/template_argument_deduction)）

2) 显式实例化定义，对所有形参进行模板实参推导

3) 显示实例化声明（当每个无默认值模板形参都被显式指定时，无模板实参推导）

4) 显示实例化声明，对所有形参进行模板实参推导

显式实例化定义强制实例化其所指代的函数或成员函数。它可以出现在程序中模板定义后的任何位置，而对于给定的实参列表，只允许它在整个程序中出现一次。 

| 显式实例化声明（extern 模板）阻止隐式实例化：本来会导致隐式实例化的代码，必须使用已在程序的别处所提供的显式实例化。 | (C++11 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

函数模板特化或成员函数模板特化的显式实例化中，尾部的各模板实参，若能从函数参数[推导](https://zh.cppreference.com/w/cpp/language/template_argument_deduction)，则可以不指定 

```c++
template<typename T>
void f(T s)
{
    std::cout << s << '\n';
}
 
template void f<double>(double); // 实例化 f<double>(double)
template void f<>(char); // 实例化 f<char>(char)，推导出模板实参
template void f(int); // 实例化 f<int>(int)，推导出模板实参
```

函数模板或类模板成员函数的显式实例化不能使用 `inline` 或 `constexpr`。若显式实例化的声明指名了某个隐式声明的特殊成员函数，则程序非良构。 

显式实例化声明并不抑制 [inline](https://zh.cppreference.com/w/cpp/language/inline) 函数，[auto](https://zh.cppreference.com/w/cpp/language/auto) 声明，引用，以及类模板特化的隐式实例化。（从而，当作为显式实例化声明目标的 inline 函数被 ODR 式使用时，函数将为内联而隐式实例化，但此翻译单元中不生成其非内联副本） 

带有[默认实参](https://zh.cppreference.com/w/cpp/language/default_arguments)的函数模板的显式实例化定义，不是对该实参的使用，且不会试图实例化之： 

```c++
char* p = 0;
template<class T> T g(T x = &p) { return x; }
template int g<int>(int);   // OK 即使 &p 不是 int。
```

####  隐式实例化

当代码在要求存在函数定义的语境中指涉某个函数，而这个特定函数尚未被显式实例化时，发生隐式实例化。若模板实参列表能从语境[推导](https://zh.cppreference.com/w/cpp/language/template_argument_deduction)，则不必提供它。 

运行此代码

```c++
#include <iostream>
 
template<typename T>
void f(T s)
{
    std::cout << s << '\n';
}
 
int main()
{
    f<double>(1); // 实例化并调用 f<double>(double)
    f<>('a'); // 实例化并调用 f<char>(char)
    f(7); // 实例化并调用 f<int>(int)
    void (*ptr)(std::string) = f; // 实例化 f<string>(string)
}
```


  

注意：完全省略 `<>` 允许[重载决议](https://zh.cppreference.com/w/cpp/language/overload_resolution)同时检验模板与非模板重载。 

###  模板实参推导

为实例化一个**函数模板**，每个模板实参都必为已知的，但并非必须指定每个模板实参。只要可能，编译器都会从函数实参推导缺失的模板实参。这发生于尝试进行函数调用时，以及取函数模板的地址时。 

```c++
template<typename To, typename From> To convert(From f);
 
void g(double d) 
{
    int i = convert<int>(d); // 调用 convert<int,double>(double)
    char c = convert<char>(d); // 调用 convert<char,double>(double)
    int(*ptr)(float) = convert; // 实例化 convert<int, float>(float)
}
```

此机制使得使用模板运算符可行，因为除了将其重写为函数调用表达式之外，不存在为运算符指定模板实参的语法。 

```c++
#include <iostream>
int main() 
{
    std::cout << "Hello, world" << std::endl;
    // operator<< 经由 ADL 查找为 std::operator<<，
    // 然后推导出 operator<<<char, std::char_traits<char>>
    // 同时推导 std::endl 为 &std::endl<char, std::char_traits<char>>
}
```

模板实参推导在函数模板的[名字查找](https://zh.cppreference.com/w/cpp/language/lookup)（可能涉及[实参依赖查找](https://zh.cppreference.com/w/cpp/language/adl)）之后，在[重载决议](https://zh.cppreference.com/w/cpp/language/overload_resolution)之间进行。 

细节见[模板实参推导](https://zh.cppreference.com/w/cpp/language/template_argument_deduction)。 

###  显式模板实参

函数模板的模板实参可从以下途径获得 

-  模板实参推导 
-  默认模板实参 
-  显式指定，可以在下列语境中进行： 



不存在为[重载的运算符](https://zh.cppreference.com/w/cpp/language/operators)、[转换函数](https://zh.cppreference.com/w/cpp/language/cast_operator)及构造函数显式指定模板实参的方法，因为它们的调用中并未使用函数名。 

所指定的各模板实参必须与各模板形参在种类上相匹配（即类型对类型，非类型对非类型，模板对模板）。不能有多于形参数量的实参（除非形参之一是形参包，这种情况下对每个非包形参必须有一个实参）。 

所指定的非类型实参必须要么与其对应的非类型模板形参的类型相匹配，要么[可转换成它们](https://zh.cppreference.com/w/cpp/language/template_parameters#.E6.A8.A1.E6.9D.BF.E9.9D.9E.E7.B1.BB.E5.9E.8B.E5.AE.9E.E5.8F.82)。 

不参与模板实参推导的函数实参（例如若对应的模板实参已被显式指定），参与到其对应函数形参类型的隐式转换（如在通常[重载决议](https://zh.cppreference.com/w/cpp/language/overload_resolution)中一样）。 

当有额外的实参时，模板实参推导可以对显式指定的模板形参包进行扩充： 

```c++
template<class ... Types> void f(Types ... values);
void g() {
  f<int*, float*>(0, 0, 0); // Types = {int*, float*, int}
}
```

###  模板实参替换

当已经指定、推导出或从默认模板实参获得了所有的模板实参之后，函数形参列表中对模板形参的每次使用都会被替换成对应的模板实参。 

函数模板的替换失败（即以推导或提供的模板实参替换模板形参失败），将函数模板从[重载集](https://zh.cppreference.com/w/cpp/language/overload_resolution)中移除。这就允许使用许多方式通过模板元编程来操作重载集：细节见 [SFINAE](https://zh.cppreference.com/w/cpp/language/sfinae)。 

替换之后，所有数组和函数类型的函数形参都被调整为指针，而所有顶层 cv 限定符都从函数形参中丢弃（如在常规[函数声明](https://zh.cppreference.com/w/cpp/language/function#.E5.87.BD.E6.95.B0.E5.A3.B0.E6.98.8E)中一样）。 

去除顶层 cv 限定符并不会影响形参在函数之内所展现的类型： 

```c++
template <class T> void f(T t);
template <class X> void g(const X x);
template <class Z> void h(Z z, Z* zp);
 
// 两个不同函数具有相同类型，但在函数中，t 有不同的 cv 限定
f<int>(1);       // 函数类型是 void(int)，t 为 int
f<const int>(1); // 函数类型是 void(int)，t 为 const int
 
// 两个不同函数具有相同类型和相同的 x
// （指向这两个函数的指针不相等，且函数局部的静态变量可以拥有不同地址）
g<int>(1);       // 函数类型是 void(int) ， x 为 const int
g<const int>(1); // 函数类型是 void(int) ， x 为 const int
 
// 仅丢弃顶层 cv 限定符：
h<const int>(1, NULL); // 函数类型是 void(int, const int*) 
                       // z 为 const int ， zp 为 int*
```

###  函数模板重载

函数模板与非模板函数可以重载。 

非模板函数始终不同于具有相同类型的模板特化。不同函数模板的特化，即使具有相同类型也始终彼此不同。两个具有相同返回类型和相同形参列表的函数模板是不同的，而且可用显式模板实参列表进行区分。 

当使用了类型或非类型模板形参的表达式在函数形参列表或返回类型中出现时，为重载的目的，该表达式保留为函数模板签名的一部分： 

```c++
template<int I, int J> A<I+J> f(A<I>, A<J>); // 重载 #1
template<int K, int L> A<K+L> f(A<K>, A<L>); // 同 #1
template<int I, int J> A<I-J> f(A<I>, A<J>); // 重载 #2
```

对于两个涉及模板形参的表达式，若两个包含这些表达式的函数定义根据 [ODR 规则](https://zh.cppreference.com/w/cpp/language/definition#.E5.8D.95.E4.B8.80.E5.AE.9A.E4.B9.89.E8.A7.84.E5.88.99.EF.BC.88ODR.EF.BC.89)相同，则称它们*等价*，就是说，除了模板形参的命名可以不同之外，这两个表达式含有相同的记号序列，其中的各个名字通过名字查找都解析到相同实体。两个 [lambda 表达式](https://zh.cppreference.com/w/cpp/language/lambda)始终不等价。 (C++20 起) 

```c++
template <int I, int J> void f(A<I+J>);  // 模板重载 #1
template <int K, int L> void f(A<K+L>);  // 等价于 #1
```

| 在确定两个[待决表达式](https://zh.cppreference.com/w/cpp/language/dependent_name)是否等价时，只考虑其中所涉及的各待决名，而不考虑名字查找的结果。如果相同模板的多个声明在名字查找的结果上有所不同，则使用首个这种声明：  `template <class T> decltype(g(T())) h(); // decltype(g(T())) 是待决类型 int g(int); template <class T> decltype(g(T())) h() { // h() 的再声明使用较早的查找     return g(T());                     // ……尽管此处的查找找到了 g(int) } int i = h<int>();   // 模板实参替换失败；在 h() 的首个声明处 g(int) 不在作用域中` | (C++14 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

当足下列条件时，认为两个函数模板*等价* 

-  它们声明于同一作用域 
-  它们具有相同的名字 
-  它们具有相同的模板形参列表 
-  其返回类型和形参列表中，各个涉及模板实参的表达式均*等价* 

| 模板形参列表之后的 requires 子句（若存在）中的各个表达式均等价  函数声明符之后的 requires 子句（若存在）中的各个表达式等价 | (C++20 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

对于两个涉及模板形参的表达式，如果它们不*等价*，但对于任何给定的模板实参集，两个表达式的求值都产生相同的值，则称它们*功能等价*。 

如果两个函数模板本可*等价*，但其返回类型和形参列表中一或多个涉及模板形参的表达式*功能等价*，则称它们*功能等价*。 

| 另外，如果为两个函数模板指定的制约不同，但它们接受且被相同的模板实参列表的集合所满足，则它们*功能等价*但不*等价*。 | (C++20 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

若程序含有*功能等价*但不*等价*的函数模板声明，则程序非良构；不要求诊断。 

```c++
// 等价
template <int I> void f(A<I>, A<I+10>); // 重载 #1
template <int I> void f(A<I>, A<I+10>); // 重载 #1 的再声明
 
// 不等价
template <int I> void f(A<I>, A<I+10>); // 重载 #1
template <int I> void f(A<I>, A<I+11>); // 重载 #2
 
// 功能等价但不等价
// 程序非良构，不要求诊断
template <int I> void f(A<I>, A<I+10>); // 重载 #1
template <int I> void f(A<I>, A<I+1+2+3+4>); // 功能等价
```

当同一个函数模板特化与多于一个重载的函数模板相匹配时（这通常由[模板实参推导](https://zh.cppreference.com/w/cpp/language/template_argument_deduction)所导致），进行*重载函数模板的部分排序*以选择最佳匹配。 

具体而言，在以下情形中发生部分排序： 

1)

 对函数模板特化的调用的

重载决议

```
template<class X> void f(X a);
template<class X> void f(X* a);
int* p;
f(p);
```

2)

 当取得

函数模板特化的地址

时 

```
template<class X> void f(X a);
template<class X> void f(X* a);
void (*p)(int*) = &f;
```

3)

 选当择作为函数模板特化的

布置 `operator delete`

 以匹配布置 

```
operator new
```

 时 

|      | 本节未完成 原因：小示例 |
| ---- | ----------------------- |
|      |                         |

4)

 当

友元函数声明

、

显式实例化

或

显式特化

指代函数模板特化时 

```
template<class X> void f(X a);  // 第一个 template f
template<class X> void f(X* a); // 第二个 template f
template<> void f<>(int *a) {} // 显式特化
 // 模板实参推导出现两个候选：
 // foo<int*>(int*) 与 f<int>(int*)
 // 部分排序选择 f<int>(int*)，因为它更特殊
```

非正式而言，“A 比 B 更特殊”意味着“A 比 B 接受更少的类型”。 

正式而言，为确定任意两个函数模板中哪个更特殊，部分排序过程首先对两个模板之一进行以下变换： 

-  对于每个类型、非类型及模板形参，包括形参包，生成一个唯一的虚构类型、值或模板，以之在模板的函数类型中进行替换 
-  若要比较的两个函数模板中只有一个是成员函数，且该函数模板是某个类 `A` 的非静态成员，则向其形参列表插入一个新的首个形参，当成员函数模板为 && 限定时，其类型为 `cv A&&`，否则为 `cv A&`（其中 cv 是成员函数模板的 cv 限定）——这有助于对运算符的排序，它们是同时作为成员与非成员函数查找的： 

```
struct A {};
template<class T> struct B {
  template<class R> int operator*(R&);                     // #1
};
template<class T, class R> int operator*(T&, R&);          // #2
int main() {
  A a;
  B<A> b;
  b * a; // 模板实参推导对于 int B<A>::operator*(R&) 给出 R=A 
         //           对于 int operator*(T&, R&)，T=B<A>，R=A
// 为进行部分排序，成员 template B<A>::operator*
// 被变换成 template<class R> int operator*(B<A>&, R&);
//     int operator*(   T&, R&)  T=B<A>, R=A
// 与  int operator*(B<A>&, R&)  R=A 间的部分排序
// 选择 int operator*(B<A>&, A&) 为更特殊者
```

在按上方描述变换两个模板之一后，以变换后模板为实参模板，以另一模板的原模板类型为形参模板，执行[模板实参推导](https://zh.cppreference.com/w/cpp/language/template_argument_deduction)。然后以第二个模板（进行变换后）为实参，以第一个模板的原始形式为形参重复这一过程。 

用于确定顺序的类型取决于语境： 

-  在函数调用的语境中，这些类型是在这个函数调用中具有实参的函数形参的类型（不考虑默认函数实参、形参包和省略号形参——见下文） 
-  在调用用户定义的转换函数的语境中，使用转换函数模板的返回类型 
-  在其他语境中，使用函数模板类型 

形参模板中的每个以上列出的类型都被推导。推导开始前，以下列方式对形参模板的每个形参 `**P**` 和实参模板的对应实参 `**A**` 进行调整： 

-  若 `**P**` 与 `**A**` 此前均为引用类型，则确定哪个更为 cv 限定（其他所有情况下，就部分排序而言都忽略 cv 限定） 
-  若 `**P**` 是引用类型，则以其所引用的类型替换它 
-  若 `**A**` 是引用类型，则以其所引用的类型替换它 
-  若 `**P**` 有 cv 限定，则 `**P**` 被替换为自身的无 cv 限定版本 
-  若 `**A**` 有 cv 限定，则 `**A**` 被替换为自身的无 cv 限定版本 

在这些调整后，遵循[从类型进行模板实参推导规则](https://zh.cppreference.com/w/cpp/language/template_argument_deduction#.E4.BB.8E.E7.B1.BB.E5.9E.8B.E6.8E.A8.E5.AF.BC)，从 `**A**` 推导 `**P**` 。 

若 P 是函数形参包，则实参模板的每个剩余形参类型的类型 A，都与该函数参数包的声明符标识的类型 P 进行比较。每次比较都为该函数参数包所展开的模板参数包中的后继位置的进行模板实参的推导。 

若 A 从函数参数包变换而来，则推导失败。 (C++14 前)将它与形参模板的每个剩余形参类型进行比较。 (C++14 起) 

若变换后的模板 1 的实参 `**A**` 可用来推导模板 2 的对应形参 `**P**`，但反之不可，则对于从这一对 P/A 所推导的类型而言，这个 `**A**` 比 `**P**` 更特殊。 

若双向推导均成功，且原 `**P**` 与 `**A**` 是引用类型，则做附加的测试： 

-  若 `**A**` 是左值引用而 `**P**` 是右值引用，则认为 A 比 P 更特殊 
-  若 `**A**` 比 `**P**` 更有 cv 限定，则认为 A 比 P 更特殊 

所有其他情况下，对于这一对 P/A 所推导的类型而言，没有模板比另一个更特殊。 

在以两个方向考虑每个 P 与 A 后，若对于所考虑的每个类型， 

-  模板 1 对所有类型至少与模板 2 一样特殊 
-  模板 1 对某些类型比模板 2 特殊 
-  模板 2 对任何类型都不比模板 1 更特殊，或并非对任何类型都至少一样特殊 

则模板 1 比模板 2 更特殊。若上述条件在切换模板顺序后为真，则模板 2 比模板 1 更特殊。否则，没有模板比另一个更特殊。 持平的情况下，若一个函数模板有一个尾部的形参包而另一个没有，则认为带有被忽略的形参者比有空形参包者更特殊。 

若在考虑所有的重载模板对之后，有一个无歧义地比所有其他的都更特殊，则选择这个模板的特化，否则编译失败。 

在下列示例中，虚构实参被称为 U1, U2 

```
template<class T> void f(T);        // 模板 #1
template<class T> void f(T*);       // 模板 #2
template<class T> void f(const T*); // 模板 #3
void m() {
  const int* p;
  f(p); // 重载决议选取：  #1：void f(T ) [T = const int *]
        // 　            #2：void f(T*) [T = const int]
        // 　            #3：void f(const T *) [T = int]
// 部分排序
// #1 从变换后的 #2：void(T) 从 void(U1*)：P=T A=U1*：推导 ok：T=U1*
// #2 从变换后的 #1：void(T*) 从 void(U1)：P=T* A=U1：推导失败
// 对于 T 而言 #2 比 #1 更特殊
// #1 从变换后的 #3：void(T) 从 void(const U1*)：P=T, A=const U1*：ok
// #3 从变换后的 #1：void(const T*) 从 void(U1)：P=const T*, A=U1：失败
// 对于 T 而言 #3 比 #1 更特殊
// #2 从变换后的 #3：void(T*) 从 void(const U1*)：P=T* A=const U1*：ok
// #3 从变换后的 #2：void(const T*) 从 void(U1*)：P=const T* A=U1*：失败
// 对于 T 而言 #3 比 #2 更特殊
// 结果：#3 被选择
// 换言之，f(const T*) 比 f(T) 或 f(T*) 更特殊
}
template<class T> void f(T, T*);    // #1
template<class T> void f(T, int*);  // #2
void m(int* p) {
    f(0, p); // #1 的推导：void f(T, T*) [T = int]
             // #2 的推导：void f(T, int*) [T = int]
 // 部分排序：
 // #1 从 #2：void(T,T*) 从 void(U1,int*)：P1=T, A1=U1：T=U1
 //                                       P2=T*, A2=int*：T=int：失败
 // #2 从 #1：void(T,int*) 从 void(U1, U2*)：P1=T A1=U1：T=U1
 //                                         P2=int* A2=U2*：失败
 // 对于 T 而言无一更特殊，调用有歧义
}
template<class T> void g(T);  // 模板 #1
template<class T> void g(T&); // 模板 #2
void m() {
  float x;
  g(x); // 从 #1 推导：void g(T ) [T = float]
        // 从 #2 推导：void g(T&) [T = float]
// 部分排序
// #1 从 #2：void(T) 从 void(U1&)：P=T, A=U1（调整后）：ok
// #2 从 #1：void(T&) 从 void(U1)：P=T（调整后） A=U1 ：ok
// 对于 T 而言无一更特殊，调用有歧义
}
template<class T> struct A { A(); };
 
template<class T> void h(const T&); // #1
template<class T> void h(A<T>&);    // #2
void m() {
  A<int> z;
  h(z);  // 从 #1 推导：void h(const T &) [T = A<int>]
         // 从 #2 推导：void h(A<T> &) [T = int]
 // 部分排序
 // #1 从 #2：void(const T&) 从 void(A<U1>&)：P=T A=A<U1>：ok T=A<U1>
 // #2 从 #1：void(A<T>&) 从 void(const U1&)：P=A<T> A=const U1：失败
 // 对于 T 而言 #2 比 #1 更特殊
 
  const A<int> z2;
  h(z2); // 从 #1 推导：void h(const T&) [T = A<int>]
         // 从 #2 推导：void h(A<T>&) [T = int]，但替换失败
 // 只有一个可选择的重载，不尝试部分排序，调用 #1
}
```

因为在调用语境中只考虑有明确的调用实参的形参，故没有明确的调用实参的形参，包括函数形参包、省略号形参及有默认实参的形参均被忽略： 

```
template<class T>  void  f(T);               // #1
template<class T>  void  f(T*, int=1);       // #2
void m(int* ip) {
  int* ip;
  f(ip);     // 调用 #2（T* 比 T 更特殊）
}
template<class  T>  void  g(T);               // #1
template<class  T>  void  g(T*, ...);         // #2
void m(int* ip) {
   g(ip);     // 调用 #2（T* 比 T 更特殊）
}
template<class T, class U> struct A { };
template<class T, class U> void f(U, A<U,T>* p = 0); // #1
template<         class U> void f(U, A<U,U>* p = 0); // #2
void h() {
  f<int>(42, (A<int, int>*)0);  // 调用 #2
  f<int>(42);                   // 错误：歧义
}
template<class T           >  void g(T, T = T());  // #1
template<class T, class... U> void g(T, U ...);    // #2
void h() {
  g(42);  // 错误：歧义
}
template<class  T, class... U> void f(T, U...);           // #1
template<class  T            > void f(T);                 // #2
void h(int i) {
  f(&i);        // 调用 #2 因为形参包与无形参之间的决胜规则
                // （注意：在 DR692 与 DR1395 之间时有歧义）
}
template<class  T, class... U> void g(T*, U...);          // #1
template<class  T            > void g(T);                 // #2
void h(int i) {
  g(&i);        // OK：调用 #1（T* 比 T 更特殊）
}
template <class ...T> int f(T*...);  // #1
template <class T>  int f(const T&); // #2
f((int*)0); // OK：选择 #1
            // （DR1395 之前有歧义，因为两个方向的推导均失败）
template<class... Args>           void f(Args... args);               // #1
template<class T1, class... Args> void f(T1 a1, Args... args);        // #2
template<class T1, class T2>      void f(T1 a1, T2 a2);               // #3
f();                  // 调用 #1
f(1, 2, 3);           // 调用 #2
f(1, 2);              // 调用 #3；非变参模板 #3 比变参模板 #1 与 #2 更特殊
```

在部分排序过程的模板实参推导期间，若实参未被部分排序所考虑的任何类型使用，则不要求该实参与模板形参相匹配 

```
template <class T>          T f(int);  // #1
template <class T, class U> T f(U);    // #2
void g() {
  f<int>(1);  // #1 的特化为显式：T f(int) [T = int]
              // #2 的特化为推导：T f(U) [T = int, U = int]
// 部分排序（仅考虑实参类型）
// #1 从 #2：T(int) 从 U1(U2)：失败
// #2 从 #1：T(U) 从 U1(int)：ok：U=int, T 未使用
// 调用 #1
}
```

对包含模板形参包的函数模板进行的部分排序，与为这些模板形参包所推导的实参数量无关。 

```
template<class...> struct Tuple { };
template<          class... Types> void g(Tuple<Types ...>);        // #1
template<class T1, class... Types> void g(Tuple<T1, Types ...>);    // #2
template<class T1, class... Types> void g(Tuple<T1, Types& ...>);   // #3
 
g(Tuple<>());                     // 调用 #1
g(Tuple<int, float>());           // 调用 #2
g(Tuple<int, float&>());          // 调用 #3
g(Tuple<int>());                  // 调用 #3
```


 

|      | 本节未完成 原因：14.8.3[temp.over] |
| ---- | ---------------------------------- |
|      |                                    |

为编译对函数模板的调用，编译器必须在非模板重载、模板重载和模板重载的特化间作出决定。 

```
template< class T > void f(T);              // #1：模板重载
template< class T > void f(T*);             // #2：模板重载
void                     f(double);         // #3：非模板重载
template<>          void f(int);            // #4：#1 的特化
 
f('a');        // 调用 #1
f(new int(1)); // 调用 #2
f(1.0);        // 调用 #3
f(1);          // 调用 #4
```

###  函数重载 vs 函数特化

注意，只有非模板和主模板重载参与重载决议。特化并不是重载而不受考虑。只有在重载决议选择最佳匹配的主函数模板后，才检验其特化以查看何者为最佳匹配。 

```
template< class T > void f(T);    // #1：所有类型的重载
template<>          void f(int*); // #2：针对指向 int 的指针的 #1 的特化
template< class T > void f(T*);   // #3：所有指针类型的重载
 
f(new int(1)); // 调用 #3，虽然 #1 的特化是完美匹配
```

在对翻译单元的头文件进行排序时，记住此规则很重要。有关函数重载与函数特化之间的更多示例，展开于下： 

------

 [[展开](https://zh.cppreference.com/w/cpp/language/function_template#)]     

------

有关重载决议的详细规则，见[重载决议](https://zh.cppreference.com/w/cpp/language/overload_resolution)。 

###  函数模板特化

|      | 本节未完成 原因：14.8[temp.fct.spec] (note that 14.8.1[temp.arg.explicit] 已在全特化专题：要么让函数特化到这里：失去部分特化、与函数重载的交互，或仅引用那边 |
| ---- | ------------------------------------------------------------ |
|      |                                                              |

###  缺陷报告

下列更改行为的缺陷报告追溯地应用于以前出版的 C++ 标准。 

| DR                                    | 应用于 | 出版时的行为                                      | 正确行为               |
| ------------------------------------- | ------ | ------------------------------------------------- | ---------------------- |
| [CWG 1395](https://wg21.link/cwg1395) | C++14  | 从形参包推导 A 时失败，且对于空形参包没有决胜规则 | 允许推导，添加决胜规则 |

###  参阅

-  [类模板](https://zh.cppreference.com/w/cpp/language/class_template) 
-  [函数声明](https://zh.cppreference.com/w/cpp/language/function) 
