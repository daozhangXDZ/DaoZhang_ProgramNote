# 模板

 

[ C++](https://zh.cppreference.com/w/cpp)

 

[C++ 语言](https://zh.cppreference.com/w/cpp/language)

 

**模板**

 

模板是定义下列之一的 C++ 实体： 

-  一族类（[类模板](https://zh.cppreference.com/w/cpp/language/class_template)），可以是[嵌套类](https://zh.cppreference.com/w/cpp/language/member_template) 
-  一族函数（[函数模板](https://zh.cppreference.com/w/cpp/language/function_template)），可以是[成员函数](https://zh.cppreference.com/w/cpp/language/member_template) 
-  一族类型的别名（[别名模板](https://zh.cppreference.com/w/cpp/language/type_alias)）(C++11 起) 
-  一族变量（[变量模板](https://zh.cppreference.com/w/cpp/language/variable_template)）(C++14 起) 
-  概念（[制约与概念](https://zh.cppreference.com/w/cpp/language/constraints)）(C++20 起) 

模板以一或多个[模板形参](https://zh.cppreference.com/w/cpp/language/template_parameters)参数化，形参有三种：类型模板形参、非类型模板形参和模板模板形参。 

当提供了模板实参，或仅对于[函数](https://zh.cppreference.com/w/cpp/language/function_template#.E6.A8.A1.E6.9D.BF.E5.8F.82.E6.95.B0.E6.8E.A8.E5.AF.BC)和[类](https://zh.cppreference.com/w/cpp/language/class_template_argument_deduction) (C++17 起)模板，当模板实参被推导出时，它们替换各模板形参，以获得模板的一个*特化（specialization）*，即一个特定类型或一个特定函数左值。特化亦可显式提供：对类和函数模板都允许[全特化](https://zh.cppreference.com/w/cpp/language/template_specialization)，只允许对类模板[部分特化](https://zh.cppreference.com/w/cpp/language/partial_specialization)。 

在要求完整对象类型的语境中引用某个类模板特化时，或在要求函数定义存在的语境中引用某个函数模板特化时，除非模板已经被显式特化或显式实例化，否则模板即被*实例化（instantiate）*（它的代码被实际编译）。类模板的实例化不会实例化其任何成员函数，除非它们也被使用。在连接时，不同翻译单元生成的相同实例被合并。 

模板的定义必须在隐式实例化点可见，这就是为何模板库通常都在头文件中提供所有模板定义的原因（例如[大多数 boost 库仅有头文件](http://www.boost.org/doc/libs/release/more/getting_started/unix-variants.html#header-only-libraries)） 

###  语法

|                                                              |      |            |
| ------------------------------------------------------------ | ---- | ---------- |
| `**template**` `**<**` 形参列表 `**>**` requires-子句(C++20)(可选) 声明 | (1)  |            |
|                                                              |      |            |
| `**export**` `**template**` `**<**` 形参列表 `**>**` 声明    | (2)  | (C++11 前) |
|                                                              |      |            |
| `**template**` `**<**` 形参列表 `**>**` `**concept**` 概念名 `**=** ` 制约表达式 `**;**` | (3)  | (C++20 起) |
|                                                              |      |            |

| 声明              | -    | [类（包括 struct 和 union）](https://zh.cppreference.com/w/cpp/language/class_template)，[成员类或成员枚举类型](https://zh.cppreference.com/w/cpp/language/member_template)，[函数](https://zh.cppreference.com/w/cpp/language/function_template)或[成员函数](https://zh.cppreference.com/w/cpp/language/member_template)，命名空间作用域的静态数据成员，[变量或类作用域的静态数据成员](https://zh.cppreference.com/w/cpp/language/variable_template)， (C++14 起)或[别名模板](https://zh.cppreference.com/w/cpp/language/type_alias) (C++11 起)的声明。它亦可定义[模板特化](https://zh.cppreference.com/w/cpp/language/template_specialization)。 |
| ----------------- | ---- | ------------------------------------------------------------ |
| 形参列表          | -    | 非空的[模板形参](https://zh.cppreference.com/w/cpp/language/template_parameters)的逗号分隔列表，其中每项是[非类型形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E9.9D.9E.E7.B1.BB.E5.9E.8B.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)、[类型形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E7.B1.BB.E5.9E.8B.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)、[模板形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E6.A8.A1.E6.9D.BF.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)或任何这些的[形参包](https://zh.cppreference.com/w/cpp/language/parameter_pack)之一。 |
| 概念名 制约表达式 | -    | 见[制约与概念](https://zh.cppreference.com/w/cpp/language/constraints) (C++20 起) |

| `export` 是一个可选的修饰符，声明模板*被导出*（用于类模板时，它声明其所有成员也被导出）。对被导出模板进行实例化的文件不需要包含其定义：有声明就足够了。`export` 的实现稀少而且在细节上互不一致。 | (C++11 前) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

| 模板形参列表可以后随一个可选的 [requires-子句](https://zh.cppreference.com/w/cpp/language/constraints#requires_.E5.AD.90.E5.8F.A5)，它指定各模板实参上的[制约](https://zh.cppreference.com/w/cpp/language/constraints)。 | (C++20 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |


 

|      | 本节未完成 原因：核心语法，模板形参，以及实例化，带出 class_template 和 function_template 间的公共内容 |
| ---- | ------------------------------------------------------------ |
|      |                                                              |

##  模板标识

|                                 |      |      |
| ------------------------------- | ---- | ---- |
| 模板名 `**<**` 形参列表 `**>**` |      |      |
|                                 |      |      |

| 模板名 | -    | 或为指名模板的[标识符](https://zh.cppreference.com/w/cpp/language/identifiers)（该情况下称之为 "简单模板标识" ），或为重载运算符模板或用户定义字面量模板的名字。 |
| ------ | ---- | ------------------------------------------------------------ |
|        |      |                                                              |

指名模板特化的 简单模板标识 指名一个类。 

指名别名模版特化的 模板标识 指名一个类型。 

指名函数模板特化的 模板标识 指名一个函数。 

模板标识 仅当符合下列条件才合法 

-  实参数量不多于形参，或有形参是模板形参包， 
-  每个无默认模板实参的不可推导的非包形参都有一个实参， 
-  每个模板实参都与对应的模板形参相匹配， 
-  替换每个模板实参到其后续模板形参（若存在）中均成功，而且 
-  (C++20) 若 模板标识 非待决，则其关联制约得以满足，如下所述。 

无效的 简单模板标识 是编译时错误，除非它指名的是函数模板特化（该情况下可适用 [SFINAE](https://zh.cppreference.com/w/cpp/language/sfinae)）。 

```
template<class T, T::type n = 0> class X;
struct S {
  using type = int;
};
using T1 = X<S, int, int>; // 错误：过多实参
using T2 = X<>;            // 错误：第一模板形参无默认实参
using T3 = X<1>;           // 错误：值 1 不匹配类型实参
using T4 = X<int>;         // 错误：第二模板形参替换失败
using T5 = X<S>;           // OK
```

| 如果在 简单模板标识 的模板名指名受制约的非函数模板或受制约的模板模板形参，但不是作为未知特化的成员的成员模板，而且 简单模板标识 中的所有模板实参均非待决，则必须满足受制约模板的各项关联制约：  `template<typename T> concept C1 = sizeof(T) != sizeof(int);   template<C1 T> struct S1 { }; template<C1 T> using Ptr = T*;   S1<int>* p;                         // 错误：不满足制约 Ptr<int> p;                         // 错误：不满足制约   template<typename T> struct S2 { Ptr<int> x; };          // 错误，不要求诊断   template<typename T> struct S3 { Ptr<T> x; };            // OK：不要求满足   S3<int> x;                          // 错误：不满足制约   template<template<C1 T> class X> struct S4 {   X<int> x;                         // 错误，不要求诊断 };   template<typename T> concept C2 = sizeof(T) == 1;   template<C2 T> struct S { };   template struct S<char[2]>;         // 错误：不满足制约 template<> struct S<char[2]> { };   // 错误：不满足制约` | (C++20 起) |
| ------------------------------------------------------------ | ---------- |
|                                                              |            |

###  模板化实体

模板化实体（某些资料称之为 "temploid"）是任何在模板定义内定义（或对于 lambda-表达式 为其所创建）的实体。下列所有实体都是模板化实体： 

-  类/函数/变量模板 
-  模板化实体的成员（例如类模板的非模板成员函数） 
-  作为模板化实体的枚举的枚举项 
-  任何模板化实体中定义或创建的实体：局部类，局部变量，友元函数，等等 
-  模板化实体的声明中出现的 lambda 表达式的闭包类型 

例如，以下模板中： 

```
template<typename T> struct A { void f() {} };
```

函数 `A::f` 不是函数模板，但仍被当做是模板化的。 
