# Effective C++读书笔记(19): 类的高效设计

**守则19: 把类的设计看作类型的设计**

> "Treat class design as type design"

------

***本篇关键词: 如何设计一个好用的类\***

------

在C++和其它面向对象的语言中，定义一个类就定义了一个新的类型。重载函数和操作符，内存的分配与释放，对象的构造与析构，全部掌握在你的手上。所以在设计类的时候，要像语言的设计者设计原始类型一样小心。

好的类型拥有自然的语法，直观的语义和高效率的实现。如何高效地设计一个类呢? 以下的问题在几乎所有的类型设计中都会遇到，以及考虑这些问题会如何影响到你的设计:

- **新类型的对象要如何创建和销毁?**

> "How should objects of your new type be created and destroyed?"

这决定了要如何写构造函数和析构函数，包括要使用什么内存分配和释放函数，即new还是new[]，delete还是delete[]，见[第16章](https://zhuanlan.zhihu.com/p/74067275)

- **对象初始化要如何区别于赋值?**

> "How should object initialisation differ from object assignment?"

这决定了你如何写，如何区别构造函数和赋值运算符，以及不要把初始化与赋值混淆，因为它们的语义不同，构造函数适用于未创建的对象，赋值适用于已创建的对象，这也是为什么我们要在构造函数中使用初始化列表而不使用赋值的原因，见[第4章](https://zhuanlan.zhihu.com/p/64141116)和[第12章](https://zhuanlan.zhihu.com/p/68633893)。

- **新类型的对象传值有什么意义?**

> "What does it mean for objects of your new type to be passed by value?"

要记住拷贝构造函数决定了你的类型是如何被传值的，因为传值会生成本地的拷贝。

- **新类型的合法数值有什么限制?**

> "What are the restrictions on legal values for your new type?"

通常情况下，并不是成员的任何数值组合都是合法的。要让数据成员合法，我们需要根据合法的组合，在成员函数中对数值进行检测，尤其是构造函数，赋值运算符和setter。这也会影响到使用它的函数会抛出什么异常。

- **新类型属于某个继承层次吗?**

> "Does your new type fit into an inheritance graph?"

如果你的新类型继承自某个已有的类，你的设计将被这些父类影响到，尤其是父类的某些函数是不是虚函数。如果你的新类型要作为一个父类，你将要决定把哪些函数声明为虚函数，尤其要注意析构函数，见[第7章](https://zhuanlan.zhihu.com/p/65257902)。

- **新类型允许什么样的转换?**

> "What kind of type conversions are allowed for your new type?"

新类型的对象将会在程序的海洋中与其它各种各样的类型并用，这时你就要决定是否允许类型的转换。如果你希望把T1隐式转换为T2，你可以在T1中定义一个转换函数，例如operator T2，或者在T2中定义一个兼容T1的不加explicit修饰的构造函数。

如果希望使用显式转换，你要定义执行显示转换的函数，详见[第15章](https://zhuanlan.zhihu.com/p/73563364)。

- **什么运算符和函数对于你的新类型是有意义的?**

> "What operators and functions make sense for the new type?"

这决定了你要声明哪些函数，包括成员函数，非成员函数，友元函数等。

- **你要禁止哪些标准函数?**

> "What standard functions should be disallowed?"

如果不希望使用编译器会自动生成的标准函数，把它们声明为私有，见[第6章](https://zhuanlan.zhihu.com/p/64638672)

- **谁可以接触到成员?**

> "Who should have access to the members of your new type?"

这影响到哪些成员是公有的，哪些是保护的，哪些是私有的。这也能帮你决定哪些类和函数是友元的，以及要不要使用嵌套类(nested class)。

- **新类型的"隐藏接口"是什么?**

> "What is the 'undeclared interface' of your new type?"

新类型对于性能，异常安全性，资源管理(例如锁和内存)有什么保障? 哪些问题是自动解决不需要用户操心的? 要实现这些保障，自然会对这个类的实现产生限制，例如要使用智能指针而不要使用裸指针。

- **新类型有多通用?**

> "How general is your new type?"

如果想让你的新类型通用于许多类型，定义一个类模板(class template)，而不是单个新类型。

- **新类型真的是你需要的吗?**

> "Is a new type what you really want?"

如果你想定义一个子类只是为了给基类增加某些新功能，定义一些非成员的函数或者函数模板更加划算。

------

以上这些问题视情况不同而答案不同，有时也会很难回答，很难找到最佳方案设计出最好的类型，但确实是在类型设计中要考虑的经典问题。在大型工程中要保证代码的安全性和可维护性，就要把类型设计得甚至像标准类型一样好用，付出的努力与获得的收益相比也是值得的。

**总结:**

- 类设计就是类型设计。要设计一个好的新类型，就要周全考虑到以上的所有问题。