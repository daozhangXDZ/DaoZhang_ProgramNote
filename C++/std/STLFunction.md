

# C++ 11 STL | functional 标准库    

最近正好用到了这个，就顺便总结下吧。

C++ 11 引入了函数对象标准库 ``，里面包含各种内建的函数对象以及相关的操作函数，非常方便。这里总结一下 `std::function` 和 `std::bind` 的相关用法。

# Callable type

Callable type 指可以像调用函数一样被调用的对象或函数，包括：

- `std::function`
- `std::bind`
- `std::result_of`
- `std::thread::thread`
- `std::call_once`
- `std::async`
- `std::packaged_task`
- `std::reference_wrapper`

根据 C++ 17 Standard，所有 Callable type 都可以通过 `std::invoke` 方法进行[显式调用](http://en.cppreference.com/w/cpp/utility/functional/invoke)。

# std::function

`std::function`类模板是一种通用的函数包装器，它可以容纳所有可以调用的对象（[Callable](http://en.cppreference.com/w/cpp/concept/Callable)），包括 **函数**、**函数指针**、**Lambda表达式**、**bind表达式**、成员函数及成员变量或者其他函数对象。通过 `std::function` 可以储存、拷贝或调用 Callable 对象。它的模板参数如下：

```c++
template< class R, class... Args >
class function<R(Args...)>
```

使用时，模板参数与要存储的函数参数一致即可，下面是一些例子：

```c++
#include <iostream>
#include <functional>
double f(int x, char y, double z) 
{    
	return x + y + z;
}

void print_num(int num) 
{    
	std::cout << num << std::endl;
}

struct Dog 
{    
	int id;    
	explicit Dog(int id): id(id) {}    
	
	void print_add(int i) const 
	{        
		std::cout << id + i << std::endl;    
	}
};

class PrintString 
{
public:    
	void operator()(std::string&& s) const 
	{        
		std::cout << s << std::endl;    
	}
};

int main(int argc, char **argv) 
{    
	// common function    
	std::function<void(int)> func_display_num = print_num;    
	func_display_num(9);    

	// common function    
	std::function<double(int, char, double)> func_display = f;    
	std::cout << func_display(3, 'a', 1.7) << "\n";    

	// lambda expression    
	std::function<void(const char*)> lbd_dsp_str = [](const char *s) 
		{std::cout << s << std::endl;};       
		
	lbd_dsp_str("Scala");    

	// bind expression    
	auto func_num_bind = std::bind(&f, std::placeholders::_1, 'c', 2.4);    
	std::cout << func_num_bind(24) << "\n";
    
	// function object    
	std::function<void(std::string&&)> func_obj_print = PrintString();    			 		func_obj_print("C++ 17 Nice!");    
	
	// member function    
	const Dog dog(2424);    
	std::function<void(const Dog&, int)> func_mem_display_num = &Dog::print_add;    		func_mem_display_num(dog, 24);    
	
	return 0;
}
```



注意声明时可用`auto`进行自动类型推导，这样可以节约时间，不过这样会牺牲代码的可读性，因此需要根据情况合理使用`auto`。

# std::bind

顾名思义，`std::bind`函数用来绑定函数的某些参数并生成一个新的`function`对象。
`bind`用于实现偏函数（Partial Function），相当于实现了函数式编程中的 **Currying**（柯里化）。
比如有一函数的定义为：

```c++
void func_muti(int a, std::string&& b, const char* c, double d, char e) 
{    
	std::cout << a << ", " << b << ", " << c << ", " << d << ", " << e << "\n";
}
```



现在将此函数的一些参数绑定上值，其余部分用占位符对象（std::placeholders）表示。占位符是有序号的，代表调用此函数对象时参数在参数列表中的位置。比如：

```c++
auto f = std::bind(&func_muti, 24, std::placeholders::_1, "Haha", std::placeholders::_2, 'P');  

f("Hehe", 24.24);
```



调用这个函数对象相当于调用以下函数：

```c++
void f(std::string&& b, double d) 
{    
	std::cout << "24" << ", " << b << ", " << "Haha" << ", " << d << ", " << 'P' << "\n";  }
```