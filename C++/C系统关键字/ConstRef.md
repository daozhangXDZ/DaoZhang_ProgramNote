# C++中的const引用和非const引用 



非const引用只能绑定到与该引用同类型的对象，const引用则可以绑定到不同但相关的类型的对象或绑定到右值。

 （1）       在实际的程序中，引用主要被用做函数的形式参数--通常将类对象传递给一个函数.引用必须初始化. 但是用对象的地址初始化引用是错误的，我们可以定义一个指针引用。

 1 int ival = 1092;

 2 int &re = ival;   //ok

 3 int &re2 = &ival;   //错误

 4 int *pi = &ival;

 5 int *&pi2 = pi;   //ok

 （2）       一旦引用已经定义，它就不能再指向其他的对象.这就是为什么它要被初始化的原因。

 （3）       const引用可以用不同类型的对象初始化(只要能从一种类型转换到另一种类型即可)，也可以是不可寻址的值，如文字常量。例如

 double dval = 3.14159;

 //下3行仅对const引用才是合法的

 const int &ir = 1024;

 const int &ir2 = dval;

 const double &dr = dval + 1.0;

 上面，同样的初始化对于非const引用是不合法的，将导致编译错误。原因有些微妙，需要适当做些解释。

 引用在内部存放的是一个对象的地址，它是该对象的别名。对于不可寻址的值，如文字常量，以及不同类型的对象，编译器为了实现引用，必须生成一个临时对象，引用实际上指向该对象，但用户不能访问它。

 例如:

 double dval = 23;

 const int &ri = dval;

 编译器将其转换为:

 int tmp = dval; // double -> int

 const int &ri = tmp;

 同理：上面代码

 double dval = 3.14159;

 //下3行仅对const引用才是合法的

 const int &ir = 1024;

 const int &ir2 = dval;

 const double &dr = dval + 1.0;

 内部转化为：

 double dval = 3.14159;

 //不可寻址，文字常量

 int tmp1 = 1024;

 const int &ir = tmp1;

 //不同类型

 int tmp2 = dval;//double -> int

 const int &ir2 = tmp2;

 //另一种情况，不可寻址

 double tmp3 = dval + 1.0;

 const double &dr = tmp3;

 （4）       不允许非const引用指向需要临时对象的对象或值，即，编译器产生临时变量的时候引用必须为const!!!!切记！！

 int iv = 100;

 int *&pir = &iv;//错误，非const引用对需要临时对象的引用

 int *const &pir = &iv;//ok

 
 const int ival = 1024;

 int *&pi_ref = &ival;    //错误，非const引用是非法的

 const int *&pi_ref = &ival;   //错误，需要临时变量，且引用的是指针，而pi_ref是一个非常量指针

 const int * const &pi_ref = &ival;  //正确

 //补充

 const int *p = &ival;

 const int *&pi_ref = p;  //正确

 （5）       ********对于const int *const & pi_ref = &iva; 具体的分析如下：*********

 1.不允许非const引用指向需要临时对象的对象或值

 int a = 2;

 int &ref1 = a;// OK.有过渡变量。

 const int &ref2 = 2;// OK.编译器产生临时变量，需要const引用

 2.地址值是不可寻址的值

 int * const &ref3 = &a;   // OK;

 3.于是，用const对象的地址来初始化一个指向指针的引用

​     const int b = 23;

​     const int *p = &b;

​     const int *& ref4 = p;

​     const int *const & ref5 = &b;   //OK

 const引用的语义到底是什么？

  

 最后，我们可能仍然不明白const引用的这个const的语义是什么

 const引用表示，试图通过此引用去(间接)改变其引用的对象的值时，编译器会报错！

 这并意味着，此引用所引用的对象也因此变成const类型了。我们仍然可以改变其指向对象的值，只是不通过引用

 下面是一个简单的例子：

  1 #include <iostream>

  2 using namespace std;

  3

  4 int main()

  5 {

  6     int val = 1024;

  7     const int &ir = val;

  8    

  9     val++;

 10     //ir++;

 11

 12     cout << val << " " << ir << endl;

 13

 14     return 0;

 15 }

  

  

 其中第10行，如果我们通过ir来改变val的值，编译时会出错。但是我们仍然可以通过val直接改变其值(第9行)

  

 总结：const引用只是表明，保证不会通过此引用间接的改变被引用的对象！

 另外，const既可以放到类型前又可以放到类型后面，放类型后比较容易理解：

 string const *t1;

 const string *t1;

 typedef string* pstring;string s;

 const pstring cstr1 = &s;就出错了

 但是放在类型后面不会出错:

 pstring const cstr2 = &s;







# C++函数中返回引用和返回值的区别

 

int& at()

{

​    return m_data_;

}

int at()

{

​    return m_data_;

}12345678

 

上面两个函数，第一个返回值是int的引用int&，第二个返回值是int，二者的区别是什么呢？

 

 

返回值为引用型（int& ）的时候，返回的是地址，因为这里用的是 int& a=mymay.at(); ，所以a和m_data_指的是同一块地址（由寄存器eax传回的5879712）。

返回值不是引用型（int）的时候，返回的是一个数值。这个时候就很有意思了，编译器是先将这个数值放入一个内存中（上面例子中，该内存地址为ebp-24h)，再把这个地址付给a，此时的a代表的地址是ebp-24h，和m_data_代表的地址不一样（m_data_代表的地址是5879712）。

综上两点可以看出，当返回的值不是引用型时，编译器会专门给返回值分配出一块内存的（例子中为ebp-24h）。
