# **类模板**

2018年12月27日 星期四

15:46

**语法**

| **template** **<** *parameter-list* **>** *class-declaration* | (1)  |              |
| ------------------------------------------------------------ | ---- | ------------ |
| **export** **template** **<** *parameter-list* **>** *class-declaration* | (2)  | (C++11   前) |

**解释**

| ***class-declaration*** | -    | [类声明](https://zh.cppreference.com/w/cpp/language/class)。声明的类名成为模板名。 |
| ----------------------- | ---- | ------------------------------------------------------------ |
| ***parameter-list***    | -    | [模板形参](https://zh.cppreference.com/w/cpp/language/template_parameters)的非空逗号分隔列表，每项是[非类型形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E9.9D.9E.E7.B1.BB.E5.9E.8B.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)、[类型形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E7.B1.BB.E5.9E.8B.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)、[模板形参](https://zh.cppreference.com/w/cpp/language/template_parameters#.E6.A8.A1.E6.9D.BF.E6.A8.A1.E6.9D.BF.E5.BD.A2.E5.8F.82)或任何这些形参的[形参包](https://zh.cppreference.com/w/cpp/language/parameter_pack)之一。 |

| export 是可选的修饰符，声明模板为*被导出*（用于声明类模板时，它也声明其所有成员为被导出）。实例化被导出模板的文件不需要包含其定义：声明即已充分。 export 的实现稀少，且在细节上不一致。 | (C++11   前) |
| ------------------------------------------------------------ | ------------ |
|                                                              |              |

**类模板实例化**

类模板自身不是类型、对象或任何其他实体。不会从从仅含模板定义的源文件生成任何代码。必须实例化模板以令任何代码出现：必须提供模板实参，使得编译器能生成实际的类（或从函数模板生成函数）。

**显式实例化**

| **template** **class\|struct** *template-name* **<** *argument-list* **> ;** | (1)  |              |
| ------------------------------------------------------------ | ---- | ------------ |
| **extern** **template** **class\|struct** *template-name* **<** *argument-list* **> ;** | (2)  | (C++11   起) |

1) 显式实例化定义

2) 显式实例化声明

显式实例化定义强制实例化其所指代的 class 、 struct 或 union 。它可以出现在程序中模板定义后的任何位置。而对于给定的实参列表，只允许它在整个程序中出现一次。

| 显式实例化声明（   extern   模板）跳过隐式实例化步骤：本来会导致隐式实例化的代码替而使用别处提供的显式实例化定义（若这种实例化不存在，则导致链接错误）。能用此机制，通过在一个文件以外的所有源文件声明模板实例化，而在剩下的那个文件中定义它，来减少编译次数。 | (C++11   起) |
| ------------------------------------------------------------ | ------------ |
|                                                              |              |

类、函数、变量和成员模板特化能从其模板显式实例化。成员函数、成员类和类模板的静态数据成员能从其成员定义显式实例化。

显式实例化只能出现于该类模板的外围命名空间，除非它使用有限定 id ：

namespace N {
   template<class T> class Y { void mf() { } }; // 模板定义
 }
 // template class Y<int>; // 错误：类模板 Y 在全局命名空间不可见
 using N::Y;
 // template class Y<int>; // 错误：显式实例化在模板的命名空间外
 template class N::Y<char*>;      // OK ：显式实例化
 template void N::Y<double>::mf(); // OK ：显式实例化

若同一组模板实参的[显式特化](https://zh.cppreference.com/w/cpp/language/template_specialization)出现于显式实例化之前，则显式实例化无效果。

显式实例化函数模板、变量模板、类模板的成员函数或静态数据成员，或成员函数模板时，仅要求声明可见。类模板、类模板的成员类或成员类模板的显式实例化之前，完整定义必须出现，除非之前出现了拥有相同模板实参的显式实例化。

若以显式实例化定义显式实例化函数模板、变量模板、成员函数模板或类模板的成员函数或静态数据成员，则模板定义必须存在于同一翻译单元中。

显式实例化指名类模板特化时，它同时作为其每个未在当前翻译单元中提前显式特化的，非继承且非模板成员的同种（声明或定义）显式实例化。若此显式实例化是定义，则它也是只对于已在此点定义的成员的显式实例化定义。

显式实例化忽略成员访问指定符：参数类型和返回类型可为 private 。

**隐式实例化**

在要求完整定义的类型的语境中，或当类型的完整性影响代码，而尚未显式实例化此特定类型时，出现隐式实例化。例如在构造此类型的对象时，但非在构造指向此类型的指针时。

这适用于类模板的成员：除非在程序中使用该成员，否则不实例化它，并且不要求定义。

template<class T> struct Z {
     void f() {}
     void g(); // 决不定义
 }; // 模板定义
 template struct Z<double>; // 显式实例化 Z<double>
 Z<int> a; // 隐式实例化 Z<int>
 Z<char>* p; // 此处不实例化任何内容
 p->f(); // 隐式实例化 Z<char> 而 Z<char>::f() 出现于此。
 // 决不需要且决不实例化 Z<char>::g() ：不必定义它

若已经声明但未定义类模板，则实例化在实例化点产生不完整类类型：

template<class T> class X; // 声明，非定义
 X<char> ch;                // 错误：不完整类型 X<char>

| [局部类](https://zh.cppreference.com/w/cpp/language/class#.E5.B1.80.E9.83.A8.E7.B1.BB)和任何用于其成员中的模板，都作为该局部类或枚举所处于的实体的实例化的一部分实例化。 | (C++17   起) |
| ------------------------------------------------------------ | ------------ |
|                                                              |              |

**参阅**

- [模板形参与实参](https://zh.cppreference.com/w/cpp/language/template_parameters)允许将模板参数化
- [函数模板声明](https://zh.cppreference.com/w/cpp/language/function_template)声明函数模板
- [模板特化](https://zh.cppreference.com/w/cpp/language/template_specialization)为特定的类型定义既存的模板
- [参数包](https://zh.cppreference.com/w/cpp/language/parameter_pack)允许在模板中使用类型列表 (C++11 起)

 

来自 <<https://zh.cppreference.com/w/cpp/language/class_template>> 
