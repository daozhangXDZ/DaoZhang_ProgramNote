# Effective C++读书笔记(12): 要完整拷贝对象

**守则12: 要完整拷贝对象**

> "Copy all parts of an object"

C++有两种**拷贝函数**(copying function): **拷贝构造函数**(copy constructor)和**拷贝赋值操作符**(copy assignment operator)。在[第五章](https://zhuanlan.zhihu.com/p/64503890)我们讲到过，如果在自己定义的类中不声明这些拷贝函数，编译器会自动为你生成。如果我们声明了自己的拷贝函数，程序将会执行我们自己的拷贝函数。我们来看一个栗子:

```text
void logCall(const std::string& funcName);
class Customer{
  public:
    ...
    Customer(const Customer& rhs);
    Customer& operator=(const Customer& rhs);
  private:
    std::string name;
};

Customer::Customer(const Customer& rhs):name(rhs.name){   //使用初始化列表
  logCall("Customer copy constructor");
}

Customer& Customer::operator=(const Customer& rhs){
  logCall("Customer copy assignment operator");
  name = rhs.name;    //拷贝数据
  return *this;       //返回*this，见第10章
}
```

以上我们定义了Customer类的构造函数(使用了初始化列表)和拷贝赋值操作符，这些代码是没有问题的。可是直到我们新增了一个数据成员:

```text
class Date{...};
class Cutomer{
  ...
  private:
    std::string name;
    Data lastTransaction;     //新增了一个交易日期的数据成员
};
```

如果我们依然使用相同的两种拷贝函数，那么我们只能得到一个**部分拷贝**的对象(partial copy)，我们只能拷贝到name而不能拷贝到lastTransaction。

**解决方法:**

很简单很直接，当我们的类新增数据成员时，要保证拷贝函数也要照顾到新来的同志们。

------

部分拷贝更可能潜在发生的地方是继承层级中，假设我们在普通用户之上定义一个VIP用户:

```text
class PriorityCustomer : public Customer{
  public:
    ...
    PriorityCustomer(const PriorityCustomer& rhs);
    PriorityCustomer& operator=(const PriorityCustomer& rhs);
  private;
    int priority;
};

PriorityCustomer::PriorityCustomer(const PriorityCustomer& rhs)
  :priority(rhs.prority){           //使用初始化列表来构造该类的数据成员
  logCall("PriorityCustomer copy constructor");  
}

PriorityCustomer& PriorityCustomer::operator=(const PriorityCustomer& rhs){
  logCall("PriorityCustomer copy assignment operator");
  priority = rhs.priority;          //拷贝该类的数据成员
  return *this;
}
```

以上代码看起来像是拷贝了所有的数据成员，但是却忘记了它的基类部分！如果我们不传入基类对象作为子类构造函数的参数，当构造这个子类的时候，它的基类的**默认**构造函数将会被调用，结果就是，基类Customer的name等数据成员被设定为了默认值，那么全体VIP用户的数据就丢失了（人家充了钱反而号被你搞丢了）

我们再来看赋值操作符，赋值操作符同样没有把基类作为传进来的参数，因此当拷贝某对象时，它的基类部分也不会被拷贝进来，所以这样的代码同样会导致一个部分拷贝。

**解决方法:**

```text
PriorityCustomer::PriorityCustomer(const PriorityCustomer& rhs)
  : priority(rhs.prority), Customer(rhs){     //要把基类部分也添加进初始化列表
  logCall("PriorityCustomer copy constructor"); 
}

PriorityCustomer& PriorityCustomer::operator=(const PriorityCustomer& rhs){
  logCall("PriorityCustomer copy assignment operator");
  Customer::operator=(rhs);         //要使用基类的拷贝操作符
  priority = rhs.priority; 
  return *this;
}
```

------

这一章讨论的是完整拷贝的问题，但一般我们也要考虑到操作符的异常安全性(exception safety)，所以需要结合[上一章](https://zhuanlan.zhihu.com/p/68201431)讨论的的异常安全性，例如使用先拷贝再调换(copy and swap)的思路，来实现万全的拷贝赋值功能。

可能大家也会发现，C++的这两种拷贝函数有相似的功能和代码，那么我们能不能避免代码重复，让其中一个拷贝函数调用另一个呢？答案是**不能**

使用拷贝赋值操作符调用拷贝构造函数，或者使用拷贝构造函数调用拷贝赋值操作符，都是没有意义的。拷贝赋值操作符适用于已经构造好的对象，而拷贝构造函数适用于还没有构造好的对象，所以这种做法在语义上是错误的。

如果我们真的想要节省代码，比如某个类有特别多的数据成员，我们可以写另一个函数用来给每个成员赋值，两个拷贝函数都可以调用，这个函数一般叫init()。

**总结：**

- 拷贝函数要照顾到类的所有部分，包括所有的数据成员和它的基类部分
- 不要用一个拷贝函数来实现另一个拷贝函数，两种拷贝函数的语义不同。如果要节省代码，可以另写一个init()函数让两个拷贝函数来调用。