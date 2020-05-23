# 彻底搞定模板类型推导

总体分为三种情况：

```c++
ParamType是一个指针或引用，但不是万能引用，形如：

template<typename T>
void f(T& param); //T&

ParamType是万能引用，形如：

template<typename T>
void f(T&& param); //T&&

ParamType不是指针，也不是引用，形如：

template<typename T>
void f(T param); // just T
```

推导方法：

对于ParamType是一个指针或引用，expr类型（传入的实参类型）去掉引用便是T类型。如：

```c++
例一：

int x = 27;    // x is an int
f(x);          // T is int, param's type is int&
```

x的类型是int，去掉引用（本身就没有），是int，所以T为int，将int带入T&，便是int&，所以ParamType 就是int&

```C++
例二：

const int cx = x;   // cx is a const int
f(cx);              // T is const int, param's type is const int&
```

cx的类型是const int，去掉引用（本身就没有），是const int，所以T是const int，将const int带入T&，ParamType便是const int&

```C++
例三：

const int& rx = x; // rx is a reference to x as a const int
f(rx);             // T is const int, param's type is const int&
```

rx的类型是const int& ，去掉引用，是const int，所以T是const int，将const int带入T&，ParamType便是const int&

ParamType是万能引用，分为两步：

```C++
第一步expr类型（传入的实参类型）去掉引用，得到T
如果expr类型是左值，给T再加上一个&

例一：

int x = 27; // as before
f(x);       // x is lvalue, so T is int&, param's type is also int&

expr的类型，也就是实参x的类型是int，去掉所有&（本身就没有），类型是int
因为x是左值，所以再加上一个&，最终T是int&
```

所以将int &带入T&&，ParamType就是int& &&，引用折叠后就是int&

```C++
例二：

const int cx = x; // as before
f(cx);            // cx is lvalue, so T is const int&, param's type is also const int&

expr的类型，也就是实参cx的类型是const int，去掉所有&（本身就没有），类型是const int
因为cx是左值，所以再加上一个&，最终T是const int&
```

所以将const int &带入T&&，ParamType就是const int& &&，引用折叠后就是const int&

```C++
例三：

const int& rx = x; // as before
f(rx);             // rx is lvalue, so T is const int&, param's type is also const int&

expr的类型，也就是实参rx的类型是const int，去掉所有&（本身就没有），类型是const int
因为cx是左值，所以再加上一个&，最终T是const int&
```

所以将const int &带入T&&，ParamType就是const int& &&，引用折叠后就是const int&

    例四

f(27); // 27 is rvalue, so T is int, param's type is therefore int&&

    expr的类型，也就是实参27的类型是int，去掉所有&（本身就没有），类型是int
    因为27是右值，没有额外操作，T就是int

所以将int带入T&&，ParamType就是 int&&

ParamType不是指针，也不是引用，直接忽略掉expr中所有的&、const、volatile便是T：

```C++
例一：

int x = 27; // as before
f(x);       // T's and param's types are both int
```

x的类型是int，去掉&、const、volatile（本身就没有），是int，所以T为int，将int带入T，便是int，所以ParamType 就是int

    例二：
    
    const int cx = x; // as before
    f(cx);            // T's and param's types are again both int

cx的类型是const int，去掉&、const、volatile，是int，所以T为int，将int带入T，便是int，所以ParamType 就是int

    例三：
    
    const int& rx = x;    // as before
    f(rx);                // T's and param's types are still both int

rx的类型是const int&，去掉&、const、volatile，是int，所以T为int，将int带入T，便是int，所以ParamType 就是int
————————————————
版权声明：本文为CSDN博主「Lailikes」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/songchuwang1868/article/details/90238715