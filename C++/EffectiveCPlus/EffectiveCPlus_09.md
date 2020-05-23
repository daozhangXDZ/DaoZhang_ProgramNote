# Effective C++读书笔记(9): 不要让虚函数出现在构造或析构过程中

**守则09: 不要在构造函数和析构函数中调用虚函数**

> "Never call virtual functions during construction or destruction"

------

***本篇关键词：构造，析构，虚函数\***

------

假如你在为某证券公司设计股市交易软件，需要有一个类用来表示股市交易:

```text
class Transaction{                              //股市交易的基类
  public:
    Transaction();
    virtual void logTransaction() const =0;     //该函数用来记录交易历史，是一个纯虚函数
    ....
};

Transaction::Transaction(){
  ...
  logTransaction();                             //在基类的构造函数中调用了这个纯虚函数
}
```

同时又有表示"买进"和"卖出"的类，继承自以上的"交易":

```text
class BuyTransaction : public Transaction{
  public:
    virtual void logTransaction() const;
  ...
};

class SellTransaction : public Transaction{
  public:
    virtual void logTransaction() const;
  ...
};
```

于是在某处定义了一个"买进"类的对象:

```text
BuyTransaction b;
```

显然这里调用了"BuyTransaction"的构造函数。但因为在C++中，当子类开始构造时，它所包含的父类的部分要先完成构造，所以率先调用的构造函数是它的父类"Transaction"的构造函数。现在问题来了，因为父类的构造函数调用了一个**纯虚函数**，这就会导致即使你创建的是它的子类对象，这个虚函数也不会绑定到子类的版本上，而是使用的父类版本。

这就"有悖常理"了，虚函数不是会**自动**绑定到继承层级里对应的一个类吗？其实C++这样做是有一个很好的原因的。我们在[第4章](https://zhuanlan.zhihu.com/p/64141116)讲过，使用未初始化的数据可能会给程序带来风险。因为在创建一个子类对象时，它的父类部分会先被创建。当父类的构造函数刚刚调用完成时，我们只能保证父类部分的数据被初始化，而不能保证衍生部分的被初始化。如果现在让这个虚函数去对应子类的版本，就可能会因为使用未初始化的数据而导致程序**运行时错误**。

事实上，正是由于这个原因，当一个子类对象在完成它自己全部成员的构造之前，C++只会把它当成父类，除了虚函数还包括typeid，dynamic_cast等，都会把当前对象当做父类，用来规避使用未初始化数据可能带来的风险。

------

同样的原理，我们也不要让析构函数调用虚函数。我们在[第7章](https://zhuanlan.zhihu.com/p/65257902)讲过，析构函数的调用顺序是从子类到父类，与构造函数的调用顺序是相反的。当子类部分的成员数据被删除时，C++同样会把当前的对象认为是父类，如果这时调用了虚函数，也会导致错误版本的虚函数被调用。

------

实际上这样在构造函数或者析构函数里直接调用虚函数，在某些编译器中是会发出警告的。不过即使无视掉这些警告，因为调用的是一个纯虚函数，通常是不会有定义的，所以在之后的链接过程中，链接器也会报错。

但如下的代码做了完全一样的事，编译器和链接器却都不会发出警告或报错。这样的代码相比前面的就更具有潜在危害性:

```text
class Transaction{
  public:
    Transaction(){ init(); }                  //调用了一个专门的init()函数
    virtual void logTransaction const =0;
    ...
  private:
    void init(){                              //这个函数不是虚函数，而且有定义
      ...                                     //编译器和链接器就都不会报错
      logTransaction();                       //但里面却包含了虚函数的代码
    }
  ...
};
```

即使init()函数有定义而且不是虚函数，它却调用了没有定义的纯虚函数logTransaction()，这就会导致在运行过程中，一旦使用了这里的代码，程序就会崩溃。

就算logTransaction()函数是一个有定义的"普通的"虚函数，即没有"=0"关键字来修饰，程序虽然不会因为缺少定义而闪退，但却一样会在子类的构造过程中调用错误版本的虚函数。所以万全的解决方法就是，不管是纯虚的还是普通的，就不要在构造或者析构函数中调用虚函数。

------

但如果一定想要对象在初始化的时候完成某些任务呢？那我们就需要在父类Transaction中，把虚函数logTransaction去掉virtual关键字，变成普通的函数，然后在子类构造过程中，把某些信息传递到父类的构造函数中。

```text
class Transaction{
  public:
    explicit Transaction(const std::string& info);      //explicit关键字用来防止隐式转换
    void logTransaction(const std::string& info) const; //增加一个传递参数，就可以从子类获得信息了
    ...
};

Transaction::Transaction(const std::string& info){
  ...
  logTransaction(info);  
}
```

现在就可以在子类对象中如下定义构造函数了，这样就能把子类的信息传递到父类中，让父类构造函数去完成子类构造函数想做的事：

```text
class BuyTransaction : public Transaction{
  public:
    BuyTransaction(...) : Transaction(createLog(...)) { ...}
    ...
  private:
    static std::string createLog(...);
};
```

这里createLog()就是一个**辅助函数**(helper function)，用来将某函数的一部分功能封装成另一个小函数，减少代码的复杂性，使代码更加可读。此外，因为这是一个子类的私有成员，父类构造函数被调用时不能保证它被初始化，所以使用static关键字可以避免意外使用了未初始化的成员数据。

**总结：**

- 不要在构造函数或者析构函数中调用虚函数，因为这样的虚函数只会对应起来当前构造或析构的类，不会上升到它的任何子类。