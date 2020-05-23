# Effective C++读书笔记(11): 要考虑到自赋值

**守则11: 赋值操作符要处理自赋值**

> “Handle assignment to self in operator=”

我们先来看一下什么叫自赋值(self-assignment):

```text
class Widget{...};
Widget w;
.....
w = w;             //自赋值
```

可能这样的代码看着有些没用也有些费解，但是在C++的语法中是合法可以编译的。我们再来看更可能会遇到的情况:

```text
a[i] = a[j];       //如果i==j,那么这行代码也构成自赋值
*px = *py;         //如果px和py指向了同一个对象，这行代码也构成自赋值
```

以上的情况都是别名(aliasing)的后果，即某个对象可以通过多于一个符号名被访问，比如上面px和py如果被声明为同一个类型，它们就可以同时可以指向同一个对象。但在一个继承层级中，即使两个对象被声明为了不同的类型，别名依然可能发生，因为基类指针或者引用可以指向任何一个它的子类，例如:

```text
class Base{...};
class Derived : public Base{...};               //同一个继承层级中

void doSomething(const Base& rb, Derived* pd);  //rb与pd就可能指向同一个对象
```

------

如果你要手动管理资源而不使用资源管理类的话(resource managing class，见[第13章](https://zhuanlan.zhihu.com/p/70415131))，你的赋值操作符就可能不是自赋值安全的(self-assignment-safe):

```text
class Bitmap{...}
class Widget{
  ...
  private:
    Bitmap *bp;
};

Widget& Widget::operator=(const Widget& rhs){
  delete pb;
  pb = new Bitmap(*rhs.bp);
  return *this;
}
```

可能第一眼看着没什么问题，但如果传入的参数rhs是它本身呢？这就会导致delete语句把*this自己的资源释放掉，同时也释放掉了rhs的资源，最后返回的*this包含了一个损坏的数据，你不能访问不能修改，甚至不能通过delete来为其释放资源，等于说这段空间就凭空消失了，所以这段代码不是自赋值安全的。

**解决方法1：检查传入的参数是不是\*this**

```text
Widget& Widget::operator=(const Widget& rhs){

  if(this == &rhs)             //先做一个身份检测
    return *this;

  delete pb;                   //如果不是自己，再执行如下操作
  pb = new Bitmap(*this.pb);
  return *this;
}
```

这个解决方法照顾到了自赋值的情况，但仍然不是异常安全(exception-safe)的。试想如果执行过了delete语句，在执行下面的new语句时抛出了异常，例如内存不足，最后仍然会导致*this储存了一个损坏的数据。因此我们来看一个更好的解决方法:

**解决方法2：重新排列语句**

```text
Widget& Widget::operator=(const Widget& rhs){
  Bitmap *pOrigin = pb;            //先保存一个原pb的备份
  pb = new Bitmap(*this.pb);       //拷贝过来rhs的pb
  delete pOrigin;                  //只删除备份
  return *this;
}
```

这条解决方法既对自赋值安全，对异常也是安全的。如果现在new的这行抛出了异常，指针pb也不会被提前删除。同时这样的语句排列省去了上一条解决方法身份检测的步骤，因为即使传入的rhs是*this本身，最后删除的也只是备份而不是*this自己的pb。

**解决方法3：先拷贝再调换(Copy and swap)**

```text
class Widget{
   ...
  void swap(Widget& rhs);   //把rhs和*this的数据成员互相调换
  ...
};

Widget& widget::operator=(const Widget& rhs){
  Widget temp(rhs);       //拷贝rhs
  swap(temp);             //将*this的数据与这个拷贝的数据调换
  return *this;
}
```

利用解决方法2相似的思路，也是相当于生成一份拷贝，再把这份拷贝复制进*this中。还有另一种形式，巧妙利用了C++传值会自动生成一份本地拷贝的特性：

```text
Widget& Widget::operator(Widget rhs){
    swap(rhs);
    return *this;
}
```

这样的代码虽然可能违反了函数要使用常量引用传递的惯例，但这样做确实能减少源代码和目标代码的长度，增加了效率。

**总结：**

- 赋值操作符要考虑到自赋值，使用参数身份检测，排列语句，先拷贝再调换的方法来确保代码是自赋值安全的。
- 同样当一个函数使用多个参数时，也要确保函数能在这些参数同时指向同一个对象时可以工作正常。