# 模板特例化



1. 函数模板特例化

```c++
template<typename T>
int func(T, T) {...};           //原始的、最通用的版本
```



```c++
template<>                      //空尖括号指出我们将为原模板的所有模板参数提供实参
int func(char, char) {...};     //特例化为char型的函数，函数可以有新的实现体
```

2. 类模板特例

```c++
template<typename T>
class C {...};            //原始的、最通用的版本
```



```c++
template<>
class C<int> {...};       //类模板特例化为int型的类
```

3. 特例化类的成员

```c++
template<typename T>
class C
 {
    void bar() {...}
 };          
template<>                //我们正在特例化一个模板
void C<int>::bar() {...}  //我们正在特例化C<int>的成员bar，可以有新的函数体
```



```c++
//使用示例：

C<string> fs;
fs.bar();                 //没有使用特例化版本
C<int> fi;
fi.bar();                 //将使用特例化版本C<int>::bar()
```

4. 类模板部分特例化（偏特化，partial specialization）

类模板的部分特例化本身是一个模板，使用它时用户还必须为那些在特例化版本中未指定的模板参数提供实参。



```c++
template<typename T>
class C {...};            //原始的、最通用的版本
```



```c++
template<typename T>
class C<T*> {...};        //该特化版本只适用于“T为原生指针”的情况
```



```c++
template<typename T>
class C<T&> {...};        //该特化版本只适用于“T为左值指针”的情况
```



```c++
template<typename T>
class C<T&&> {...};       //该特化版本只适用于“T为右值指针”的情况
```



5.普通函数模板的使用

```c++
template<typename T>
```


```c++
int C<T>::func(int, int) {...};           //原始的、最通用的版本
```

作者：Peakin 
来源：CSDN 
原文：https://blog.csdn.net/u014587123/article/details/82779357 
版权声明：本文为博主原创文章，转载请附上博文链接！
