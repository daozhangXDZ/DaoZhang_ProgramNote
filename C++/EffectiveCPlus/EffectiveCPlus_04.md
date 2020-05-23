# Effective C++ 读书笔记(4): 对象要初始化

**守则04: 在使用前保证对象是初始化的**

> “Make sure objects are initialized before used”

------

***本篇关键词: 初始化，构造函数，初始化列表，全局变量初始化\***

------

C++并不能保证每个对象在定义时都被自动初始化。就像书中第一条提到的一样，C++包含多种子语言，例如定义一个C风格的整型数组(int[])时，其中就可能包含非零初始化的元素，而在定义标准库(STL)中的容器时，例如一个整型向量(std::vector<int>)，其强大的函数库可以保证所有元素都被零初始化。

**①自有类型(built-in type)的初始化**

C++的自有类型继承于C，因此不能保证此类型的变量在定义时被初始化。使用未初始化的数据可能会导致程序不正常运作，因此在定义变量的时候，需要对其进行初始化，例如将如下代码:

```text
int x;
double d;
```

改为:

```text
int x=0;
double d;
std::cin>>d;
```

**②类的初始化**

对于用户自定义的类，我们需要构造函数(constructor)来完成此类的初始化，例如:

```text
class Coordinate{
  private:
    int x;
    double y;
    const std::list<double>& num;

  public:
    Coordinate(const int& _x, const int& _y, const std::list<double>& _num);
};

//以下构造函数为成员x, y, num赋值来完成对象的初始化
Coordinate::Coordinate(const int& _x, const int& _y, const std::list<double>& _num){
    x = _x;
    y = _y;
    num = _num;
}
```

可能这是一个易于记忆的方法，但并不是最好的方法，因为此构造函数并没有真正完成“初始化”，只不过是做了“赋值”的操作。而C++规定，在进入构造函数**之前**，如果用户没有规定初始化过程，C++将自动调用各成员对应类型的默认构造函数。

这样一来，此构造函数就相当于先调用了C++的默认构造函数，又做了一次赋值操作覆盖掉了先前的结果，造成了浪费。

解决方法：使用初始化列表(initialization list)，C++就不必额外调用默认构造函数了

```text
Coordinate::Coordinate(const int& _x, const int& _y, const std::list<double>& _num):
x(_x), y(_y), num(_num) {}
```

另外，构造函数是可以被重载(overload)的，对于这个我们自己定义的类，还需要一个没有参数输入的默认构造函数，因此我们可以定义:

```text
Coordinate::Coordinate():x(0), y(0), num() {}
//num()调用了std::list<double>类型的默认构造函数
```

**③某些初始化是语法必要的**

例如在定义引用(reference)和常量(const)时，不将其初始化会导致编译器报错

```text
const int a;                //报错，需要初始化！
int& b;                     //报错，需要初始化！

//现在对其进行初始化：

const int a = 3;            //编译通过

int c = 3;
int& b = c;                 //编译通过！
```

**④数据初始化的顺序**

在继承关系中，基类(base class)总是先被初始化。

在同一类中，成员数据的初始化顺序与其声明顺序是一致的，而不是初始化列表的顺序。因此，为了代码一致性，要保证初始化列表的顺序与成员数据声明的顺序是一样的。

```text
class myClass{
  private:
    int a;
    int b;
    int c;
  public:
    myClass(int _a, int _b, int _c);
};

//注意，即使初始化列表是c->b->a的顺序，真正的初始化顺序还是按照a->b->c
myClass::myClass(int _a, int _b, int _c): c(_c), a(_a), b(_b) {}
```

**⑤初始化非本地静态对象**

现在还有一种特殊情况，尤其是在大型项目中比较普遍：在两个编译单元中，分别包含至少一个非本地静态对象，当这些对象发生互动时，它们的初始化顺序是不确定的，所以直接使用这些变量，就会给程序的运行带来风险。

先简要解释一下概念，

**编译单元**(translation unit): 可以让编译器生成代码的基本单元，一般一个源代码文件就是一个编译单元。

**非本地静态对象**(non-local static object): 静态对象可以是在全局范围定义的变量，在名空间范围定义的变量，函数范围内定义为static的变量，类的范围内定义为static的变量，而除了函数中的静态对象是本地的，其他都是非本地的。

此外注意，静态对象存在于程序的开始到结束，所以它不是基于堆(heap)或者栈(stack)的。初始化的静态对象存在于.data中，未初始化的则存在于.bss中。

回到问题，现有以下服务器代码:

```text
class Server{...};     
extern Server server;                 //在全局范围声明外部对象server，供外部使用
```

又有某客户端：

```text
class Client{...};
Client::Client(...){
    number = server.number;
}

Client client;                       //在全局范围定义client对象，自动调用了Client类的构造函数
```

以上问题在于，定义对象client自动调用了Client类的构造函数，此时需要读取对象server的数据，但全局变量的不可控性让我们不能保证对象server在此时被读取时是初始化的。试想如果还有对象client1, client2等等不同的用户读写，我们不能保证当前server的数据是我们想要的。

**解决方法:** 将全局变量变为本地静态变量

使用一个函数，只用来定义一个本地静态变量并返回它的引用。因为C++规定在本地范围(函数范围)内定义某静态对象时，当此函数被调用，该静态变量一定会被初始化。

```text
class Server{...};

Server& server(){                         //将直接的声明改为一个函数
    static Server server;
    return server;
}
```



```text
class Client{...};

Client::client(){                        //客户端构造函数通过函数访问服务器数据
    number = server().number;
}

Client& client(){                        //同样将客户端的声明改为一个函数
    static Client client;
    return client;
}
```

**总结:**

- 对于自由类型，要保证在定义时手动初始化
- 在定义构造函数时，要用初始化列表，避免使用在函数体内的赋值初始化。在使用初始化列表时，为了保持代码一致性，初始化列表中变量的顺序要与其声明顺序相同
- 当不同的编译单元产生互动时，要将其中非本地的静态变量变为本地的静态变量才能保证安全的读写