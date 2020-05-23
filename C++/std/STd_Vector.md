# std::vector



 vector是C++标准模板库中的部分内容，它是一个多功能的，能够操作多种数据结构和算法的模板类和函数库。vector之所以被认为是一个容器，是因为它能够像容器一样存放各种类型的对象，简单地说，vector是一个能够存放任意类型的动态数组，能够增加和压缩数据。
 为了可以使用vector，必须在你的头文件中包含下面的代码：
 \#include <vector>
 vector属于std命名域的，因此需要通过命名限定，如下完成你的代码：
 using std::vector;
 vector<int> vInts;
  或者连在一起，使用全名：
 std::vector<int> vInts;
  
    建议使用全局的命名域方式：usingnamespace std;     
 函数 
 表述   
 c.assign(beg,end)
 c.assign(n,elem) 将[beg; end)区间中的数据赋值给c。
 将n个elem的拷贝赋值给c。   
 c.at(idx) 传回索引idx所指的数据，如果idx越界，抛出out_of_range。   
 c.back() 传回最后一个数据，不检查这个数据是否存在。   
 c.begin() 传回迭代器中的第一个数据地址。   
 c.capacity() 返回容器中不用扩充容量能存储的数据个数。   
 c.clear() 移除容器中所有数据。   
 c.empty() 判断容器是否为空。   
 c.end() 指向迭代器中的最后一个数据的下一个地址。   
 c.erase(pos)
 c.erase(beg,end) 删除pos位置的数据，传回下一个数据的位置。
 删除[beg,end)区间的数据，传回下一个数据的位置。   
 c.front() 传回第一个数据。   
 get_allocator 使用构造函数返回一个拷贝。   
 c.insert(pos,elem) 
 c.insert(pos,n,elem)
 c.insert(pos,beg,end) 在pos位置插入一个elem拷贝，传回新数据位置。
 在pos位置插入n个elem数据。无返回值。
 在pos位置插入在[beg,end)区间的数据。无返回值。   
 c.max_size() 返回容器中最大数据的数量。   
 c.pop_back() 删除最后一个数据。   
 c.push_back(elem) 在尾部加入一个数据。   
 c.rbegin() 传回一个逆向队列的第一个数据。   
 c.rend() 传回一个逆向队列的最后一个数据的下一个位置。   
 c.resize(num) 重新指定队列的长度。   
 c.reserve() 保留适当的容量。   
 c.size() 返回容器中实际数据的个数。   
 c1.swap(c2) 
 swap(c1,c2) 将c1和c2元素互换。
 同上操作。   
 vector<Elem> c
 vector<Elem> c1(c2)
 vector <Elem> c(n)
 vector <Elem> c(n, elem)
 vector <Elem> c(beg,end)
 c.~ vector <Elem>() 创建一个空的vector。
 复制一个vector。
 创建一个vector，含有n个数据，数据均已缺省构造产生。
 创建一个含有n个elem拷贝的vector。
 创建一个以[beg;end)区间的vector。
 销毁所有数据，释放内存。   
   operator[] 返回容器中指定位置的一个引用。     
  

  
 创建一个vector
 vector容器提供了多种创建方法，下面介绍几种常用的。
 创建一个Widget类型的空的vector对象：
 vector<Widget> vWidgets;

 创建一个包含500个Widget类型数据的vector：
 vector<Widget> vWidgets(500);

  创建一个包含500个Widget类型数据的vector，并且都初始化为0：
 vector<Widget> vWidgets(500, Widget(0));

  创建一个Widget的拷贝：
 vector<Widget> vWidgetsFromAnother(vWidgets);

  
 向vector添加一个数据
 vector添加数据的缺省方法是push_back()。push_back()函数表示将数据添加到vector的尾部，并按需要来分配内存。例如：向vector<Widget>中添加10个数据，需要如下编写代码：
 for(int i= 0;i<10; i++)
     vWidgets.push_back(Widget(i));

 获取vector中指定位置的数据
 vector里面的数据是动态分配的，使用push_back()的一系列分配空间常常决定于文件或一些数据源。如果想知道vector存放了多少数据，可以使用empty()。获取vector的大小，可以使用size()。例如，如果想获取一个vector  v的大小，但不知道它是否为空，或者已经包含了数据，如果为空想设置为-1，你可以使用下面的代码实现：
 int nSize = v.empty() ? -1 : static_cast<int>(v.size());

  
 访问vector中的数据
 使用两种方法来访问vector。
 1、   vector::at()
 2、   vector::operator[]
 operator[]主要是为了与C语言进行兼容。它可以像C语言数组一样操作。但at()是我们的首选，因为at()进行了边界检查，如果访问超过了vector的范围，将抛出一个例外。由于operator[]容易造成一些错误，所有我们很少用它，下面进行验证一下：
 分析下面的代码：
 vector<int> v;
 v.reserve(10);
  
 for(int i=0; i<7; i++)
     v.push_back(i);
  
 try
 {
  int iVal1 = v[7]; // not bounds checked - will not throw
  int iVal2 = v.at(7); // bounds checked - will throw if out of range
 }
 catch(const exception& e)
 {
  cout << e.what();
 }

  
 删除vector中的数据
 vector能够非常容易地添加数据，也能很方便地取出数据，同样vector提供了erase()，pop_back()，clear()来删除数据，当删除数据时，应该知道要删除尾部的数据，或者是删除所有数据，还是个别的数据。
 Remove_if()算法 如果要使用remove_if()，需要在头文件中包含如下代码：：
 \#include <algorithm>

​      Remove_if()有三个参数：
 1、   iterator _First：指向第一个数据的迭代指针。
 2、   iterator _Last：指向最后一个数据的迭代指针。
 3、   predicate _Pred：一个可以对迭代操作的条件函数。
 条件函数  条件函数是一个按照用户定义的条件返回是或否的结果，是最基本的函数指针，或是一个函数对象。这个函数对象需要支持所有的函数调用操作，重载operator()()操作。remove_if()是通过unary_function继承下来的，允许传递数据作为条件。
 例如，假如想从一个vector<CString>中删除匹配的数据，如果字串中包含了一个值，从这个值开始，从这个值结束。首先应该建立一个数据结构来包含这些数据，类似代码如下：
 \#include <functional>
 enum findmodes 
 {
  FM_INVALID = 0,
  FM_IS,
  FM_STARTSWITH,
  FM_ENDSWITH,
  FM_CONTAINS
 };
 typedefstruct tagFindStr
 {
  UINT iMode;
  CString szMatchStr;
 } FindStr;
 typedef FindStr* LPFINDSTR;

  
 然后处理条件判断：
 class FindMatchingString 
     : public std::unary_function<CString, bool> 
 {
     
 public: 
  FindMatchingString(const LPFINDSTR lpFS) : m_lpFS(lpFS) {} 
     
  bool operator()(CString& szStringToCompare) const
  { 
      bool retVal = false;
  
      switch(m_lpFS->iMode) 
      {
      case FM_IS: 
        { 
          retVal = (szStringToCompare == m_lpFDD->szMatchStr); 
          break;
        }
      case FM_STARTSWITH: 
        { 
          retVal = (szStringToCompare.Left(m_lpFDD->szMatchStr.GetLength())
                == m_lpFDD->szWindowTitle);
          break;
        } 
      case FM_ENDSWITH: 
        {
          retVal = (szStringToCompare.Right(m_lpFDD->szMatchStr.GetLength()) 
                == m_lpFDD->szMatchStr);
          break; 
        } 
      case FM_CONTAINS: 
        {
          retVal = (szStringToCompare.Find(m_lpFDD->szMatchStr) != -1);
          break; 
        }
      }
         
      return retVal;
  }
         
 private: 
     LPFINDSTR m_lpFS;
 };

  
 通过这个操作你可以从vector中有效地删除数据：
 FindStr fs;
 fs.iMode = FM_CONTAINS;
 fs.szMatchStr = szRemove;
  
 vs.erase(std::remove_if(vs.begin(), vs.end(), FindMatchingString(&fs)), vs.end());

​     Remove(),remove_if()等所有的移出操作都是建立在一个迭代范围上的，不能操作容器中的数据。所以在使用remove_if()，实际上操作的时容器里数据的上面的。

 看到remove_if()实际上是根据条件对迭代地址进行了修改，在数据的后面存在一些残余的数据，那些需要删除的数据。剩下的数据的位置可能不是原来的数据，但他们是不知道的。
 调用erase()来删除那些残余的数据。注意上面例子中通过erase()删除remove_if()的结果和vs.enc()范围的数据。



# C++：如何高效的使用std::vector？



一、在std::vector尾部添加对象时应尽量使用emplace_back，而不要使用push_back

二、添加多个元素前应使用reserve设置容量，防止扩容时发生元素复制

三、删除元素时应从最后一个元素开始删除，不要从中间开始删除

四、添加新对象时应从结尾处添加，而不要从中间添加

五、使用std::vector(std::vector)和std::vector(std::initializer_list)对std::vector赋初始值会将std::vector和std::initializer_list中所有对象复制

六、需要将对象全部转移到另外一std::vector时，应使用std::vector.swap()、std::swap()、std::move(std::vector)

七、如果std::vector中在存放指针对象，即std::vector，则应使用智能指针

先说一下关于std::vector的一些基本知识：

    std::vector<T>中存放的T对象是在堆中分配的。
    std::vector<T>会负责管理T对象的生命周期，所以当将T对象存放到std::vector<T>中时，std::vector<T>会构造一个自己能完全控制的T对象，构造方式可以是转移构造函数、拷贝构造函数还是普通构造函数。
    当std::vector<T>的生命周期结束时，std::vector<T>也同时会将其中存放的对象析构。

对于如何高效使用std::vector，以下有几点建议。先给出一个类的代码，后面会用到它：

    class Girl {
     
    public:
    	string name;
    	int age;


​     
    	Girl() {
    		cout << "Girl()" << endl;
    	}
     
    	Girl(const string& _name, int _age) : name(_name), age(_age) {
    		cout << "Girl(string _name, int _age)" << name << endl;
    	}
     
    	Girl(const Girl& b) : name(b.name), age(b.age) {
    		cout << "Girl(const Girl&)" << name << endl;
    	}
     
    	Girl(Girl&& b) : name(move(b.name)), age(move(b.age)) {
    		cout << "Girl(Girl&&)" << name << endl;
    	}
     
    	Girl& operator=(const Girl& b) {
    		this->name = b.name;
    		this->age = b.age;
     
    		cout << "operator=(const Girl&)" << name << endl;
     
    		return *this;
    	}
     
    	~Girl() {
    		cout << "~Girl()" << name << endl;
    	}
     
    };

一、在std::vector<T>尾部添加对象时应尽量使用emplace_back，而不要使用push_back

    int main() {
    	vector<Girl> vvv1;
    	vector<Girl> vvv2;
     
    	cout << "------------------------------------------------" << endl;
     
    	vvv1.push_back(Girl("dd", 90));
     
    	cout << "------------------------------------------------" << endl;
     
    	vvv2.emplace_back("dd", 90);
     
    	cout << "------------------------------------------------" << endl;
     
    	return 1;
    }
    
    ------------------------------------------------
    Girl(string _name, int _age)dd
    Girl(Girl&&)dd
    ~Girl()
    ------------------------------------------------
    Girl(string _name, int _age)dd
    ------------------------------------------------
    ~Girl()dd
    ~Girl()dd

从结果中可以看到，使用push_back会比emplace_back多调了转移构造函数和析构函数，因而性能偏低。
二、添加多个元素前应使用reserve设置容量，防止扩容时发生元素复制

    int main() {
    	vector<Girl> vvv1;
     
    	cout << vvv1.size() << endl;
    	cout << vvv1.capacity() << endl;
     
    	vvv1.emplace_back("ss", 12);
    	cout << "------------------------------------------------" << endl;
    	vvv1.emplace_back("xx", 33);
    	cout << "------------------------------------------------" << endl;
    	vvv1.emplace_back("wq", 123);
     
    	cout << "------------------------------------------------" << endl;
     
    	cout << vvv1.size() << endl;
    	cout << vvv1.capacity() << endl;
    	cout << "------------------------------------------------" << endl;
     
    	vector<Girl> vvv2;
    	vvv2.reserve(10);
     
    	cout << vvv2.size() << endl;
    	cout << vvv2.capacity() << endl;
     
    	vvv2.emplace_back("ss", 12);
    	cout << "------------------------------------------------" << endl;
    	vvv2.emplace_back("xx", 33);
    	cout << "------------------------------------------------" << endl;
    	vvv2.emplace_back("wq", 123);
     
    	cout << "------------------------------------------------" << endl;
     
    	cout << vvv2.size() << endl;
    	cout << vvv2.capacity() << endl;
    	cout << "------------------------------------------------" << endl;
     
    	return 1;
    }
    
    0
    0
    Girl(string _name, int _age)ss
    ------------------------------------------------
    Girl(string _name, int _age)xx
    Girl(const Girl&)ss
    ~Girl()ss
    ------------------------------------------------
    Girl(string _name, int _age)wq
    Girl(const Girl&)ss
    Girl(const Girl&)xx
    ~Girl()ss
    ~Girl()xx
    ------------------------------------------------
    3
    3
    ------------------------------------------------
    0
    10
    Girl(string _name, int _age)ss
    ------------------------------------------------
    Girl(string _name, int _age)xx
    ------------------------------------------------
    Girl(string _name, int _age)wq
    ------------------------------------------------
    3
    10
    ------------------------------------------------
    ~Girl()ss
    ~Girl()xx
    ~Girl()wq
    ~Girl()ss
    ~Girl()xx
    ~Girl()wq

从结果中可以看到，由于vvv1没有设置reserver，导致初始容量不足，每添加一个新的对象都要先扩容，然后将以前存放的对象复制过去，因而性能偏低。
三、删除元素时应从最后一个元素开始删除，不要从中间开始删除

    int main() {
    	vector<Girl> vvv1;
    	vvv1.reserve(10);
     
    	vvv1.emplace_back("ss", 12);
    	vvv1.emplace_back("xx", 33);
    	vvv1.emplace_back("wq", 123);
     
    	cout << "------------------------------------------------" << endl;
     
    	vector<Girl> vvv2;
    	vvv2.reserve(10);
     
    	vvv2.emplace_back("ss", 12);
    	vvv2.emplace_back("xx", 33);
    	vvv2.emplace_back("wq", 123);
     
    	cout << "------------------------------------------------" << endl;
     
    	vector<Girl> vvv3;
    	vvv3.reserve(10);
     
    	vvv3.emplace_back("ss", 12);
    	vvv3.emplace_back("xx", 33);
    	vvv3.emplace_back("wq", 123);
     
    	cout << "++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
    	
    	vvv1.erase(vvv1.begin());
    	cout << "------------------------------------------------" << endl;
    	vvv1.erase(vvv1.begin());
    	cout << "++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
     
    	vvv2.erase(vvv2.end() - 1);
    	cout << "------------------------------------------------" << endl;
    	vvv2.erase(vvv2.end() - 1);
    	cout << "++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
     
    	vvv3.pop_back();
    	cout << "------------------------------------------------" << endl;
    	vvv3.pop_back();
    	cout << "++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
     
    	return 1;
    }
    
    Girl(string _name, int _age)ss
    Girl(string _name, int _age)xx
    Girl(string _name, int _age)wq
    ------------------------------------------------
    Girl(string _name, int _age)ss
    Girl(string _name, int _age)xx
    Girl(string _name, int _age)wq
    ------------------------------------------------
    Girl(string _name, int _age)ss
    Girl(string _name, int _age)xx
    Girl(string _name, int _age)wq
    ++++++++++++++++++++++++++++++++++++++++++++++++
    operator=(const Girl&)xx
    operator=(const Girl&)wq
    ~Girl()wq
    ------------------------------------------------
    operator=(const Girl&)wq
    ~Girl()wq
    ++++++++++++++++++++++++++++++++++++++++++++++++
    ~Girl()wq
    ------------------------------------------------
    ~Girl()xx
    ++++++++++++++++++++++++++++++++++++++++++++++++
    ~Girl()wq
    ------------------------------------------------
    ~Girl()xx
    ++++++++++++++++++++++++++++++++++++++++++++++++
    ~Girl()ss
    ~Girl()ss
    ~Girl()wq

从结果中可以看到，如果从中间或开头开始删除，后面的对象由于要向前移动而要调用赋值函数，运行性能偏低。这里移动的方式要注意，它是每二个对象赋值给第一个对象，第三个对象赋值给第二个对象，第三个对象析构销毁。
四、添加新对象时应从结尾处添加，而不要从中间添加

    int main() {
    	vector<Girl> vvv1;
    	vvv1.reserve(10);
     
    	vvv1.emplace_back("ss", 12);
     
    	cout << "------------------------------------------------" << endl;
    	vvv1.insert(vvv1.begin(), Girl("xx", 33));
    	
    	cout << "------------------------------------------------" << endl;
    	vvv1.insert(vvv1.begin(), Girl("wq", 123));
     
    	cout << "------------------------------------------------" << endl;
    	cout << "------------------------------------------------" << endl;
     
    	vector<Girl> vvv2;
    	vvv2.reserve(10);
     
    	vvv2.emplace_back("ss", 12);
     
    	cout << "------------------------------------------------" << endl;
    	vvv2.emplace(vvv2.begin(), "xx", 33);
     
    	cout << "------------------------------------------------" << endl;
    	vvv2.emplace(vvv2.begin(), "wq", 123);
     
    	cout << "------------------------------------------------" << endl;


​     
    	return 1;
    }
    
    Girl(string _name, int _age)ss
    ------------------------------------------------
    Girl(string _name, int _age)xx
    Girl(Girl&&)xx
    Girl(Girl&&)ss
    operator=(const Girl&)xx
    ~Girl()xx
    ~Girl()
    ------------------------------------------------
    Girl(string _name, int _age)wq
    Girl(Girl&&)wq
    Girl(Girl&&)ss
    operator=(const Girl&)xx
    operator=(const Girl&)wq
    ~Girl()wq
    ~Girl()
    ------------------------------------------------
    ------------------------------------------------
    Girl(string _name, int _age)ss
    ------------------------------------------------
    Girl(string _name, int _age)xx
    Girl(Girl&&)ss
    operator=(const Girl&)xx
    ~Girl()xx
    ------------------------------------------------
    Girl(string _name, int _age)wq
    Girl(Girl&&)ss
    operator=(const Girl&)xx
    operator=(const Girl&)wq
    ~Girl()wq
    ------------------------------------------------
    ~Girl()wq
    ~Girl()xx
    ~Girl()ss
    ~Girl()wq
    ~Girl()xx
    ~Girl()ss

从运行结果可以看到，无论是使用emplace还是insert，在插入位置后的对象都会发生移动，这样会影响性能。
五、使用std::vector(std::vector)和std::vector(std::initializer_list<T>)对std::vector赋初始值会将std::vector和std::initializer_list<T>中所有对象复制

    int main() {
     
    	cout << "------------------------------------------------" << endl;
     
    	vector<Girl> vv({ Girl("d",90), Girl("ll",80) });
     
    	cout << "------------------------------------------------" << endl;
     
    	vector<Girl> vvv1;
    	vvv1.reserve(10);
     
    	vvv1.emplace_back("ss", 12);
    	vvv1.emplace_back("xx", 33);
     
    	cout << "------------------------------------------------" << endl;
     
    	vector<Girl> vvv2(vvv1);
     
    	cout << "------------------------------------------------" << endl;


​     
    	return 1;
    }
    
    ------------------------------------------------
    Girl(string _name, int _age)d
    Girl(string _name, int _age)ll
    Girl(const Girl&)d
    Girl(const Girl&)ll
    ~Girl()ll
    ~Girl()d
    ------------------------------------------------
    Girl(string _name, int _age)ss
    Girl(string _name, int _age)xx
    ------------------------------------------------
    Girl(const Girl&)ss
    Girl(const Girl&)xx
    ------------------------------------------------
    ~Girl()ss
    ~Girl()xx
    ~Girl()ss
    ~Girl()xx
    ~Girl()d
    ~Girl()ll

通过运行结果可以看到，当初始化std::vector时，对象双被复制了一份。通过初始化的方式无法将对象在多个集合中共享。如果像让std::vector中的所有对象暴露出来，可以使用T* std::vector.data()，它会返回std::vector中所包含的对象的指针。
六、需要将对象全部转移到另外一std::vector时，应使用std::vector.swap()、std::swap()、std::move(std::vector)

    int main() {
    	{
    		cout << "------------------------------------------------" << endl;
     
    		vector<Girl> vvv1;
    		vvv1.reserve(10);
     
    		vvv1.emplace_back("ss", 12);
    		vvv1.emplace_back("xx", 33);
    		vvv1.emplace_back("wq", 123);
     
    		cout << "------------------------------------------------" << endl;
     
    		vector<Girl> vvv2 = move(vvv1);
    		cout << "------------------------------------------------" << endl;
    	}
    	{
    		cout << "------------------------------------------------" << endl;
     
    		vector<Girl> vvv1;
    		vvv1.reserve(10);
     
    		vvv1.emplace_back("ss", 12);
    		vvv1.emplace_back("xx", 33);
    		vvv1.emplace_back("wq", 123);
     
    		cout << "------------------------------------------------" << endl;
     
    		vector<Girl> vvv2;
    		vvv2.swap(vvv1);
    		cout << "------------------------------------------------" << endl;
    	}
    	{
    		cout << "------------------------------------------------" << endl;
     
    		vector<Girl> vvv1;
    		vvv1.reserve(10);
     
    		vvv1.emplace_back("ss", 12);
    		vvv1.emplace_back("xx", 33);
    		vvv1.emplace_back("wq", 123);
     
    		cout << "------------------------------------------------" << endl;
     
    		vector<Girl> vvv2;
    		swap(vvv1, vvv2);
    		cout << "------------------------------------------------" << endl;
    	}
     
    	return 1;
    }

 


    ------------------------------------------------
    Girl(string _name, int _age)ss
    Girl(string _name, int _age)xx
    Girl(string _name, int _age)wq
    ------------------------------------------------
    ------------------------------------------------
    ~Girl()ss
    ~Girl()xx
    ~Girl()wq
    ------------------------------------------------
    Girl(string _name, int _age)ss
    Girl(string _name, int _age)xx
    Girl(string _name, int _age)wq
    ------------------------------------------------
    ------------------------------------------------
    ~Girl()ss
    ~Girl()xx
    ~Girl()wq
    ------------------------------------------------
    Girl(string _name, int _age)ss
    Girl(string _name, int _age)xx
    Girl(string _name, int _age)wq
    ------------------------------------------------
    ------------------------------------------------
    ~Girl()ss
    ~Girl()xx
    ~Girl()wq

通过运行结果可以看到，转移的过程只是更改了指针的指向，没有发生任何复制或拷贝。
七、如果std::vector中在存放指针对象，即std::vector<T*>，则应使用智能指针

    std::vector<std::unique_ptr<T>>
    
    std::vector<std::shared_ptr<T>>

因为如果std::vector中存放指针，指针指向的对象并不受std::vector管理，所以需要智能指针帮助管理这些对象。
--------------------- 
作者：netyeaxi 
来源：CSDN 
原文：https://blog.csdn.net/netyeaxi/article/details/83277810 
版权声明：本文为博主原创文章，转载请附上博文链接！
