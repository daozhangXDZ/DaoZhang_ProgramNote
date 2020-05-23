# C++模版元编程中如何拼接两个const char*？

作者：Starve Jokes
链接：https://www.zhihu.com/question/53372308/answer/134717572
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



如果利用宏，上面有别人贴过的爆栈的link应该够用了

如果洁癖不利用宏，必须先把const char[]类型的string literal转为可以其他类型，以便下手。
原因是C++里面built-in数组没有constexpr的构造函数，仅有{}形式一种（修正：这里其实是因为gcc一个bug导致数组的built-in copy constructor不被认为constexpr，clang是支持的）

这里为了保证构造函数constexpr，取巧利用了一个C++规范外，但是基本是事实标准的class layout，即单一继承情况下，base class的成员在derived class的成员之前。

```cpp
template <size_t N>
struct String : String<N-1> {
	constexpr String(const char(&str)[N]) : String<N-1>(str), c(str[N-1]) {}
protected:
	template <size_t M>
	constexpr String(const char(&str)[M]) : String<N-1>(str), c(str[N-1]) {}
	char c;
};
template <>
struct String<0> {
	template <typename ...T>
	constexpr String(T...) {}
};
```

这样进行任何String的实例即可生成一个memory layout和const char[]一致的实例
如String<6>("hello")。
可以用个辅助函数来使用时避开模板参数

```cpp
template <size_t N>
constexpr String<N> mkString(const char(&str)[N]) { return String<N>(str);}
constexpr String<0> mkString(const char(&str)[0]) { return String<0>(str);}
```

这样使用时只需要mkString("hello")即可。

然后有了这个String类，想拼接就很容易啦，我这里上一个***偷懒的版本\***，即String<M+1>+String<N+1>后结果不为String<M+N+1>而是其他类型。完全是因为我懒。因为要写成String<M+N+1>的话，String类的构造函数要写的很复杂，留作思考题大家回去做作业

```cpp
template <size_t M, typename T>
struct StringCat : String<M-1>
{
	T t;
    constexpr StringCat(const char(&str)[M], const T& str2) : String<M-1>(str), t(str2) 	{
        
    }
};
  
template <size_t M, size_t N>
constexpr StringCat<M, String<N>> catString(const char(&str)[M], const char(&str2)[N]) 
{
	return StringCat<M, String<N>>(str, mkString(str2));
}  
```

这样使用时，只要直接用auto + catString即可
（这里catString暴露的接口是2个const char (&)[]，你可以在中间增加别的接口，例如直接用上面的String类，同时你也可以考虑用variadic template来实现多个字符串的拼接）

```cpp
const char hello[] = "hello, ";
const char world[] = "world!!";
//这里hello和world声明为array而不是pointer
//是因为String类的构造函数做了保护性检查，public构造函数仅接受const char [SIZE]的array
//可以修改String类的构造函数的参数为const char *
//来使用const char *类型的字符常量
const auto helloworld = catString(hello, world);
```

生成汇编如下

```text
helloworld:
        .byte   104
        .byte   101
        .byte   108
        .byte   108
        .byte   111
        .byte   44
        .byte   32
        .byte   119
        .byte   111
        .byte   114
        .byte   108
        .byte   100
        .byte   33
        .byte   33
        .byte   0
```

需要const char*的话，reinterpret_cast<const char*>(&helloworld)