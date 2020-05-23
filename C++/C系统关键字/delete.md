- # delete 与 delete[] 区别

- 1、针对简单类型 使用 new 分配后的不管是数组还是非数组形式内存空间用两种方式均可 如：

- int *a = new int[10];   
     delete a;   
     delete [] a; 

- 此种情况中的释放效果相同，原因在于：分配简单类型内存时，内存大小已经确定，系统可以记忆并且进行管理，在析构时，系统并不会调用析构函数，  它直接通过指针可以获取实际分配的内存空间，哪怕是一个数组内存空间(在分配过程中  系统会记录分配内存的大小等信息，此信息保存在结构体_CrtMemBlockHeader中，  具体情况可参看VC安装目录下CRT\SRC\DBGDEL.cpp)

- 2、针对类Class，两种方式体现出具体差异

- 当你通过下列方式分配一个类对象数组：

- class A
     {
         private:
             char *m_cBuffer;
             int  m_nLen;
         public:
             A(){ m_cBuffer = new char[m_nLen];  }
             ~A() { delete [] m_cBuffer; }
     };
     A *a = new A[10];

- //  仅释放了a指针指向的全部内存空间 但是只调用了a[0]对象的析构函数 剩下的从a[1]到a[9]这9个用户自行分配的m_cBuffer对应内存空间将不能释放  从而造成内存泄漏
     delete a;

- //  调用使用类对象的析构函数释放用户自己分配内存空间并且    释放了a指针指向的全部内存空间
     delete [] a;

- 所以总结下就是，如果ptr代表一个用new申请的内存返回的内存空间地址，即所谓的指针，那么：

- - **delete ptr** -- 代表用来释放内存，且只用来释放ptr指向的内存。
  - **delete[] rg** -- 用来释放rg指向的内存，！！还逐一调用数组中每个对象的       destructor！！

- 对于像 int/char/long/int*/struct 等等简单数据类型，由于对象没有  destructor，所以用 delete 和 delete [] 是一样的！但是如果是C++ 对象数组就不同了！

-  

- 来自 <<http://www.runoob.com/note/15971>> 

-  
