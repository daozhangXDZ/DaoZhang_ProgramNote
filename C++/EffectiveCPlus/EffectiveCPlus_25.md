# Effective C++读书笔记(25): swap的高效实现

**守则25: 要优化不抛出异常的swap函数**

> "Consider support for a non-throwing swap."

------

***本篇关键词: swap函数，pimpl，特殊化，重载，名空间***

------

swap函数是一个非常经典又有用的函数，除了它本身用来交换两个对象数值的功能，还可以用来实现异常安全的赋值，避免自赋值(见[第11章](https://zhuanlan.zhihu.com/p/68201431))等等用途。在std标准库里，swap函数就是这样实现的，和你想的一模一样:

```text
namespace std{
  template<typename T>
  void swap(T& a, T& b){
    T temp(a);
    a = b;
    b = temp;
  }
}
```

如果要用在自己定义的类型上，只要能支持拷贝，即拷贝构造函数或者拷贝赋值运算符，功能上std::swap完全能实现你想要的。但你可能也注意到了，这个实现会生成许多拷贝，把a拷贝进temp，把b拷贝进a，最后把temp拷贝进b，一共有三份拷贝。假如要调换两个包含10万个元素的std::vector，这么做要消耗的内存实在是太大了。

要解决这样的问题，有一个常用的方法叫**pimpl**(the "pimpl" idiom，即"pointer to implementation")。它的概念就是要把类的实现细节从中移除，放在另一个类中，并通过一个指针进行访问。使用pimpl设计手法的类大概长这样:

```text
 //这个类包含Widget类的数据
class WidgetImpl{
  public:
    ...
  private:
    int a,b,c;
    std::vector<double> v; //高成本拷贝警告！
};

//使用pimpl手法的类
class Widget{  
  public:
    Widget(const Widget& rhs);
    //赋值运算符的实现见10,11,12章
    Widget& operator=(const Widget& rhs){
      ...
      *pImpl = *(rhs.pImpl);
      ...
   }
  ...
  private:
    WidgetImpl* pImpl; //使用pimpl指针来指向我们的数据
};
```

这样一来，要调换两个对象，直接交换指针就行了，不用再对成千上万的数据进行交换。可是默认的std::swap并不知道这些，而且直接使用std::swap的话，除了生成3份Widget对象本身的拷贝，还有3份它包含的WidgetImpl对象的拷贝。这要怎么办呢? 

既然它自己不知道，那就让我们告诉std::swap，当传进来Widget对象时，要特别对待，这就是今天要讲的**特殊化**(specialization):

```text
namespace std{
  //特殊化的std::swap，当T是Widget类型时使用如下实现
  template<>
  void swap<Widget>(Widget& a, Widget& b){
    swap(a.pImpl,b.pImpl); //这里的参数是指针，不会用到该特殊化，所以不用担心无限递归
  }
}
```

"template<>"代表了下面的代码是对std::swap的**完全特殊化**(total specialization)实现，函数名字后面的"<Widget>"则代表了当T是Widget类型时使用这个特殊实现。也就是对于其它类型依然使用默认的std::swap，仅仅对于Widget类型才使用特殊化。

这里要注意，我们当然不能对std名空间进行修改，例如在里面增加一个函数(名空间的介绍详见[第23章](https://zhuanlan.zhihu.com/p/81361540))，但对其进行特殊化是合理并且允许的，因为我们自己创造的类可能会有我们自己的特殊要求，而std的标准模板并不一定都是最合适的。

以上的这段代码仅仅是为了展示特殊化的概念和语法，并不可以编译，因为pImpl是Widget的私有成员。要让这段代码编译和正常运行，我们可以把这个特殊化函数变为友元函数，但编程惯例是在Widget里声明一个公有的swap成员函数，然后特殊化std::swap来调用这个成员函数:

```text
class Widget{
  public:
    ...
    void swap(Widget& data){
      using std::swap; //这句稍后解释
      swap(pImpl, other.pImpl); //执行真正的swap，只交换指针
    }
   ...
};

namespace std{
  template<> //完全特殊化的std::swap
  void swap<Widget>(Widget& a, Widget& b){
    a.swap(b);
  }
}
```

这样就可以编译了，而且这也是STL标准容器实现swap的方法，STL容器也使用了公有的swap成员函数和一个特殊化的std::swap来调用这个成员函数实现高效交换功能。

------

以上我们讨论过了类，那么对于**类模板**又要怎么做呢?

```text
template<typename T>
class WidgetImpl{...};
template<typename T>
class Widget{...};
```

如果我们还按照上面一样的方法，当然十分简单，但这样的特殊化是过不了编译的:

```text
namespace std{
  template<typename T>
  void swap<Widget<T>>(Widget<T>& a, Widget<T>& b){ //非法代码
    a.swap(b);
  }
}
```

这种做法叫**部分特殊化**(partial  specialization)，即"template<...>"参数表里面还有一个模板参数而不是完全特殊化的"template<>"。C++允许对类模板进行部分特殊化，但不允许对函数模板进行部分特殊化，因此这个方法是行不通的。那我们怎么办呢? 理论上我们可以写一个std::swap模板的**重载**:

```text
namespace std{
  //定义一个重载函数模板
  template<typename T>
  void swap(Widget<T>& a, Widget<T>& b){ //函数名后面没有了<...>就不是特殊化了
    a.swap(b);
  }
}
```

但这种方法并不太推荐，只能叫一个hack，因为std是一个特殊的名空间，我们可以对其中的功能进行特殊化，但不允许往里面再塞东西，因为只有C++委员会才可以对std的内容进行修改。当然理论上即使你加了东西程序也可以编译，但可能会导致我们看不到的冲突，就会导致程序崩溃。

那么现在这么办呢? 其实也很简单，我们依然使用相同的方法定义一个非成员swap函数调用成员swap函数，但不要放在std名空间里，而是放在和我们类模板相同的名空间里:

```text
//我们自己的名空间
namespace WidgetStuff{
  //我们的类模板
  template<typename T>
  class Widget{...};
  ...
  //swap函数和类模板在同一名空间
  template<typename T>
  void swap(Widget<T>& a, Widget<T>& b){
    a.swap(b);
  }
  ...
}
```

这样做还有一个好处就是能把和我们自定义的类相关的所有功能全部整合在一起，在逻辑上和代码上都更加整洁。而且这也符合C++的函数搜索规则，会自动在函数每个实参的名空间和全局作用域内查找函数，即**实参依赖查找**(argument dependent lookup)。当然我们也可以把这个函数放在全局作用域里，但是这样做会显得代码不工整。

这个方法既适用于类也适用于类模板，那看起来是不是比对std名空间进行特殊化舒服多了? 那不论对于类还是类模板是不是应该一直用这个方法?  但其实对std进行特殊化依然是有原因的，如果想让我们的swap函数适用于更多情况，那么除了在我们自己的名空间里写一个swap，在std里面依然要特殊化一个swap，下面就会讲到。

------

目前为止我们都是以一个开发者的角度来思考问题，那么换做用户，假如你再写一个函数要用到swap功能来交换两个对象的数据:

```text
template<typename T>
void doSomething(T& obj1, T& obj2){
  ...
  swap(obj1,obj2);
  ..
}
```

现在要使用哪个swap? 一定存在的std::swap，不一定存在的特殊化std::swap，还是也不一定存在的自定义swap? 最理想的情况是，使用对类型T具体的自定义swap，如果没有则使用std::swap:

```text
template<typename T>
void doSomething(T1& obj1, T2& obj2){
  ..
  using std::swap; //让std::swap对编译器可见
  swap(obj1,obj2); //调用最好的swap
  ...
}
```

当编译器看到要调用swap的时候，实参依赖查找会让编译器在全局作用域和实参的名空间里搜索。例如，如果T是Widget类型，那么编译器就会使用实参依赖查找找到Widget的名空间里的swap。如果没有的话，编译器只能报错。

但是加了这行using语句，编译器便会找到std名空间里的swap。可如果我们不希望使用低效率的默认std::swap，就需要对其进行特殊化，这是依然需要特殊化std::swap的理由之一。如果两个名空间都找到了swap，编译器则会优先选择实参依赖查找的swap。但如果你写:

```text
std::swap(obj1,obj2); //std名空间资格限制
```

这时编译器就只会在std里找到swap函数，那么我们自己名空间下的swap函数编译器连看都不会看。但是这样的代码还可能会藏在标准库或者其它库里的某处，因此对std::swap进行特殊化还是很有必要的，所以为了提升代码对不同情况的适应性，我们需要写自己的swap同时也要对std::swap进行特殊化，作为一个补救措施。

------

现在我们讨论了默认的std::swap，特殊化的std::swap，以及在我们自定义的对类型T具体的swap，可能这章的内容有些多，我们先总结一下:

- 如果默认的std::swap不会对效率产生比较大的影响，例如对象的成员数据不多，直接使用是没有问题的，就不用大费周章搞这些了
- 如果默认的std::swap会对你的函数/类模板产生效率影响: 给你的类使用pimpl手法，然后给它写一个只交换指针的swap成员函数，而且这个函数禁止抛出异常，然后: 
- 对于类模板，要在类模板相同的名空间下写一个自定义的swap，在里面调用swap成员函数
- 对于类(不是类模板)，还要给std::swap进行特殊化，也在它里面调用swap成员函数
- 调用swap的时候确保加上using语句来让std名空间里面的swap对编译器可见，然后swap函数前不要加任何名空间资格限制(qualification)

为什么成员函数swap不能抛出异常?  因为swap这个功能本身经常会被用来实现异常安全。但是非成员函数的swap则可能会抛出异常，因为它还包括了拷贝构造等功能，而这些功能则是允许抛出异常的。当你写一个高效的swap实现时，要记住不仅仅是为了高效，更要保证异常安全，但总体来讲，高效和异常安全是相辅相成的。

------

**总结:**

- 当默认的std::swap可能会拉低你自己的类的效率时，在自己的类里写一个swap成员函数，而且要保证它不会抛出异常
- 写了swap成员函数，按照编程惯例还要写一个非成员swap函数，放在类或者类模板的名空间下，用它来调用成员swap函数。对于类(非模板)，还要特殊化std::swap
- 在调用swap时，要加上一句using std::swap，然后调用时不需要再加任何名空间资格限制
- 为了自定义的类而完全特殊化std模板是没问题的，但千万不要给std里添加任何东西。