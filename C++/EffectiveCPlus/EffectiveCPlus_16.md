# Effective C++读书笔记(16): new与delete要对应

**守则16: 对应的new和delete要使用相同的形式**

> "Use the same form in corresponding uses of new and delete"

------

***本篇关键词：动态分配的数组， delete[]\***

------

我们先来看下面这段代码有什么问题：

```text
std::string *strArr = new std::string[100]; //动态分配100元素的字符串数组
...             //使用
delete strArr;  //释放
```

看起来new与delete似乎是对应了，可是这样只会释放数组的第一个元素，其他99个对象则不会被释放，因为它们的析构函数没有被调用。

我们来看一下new和delete的工作原理：当你使用new运算符的时候会发生两件事，你所申请的内存空间会先被分配出来，然后一个或者多个对象的构造函数被调用来填满这些空间。当你使用delete的时候，则是先调用这些对象的析构函数，最后释放内存资源。

delete要删除多少个对象取决于在当前内存空间中调用多少个析构函数，那么编译器就需要知道到底是删除单个对象还是一个数组，因为单个对象和一个数组的对象有**不同的内存布局**：数组的内存除了它所包含的对象，还包括了一个额外的数，即数组的大小，用来告诉编译器调用多少个析构函数:

```text
以下为内存示意图
单个对象：       |对象|
一个数组的对象： | n | 对象 | 对象 | 对象 | 对象 |...  //n即为数组的大小
```

现在你需要告诉编译器具体是删除单个对象还是一个数组，即使用delete还是delete[]

```text
std::string strPtr1 = new std::string;  //分配单个对象
std::string strPtr2 = new str::string[100];  //分配一个数组
...
delete strPtr1;   //使用delete删除单个对象
delete[] strPtr2; //使用delete[]删除数组
```

但是如果我们使用delete[]来释放单个对象会发生什么？未定义，因为决定于不同的编译器，delete[]可能会读取一些内存作为上面的n，然后调用析构函数n次，这就可能会损坏到其他数据，或者它根本就调用不了任何析构函数，因为它读取对象的地址是不正确的。

总之，结论很简单，如果你在new里分配了数组，就要确保delete也释放数组，如果你没有在new里分配数组，就不要在delete里释放数组。同样如果一个类含有动态分配的数组成员，并且支持多个构造函数，就要确保**每个**构造函数都使用数组版本的new，否则析构函数就可能不会使用正确版本的delete。

------

在**typedef**类型中需要另加注意，最好在代码注释中标出要使用什么版本的delete:

```text
typedef std::string AddressLines[4]; //定义AddressLines类型为
                                     //一个包含4个字符串的数组
                                     //所以需要对其使用delete[]
std::string *pal = new AddressLines; //相当于new string[4]
...
delete pal;   //错误
delete[] pal; //正确
```

这种方法可能会引起误解，如果这个类型在别的文件中定义，我们就不知道它其实是一个数组，自然也就不会在释放资源时使用delete[]，所以避免给数组使用typedef。而且我们完全可以用标准容器来替代，例如std::vector，它们的模板让我们不再需要手动typedef，功能也远比原生数组强大。那么AddressLines类型就可以被替代为一个标准字符串的向量，即std::vector<std::string>

------

**总结：**

- 如果在new语句中使用了[ ]，就必须在对应的delete语句中也使用[ ]。如果在new语句中没有使用[ ]，就不要在对应的delete语句中使用[ ]。