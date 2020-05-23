# C++11 多线程std:: async与std::thread的区别

1. std::async与std::thread的区别

std::async()与std::thread()最明显的不同，就是async并不一定创建新的线程

std::thread() 如果系统资源紧张，那么可能创建线程失败，整个程序可能崩溃。

std::thread()创建线程的方式，如果线程返回值，你想拿到这个值也不容易；

std::async()创建异步任务，可能创建也可能不创建线程；并且async调用方式很容易拿到线程入口函数的返回值。

由于系统资源限制：

（1）如果使用std::thread()创建的线程太多，则可能创建线程失败，系统报告异常，崩溃；

（2）如果用std::async,一般就不会报异常崩溃，因为如果系统资源紧张导致无法创建新线程的时候，std::async这种不加额外参数的调用就不会创建新线程，而是后续谁调用了future::get()来请求结果，那么这个异步任务就运行在执行这条get()语句所在的线程上。

（3）如果你强制std::async创建新线程，那么就必须使用std::launch::async，承受的代价就是系统资源紧张时，可能程序崩溃。经验：一个程序里，线程的数量不易超过100-200，与时间片有关，详情参考操作系统。
2.2 std::async参数详谈

参数std::launch::deferred 延迟调用；参数std::launch::async 强制创建一个新线程

    如果你用std::launch::deferred来调用async会怎么样？std::launch::deferred延迟调用，延迟到future对象调用get()或者wait()的时候才执行mythread();如果不调用get()或者wait()，mythread()不会执行。
    std::launch::async：强制这个异步任务在新线程上执行，这意味着，系统必须要给我创建出新线程来运行mythread();
    std::launch::async |std::launch::deferred      这里这个 |：以为这调用async的行为可能是 创建新线程并立即执行，或者没有创建新线程并且延迟调用result.get()才开始执行任务入口函数，两者居其一。
    不带额外参数；只给一个入口函数名；默认是应该是std::launch::async |std::launch::deferred，和c)效果一致，换句话说，系统会自行决定是异步（创建新线程）还是同步（不创建新线程）方式运行

2.3 std::async不确定问题的解决

不加额外参数的std::async调用问题，让系统自行决定是否创建新的线程。

问题的焦点在于 std::future<int> result = std::async(mythread)写法，这个异步任务到底 有没有被推迟执行。

实例代码如下：

    #include<iostream>
    #include<thread>
    #include<string>
    #include<vector>
    #include<list>
    #include<mutex>
    #include<future>
    using namespace std;
     
    int mythread() //线程入口函数
    {
    	cout << "mythread start" << "threadid= " << std::this_thread::get_id() << endl; //打印线程id
     
    	std::chrono::milliseconds dura(5000); //定一个5秒的时间
    	std::this_thread::sleep_for(dura);  //休息一定时常
     
    	cout << "mythread end" << "threadid= " << std::this_thread::get_id() << endl; //打印线程id
     
    	return 5;
    }
    int main()
    {
    	cout << "main" << "threadid= " << std::this_thread::get_id() << endl;
    	std::future<int> result = std::async(mythread);//流程并不卡在这里
    	cout << "continue....." << endl;
     
    	//枚举类型
    	std::future_status status = result.wait_for(std::chrono::seconds(0));//等待一秒
    	
    	if (status == std::future_status::deferred)
    	{
    		//线程被延迟执行了，系统资源紧张
    		cout << result.get() << endl; //此时采取调用mythread()
    	}
    	else if (status == std::future_status::timeout)//
    	{
    		//超时：表示线程还没执行完；我想等待你1秒，希望你返回，你没有返回，那么 status = timeout
    		//线程还没执行完
    		cout << "超时：表示线程还没执行完!" << endl;
    	}
    	else if (status == std::future_status::ready)
    	{
    		//表示线程成功返回
    		cout << "线程成功执行完毕，返回!" << endl;
    		cout << result.get() << endl;
    	}
     
    	cout << "I love China!" << endl;
    	return 0;
    }
————————————————
版权声明：本文为CSDN博主「u012507022」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u012507022/article/details/86100716





# C++11 Multithreading – Part 9: std::async Tutorial & Example

[Varun](https://thispointer.com/author/admin/) May 5, 2017 [C++11 Multithreading – Part 9: std::async Tutorial & Example](https://thispointer.com/c11-multithreading-part-9-stdasync-tutorial-example/)2018-08-18T15:22:50+00:00[C++](https://thispointer.com/category/c/), [C++ 11](https://thispointer.com/category/c/c-11/), [c++11 Threads](https://thispointer.com/category/c/c-11/c11-threads/), [Multithreading](https://thispointer.com/category/java/multithreading-java/) [4 Comments](https://thispointer.com/c11-multithreading-part-9-stdasync-tutorial-example/#comments)

In this article we will discuss how to execute tasks asynchronously with std::async in C++11.

std::async is introduced in c++11.

## what is std::async()

**std::async()** is a function template that accepts a  callback(i.e. function or function object) as an argument and  potentially executes them asynchronously.

 

| 1 			2 | template <class Fn, class... Args> 			future<typename result_of<Fn(Args...)>::type> async (launch policy, Fn&& fn, Args&&... args); |
| --------------- | ------------------------------------------------------------ |
|                 |                                                              |

**std::async** returns a **std::future,** that stores the value returned by function object executed by **std::async()**. Arguments expected by function can be passed to std::async() as arguments after the function pointer argument.

First argument in std::async is launch policy, it control the  asynchronous behaviour of std::async. We can create std::async with 3  different launch policies i.e.

- std::launch::async
  - It guarantees the asynchronous behaviour i.e. passed function will be executed in seperate thread.
- std::launch::deferred
  - Non asynchronous behaviour i.e. Function will be called when other thread will call get() on future to access the shared state.
- std::launch::async | std::launch::deferred
  - Its the default behaviour. With this launch policy it can run  asynchronously or not depending on the load on system. But we have no  control over it.

If we do not specify an launch policy. Its behaviour will be similar to **std::launch::async | std::launch::deferred**.

We are going to use std::launch::async launch policy in this article.

We can pass any callback in std::async i.e.

- Function Pointer
- Function Object
- Lambda Function

Let’s understand the need of std::async by an example,

## Need of std::async()

Suppose we have to fetch some data (string) from DB and some from  files in file-system. Then I need to merge both the strings and print.

In a single thread we will do like this,

```cpp
#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <future>
 
using namespace std::chrono;
 
std::string fetchDataFromDB(std::string recvData) {
  //确保函数要5秒才能执行完成
  std::this_thread::sleep_for(seconds(5));
 
  //处理创建数据库连接、获取数据等事情
  return "DB_" + recvData;
}
 
std::string fetchDataFromFile(std::string recvData) {
  //确保函数要5秒才能执行完成
  std::this_thread::sleep_for(seconds(5));
 
  //处理获取文件数据
  return "File_" + recvData;
}
 
int main() {
  //获取开始时间
  system_clock::time_point start = system_clock::now();
 
  std::future<std::string> resultFromDB = std::async(std::launch::async, fetchDataFromDB, "Data");
 
  //从文件获取数据
  std::string fileData = fetchDataFromFile("Data");
 
  //从DB获取数据
  //数据在future<std::string>对象中可获取之前，将一直阻塞
  std::string dbData = resultFromDB.get();
 
  //获取结束时间
  auto end = system_clock::now();
 
  auto diff = duration_cast<std::chrono::seconds>(end - start).count();
  std::cout << "Total Time taken= " << diff << "Seconds" << std::endl;
 
  //组装数据
  std::string data = dbData +  " :: " + fileData;
 
  //输出组装的数据
  std::cout << "Data = " << data << std::endl;
 
  return 0;
}
```

**Output:**

 

```
std::future<std::string> resultFromDB = std::async(std::launch::async, fetchDataFromDB, "Data"); 
// Do Some Stuff 			  		
//Fetch Data from DB 		
// Will block till data is available in future<std::string> object. 			
std::string dbData = resultFromDB.get();
```



As both the functions **fetchDataFromDB()** & **fetchDataFromFile()** takes 5 seconds each and are running in a single thread so, total time consumed will be 10 seconds.

Now as fetching data from DB and file are independent of each other and also time consuming. So, we can run them in parallel.
 One way to do is create a new thread pass a promise as an argument to  thread function and fetch data from associated std::future object in  calling thread.

The other easy way is using std::async.

## Calling std::async with function pointer as callback

Now let’s modify the above code and call fetchDataFromDB() asynchronously using std::async() i.e.

 

**std::async() does following things,**

- It automatically creates a thread (Or picks from internal thread pool) and a promise object for us.
- Then passes the std::promise object to thread function and returns the associated std::future object.
- When our passed argument function exits then its value will be set  in this promise object, so eventually return value will be available in  std::future object.

Now change the above example and use std::async to read data from DB asyncronously i.e.

Checkout the compete example as follows,

 

```
#include <chrono>
#include <future>
#include <iostream>
#include <string>
#include <thread>

using namespace std::chrono;
std::string fetchDataFromDB(std::string recvdData)
{
    // Make sure that function takes 5 seconds to complete
    std::this_thread::sleep_for(seconds(5));
    //Do stuff like creating DB Connection and fetching Data
    return "DB_" + recvdData;
}

std::string fetchDataFromFile(std::string recvdData)
{
    // Make sure that function takes 5 seconds to complete
    std::this_thread::sleep_for(seconds(5));
    //Do stuff like fetching Data File
    return "File_" + recvdData;
}

int main()
{
    // Get Start Time
    system_clock::time_point start = system_clock::now();
    std::future<std::string> resultFromDB = std::async(std::launch::async, fetchDataFromDB, "Data");
    //Fetch Data from File
    std::string fileData = fetchDataFromFile("Data");
    //Fetch Data from DB
    // Will block till data is available in future<std::string> object.
    std::string dbData = resultFromDB.get();
    // Get End Time
    auto end = system_clock::now();
    auto diff = duration_cast<std::chrono::seconds>(end - start).count();
    std::cout << "Total Time Taken = " << diff << " Seconds" << std::endl;
    //Combine The Data
    std::string data = dbData + " :: " + fileData;
    //Printing the combined Data
    std::cout << "Data = " << data << std::endl;
    return 0;
}
```

Now it will take 5 seconds only.

**Output:**

 

| 1 			2 | Total Time Taken = 5 Seconds 			Data = DB_Data :: File_Data |
| --------------- | ------------------------------------------------------------ |
|                 |                                                              |

 

##  Calling std::async with Function Object as callback

 

 

| 1 			2 			3 			4 			5 			6 			7 			8 			9 			10 			11 			12 			13 			14 			15 			16 			17 | /* 			* Function Object 			*/ 			struct DataFetcher 			{ 			std::string operator()(std::string recvdData) 			{ 			// Make sure that function takes 5 seconds to complete 			std::this_thread::sleep_for (seconds(5)); 			//Do stuff like fetching Data File 			return "File_" + recvdData; 			  		} 			}; 			  		//Calling std::async with function object 			std::future<std::string> fileResult = std::async(DataFetcher(), "Data"); |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |

 

## Calling std::async with Lambda function as callback

 

 

| 1 			2 			3 			4 			5 			6 			7 			8 | //Calling std::async with lambda function 			std::future<std::string> resultFromDB = std::async([](std::string recvdData){ 			  		std::this_thread::sleep_for (seconds(5)); 			//Do stuff like creating DB Connection and fetching Data 			return "DB_" + recvdData; 			  		}, "Data"); |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |

ps:

async 相当于又对promise/future封装了一层, 来让写代码/看代码更舒服