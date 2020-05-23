# Effective C++读书笔记(26): 推迟变量定义

**守则26: 要尽量长地推迟变量的定义**

> "Postpone variable definitions as long as possible"

------

***本篇关键词: 函数里的变量在哪定义，循环里的变量在哪定义***

------

每当定义一个变量时，就会带来构造和析构的运行成本，因为代码运行到定义时会调用对象的构造函数，当离开作用域时便会调用析构函数。那么我们可能会直接想到，不定义未使用的变量不就可以了吗? 但这只是一部分，有时候定义了要使用的变量依然有几率会导致浪费。

我们看下面的例子，一个用来给足够长的密码进行加密的函数，如果密码不够长则抛出标准C++的logic_error:

```text
std::string encryptPassword(const std::string& password){
  using namespace std;
  string encrypted; //定义太早了
  encrypted = password;

  if(password.length() < minPasswordLength)
    throw logic_error("Password too short");
  ....//加密
  return encrypted;
}
```

字符串对象encrypted显然不是我们所讲的"未使用的变量"，因为下面的代码明显要用到它。但如果这个函数抛出了异常，那它就是一个未使用变量了，它所消耗的资源也都浪费了。因此我们需要把它的定义尽量往后推迟，直到我们100%确定要用到:

```text
std::string encryptPassword(const std::string& password){
  using namespace std;

  if(password.length() < minPasswordLength)
    throw logic_error("Password too short");

  string encrypted;  //这时我们才确定它会被用到
  encrypted = password;
  ....//加密
  return encrypted;
}
```

但其实还可以进一步优化一下。注意上面encrypted是默认构造的，因为没有任何参数传进构造函数。[第四章](https://zhuanlan.zhihu.com/p/64141116)讲到默认构造一个对象再进行赋值是比较低效的，我们应该直接使用带有参数的构造函数:

```text
//用:
string encrypted(password);
//替换掉:
string encrypted;
encrypted = password;
```

要注意这是"推迟定义"的另一个意义。我们不仅仅需要把变量的定义推迟到**100%要用到**的地方，还要把它推迟到**100%有构造参数可用**的时候。这样做既可以避免不必要的构造和析构过程，也能节省默认构造再赋值的成本。而且这样的代码也更可读，因为变量定义在了真正需要它的环境下。

------

那么循环呢? 如果一个变量只在循环里用到，把它定义在循环外面然后每次在里面赋值好，即代码A，还是直接在里面定义呢，即代码B?

```text
//代码A，在外面定义
Widget w;
for(int i=0; i<n, i++){
  w=...;
  ...
}

//代码B，在里面定义
for(int i=0; i<n; i++){
  Widget w(...);
  ...
}
```

那么我们就来分析一下A和B各自的运行成本:

```text
A: 1个构造 + n个赋值 + 1个析构
B: n个构造 + n个析构
```

现在我们就可以看出来了，对于赋值成本低于(构造+析构)的类，A是更高效的选择，尤其是当n很大的时候。反之如果赋值成本大于(构造+析构)，B则是更好的选择。但是对象在A的作用域比在B要大，有时是不利于程序的可读性和可维护性的。因此**除非**你知道赋值成本低于(构造+析构)，而且这段代码要更注重效率，那么我们应该默认使用B。

**总结:**

- 要尽量长地推迟变量定义，直到我们确定它会被用到，而且有构造参数可用的时候。这样既能增加程序可读性，也能提升效率