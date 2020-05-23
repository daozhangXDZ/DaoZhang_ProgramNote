# 模板形参与模板实参

 

[ C++](https://zh.cppreference.com/w/cpp)

 

[C++ 语言](https://zh.cppreference.com/w/cpp/language)

 

# 模板形参

每个[模板](https://zh.cppreference.com/w/cpp/language/templates)都是由一或多个模板形参所参数化的，它们在模板声明语法中的 形参列表 中指定： 

|                                              |      |      |
| -------------------------------------------- | ---- | ---- |
| `**template**` `**<**` 形参列表 `**>**` 声明 | (1)  |      |
|                                              |      |      |

形参列表 中的每个形参可以是： 

-  非类型模板形参； 
-  类型模板形参； 
-  模板模板形参。 

####  非类型模板形参

|                                  |      |            |
| -------------------------------- | ---- | ---------- |
| 类型 名字(可选)                  | (1)  |            |
|                                  |      |            |
| 类型 名字(可选) `**=** ` default | (2)  |            |
|                                  |      |            |
| 类型 `**...**` 名字(可选)        | (3)  | (C++11 起) |
|                                  |      |            |
| 占位符 名字                      | (4)  | (C++17 起) |
|                                  |      |            |

1) 带可选名字的非类型模板形参。

2) 带可选名字和默认值的非类型模板形参。

3) 带可选名字的非类型模板[形参包](https://zh.cppreference.com/w/cpp/language/parameter_pack)。

4) 带占位符类型的非类型模板形参。占位符 可为包含占位符 [`auto`](https://zh.cppreference.com/w/cpp/language/auto) 的任何类型（例如单纯的 auto、auto ** 或 auto &），[被推导类类型的占位符](https://zh.cppreference.com/w/cpp/language/class_template_argument_deduction) (C++20 起)，或者 decltype(auto)。

类型 是下列类型之一（可选地有 cv 限定，忽略限定符）： 

-  （到对象或函数的）[左值引用类型](https://zh.cppreference.com/w/cpp/language/reference#.E5.B7.A6.E5.80.BC.E5.BC.95.E7.94.A8)； 

| [std::nullptr_t](https://zh.cppreference.com/w/cpp/types/nullptr_t) (C++11 起)；  [整型类型](https://zh.cppreference.com/w/cpp/language/type)；  （指向对象或函数的）[指针类型](https://zh.cppreference.com/w/cpp/language/pointer)；  （指向成员对象或成员函数的）[成员指针类型](https://zh.cppreference.com/w/cpp/language/pointer#.E6.88.90.E5.91.98.E6.8C.87.E9.92.88)；  [枚举类型](https://zh.cppreference.com/w/cpp/language/enum)。 | (C++20 前) |
| ------------------------------------------------------------ | ---------- |
| 符合下列条件的类型：   满足[字面类型](https://zh.cppreference.com/w/cpp/named_req/LiteralType) (*LiteralType*) ，且  具有*强结构相等性*（见下文），  这包括[整型类型](https://zh.cppreference.com/w/cpp/language/type)，[指针类型](https://zh.cppreference.com/w/cpp/language/pointer)，[成员指针类型](https://zh.cppreference.com/w/cpp/language/pointer#.E6.88.90.E5.91.98.E6.8C.87.E9.92.88)，[std::nullptr_t](https://zh.cppreference.com/w/cpp/types/nullptr_t)，以及无自定义 `operator<=>` 重载的枚举类型，但不包括浮点类型。  对于 const T 类型的泛左值 `x`，以下情况下称类型拥有*强结构相等性（strong structural equality）*：   若 T 为非类类型，则   x <=> x 是类型为 std::strong_ordering 或 std::strong_equality 的合法表达式；    若 T 为类类型，则   operator== 在 T 的定义中定义为预置的，且  x==x 在转换为 `bool` 时良构，且  递归地，T 的所有基类子对象与非静态数据成员均具有强结构相等性，且  T 没有 mutable 或 volatile 子对象。 | (C++20 起) |

数组与函数类型可以写在模板声明中，但它们被自动替换为适合的对象指针和函数指针。 

当在类模板体内使用非类型模板形参的名字时，它是不可修改的[纯右值](https://zh.cppreference.com/w/cpp/language/value_category)，除非其类型是左值引用类型，或其类型是类类型 (C++20 起)。 

形式为 class Foo 的模板形参不是类型为 `Foo` 的非类型模板形参，虽然 class Foo 还能是[详述类型说明符](https://zh.cppreference.com/w/cpp/language/elaborated_type_specifier)且 class Foo x; 声明 `x` 为 `Foo` 类型的对象。 

| 若非类型模板形参的类型包含占位符类型 `auto`，被推导类型的占位符 (C++20 起)，或 `decltype(auto)`，则可以推导它。如同在虚设的声明 T x = 模板实参; 中推导变量 `x` 的类型一般进行推导，其中 `T` 是模板形参的声明类型。若被推导类型对于非类型模板形参不允许使用，则程序非良构。  `template<auto n> struct B { /* ... */ }; B<5> b1;   // OK：非类型模板形参类型为 int B<'a'> b2; // OK：非类型模板形参类型为 char B<2.5> b3; // 错误：非类型模板形参类型不能是 double` 对于类型中使用了占位符类型的非类型模板形参包，每个模板实参的类型是独立地进行推导的，而且不需要互相匹配：  `template<auto...> struct C {}; C<'C', 0, 2L, nullptr> x; // OK` | (C++17 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

| 指名类类型 `T` 的某个非类型模板形参的[标识符](https://zh.cppreference.com/w/cpp/language/identifiers)，代表一个 const T 类型的静态存储期对象，称该对象为*模板形参对象*，其值是对应模板实参转换到模板形参的类型之后的值。程序中具有相同类型、相同值的所有这种模板形参，都代表同一模板形参对象。  `struct A { friend bool operator==(const A&, const A&) = default; }; template<A a> void f() {     &a; // OK     const A& ra = a, &rb = a; // 都绑定到同一模板形参对象     assert(&ra == &rb); // 通过 }` | (C++20 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

####  类型模板形参

|                                           |      |            |
| ----------------------------------------- | ---- | ---------- |
| 类型形参关键词 名字(可选)                 | (1)  |            |
|                                           |      |            |
| 类型形参关键词 名字(可选) `**=** ` 默认值 | (2)  |            |
|                                           |      |            |
| 类型形参关键词 `**...**` 名字(可选)       | (3)  | (C++11 起) |
|                                           |      |            |
| 类型制约 名字(可选)                       | (4)  | (C++20 起) |
|                                           |      |            |
| 类型制约 名字(可选) `**=**` 默认值        | (5)  | (C++20 起) |
|                                           |      |            |
| 类型制约 `**...**` 名字(可选)             | (6)  | (C++20 起) |
|                                           |      |            |

| 类型制约 | -    | 或为[概念](https://zh.cppreference.com/w/cpp/language/constraints)的名字，或为概念名后随模板实参列表（在角括号中）。无论何种方式，概念名均可选有限定 |
| -------- | ---- | ------------------------------------------------------------ |
|          |      |                                                              |

类型形参关键词 是 `**typename**` 或 `**class**` 之一。这两个关键词在类型模板形参声明中没有区别。 

1)

 无默认类型的类型模板实参。 

```
template<class T>
class My_vector { /* ... */ };
```

2)

 有默认类型的类型模板实参。 

```
template<class T = void>
struct My_op_functor { /* ... */ };
```

3)

 类型模板

形参包

。 

```
template<typename... Ts>
class My_tuple { /* ... */ };
```

形参的名字是可选的： 

```
// 对上面所示模板的声明：
template<class> class My_vector;
template<class = void> struct My_op_functor;
template<typename...> class My_tuple;
```

在模板声明体内，类型形参之名是 typedef 名，是当模板被实例化时所提供的类型的别名。 

| 每个有制约形参 `P`，其 类型制约 Q 指定了概念 `C`，则根据以下规则引入一个[制约表达式](https://zh.cppreference.com/w/cpp/language/constraints) `E`：   若 `Q` 为 `C`（无实参列表），   若 `P` 不是形参包，则 `E` 为简单的 `C<P>`  否则，`P` 是形参包，`E` 为折叠表达式 `(C<P> && ...)`    若 `Q` 为 `C<A1,A2...,AN>`，则 `E` 分别为 `C<P,A1,A2,...AN>` 或 `(C<P,A1,A2,...AN> && ...)`。  `template<typename T> concept C1 = true; template<typename... Ts> concept C2 = true; // 变参概念 template<typename T, typename U> concept C3 = true;   template<C1 T> struct s1;         // 制约表达式为 C1<T> template<C1... T> struct s2;      // 制约表达式为 (C1<T> && ...) template<C2... T> struct s3;      // 制约表达式为 (C2<T> && ...) template<C3<int> T> struct s4;    // 制约表达式为 C3<T, int> template<C3<int>... T> struct s5; // 制约表达式为 (C3<T, int> && ...)` | (C++20 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

####  模板模板形参

|                                                              |      |            |
| ------------------------------------------------------------ | ---- | ---------- |
| `**template**` `**<**` 形参列表 `**>**` `**typename(C++17)|class**` 名字(可选) | (1)  |            |
|                                                              |      |            |
| `**template**` `**<**` 形参列表 `**>**` `**typename(C++17)|class**` 名字(可选) `**=**` default | (2)  |            |
|                                                              |      |            |
| `**template**` `**<**` 形参列表 `**>**` `**typename(C++17)|class**` `**...**` 名字(可选) | (3)  | (C++11 起) |
|                                                              |      |            |

1) 带可选名字的模板模板形参。

2) 带可选名字和默认模板的模板模板形参。

3) 带可选名字的模板模板[形参包](https://zh.cppreference.com/w/cpp/language/parameter_pack)。

| 不同于类型模板形参声明，模板模板形参只能用关键词 `**class**` 而不能用 `**typename**`。 | (C++17 前) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

在模板声明体内，此形参的名字是一个模板名（且需要实参以实例化）。 

```
template<typename T> class my_array {};
 
// 两个类型模板形参和一个模板模板形参：
template<typename K, typename V, template<typename> typename C = my_array>
class Map
{
    C<K> key;
    C<V> value;
};
```

###  模板实参

为使模板被实例化，其每个模板形参（类型、非类型或模板）必须由一个对应的模板实参所替换。对于[类模板](https://zh.cppreference.com/w/cpp/language/class_template)，实参或被显式提供，或[从初始化器推导](https://zh.cppreference.com/w/cpp/language/class_template_argument_deduction)， (C++17 起)或为默认。对于[函数模板](https://zh.cppreference.com/w/cpp/language/function_template)，实参或被显式提供，或[从语境推导](https://zh.cppreference.com/w/cpp/language/template_argument_deduction)，或为默认。 

若实参同时可被解释成[类型标识](https://zh.cppreference.com/w/cpp/language/type#.E7.B1.BB.E5.9E.8B.E7.9A.84.E5.91.BD.E5.90.8D)和表达式，则它始终被解释成类型标识，即使其对应的是非类型模板形参也是如此： 

```
template<class T> void f(); // #1
template<int I> void f(); // #2
void g() {
    f<int()>(); // "int()" 既是类型又是表达式，
                // 调用 #1 因为它被解释成类型
}
```

####  模板非类型实参

实例化拥有非类型模板形参的模板时，应用下列限制： 

| 对于整型和算术类型，实例化时所提供的模板实参必须是模板形参类型的[经转换常量表达式](https://zh.cppreference.com/w/cpp/language/constant_expression)（因此适用某些隐式转换）。  对于对象指针，模板实参必须指定某个具有静态[存储期](https://zh.cppreference.com/w/cpp/language/storage_duration)和（内部或外部）[连接](https://zh.cppreference.com/w/cpp/language/storage_duration#.E8.BF.9E.E6.8E.A5)的完整对象的地址，或者是求值为适当的空指针或 [std::nullptr_t](https://zh.cppreference.com/w/cpp/types/nullptr_t) 值的常量表达式。  对于函数指针，合法的实参是指向具有连接的函数的指针（或求值为空指针值的常量表达式）。  对于左值引用形参，实例化时所提供的实参不能是临时量、无名左值或无连接的具名左值（换言之，实参必须具有连接）。  对于成员指针，实参必须是表示成 &Class::Member 的成员指针，或求值为空指针值或 [std::nullptr_t](https://zh.cppreference.com/w/cpp/types/nullptr_t) 值的常量表达式。  特别是，这意味着字符串字面量、数组元素的地址和非静态成员的地址，不能被用作模板实参，来实例化其对应非类型模板形参是对象指针的模板形参的模板。 | (C++17 前) |
| ------------------------------------------------------------ | ---------- |
| 非类型模板形参可以使用的模板实参，可以是该模板形参类型的任何[经转换常量表达式](https://zh.cppreference.com/w/cpp/language/constant_expression)。  `template<const int* pci> struct X {}; int ai[10]; X<ai> xi;  // ok：数组到指针转换和 cv 限定转换   struct Y {}; template<const Y& b> struct Z {}; Y y; Z<y> z;  // ok：无转换   template<int (&pa)[5]> struct W {}; int b[5]; W<b> w; // ok：无转换   void f(char); void f(int); template<void (*pf)(int)> struct A {}; A<&f> a; // ok：重载决议选择 f(int)` 仅有的例外是，*引用*或*指针*类型的非类型模板形参，以及类类型的非类型模板形参及其子对象之中的引用或指针类型的非静态数据成员 (C++20 起)，不能指代下列对象/是下列对象的地址   子对象（包括非静态类成员、基类子对象或数组元素）；  临时对象（包括在[引用初始化](https://zh.cppreference.com/w/cpp/language/reference_initialization)期间创建者）；  [字符串字面量](https://zh.cppreference.com/w/cpp/language/string_literal)；  [typeid](https://zh.cppreference.com/w/cpp/language/typeid) 的结果；  或预定义变量 __func__。  `template<class T, const char* p> class X {}; X<int, "Studebaker"> x1; // 错误：字符串字面量用作模板实参   template<int* p> class X {}; int a[10]; struct S {     int m;     static int s; } s; X<&a[2]> x3;  // 错误：数组元素的地址 X<&s.m> x4;   // 错误：非静态成员的地址 X<&s.s> x5;   // ok：静态成员的地址 X<&S::s> x6;  // ok：静态成员的地址   template<const int& CRI> struct B {}; B<1> b2;     // 错误：临时量会为模板实参所要求 int c = 1; B<c> b1;     // ok` | (C++17 起) |

####  模板类型实参

类型模板形参的模板实参必须是[类型标识](https://zh.cppreference.com/w/cpp/language/type#.E7.B1.BB.E5.9E.8B.E7.9A.84.E5.91.BD.E5.90.8D)，它可以指名不完整类型： 

```
template<typename T> class X {}; // 类模板
 
struct A; // 不完整类型
typedef struct {} B; // 无名类型的类型别名
 
int main()
{
    X<A> x1; // ok：'A' 指名类型
    X<A*> x2; // ok：'A*' 指名类型
    X<B> x3; // ok：'B' 指名类型
}
```

####  模板模板实参

模板模板形参的模板实参是必须是一个 [标识表达式](https://zh.cppreference.com/w/cpp/language/identifiers#.E5.9C.A8.E8.A1.A8.E8.BE.BE.E5.BC.8F.E4.B8.AD)，它指名一个类模板或模板别名。 

当实参是类模板时，进行形参匹配时只考虑其主模板。部分特化若存在，也仅在基于此模板模板形参的特化恰好要被实例化时才予以考虑。 

```
template<typename T> class A { int x; }; // 主模板
template<class T> class A<T*> { long x; }; // 部分特化
 
// 带有模板模板形参 V 的类模板
template<template<typename> class V> class C
{
    V<int> y; // 使用主模板
    V<int*> z; // 使用部分特化
};
 
C<A> c; // c.y.x 类型为 int，c.z.x 类型为 long
```

为匹配模板模板实参 `A` 与模板模板形参 `P`，`A` 的每个模板形参必须与 `P` 的对应模板形参严格匹配 (C++17 前)`P` 必须至少与 `A` 一样特殊 (C++17 起)。若 `P` 的形参列表包含一个[形参包](https://zh.cppreference.com/w/cpp/language/parameter_pack)，则来自 `A` 的模板形参列表中的零或更多模板形参（或形参包）与之匹配。 

```
template<typename T> struct eval; // 主模板 
 
template<template<typename, typename...> class TT, typename T1, typename... Rest>
struct eval<TT<T1, Rest...>> {}; // eval 的部分特化
 
template<typename T1> struct A;
template<typename T1, typename T2> struct B;
template<int N> struct C;
template<typename T1, int N> struct D;
template<typename T1, typename T2, int N = 17> struct E;
 
eval<A<int>> eA; // ok：匹配 eval 的部分特化
eval<B<int, float>> eB; // ok：匹配 eval 的部分特化
eval<C<17>> eC; // 错误：C 在部分特化中不匹配 TT，因为 TT 的首个形参是类型模板形参
                // 而 17 不指名类型
eval<D<int, 17>> eD; // 错误：D 在部分特化中不匹配 TT，
                     // 因为 TT 的第二形参是类型形参包，而 17 不指名类型
eval<E<int, float>> eE; // 错误：E 在部分特化中不匹配 TT
                        // 因为 E 的第三（默认）形参是非类型形参
template<class T> class A { /* ... */ };
template<class T, class U = T> class B { /* ... */ };
template <class ...Types> class C { /* ... */ };
 
template<template<class> class P> class X { /* ... */ };
X<A> xa; // OK
X<B> xb; // C++17 在 CWG 150 后 OK
         // 更早时为错误：非严格匹配
X<C> xc; // C++17 在 CWG 150 后 OK
         // 更早时为错误：非严格匹配
 
template<template<class ...> class Q> class Y { /* ... */ };
Y<A> ya; // OK
Y<B> yb; // OK
Y<C> yc; // OK
 
template<auto n> class D { /* ... */ }; // 注意：C++17
template<template<int> class R> class Z { /* ... */ };
Z<D> zd; // OK
 
template <int> struct SI { /* ... */ };
template <template <auto> class> void FA();  // 注意：C++17
FA<SI>();  // 错误
```

| 正式来说，给定以下对两个函数模板的重写，根据[函数模板](https://zh.cppreference.com/w/cpp/language/function_template)的部分排序规则，如果对应于模板模板形参 `P` 的函数模板，至少与对应于模板模板实参 `A` 的函数模板同样特殊，则 `P` 至少与 `A` 同样特殊。给定一个虚设的模板 `X`，它拥有 `A` 的模板形参列表（包含默认实参）：   两个函数模板各自分别拥有与 `P` 或 `A` 相同的各个模板形参。  每个函数模板均拥有单个函数形参，其类型是以对应于各自函数模板的模板形参的模板实参对 `X` 的特化，其中对于函数模板的模板形参列表中的每个模板形参 `PP`，构成一个对应的模板实参 `AA`。若 `PP` 声明参数包，则 `AA` 是包展开 `PP...`；否则，`AA` 是标识表达式 `PP`。  若重写生成了非法类型，则 `P` 并非至少与 `A` 同样特殊。 | (C++17 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

####  默认模板实参

默认模板实参在形参列表中于 = 号之后指定。可以为任何种类的模板形参（类型、非类型或模板）指定默认实参，但不能对形参包指定。 

若为主类模板、主变量模板 (C++14 起)或别名模版的模板形参指定默认实参，则其每个后继模板形参都必须有默认实参，但最后一个可以是模板形参包。在函数模板中，对跟在默认实参之后的形参没有限制，而仅当类型形参具有默认实参，或可从函数实参推导时，才可跟在形参包之后。 

以下情况不允许默认形参 

-  在[类模板](https://zh.cppreference.com/w/cpp/language/class_template)的成员的类外定义中（必须在类体内的声明中提供它们）。注意非模板类的[成员模板](https://zh.cppreference.com/w/cpp/language/member_template)可以在其类外定义中使用默认形参（见 [GCC 漏洞 53856](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53856)） 
-  在[友元类模板](https://zh.cppreference.com/w/cpp/language/friend#.E6.A8.A1.E6.9D.BF.E5.8F.8B.E5.85.83)声明中 

| 在任何[函数模板](https://zh.cppreference.com/w/cpp/language/function_template)声明或定义中 | (C++11 前) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

| 在友元函数模板的声明上，仅当声明是定义，且此翻译单元不出现此函数的其他声明时，才允许默认模板实参。 | (C++11 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

各个声明和定义中所出现的默认模板实参，以类似默认函数实参的方式合并： 

```
template<typename T1, typename T2 = int> class A;
template<typename T1 = int, typename T2> class A;
// 如上与如下相同：
template<typename T1 = int, typename T2 = int> class A;
```

但在同一作用域中不能两次为同一形参指定默认实参 

```
template<typename T = int> class X;
template<typename T = int> class X {}; // 错误
```

模板模板形参的模板形参列表可拥有其自己的默认实参，它仅在模板模板实参自身处于作用域中时有效： 

```
// 类模板，带有默认实参的类型模板形参
template<typename T = float> struct B {};
 
// 模板模板形参 T 有形参列表，
// 它由一个带默认实参的类型模板形参组成
template<template<typename = float> typename T> struct A
{
    void f();
    void g();
};
 
// 类体外的成员函数模板定义
template<template<typename TT> class T>
void A<T>::f()
{
    T<> t; // 错误：TT 在作用域中无默认实参
}
template<template<typename TT = char> class T>
void A<T>::g()
{
    T<> t; // ok：t 为 T<char>
}
```

默认模板形参中所用的名字的[成员访问](https://zh.cppreference.com/w/cpp/language/access)，在声明中，而非在使用点检查： 

```
class B {};
 
template<typename T> class C
{
    protected:
        typedef T TT;
};
 
template<typename U, typename V = typename U::TT> class D: public U {};
 
D<C<B>>* d; // 错误：C::TT 为受保护
```

| 默认模板实参在需要该默认实参的值时被隐式实例化，除非模板用于指名函数：  `template<typename T, typename U = int> struct S { }; S<bool>* p; // 默认模板实参 U 在此点实例化             // p 的类型是 S<bool, int>*` | (C++14 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

###  示例

####  非类型模板形参

运行此代码

```
#include <iostream>
 
// 简单的非类型模板形参
template<int N>
struct S { int a[N]; };
 
template<const char*>
struct S2 {};
 
// 复杂的非类型形参的例子
template
<
    char c, // 整型类型
    int (&ra)[5], // 到（数组类型）对象的左值引用
    int (*pf)(int), // 函数指针
    int (S<10>::*a)[10] // 指向（int[10] 类型的）成员对象的指针
> struct Complicated
{
    // 调用编译时所选择的函数
    // 并在编译时将其结果存储于数组中
    void foo(char base)
    {
        ra[4] = pf(c - base);
    }
};
 
S2<"fail"> s2; // 错误：不能用字符串字面量
char okay[] = "okay"; // 有连接的静态对象
S2< &okay[0] > s2; // 错误：数组元素无连接
S2<okay> s2; // 能用
 
int a[5];
int f(int n) { return n; }
 
int main()
{
    S<10> s; // s.a 是 10 个 int 的数组
    s.a[9] = 4;
 
    Complicated<'2', a, f, &S<10>::a> c;
    c.foo('0');
 
    std::cout << s.a[9] << a[4] << '\n';
}
```

输出： 

```
42
```

|      | 本节未完成 原因：更多示例 |
| ---- | ------------------------- |
|      |                           |
