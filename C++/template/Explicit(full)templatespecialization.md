# 显式（全）模板特化

 

[ C++](https://zh.cppreference.com/w/cpp)

 

[C++ 语言](https://zh.cppreference.com/w/cpp/language)

 

[模板](https://zh.cppreference.com/w/cpp/language/templates)

 

允许对给定的模板实参集定制模板代码。 

###  语法

|                              |      |      |
| ---------------------------- | ---- | ---- |
| `**template**` `**<>**` 声明 |      |      |
|                              |      |      |

以下任何一项均可以完全特化： 

1.  [函数模板](https://zh.cppreference.com/w/cpp/language/function_template) 
2.  [类模板](https://zh.cppreference.com/w/cpp/language/class_template) 
3.  (C++14 起)[变量模板](https://zh.cppreference.com/w/cpp/language/variable_template) 
4.  类模板的[成员函数](https://zh.cppreference.com/w/cpp/language/member_functions) 
5.  类模板的[静态数据成员](https://zh.cppreference.com/w/cpp/language/static) 
6.  类模板的[成员类](https://zh.cppreference.com/w/cpp/language/nested_types) 
7.  类模板的成员[枚举](https://zh.cppreference.com/w/cpp/language/enum) 
8.  类或类模板的[成员类模板](https://zh.cppreference.com/w/cpp/language/member_template) 
9.  类或类模板的[成员函数模板](https://zh.cppreference.com/w/cpp/language/member_template#.E6.88.90.E5.91.98.E5.87.BD.E6.95.B0.E6.A8.A1.E6.9D.BF) 

例如，  

运行此代码

```
#include <iostream>
template<typename T>   // 主模板
struct is_void : std::false_type
{
};
template<>  // 对 T = void 显式特化
struct is_void<void> : std::true_type
{
};
int main()
{
    // 对于任何非 void 的类型 T，该类均派生自 false_type
    std::cout << is_void<char>::value << '\n'; 
    // 但当 T 为 void 时类派生自 true_type
    std::cout << is_void<void>::value << '\n';
}
```


  

###  细节

显式特化可以在可以定义其主模板的任何作用域中声明（这可以不同于定义其主模板定义的作用域；例如同[成员模板](https://zh.cppreference.com/w/cpp/language/member_template)的类外特化）。显式特化必须出现在非特化模板声明后。 

```
namespace N {
    template<class T> class X { /*...*/ }; // 主模板
    template<> class X<int> { /*...*/ }; // 同命名空间中的特化
 
    template<class T> class Y { /*...*/ }; // 主模板
    template<> class Y<double>; // 对 double 特化的前置声明
}
template<>
class N::Y<double> { /*...*/ }; // OK：同命名空间中的特化
```

特化必须在第一条导致隐式实例化的使用之前，在每个发生这种使用的翻译单元中声明： 

```
class String {};
template<class T> class Array { /*...*/ };
template<class T> void sort(Array<T>& v) { /*...*/ } // 主模板
 
void f(Array<String>& v) {
    sort(v); // 隐式实例化 sort(Array<String>&), 
}            // 使用初等模板 sort()
 
template<>  // 错误：sort(Array<String>) 的显式特化出现在隐式实例化之后
void sort<String>(Array<String>& v);
```

仅声明但未定义的模板特化，可像其他[不完整类型](https://zh.cppreference.com/w/cpp/language/type#.E4.B8.8D.E5.AE.8C.E6.95.B4.E7.B1.BB.E5.9E.8B)一样使用（例如可以使用到它的指针和引用） 

```
template<class T> class X; // 主模板
template<> class X<int>; // 特化（声明，不定义）
X<int>* p; // OK：指向不完整类型的指针
X<int> x; // 错误：不完整类型的对象
```

###  函数模板的显式特化

当特化函数模板时，若[模板实参推导](https://zh.cppreference.com/w/cpp/language/template_argument_deduction)能从函数实参予以提供，则可忽略其实参： 

```
template<class T> class Array { /*...*/ };
template<class T> void sort(Array<T>& v); // 主模板
template<> void sort(Array<int>&); // 对 T = int 的特化
// 不需要写为
// template<> void sort<int>(Array<int>&);
```

与某个特化带有相同名字和相同形参列表的函数不是特化（见[函数模板](https://zh.cppreference.com/w/cpp/language/function_template)中的重载） 

仅当函数模板的显式特化声明为带 [inline 说明符](https://zh.cppreference.com/w/cpp/language/inline)（或定义为弃置）时，它是内联函数，主模板是否为内联对其没有影响。 

不能在函数模板，成员函数模板，以及在隐式实例化类时的类模板的成员函数的显式特化中指定[默认函数实参](https://zh.cppreference.com/w/cpp/language/default_arguments)。 

显式特化不能是[友元声明](https://zh.cppreference.com/w/cpp/language/friend)。 

若主模板具有并非 `noexcept(false)` 的异常说明，则显式特化必须具有兼容的异常说明。 

###  特化的成员

在类体外定义显式特化的类模板的成员时，不使用 template <> 语法，除非它是某个被特化为类模板的显式特化的成员类模板的成员，因为其他情况下，语法会要求这种定义以嵌套模板所要求的 template<形参> 开始 

```
template< typename T>
struct A {
    struct B {};  // 成员类 
    template<class U> struct C { }; // 成员类模板
};
 
template<> // 特化
struct A<int> {
    void f(int); // 特化的成员函数
};
// template<> 不用于特化的成员
void A<int>::f(int) { /* ... */ }
 
template<> // 成员类的特化
struct A<char>::B {
    void f();
};
// template<> 亦不用于特化的成员类的成员
void A<char>::B::f() { /* ... */ }
 
template<> // 成员类模板的的定义
template<class U> struct A<char>::C {
    void f();
};
 
// template<> 在作为类模板定义显式特化的成员类模板时使用
template<>
template<class U> void A<char>::C<U>::f() { /* ... */ }
```


 模板的静态数据成员的显式特化，若其声明包含初始化器则为定义；否则，它是声明。这些定义对于默认初始化必须用花括号： 

```
template<> X Q<int>::x; // 静态成员的声明
template<> X Q<int>::x (); // 错误：函数声明
template<> X Q<int>::x {}; // 静态成员的默认初始化定义
```

类模板的成员或成员模板可对于类模板的隐式实例化显式特化，即使成员或成员模板定义于类模板定义中。 

```
template<typename T>
struct A {
    void f(T); // 成员，声明于主模板中
    void h(T) {} // 成员，定义于主模板中
    template<class X1> void g1(T, X1); // 成员模板
    template<class X2> void g2(T, X2); // 成员模板
};
 
// 成员的特化
template<> void A<int>::f(int);
// 成员特化 OK，即使定义于类中
template<> void A<int>::h(int) {}
 
// 类外成员模板定义
template<class T>
template<class X1> void A<T>::g1(T, X1) { }
 
// 成员模板特化
template<>
template<class X1> void A<int>::g1(int, X1);
 
// 成员模板特化
template<>
template<> void A<int>::g2<char>(int, char); // 对于 X2 = char
// 同上，用模板实参推导 (X1 = char)
template<> 
template<> void A<int>::g1(int, char);
```

成员或成员模板可嵌套于多个外围类模板中。在这种成员的显式特化中，对每个显式特化的外围类模板都有一个 template<>。 

```
template<class T1> class A {
    template<class T2> class B {
        void mf();
    };
};
template<> template<> class A<int>::B<double>;
template<> template<> void A<char>::B<char>::mf();
```

在这种嵌套声明中，某些层次可保留不特化（但若其外围类未被特化，则不能特化类成员模板）。对于每个这种层次，声明需要 template<实参>，因为这种特化自身也是模板： 

```
template <class T1> class A {
    template<class T2> class B {
        template<class T3> void mf1(T3); // 成员模板
        void mf2(); // 非模板成员
     };
};
 
// 特化
template<> // 对于特化的 A
template<class X> // 对于未特化的 B
class A<int>::B {
    template <class T> void mf1(T);
};
 
// 特化
template<> // 对于特化的 A
template<> // 对于特化的 B
template<class T> // 对于未特化的 mf1
void A<int>::B<double>::mf1(T t) { }
 
// 错误：B<double> 被特化而且是成员模板，故其外围的 A 也必须特化
template<class Y>
template<> void A<Y>::B<double>::mf2() { }
```

###  缺陷报告

下列更改行为的缺陷报告追溯地应用于以前出版的 C++ 标准。 

| DR                                  | 应用于 | 出版时的行为                               | 正确行为                 |
| ----------------------------------- | ------ | ------------------------------------------ | ------------------------ |
| [CWG 727](https://wg21.link/cwg727) | C++14  | 不允许在类作用域的全特化，即使允许部分特化 | 允许在任何作用域的全特化 |
