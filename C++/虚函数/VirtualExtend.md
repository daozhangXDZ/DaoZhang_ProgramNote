# 虚继承、虚函数 、sizeof

 

一、含有虚函数的类的sizeof 

假设一个类含有虚函数，那么它就有个隐藏的虚表指针。 

比如

 

class Base {

 

​    int a;

 

​    virtual void f() {}

​    virtual void g() {}

​    virtual void h() {}

 

};

// win32下，sizeof(Base) = 8;也就是int的4个字节和虚表地址的4个字节。

若有声明了Base b；则示意图如下：指向虚函数表的指针在对象b的最前面。 

![虚表指针](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image001.jpg)

 

 

二、非虚继承 

（1）如果是单继承，则派生类只含有一个虚函数表。如果派生类重写了基类函数，则在虚函数表中函数地址被替换；如果派生类有新的自己的虚函数，则追加到虚函数表中；如果派生类新定义了一个和基类虚函数同名的函数，但是函数参数却不同，则在派生类中，该基类同名函数被隐藏（这一点要注意）。

 

class Derived: public Base

{

 

public:

 

virtual void f1() { cout << "Derived::f1" << endl; }

 

virtual void g1() { cout << "Derived::g1" << endl; }

 

virtual void h1() { cout << "Derived::h1" << endl; }

 

};

 

//sizeof（Derived）= 8;也就是基类数据成员int a（4个字节） + Derived类的虚表指针（4个字节）

 

(2)如果是多继承，则在派生类中，有每个基类函数的虚表指针；派生类的成员虚函数被放到第一个类的表中。例如 

 

 

 

 

class Base1

{

​    int a;

​    virtual void f();

​    virtual void g();

​    virtual void h();

}

class Base2

{

​    virtual void f();

​    virtual void g();

​    virtual void h();

}

class Base1

{

​    virtual void f();

​    virtual void g();

​    virtual void h();

}

class Derived: public Base1, public Base2, public Base3

{

 

virtual void f() {}

 

virtual void g1() { }

};

//则`sizeof(Derive) = 4 + 3 * 4`

 

三、虚继承 

虚继承中，派生类会保存一个指向虚基类的指针，而且如果虚基类包含虚函数，则还会保存虚基类中的虚表指针。【如果虚基类（父类）中包含指向其虚基类（爷爷类）的指针，则这个指针，也会继承到派生类中】 

注意：虚继承的具体对象内存分布，不同的编译器实现不同，本文是在VS2015的win32下的结果。 

（1）所有的都是虚继承。

 

class A {

 

​    int a;

 

​    virtual void f() {}

 

};

 

class B :virtual public A {

 

​    virtual void myfunB() {}

 

};

 

class C :virtual public A {

 

​    virtual void myfunC() {}

 

};

 

class D :virtual public B, virtual public C {

 

​    virtual void myfunD() {}

 

};

int main()

{

​    cout << sizeof(A) << endl << sizeof(B) << endl << sizeof(C) << endl << sizeof(D);

​    //输出结果为8 16 16 32

​    return 0;

}

解释： 

sizeof(A)没得说int a 的4个字节加上虚表指针的4个字节 = 8； 

sizeof(B) ：数据也就是A中的int a 4个字节，自己的虚表指针4个字节（注意，这里如果B类没有自己的虚函数，则没有虚表指针），指向虚基类A的指针4个字节，虚基类A的虚表指针。总共16字节； 

sizeof(C) ：与sizeof(B)道理相同。 

sizeof(D) ：数据也就是A中的int a 4个字节，自己的虚表指针4个字节，指向虚基类B的指针4个字节，指向虚基类C的指针4个字节，虚基类B的虚表指针4个字节，虚基类C的虚表指针4个字节，虚基类B中指向其虚基类A的指针4个字节，虚基类C中指向其虚基类A的指针4个字节。总共32字节；【或者换一个角度来算：数据成员 + B的虚表 + B中指向A的指针 + C的虚表 + C中指向A的指针 + D自己的虚表 + D中指向B的指针 + D中指向C的指针】

 

class A {

 

​    int a;

 

​    virtual void f() {}

 

};

 

class B :virtual public A {

 

​    //virtual void myfunB() {}

​    virtual void f() {}

};

 

class C :virtual public A {

 

​    virtual void myfunC() {}

 

};

 

class D :virtual public B, virtual public C {

 

​    virtual void myfunD() {}

 

};

int main()

{

​    cout << sizeof(A) << endl << sizeof(B) << endl << sizeof(C) << endl << sizeof(D);

​    //输出结果为8 12 16 28

​    return 0;

}

（2）既有虚继承，又有非虚继承 

根据节省空间的原则，派生类不再有自己的虚表指针，而是用第一个非虚继承的虚表指针。

 

class A {

 

​    int a;

 

​    virtual void f() {}

 

};

 

class B :virtual public A {

 

​    virtual void myfunB() {}

​    //virtual void f() {}

};

 

class C :virtual public A {

 

​    virtual void myfunC() {}

 

};

 

class D :virtual public B, public C {

 

​    virtual void myfunD() {}

 

};

int main()

{

​    cout << sizeof(A) << endl << sizeof(B) << endl << sizeof(C) << endl << sizeof(D);

​    //输出结果为8 16 16 24

​    return 0;

}

**解释：**class D在上述的全都是虚继承 class D : virutal public B, virtual public C 的基础上，少了一个自己的虚表指针，少了一个指向C的指针，也就是32 - 8 = 24；

 

至此，总结完毕。

\--------------------- 

作者：小鱼Doris 

来源：CSDN 

原文：https://blog.csdn.net/yulijuanxmu/article/details/81022977 

版权声明：本文为博主原创文章，转载请附上博文链接！
