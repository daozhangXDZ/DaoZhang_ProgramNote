# 现代c++之移动构造, 移动赋值, 拷贝构造, 拷贝赋值



```cpp
#include <string>
#include <iostream>
#include <memory>
#include <vector>


class CMyString {
private:
	char * buf;
	int len;

private:
	void copy(const char* s) {
		buf = new char[len+1];
		memcpy(buf, s, len);
		buf[len] = '\0';
	}

public:
	CMyString() {
		std::cout << "构造函数" << std::endl;	
	buf = nullptr;
	len = 0;
}
 
CMyString(const char* str = nullptr) {
	if (str == nullptr) {
		std::cout << "构造函数" << std::endl;
 
		buf = nullptr;
		len = 0;
	}
	else {
		std::cout << "构造函数" << str << std::endl;
		len = strlen(str);
		copy(str);
	}
}
 
CMyString(const CMyString& str) {
	std::cout << "拷贝构造函数" << str.buf << std::endl;
 
	len = str.len;
	copy(str.buf);		
}
 
CMyString(CMyString&& str) {
	std::cout << "移动构造函数" << str.buf << std::endl;
 
	//也可以直接使用std::move
 
	len = str.len;
	buf = str.buf;
	str.len = 0;
	str.buf = nullptr;
}
 
CMyString& operator=(const CMyString& str) {
	std::cout << "拷贝赋值函数" << str.buf << std::endl;
 
	if (&str != this) {
		if (buf != nullptr) {
			delete[] buf;
			buf = nullptr;
		}
 
		len = str.len;
		copy(str.buf);
	}
 
	return *this;
}

CMyString& operator=(CMyString&& str) {
	std::cout << "移动赋值函数" << str.buf << std::endl;
 
	if (this != &str) {
 
		if (buf != nullptr) {
			delete[] buf;
			buf = nullptr;
		}
 
		len = str.len;
		buf = str.buf;
		str.len = 0;
		str.buf = nullptr;
	}
 
	return *this;
}
 
~CMyString() {
	if (buf == nullptr)
	{
		std::cout << "析构函数" << std::endl;
	}
	else
	{
		std::cout << "析构函数" << buf << std::endl;
		delete[] buf;
		buf = nullptr;
	}
}
 
void print() {
	if (buf != nullptr)
		std::cout << buf << std::endl;
	else
		std::cout << "buf is null" << std::endl;
}

};

void func1(CMyString str) {
	
}

CMyString func2() {
	CMyString s("34");
	return s;
}

void test0() {
	CMyString s1("12");

	func1(s1); //对象str尚未初始化，会调用拷贝构造函数
	 
	CMyString s2 = func2(); // 对象s2尚未初始化，会产生临时对象，调用移动构造函数

 

	CMyString s3 = "56";
	 
	s3 = s1; //对象s3已初始化，会调用拷贝赋值函数

}

void test1() {
	CMyString s4 = "78";
	std::vector<CMyString> v1;
	//v1.push_back(s4);
	v1.push_back(std::move(s4)); // 对象尚未初始化，会调用移动构造函数

	std::cout << "开始输出v1\n";
	for (auto& str : v1)
		str.print();
	 
	std::vector<CMyString> v2;
	v2 = std::move(v1);
	 
	std::cout << "开始输出v1\n";
	for (auto& str : v1)
		str.print();
	 
	std::cout << "开始输出v2\n";
	for (auto& str : v2)
		str.print();

}

void test2() {
	

	CMyString s5 = "9";
	s5 = func2(); // 对象s5已初始化， 会产生临时对象，调用移动赋值函数

}

int main(void)
{	
	std::cout << "begin test0()" << std::endl;
	test0();
	std::cout << std::endl;

	std::cout << "begin test1()" << std::endl;
	test1();
	std::cout << std::endl;
	 
	std::cout << "begin test2()" << std::endl;
	test2();
	 
	return 0;

}
```


————————————————
版权声明：本文为CSDN博主「我的微信公众号」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/chenhaifeng2016/article/details/74192525