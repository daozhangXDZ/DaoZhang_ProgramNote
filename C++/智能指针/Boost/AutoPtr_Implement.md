# C++ -- 智能指针（自己模拟实现简单的智能指针）

上一篇文章介绍了智能指针的基本概念及boost库里基本的智能指针，这里主要模拟实现库里面的智能指针（简单实现）。https://blog.csdn.net/xu1105775448/article/details/80625936

## auto_ptr

1.auto_ptr具有RAII和像指针一样的特点。
2.模拟实现：



```c++
  template<class T>
class Auto_Ptr
{
public:
      //RAII
      Auto_Ptr(T* ptr)
           :_ptr(ptr)
      {}
  ~Auto_Ptr()
  {
       delete _ptr;
  }

  //像指针一样
  T& operator*()
  {
       return *_ptr;
  }

  T* operator->()
  {
       return _ptr;
  }
protected:
      T* _ptr;
};

void TestAutoPtr()
{
      int *ptr = new int(10);
      Auto_Ptr<int> p(ptr);
      /**p = 20;
      cout << *p << endl;*/
      Auto_Ptr<int> p1(p);

}
```
3.但是如果只写上面的代码就会有一个问题，当我们想将一个AutoPtr赋值（或拷贝构造）给另一个AutoPtr，我们没写它的拷贝构造和赋值运算符重载，就会调用编译器的，这是浅拷贝，就会导致空间被多次释放。
4.auto_ptr思想是：管理权的转移。也就是当发现有一个auto_ptr对象a1赋值给另一个对象a2或者拷贝构造a2，那么a1获得的资源就交给a2，a2来管理a1指向的那块空间，a1就指向NULL,这样就保证了每块空间只有一个auto_ptr对象指向它，就不会有空间被释放多次的问题。
5.自己模拟实现完善版本的：



```c++
 template<class T>
class AutoPtr
{
public:
      //构造函数获得资源
      AutoPtr(T* ptr)
           :_ptr(ptr)
      {}
      //管理权转移
      AutoPtr(AutoPtr<T>& ap)   //参数不能加const
           :_ptr(ap._ptr)
      {
           ap._ptr = NULL;
      }
      AutoPtr<T>& operator=(AutoPtr<T>& ap)
      {
           if (this != &ap)
           {
                 //先释放自己的
                 delete _ptr;
                 _ptr = ap._ptr;
                 ap._ptr = NULL;
           }
           return *this;
      }
      //析构函数清理资源
      ~AutoPtr()
      {
           if (_ptr != NULL)
           {
                 delete _ptr;
                 printf("0X%p\n", _ptr);
           }
      }

      //像指针一样
      T& operator*()
      {
           return *_ptr;
      }

      T* operator->()
      {
           return _ptr;
      }
  protected:
      T* _ptr;
};

void TestAutoPtr()
{
      AutoPtr<int> ap1(new int(10));
      AutoPtr<int> ap2(new int(20));
      ap1 = ap2;
}
```


6.auto_ptr管理权的另一种实现方式：（增加一个bool类型的owner,作为一个标志，如果我管理这块空间，那么我的owner就为true，没有管理就为false）；但是这种方式没有上面直接将指向的空间置空好，若ap1拷贝构造ap2，那么这里的所有权就在ap2上，即ap2的owner为true，ap1的owner为false,但是如果ap2的生命周期比ap1短就有问题。例如函数传参时，当用ap2传给一个函数fun，而fun得参数为一个auto_ptr对象ap，就会将ap2得管理权转移给ap，当ap出了作用域就会调用其析构函数，就会将ap指向的空间释放掉，就会使得再想访问ap2就会出错。



```c++
  template<class T>
class AutoPtr
{
public:
      //构造函数获得资源
      AutoPtr(T* ptr)
           :_ptr(ptr)
           ,_owner(true)
      {}
  //管理权转移
  AutoPtr(AutoPtr<T>& ap)
       :_ptr(ap._ptr)
  {
       ap._owner = false;
       _owner = true;
  }
  AutoPtr<T>& operator=(AutoPtr<T>& ap)
  {
       if (this != &ap)
       {
             //先释放自己的
             delete _ptr;
             _ptr = ap._ptr;
             ap._owner = false;
             _owner = true;
       }
       return *this;
  }
  //析构函数清理资源
  ~AutoPtr()
  {
       if (_owner == true)
       {
             delete _ptr;
             printf("0X%p\n", _ptr);
       }
  }

  //像指针一样
  T& operator*()
  {
       return *_ptr;
  }

  T* operator->()
  {
       return _ptr;
  }
  protected:
      T* _ptr;
      bool _owner;
};
```
7.但是autoptr有个很大的缺点，当将ap1的管理权交给ap2后，就会使得ap1指向一块空的空间，当需要解引用ap1时，就是解引用空指针。

## scoped_ptr

1.scoped_ptr也要有RAII和像指针一样的特点，它采用防拷贝的方式。（防拷贝：将拷贝构造和赋值运算符是声明实现，并且声明为私有，因为我们自己声明，就不会调用系统自动生成的，而且如果只声明，就会有人在类外定义，所以必须声明为私有）
2.模拟实现：

```c++
  template<class T>
class ScopedPtr
{
public:
      //RAII
      ScopedPtr(T* ptr)
           :_ptr(ptr)
      {}
  ~ScopedPtr()
  {
       if (_ptr)
       {
             delete _ptr;
       }
  }

  //像指针一样
  T& operator*()
  {
       return *_ptr;
  }

  T* operator->()
  {
       return _ptr;
  }
  public:
      //将拷贝构造和赋值运算符重载声明为私有
      ScopedPtr(const ScopedPtr<T>& sp);
      ScopedPtr<T> operator=(const ScopedPtr<T>& sp);

protected:
      T* _ptr;
};

void TestScopedPtr()
{
      ScopedPtr<int> sp(new int(10));
      ScopedPtr<int> sp1(sp);
}
```



scoped_array

1.scoped_ptr用于管理new单个对象的空间的释放，而scoped_array用于管理new多个对象的释放（即调用new[]），而且scoped_array里面不支持operator*和operator->。对数据的访问采用[]（像数组一样，通过下标的形式）。
2.模拟实现：



```c++
  template<class T>
class ScopedArray
{
public:
      //RAII
      ScopedArray(T* ptr)
           :_ptr(ptr)
      {}
  ~ScopedArray()
  {
       if (_ptr)
       {
             delete[] _ptr;
       }
  }

  T& operator[](size_t pos)
  {
       return _ptr[pos];
  }
  public:
      ScopedArray(const ScopedArray<T>& sp);
      ScopedArray<T> operator=(const ScopedArray<T>& sp);

protected:
      T* _ptr;
};
void TestScopedArray()
{
      ScopedArray<int> sp1(new int[10]);
}
```

shared_ptr

1.shared_ptr为共享指针，意味我们共同指向一块空间；里面采用引用计数，当有别的shared_ptr指向我这块空间时，就增加引用计数，当引用计数减为0的时候，才释放这块空间。
2.模拟实现：



```c++
  template<class T>
class SharedPtr
{
public:
      SharedPtr(T* ptr)
           :_ptr(ptr)
           , _pCount(new int(1))
      {}
  SharedPtr(const SharedPtr<T>& ap)
       :_ptr(ap._ptr)
       , _pCount(ap._pCount)
  {
       ++(*_pCount);
  }

  SharedPtr<T>& operator=(const SharedPtr<T>& ap)
  {
       if (_ptr != ap._ptr)
       {
             if (--(*_pCount) == 0)
             {
                  delete _ptr;
                  delete _pCount;
             }
             _ptr = ap._ptr;
             _pCount = ap._pCount;
             ++(*_pCount);
       }
       return *this;
  }
  ~SharedPtr()
  {
       if (--(*_pCount) == 0)
       {
             delete _ptr;
             delete _pCount;
             cout << "~SharedPtr()" << endl;
       }
  }

  T& operator*()
  {
       return *_ptr;
  }

  T* operator->()
  {
       return _ptr;
  }
  protected:
      T* _ptr;
      int* _pCount;
};


void TestSharedPtr()
{
      SharedPtr<int> sp1(new int(10));
      SharedPtr<int> sp2(sp1);
      sp1 = sp2;
}
```
3.但是shared_ptr会出现一个问题，就是循环引用，就会导致引用计数一直无法减到0，就会导致空间没有释放。例如如下代码：



```c++
  template<class T>
class SharedPtr;

template<class T>
struct ListNode
{
      T _data;
      SharedPtr<ListNode<T>> _next;
      SharedPtr<ListNode<T>> _prev;
  ListNode(T data)
       :_data(data)
       , _next(NULL)
       , _prev(NULL)
  {}
  };
//中间部分与上面SharedPtr代码一样
void TestSharedPtr()
{
      SharedPtr<ListNode<int>> sp1(new ListNode<int> (10));
      SharedPtr<ListNode<int>> sp2(new ListNode<int>(20));
      sp1->_next = sp2;
      sp2->_prev = sp1;
}
```


分析：

    有两个share_ptr对象sp1和sp2，刚开始sp1和sp2的引用计数都为1；
    将sp2赋值给sp1->_next的时候，sp1->_next的引用计数变为2且sp2的引用计数也变为2；将sp1赋值给sp2->_prev时，sp2->_prev的引用计数变为2且sp1的引用计数也变为2。
    又因为sp1里的_next和_prev两个指针的释放依赖于sp1，而sp1的释放又依赖于sp2->_prev，sp2的_prev的释放又依赖于sp2，sp2又依赖于sp1的_next的释放，这就是我的释放依赖于你，你的释放依赖于我，就会导致陷入死循环中，导致空间没有被释放，进而就会产生内存泄露的问题。
    这里写图片描述
    4.shared_ptr采用weak_ptr解决循环引用的问题，将会出现循环引用的shared_ptr通过weak_ptr的构造函数保存下来，并且weak_ptr里面不增加引用计数。但是它不是严格意义上的智能指针，它是辅助shared_ptr的使用，为了解决shared_ptr循环引用的问题。



    template<class T>
    class WeakPtr
    {
    public:
          WeakPtr(SharedPtr<T> sp)
               :ptr(sp._ptr)
          {}
    WeakPtr(const WeakPtr<T>& sp)
           :ptr(sp.ptr)
      {}
    
      WeakPtr<T>& operator=(const WeakPtr<T>& wp)
      {
           if (this != &wp)
           {
                 ptr = wp.ptr;
           }
           return *this;
      }
      protected:
          T* ptr;
    };

shared_array

1.shared_ptr用于管理单个对象的释放，而shared_array用于管理多个对象的释放。对于scoped_array来说，它不支持*和->，它支持[]的形式访问。
2.模拟实现：



```c++
  template<class T>
class SharedArray
{
public:
      SharedArray(T* ptr)
           :_ptr(ptr)
           , _pCount(new int(1))
      {}
  SharedArray(const SharedArray<T>& sa)
       :_ptr(sa._ptr)
       , _pCount(sa._pCount)
  {}

  SharedArray<T>& operator=(const SharedArray<T>& sa)
  {
       if (_ptr != sa._ptr)
       {
             if (--(*_pCount) == 0)
             {
                  delete[] _ptr;
                  delete _pCount;
             }
             _ptr = sa._ptr;
             _pCount = sa._pCount;
             ++(*_pCount);
       }
       return *this;
  }

  T& operator[](size_t pos)
  {
       return _ptr[pos];
  }

  ~SharedArray()
  {
       if (--(*_pCount) == 0)
       {
             delete[] _ptr;
             delete _pCount;
       }
  }
  protected:
      T *_ptr;
      int* _pCount;
};
```


定制删除器

1.对于C++11来说，它的库里面不包含shared_array和scoped_array，所以当new[]时，必须要依靠别的方式才能按照delete[]的形式释放。C++11和boost里面都包含定址删除器，当我以何种方式动态开辟的空间，我就要以什么样的方式去释放空间。（对于new[]就要delete[],对于fopen就要fclose，对于lock就要unlock）
2.当自己模拟实现的时候，对于shared_ptr来说，可以给它两个模板参数，一个表示指针的类型，一个表示采用何种方式删除。
3.定址删除器就是一个仿函数，通过函数对象调用重载的operator()函数，里面是delete，就调用delete，里面是delete[]就是delete[]。
4.模拟实现：
（1）首先包含仿函数，这里定义了3个仿函数，一个是专门用来进行delete，一个用来delete[]，一个用来fclose；



```C++
template<class T>
struct Delete
{
      void operator()(T* ptr)
      {
           delete ptr;
      }
};

template<class T>
struct DeleteArray
{
      void operator()(T* ptr)
      {
           delete[] ptr;
      }
};

struct Fclose
{
      void operator()(FILE* fp)
      {
           fclose(fp);
      }
};
```

（2）前面实现的SharedPtr进一步改进，增加一个模板参数，用来管理指针的释放。增加一个模板参数D，给一个缺省参数为Delete，当我们不适用第二个模板参数表示采用delete的方式，当我们给定第二个模板参数之后，我们使用哪个模板参数，就调用哪个仿函数。



```c++
template<class T,class D = Delete<T>>
class SharedPtr
{
      friend class WeakPtr<T>;
public:
		SharedPtr(T* ptr)
           :_ptr(ptr)
           , _pCount(new int(1))
      {}  
	
		SharedPtr(T* ptr, D d)
       :_ptr(ptr)
       , _d(d)
       , _pCount(new int(1))
  		{}

  SharedPtr(const SharedPtr<T,D>& ap,D d)
       :_ptr(ap._ptr)
       , _pCount(ap._pCount)
       , _d(d)
  {
       ++(*_pCount);
  }

  SharedPtr<T, D>& operator=(const SharedPtr<T, D>& ap)
  {
       if (_ptr != ap._ptr)
       {
             if (--(*_pCount) == 0)
             {
                  _d(_ptr);     //_d为仿函数对象，通过()就可以调用对应的函数
                  delete _pCount;
             }
             _ptr = ap._ptr;
             _pCount = ap._pCount;
             ++(*_pCount);
       }
       return *this;
  }

  ~SharedPtr()
  {
       if (--(*_pCount) == 0)
       {
             if (_ptr)
             {
                  _d(_ptr);
                  delete _pCount;
                  cout << "~SharedPtr()" << endl;
             }
       }
  }

  T& operator*()
  {
       return *_ptr;
  }

  T* operator->()
  {
       return _ptr;
  }
protected:
      T* _ptr;
      int* _pCount;
      D _d;
};

void TestSharedPtr()
{
      DeleteArray<string> da;
      SharedPtr<string,DeleteArray<string>> sp(new string[10],da);
      SharedPtr<int> sp1(new int(10));
      SharedPtr<string, DeleteArray<string>> sp2(new string[20]);
      /*SharedPtr<FILE, Fclose>  sp2(fopen("text.txt", "r"), Fclose());
      SharedPtr<FILE, Fclose>  sp3(fopen("text.txt", "w"));*/
}
```


    

————————————————
版权声明：本文为CSDN博主「Nicole  xu」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/xu1105775448/article/details/80627371