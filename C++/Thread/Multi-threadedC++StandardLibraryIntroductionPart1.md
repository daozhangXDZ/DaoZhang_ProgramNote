# C++标准库多线程简介Part1

**Part1:线程与互斥量**

本篇文章将简单的介绍一下C++的标准线程库，本篇内容十分基础，如果你有C++多线程相关的使用经验或者知识，就不必在这篇文章上浪费时间了...

**如果你认为本篇文章对你有帮助，请点赞！！！**

## **1.进程与线程**

在介绍标准库多线程之前，需要先介绍一下进程与线程的概念与它们之间的差别。

进程是被执行的应用程序(程序即指令(code)与数据(data)的集合)的实例(可以启动多个相同的应用程序，它们是不同的进程)，同时也是系统资源分配的最小单位(虚拟地址空间等资源，见下图)，一个进程中可以包含多个线程。

![img](Multi-threaded C ++ Standard Library Introduction Part1.assets/v2-e4083befea6eee2a3b117c9a7b11dfc8_hd.jpg)操作系统会为每个进程分配一定的虚拟地址空间，该虚拟地址空间由进程独享

线程则是CPU进行运算调度的最小单位。线程被包含在进程之中，是进程中的实际运作单位。一个进程中可以包含多个线程，这些线程可以同时执行不同的任务(例如一个线程监听用户输入，一个线程执行IO任务，它们是同时进行互相独立的)。同一个进程中的多个线程共享操作系统为该进程分配的系统资源(如虚拟地址空间，信号量等...)，但同时多个线程又独立的拥有各自的调用栈，寄存器环境，和线程本地存储(thread-local storage)。

一个操作系统中可以有多个进程，这些进程可以异步(同时)或同步(顺序)执行，操作系统为这些进程分配独立的系统资源。而进程中又可以拥有多个线程(至少一个)，这些线程共享进程的系统资源，线程又被称为轻量级的进程。

## **2.并发与并行**

并发与并行对于初学者来说是很难区分的两种概念。

并发是指的是在一个重叠的时间段内，有多个任务(两个以上的task)可以被启动，执行或者完成，但是这并不意味着，这些任务必须在这一时间段内的某一时刻同时被运行。比如在一个拥有单核CPU上计算机上，我们可以同时运行浏览器和文档编辑器程序，却并不会感受到任何操作上的延迟。这是因为操作系统采用了时间片轮转算法(**Round-Robin，RR**)，操作系统中的每个进程被分配了一定的时间段(时间片)，操作系统将CPU分配给某一进程让其在处理器上执行一个时间片。当进程占用CPU的时间超过时间片的时间后，将由计时器发起中断请求，随后操作系统保存该进程的执行状态并将其挂起，然后将CPU分配给另一个进程执行一个时间片。由于时间片划分的很短，而且进程间的切换(进程间的切换也被称为上下文切换Context switch)也很快，所以会给人一种好像多个进程在同时执行的错觉。(在进行context  switch的时候也会占用一定的时间，需要保存将被挂起的进程的执行状态，还需要把将要执行的进程的指令与内存载入到缓存中，在这期间CPU无法执行其他指令，因而过多的context switch会降低CPU的效率。)

![img](Multi-threaded C ++ Standard Library Introduction Part1.assets/v2-1aabf12e0ccd3624fc1ef4d112f10973_hd.png)在单核CPU上同时运行进程A(红色)与进程B(蓝色)，灰色为Context switch所占用的CPU时间

并行是指在同一时刻有多个任务同时运行。比如在一个双核的CPU上，在A核心上运行浏览器进程，而在B核心上运行文档编辑器进程，在两个核心上运行的进程相互独立，同时运行(多进程并发)。又比如在一个游戏进程中，可以同时存在一个逻辑线程(处理游戏逻辑)和一个IO线程(处理IO任务)，它们可以同时运行在两个不同的CPU核心上(多线程并发)。(并发的概念是包含并行的，并行是多线程的一种形式，多线程是并发的一种形式。)

使用多进程并发时，进程的创建与销毁速度都比较慢，而且进程间的通信也比较复杂(需要通过套接字，管道等..)，但是操作系统会在进程间提供附加的保护机制，这可以我们更容易写出并发安全的代码。而使用多线程并发时，线程的创建与销毁速度则要更快，由于同一进程中的所有线程共享虚拟地址空间，因此线程间的通信开销要小得多，但由于缺少线程间的数据保护，可能会出现多个线程同时读写同一数据造成的数据不一致现象。

在C++11标准中引入了对于线程的支持，而本篇文章的主要内容就与多线程并发相关。

## **3.C++11中的线程**

C++11中thread与thread id的定义如下：

```cpp
//thread 定义
class thread {
	class id;

	// native_handle_type 是连接 thread 类和操作系统 SDK API 之间的桥梁。
	typedef implementation - dependent native_handle_type;

	// 构造与析构
	thread() noexcept;
	template<class F, class… Args> explicit thread(F&f, Args&&… args);
	~thread();
	thread(const thread&) = delete;
	thread(thread&&) noexcept;
	thread& operator=(const thread&) = delete;
	thread& operator=(thread&&) noexcept;
	//
	void swap(thread&) noexcept;
	bool joinable() const noexcept;
	void join();
	void detach();
	//获取线程id
	id get_id() const noexcept;
	// 获取物理线程数目
	static unsigned hardware_concurrency() noexcept;
        //获取底层实现定义的线程句柄 
	native_handle_type native_handle();

	//thread id定义
	class id {
		id() noexcept;
		// 可以由==, < 两个运算衍生出其它大小关系运算。
		bool operator==(thread::id x, thread::id y) noexcept;
		bool operator<(thread::id x, thread::id y) noexcept;
		// !=, <=, >=, >...
		template<class charT, class traits>
		basic_ostream<charT, traits>&
			operator<<(basic_ostream<charT, traits>&out, thread::id id);
	};
}
```

首先std::thread类的对象是只能够被移动(move，移动构造，移动赋值)，而不能被拷贝(copy，拷贝构造，拷贝赋值)的。其次thread类存在一个无参的默认构造函数，与一个接受可调用对象与可调用对象参数的构造函数。thread类内也定义了一个id类，id类可以表示线程在操作系统内的唯一标志符，它重载了多个比较运算符还有输出运算符。id类也可以表示线程运行状态，它的默认值(thread::id()，构造函数)不表示任何执行中的线程。如果一个thread类的实例，其get_id方法返回的id与id类的默认值相等，则该线程实例处于一下状态之一：

- 尚未指定运行的任务
- 线程运行完毕
- 线程已经被转移 (move) 到另外一个线程类实例
- 线程已经被分离 (detached)

thread类中还定义了nativehandle方法，可以返回对应平台的线程句柄(如linux中pthread的pthread_t)，在我们需要使用一些原生线程支持而std::thread不支持的功能上，这个方法会比较有用(比如设置线程的优先级)。

thread类的hardware_concurrency静态方法可以返回当前处理器所支持的最大并发线程数(比如我现在正在使用的e3-1230v3，hardware_concurrency的返回值为8)。

线程的移动操作只是改变了线程实例的id，线程的swap操作也是通过移动操作实现的。

**3.1线程的管理**

之前内容提到了一个进程中至少存在一个线程，这个线程被称为主线程，我们可以在任意线程中创建线程类的实例。每个线程都需要一个入口函数，当入口函数返回时，线程就会退出，主线程的入口函数为main()。

**a.线程的启动**

线程的创建十分简单，我们只需创建一个线程类的实例，并为它传入一个可调用对象，就可以启动一个线程了：

```cpp
void do_work()
{
	std::cout << "work done" << std::endl;
}

void test()
{
	std::thread worker(do_work);
	worker.detach();
}
```

这里的可调用对象可以是lambda表达式，std::function，也可以是重载了调用运算符的类，或者成员函数或普通函数：

```cpp
class Work
{
public:
	void operator()()
	{
		std::cout << "callable object" << std::endl;
	}
};

void test()
{
	std::thread worker0([]() {
		std::cout << "lambda call" << std::endl;
	});
	worker0.detach();

	std::thread worker1(Work{});
	worker1.detach();
}
```

也可以在线程的构造函数中传入可调用对象的参数，此时线程构造函数的第一个参数为可调用对象，此后的参数为可调用对象的参数：

```cpp
class Work
{
public:
	void operator()(int id)
	{
		std::cout << "work id:" << id << std::endl;
	}
};

void test()
{
	std::thread worker(Work{}, 0);
	worker.join();
}
```

如果传入的可调用对象是某个类的成员函数，则线程构造函数的第一个参数为该类型的成员函数指针，第二个参数为指向该类型的实例的指针，其后为成员函数的参数：

```cpp
class Sampler
{
public:
	void sample(int random)
	{
		std::cout << "sample with:" << random << std::endl;
	}
};

void test()
{
	Sampler obj;
	std::thread worker(&Sampler::sample, &obj, 0);
	worker.join();
}
```

在向线程中传递参数时需要注意的一点是：默认情况下会将传递的参数拷贝到线程的独立内存中，即使传入参数的类型为引用，但是可以使用std::ref将参数传递的方式更改为引用。

```cpp
void test()
{
	int work_id = 1;

	std::thread worker([](int &id) {
		std::cout << "do work:" << id << std::endl;
	}, std::ref(work_id));
	work_id = 2;

	worker.join();
}
```

**b.等待线程完成或分离线程**

在启动一个线程后，必须在线程相关联的std::thread对象销毁之前，决定以何种方式等待线程结束(等待线程执行结束(join)还是让其自主运行(detach))。如果在std::thread对象销毁前，还没有作出决定那么在std::thread对象的析构函数中就会触发std::terminate导致进程终止，如下所示：

```cpp
void test()
{
	{
		std::thread worker([]() {
			std::cout << "do work:" << std::endl;
		});
		//错误，未调用线程的join或者detach函数，会导致进程被终止
	}
}
```

即使在有异常的情况下也必须保证线程能够被正确的被detach或join:

```cpp
void test()
{
	std::thread worker(do_work);
	try
	{
		error_fun();
	}
	catch (const std::exception&)
	{
		worker.join();
		throw;
	}
	worker.join();
}
```

也可以使用RAII(资源获取即初始化，Resource Acquisition Is Initialization)的方式保证线程可以被正确的join：

```cpp
class ThreadGuard
{
	std::thread &m_thread;
public:
	explicit ThreadGuard(std::thread &t) : m_thread(t) {}
	~ThreadGuard()
	{
		if (m_thread.joinable())
		{
			m_thread.join();
		}
	}

	ThreadGuard(ThreadGuard	const&) = delete;
	ThreadGuard &operator=(ThreadGuard	const&) = delete;
};

void test()
{
	{
		std::thread worker(do_work);
		ThreadGuard guard(worker);
	}
}
```

当在某一线程调用另一个线程对象的join方法时，调用join的线程就会被阻塞，直到被调用的线程执行完毕，调用join的线程才能继续执行，如下所示，若在主线程调用test函数，主线程在调用worker线程的join方法后，会一直等待worker线程执行完毕后才会继续执行输出语句:

```cpp
void test()
{
	std::thread worker(do_work);
	worker.join();
	std::cout << "test done" << std::endl;
}
```

如果不想等待线程运行结束(比如一个在后台进行垃圾回收的线程)，那么就可以调用detach使被调用的线程在后台自主运行，而调用detach的线程则不会等待被调用线程执行结束，会直接继续执行。如下所示，执行test函数的线程在调用worker线程的detach方法后继续执行，输出"test exit"，而worker线程会休眠2秒后才会输出"awakening"，因此"test exit"会在"awakening"之前输出：

```cpp
void sleep()
{
	using namespace std::chrono_literals;
	std::this_thread::sleep_for(2s);
	std::cout << "awakening" << std::endl;
}

void test()
{
	std::thread worker(sleep);
	worker.detach();
	std::cout << "test exit" << std::endl;
}
```

使用detach时一定要注意，如果被调用detach的线程使用了调用detach线程的局部变量，那么在局部变量生命周期结束后，若被调用detach的线程还试图访问该局部变量时，就会出现错误：

```cpp
void test()
{
	size_t length = 10;
	int *value = new int [length];
	for (size_t i = 0; i < length; i++)
	{
		value[i] = i;
	}

	std::thread worker([&]() {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(5s);
		for (size_t i = 0; i < length; i++)
		{
			//会出现悬空指针
			std::cout << value[i] << std::endl;
		}
	});
	worker.detach();
	//局部变量已经被释放
	delete[] value;
	std::cout << "test exit" << std::endl;
}
```

对于一个std::thread对象，只能对其调用一次join或者detach，被调用join后就无法再次调用join或者detach，同样被调用detach后也无法再次被调用join或者detach。可以使用std::thread的joinable方法判断std::thread对象是否时可以被join的，对一个std::thread对象在如下几种情况下joinable方法会返回false:

- 空线程(在构造没有附加任何运行任务)
- 已经被调用join方法的线程
- 已经被调用detach方法的线程
- 已经被move的线程

**c.线程所有权的转移**

之前提到std::thread对象是只可以被move，而不能被copy的。可以通过move，转移线程的所有权：

```cpp
void test()
{
	std::thread thread0(task);
	//显式调用move方法，转移线程所有权
	std::thread thread1 = std::move(thread0);

	std::thread thread2;
	//对于临时对象，隐式地调用move，转移线程所有权
	thread2 = std::thread(task);

	thread1.join();
	thread2.join();
}
```

被move后的std::thread对象将不再代表执行线程，也无法再被join或者detach。

借助与move操作，我们可以在函数间，或者容器中转移线程的所有权：

```cpp
void test()
{
	std::vector<std::thread> workers;
	for (size_t i = 0; i < 4; i++)
	{
		//被创建出的线程的所有权被转移到vector容器中
		workers.push_back(std::thread(task));
	}

	for (auto &t : workers)
	{
		t.join();
	}
}
```

**d.线程的调度**

标准库中出了std::thread和id定义外，还有定义了一个std::this_thread命名空间：

```cpp
namespace this_thead {
	thread::id get_id();
	void yield();
	template<class Clock, class Duration>
	void sleep_until(const chrono::time_point<Clock, Duration>& abs_time);
	template<class Rep, class Period>
	void sleep_for(const chromo::duration<Rep, Period>& rel_time);
}
```

通过getid方法可以获得当前线程的id，而yield，sleep_until和sleep_for方法则可以用于线程的调度。

调用yield方法会使操作系统重新调度当前线程，并允许其他线程运行一段时间。yield函数的准确行为依赖于具体实现，特别是使用中的 OS 调度器机制和系统状态。[例如，先进先出实时调度器（ Linux 的SCHED_FIFO）将悬挂当前线程并将它放到准备运行的同优先级线程的队列尾（而若无其他线程在同优先级，则yield无效果）](https://link.zhihu.com/?target=https%3A//zh.cppreference.com/w/cpp/thread/yield)。

sleep_for则是将当前线程阻塞一定时间段后唤醒，而sleep_until则是阻塞当前线程直至某一时间点后将当前线程唤醒：

```cpp
void test()
{
	std::thread thread_a([]() {
		using namespace std::chrono_literals;
		//线程a将被阻塞2s
		std::this_thread::sleep_for(2s);
	});

	using namespace std::chrono_literals;
	auto time_point = std::chrono::steady_clock::now() + 10s;
	std::thread thread_b([=]() {
		//线程b将被阻塞，并在10s后被唤醒
		std::this_thread::sleep_until(time_point);
	});

	thread_a.join();
	thread_b.join();
}
```

## **4.C++11中的互斥量与锁管理**

**4.1数据竞争(Data race)**

同一进程中的线程共享虚拟地址空间，这一特性为我们带来便利的同时，也会产生一些麻烦，特别是在多个线程共享数据时。如果多个线程以只读的方式共享数据，那么和单线程访问数据的情况没有什么不同，多个线程访问到的数据都是一致的。但是如果在多个线程同时读写共享数据时，共享数据的一致性就会被破坏，这种情况也被称为data race。

在下面的例子中线程a和b共享person变量，a线程对person数据进行修改，同时b线程读取并输出person数据。由于两个线程是同时运行的，所以可能出现a线程刚刚把person数据的age成员修改为Dio Brando的age，而同时b线程刚刚输出了Jonathan Joestar的名字，正准备读取Jonathan  Joestar的age时却读到了Dio Brando的age，这里就出现了数据的不一致，线程b读取到的person数据既不是Jonathan  Joestar的也不是Dio Brando的(或者说一半是Jonathan Joestar的，另一半是Dio  Brando的)，这种情况就是data race，是我们必须要尽量避免的。下面的程序可能输出为Jonathan Joestar, 121, 0。

```cpp
struct Person
{
	std::string m_name;
	int m_age;
	int m_gender;
};

void test()
{
	Person person{ "Jonathan Joestar", 21, 0};

	std::thread thread_a([&](){
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(10ns);
		person.m_name = "Dio Brando";
		person.m_age = 121;
		person.m_gender = 0;
		});

	std::thread thread_b([&]() {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(10ns);
		std::cout << person.m_name << ", " << person.m_age << ", " << person.m_gender;
	});

	thread_b.join();
	thread_a.join();
}
```

**4.2使用互斥量保护共享数据**

为了保持共享数据的一致性，我们可以采用c++标准库提供的互斥量(std::mutex,  std::recursive_mutex等..)对共享数据进行保护。(一般来说互斥量同一时刻只能被一个线程锁定，在互斥量已经被锁定的情况下，其他线程尝试锁定互斥量就会被阻塞。不过也有一些特殊的互斥量可以同时被多个线程锁定。在之后的内容中锁与互斥量为同义词)

C++标准库中提供的互斥量一般都有定义lock，unlock，trylock三个方法。这里以std::mutex为例做说明。

- 使用std::mutex的lock方法可以在调用lock的线程上锁住互斥量，若互斥量已被其他线程上锁，则当前调用lock的线程将被阻塞，直其他占有互斥量的线程解锁互斥量使得当前线程获得互斥量。对std::mutex来说，在已经占有互斥量的线程上调用lock方法是未定义行为。
- std::mutex的unlock方法可以解锁当前线程占有的互斥量，若在未占有互斥量的线程上调用unlock则为未定义行为。
- std::mutex的trylock方法可以尝试锁定互斥量，若成功锁定互斥量则返回true，否则返回false。在已经占有互斥量的线程上调用trylock为未定义行为。在互斥量未被任何线程锁定的情况下，此函数也可能会返回false。

在调用std::mutex的lock方法锁定互斥量后一定要记得在不需要占有互斥量的时候调用unlock解锁互斥量，否则其他任何想要获取锁的线程都会被阻塞，此时多线程就可能会退化成为单线程。占有  std::mutex的线程在std::mutex对象销毁前未调用其unlock方法则为未定义行为，且std::mutex对象不可复制也不可移动。

4.1中提到的例子可以使用std::mutex来保证共享数据的一致性：

```cpp
void test()
{
	Person person{ "Jonathan Joestar", 21, 0};
	std::mutex mutex;

	std::thread thread_a([&](){
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(10ns);
		//锁住互斥量
		mutex.lock();
		person.m_name = "Dio Brando";
		person.m_age = 121;
		person.m_gender = 0;
		//解锁互斥量
		mutex.unlock();
		});

	std::thread thread_b([&]() {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(10ns);
		//锁住互斥量
		mutex.lock();
		std::cout << person.m_name << ", " << person.m_age << ", " << person.m_gender;
		//解锁互斥量
		mutex.unlock();
	});

	thread_b.join();
	thread_a.join();
}
```

上面的代码在使用锁的情况下，只存在两种情况：

- 线程a获取锁，修改数据，修改完毕后解锁互斥量，若线程b在此期间调用互斥量的lock方法获取锁则会被阻塞，直到线程a解锁互斥量，线程b读取到的数据为修改后的数据。
- 线程b获取锁，读取到未修改的数据，输出完毕后解锁互斥量，若线程a在此期间调用互斥量的lock方法获取锁则会被阻塞，直到线程b解锁互斥量，线程a读才能锁定互斥量并修改数据。

此时共享数据的一致性得到了保证，线程b读取到的数据要么是未修改的数据，要么是修改后的数据，不会读取到只修改了一部分的数据。

**4.3死锁**

互斥量虽然可以用来保护共享数据，但是也并非完美。

假设现在有两个线程a和b，两个互斥量M和N。线程a会先锁住互斥量M随后再锁住互斥量N，而线程b则会先锁住互斥量N然后再锁住互斥量M：

```cpp
void test()
{
	std::mutex M;
	std::mutex N;

	std::thread thread_a([&](){
		//锁住互斥量
		M.lock();
		N.lock();

		change("thread a");

		//解锁互斥量
		M.unlock();
		N.lock();
		});

	std::thread thread_b([&]() {
		//锁住互斥量
		N.lock();
		M.lock();

		change("thread b");

		//解锁互斥量
		N.unlock();
		M.lock();
	});

	thread_b.join();
	thread_a.join();
}
```

可能会出现线程a和线程b在同一时刻分别锁住了互斥量M和N，随后a想要锁住互斥量N时发现互斥量N已被线程b上锁，于是线程a被阻塞，而线程b想要锁住互斥量M时发现互斥量M已经被线程a上锁，于是线程b也被阻塞。两个线程都想要锁住对方占有的互斥量，于是两个线程便僵持不下，谁也无法继续运行，这种状况就被称为死锁。

避免死锁最简单的方法就是在任何时候都保持以固定顺序上锁互斥量，在持有锁的时候也要避免调用包含锁操作的代码(在持有锁时，调用包含锁操作的代码，可能会造成死锁。)对于上面的例子按这条原则修改如下：

```cpp
void test()
{
	std::mutex M;
	std::mutex N;

	std::thread thread_a([&](){
		//以固定顺序上锁互斥量
		M.lock();
		N.lock();

		change("thread a");

		//解锁互斥量
		M.unlock();
		N.lock();
		});

	std::thread thread_b([&]() {
		//以固定顺序上锁互斥量
		M.lock();
		N.lock();

		change("thread b");

		//解锁互斥量
		M.unlock();
		N.lock();
	});

	thread_b.join();
	thread_a.join();
}
```

以固定顺序上锁可以保持同一时刻只有一个线程可以占有互斥量，而其他线程只有等到占有互斥量的线程解锁互斥量才能够占有互斥量。

避免死锁的另一种方法是使用标准库提供的锁管理工具std::lock(c++11)或std::scopedlock(c++17)。在介绍std::lock之前，需要先介绍一下std::lock_guard和std::unique_lock。

std::lock_guard是标准库提供的基于RAII的锁管理工具。std::lock_guard类提供了两种构造函数：

- 在std::lock_guard类的对象在构造时接受一个互斥量作为参数，并对该互斥量进行上锁操作。
- 在std::lock_guard类的对象在构造时接受一个互斥量和std::adopt_lock作为参数，互斥的获取互斥量的所有权，但并不对互斥量进行上锁。

在std::lock_guard类对象析构时回对其占有的互斥量解锁，除析构和构造函数外std::lock_guard没有定义其他任何方法。

std::unique_lock则RAII式锁管理的基础上提供了更多的灵活性。std::unique_lock提供的lock，unlock，trylock方法与其所管理的互斥量提供的lock，unlock，trylock行为相同。std::unique_lock还提供了移动构造和移动赋值操作(支持移动操作意味着我们可以在函数和容器中转移std::unique_lock的所有权)，std::unique_lock的移动构造函数会以参数的内容初始化当前对象，并解除参数与其所管理的互斥量之前的关系。在调用std::unique_lock的移动赋值函数时，若当前对象有互斥量与其关联且已对其上锁，则对互斥量解锁并解除关联，随后获取参数所管理的互斥量，并解除参数锁管理的互斥量与参数间的关系。

std::unique_lock的构造函数同std::lock_guard的构造函数一样也提供了初始化策略：

- 在std::unique_lock类的对象在构造时接受一个互斥量作为参数，并对该互斥量进行上锁操作。
- 在std::unique_lock类的对象在构造时接受一个互斥量和std::defer_lock作为参数，则不对该互斥量进行上锁。
- 在std::unique_lock类的对象在构造时接受一个互斥量和std::try_to_lock作为参数，则尝试对互斥量上锁，上锁失败时不会阻塞线程。
- 在std::unique_lock类的对象在构造时接受一个互斥量和std::adopt_lock作为参数，则假定当前线程已经拥有互斥量的所有权。

std::unique_lock的owns_lock方法可以检查std::unique_lock是否有互斥量与其关联，且是否已对互斥量上锁，若有互斥量与std::unique_lock对象关联，且已经被std::unique_lock对象获得所有权则返回true，否则返回false。

下面是std::lock_guard与std::unique_lock的简单使用示例：

```cpp
void test()
{
	Person person{ "Jonathan Joestar", 21, 0 };
	std::mutex mutex;

	std::thread thread_a([&]() {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(10ns);

		//关联到mutex并对其上锁
		std::lock_guard lg(mutex);

		//等价代码
		//std::unique_lock ul(mutex);

		person.m_name = "Dio Brando";
		person.m_age = 121;
		person.m_gender = 0;

		//lg(或ul)生命周期结束后解锁mutex
	});

	std::thread thread_b([&]() {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(10ns);

		//关联到mutex并对其上锁
		std::lock_guard lg(mutex);

		//等价代码
		//std::unique_lock ul(mutex);

		std::cout << person.m_name << ", " << person.m_age << ", " << person.m_gender;

		//lg(或ul)生命周期结束后解锁mutex
	});

	thread_b.join();
	thread_a.join();
}
```

介绍完std::unique_lock与std::lock_guard之后，我们再回到使用标准库提供的锁管理工具避免死锁的内容上来。

标准库提供的std::lock函数可以配合std::unique_lock或std::lock_guard来避免死锁。在C++17中提供了基于RAII的更便于使用的std::scopedlock类也可以用于避免死锁。

现在假设每条数据包含数据项和互斥量，在互换两条数据内容时，需要对两条数据的互斥量都进行上锁。下面的代码展示了如何在这种情况下使用std::lock或std::scopedlock避免死锁：

```cpp
struct Datum
{
	//数据项
	std::string m_name;
	//互斥量
	std::mutex m_mutex;

	Datum(const std::string name) : m_name(name) {}
};

void swap_data(Datum &lhs, Datum &rhs)
{
	using namespace std::chrono_literals;
	std::this_thread::sleep_for(10ns);

	//使用std::lock避免死锁
	std::lock(lhs.m_mutex, rhs.m_mutex);
	std::lock_guard lg0(lhs.m_mutex, std::adopt_lock);
	std::lock_guard lg1(rhs.m_mutex, std::adopt_lock);

	//等价代码
	//std::unique_lock ul0(lhs.m_mutex, std::defer_lock);
	//std::unique_lock ul1(rhs.m_mutex, std::defer_lock);
	//std::lock(ul0, ul1);

	//C++17等价代码，使用std::scoped_lock避免死锁
	//std::scoped_lock sl(lhs.m_mutex, rhs.m_mutex);

	std::string temp = lhs.m_name;
	lhs.m_name = rhs.m_name;
	rhs.m_name = temp;
}

void test()
{
	Datum leon("Leon"), claire("Claire"), ada("Ada"), sherry("Sherry");

	std::vector<std::thread> workers;

	workers.emplace_back(swap_data, std::ref(leon), std::ref(ada));
	workers.emplace_back(swap_data, std::ref(claire), std::ref(ada));
	workers.emplace_back(swap_data, std::ref(leon), std::ref(sherry));
	workers.emplace_back(swap_data, std::ref(sherry), std::ref(claire));
	workers.emplace_back(swap_data, std::ref(sherry), std::ref(ada));
	workers.emplace_back(swap_data, std::ref(claire), std::ref(leon));

	for (auto &t : workers)
	{
		t.join();
	}

	std::cout << "Leon's current name is :" << leon.m_name << std::endl;
	std::cout << "Claire's current name is :" << claire.m_name << std::endl;
	std::cout << "Ada's current name is :" << ada.m_name << std::endl;
	std::cout << "Sherry's current name is :" << sherry.m_name << std::endl;
}
```

上面代码的可能输出为：

```cpp
Leon's current name is :Sherry
Claire's current name is :Claire
Ada's current name is :Leon
Sherry's current name is :Ada
```

**4.4锁的粒度**

在使用互斥量时除了死锁，锁的粒度也是一个很值得关注的问题。锁的粒度是指一个互斥量锁保护的数据量的大小。一个细粒度的锁所保护的数据量较小，而一个粗粒度的锁所保护的数据量则较大。由于互斥量在同一时刻只能被一个线程锁定，所以在使用粗粒度锁的情况下一个线程会长时间占有互斥量，而其他尝试锁定互斥量的线程都会被长时间阻塞，这样程序整体的效率便会降低。

最能体现锁的粒度对程序效率影响的容器可能是hash map，我们知道一个hash map由多个bucket组成。假如现在我们需要一个可供多个线程安全读写的hash map，有如下两种实现方法：

- 使用粗粒度锁。使用一个互斥量保护整个hash map，这种方法实现起来简单粗暴，而且十分有效，但是同一时刻只有一个线程能够读写hash map。
- 使用细粒度锁。对组成hash map的每个bucket分别使用一个互斥量进行保护，这样一来每个互斥量所保护的数据量变少了，也可以支持多个线程同时读写hash map的不同bucket(此时读写同一个bucket的不同线程还是会被阻塞)。

上面两种实现方案中，使用细粒度锁的hash map显然具有更高的效率。

除了锁所保护的数据量大小外，持有锁的时间的长短对程序的运行效率也会有很大的影响。现在假设要对一段数据依次进行读取，处理和修改操作。为了保证线程安全，我们首先可以考虑使用std::lock_guard对这一系列操作进行保护：

```cpp
struct DataBlock
{
	std::string m_name;
};

std::vector<DataBlock> data;
size_t index = 0;
std::mutex mutex;

DataBlock& get_data()
{
	return data[index++];
}

void update_data(DataBlock& old_bl, const DataBlock& new_bl)
{
	old_bl = new_bl;
}

DataBlock process_data(const DataBlock& block)
{
	return DataBlock{ block.m_name + " processed" };
}

void get_and_update_data()
{
	std::scoped_lock sl(mutex);
	DataBlock& original_data = get_data();
	DataBlock processed_data = process_data(original_data);
	update_data(original_data, processed_data);
}

void test()
{
	data.push_back(DataBlock{ "ada" });
	data.push_back(DataBlock{ "leon" });
	data.push_back(DataBlock{ "claire" });
	data.push_back(DataBlock{ "sherry" });


	std::vector<std::thread> workers;

	{
		workers.emplace_back(get_and_update_data);
		workers.emplace_back(get_and_update_data);
		workers.emplace_back(get_and_update_data);
		workers.emplace_back(get_and_update_data);
	}

	for (auto &t : workers)
	{
		t.join();
	}

	for (auto &item : data)
	{
		std::cout << item.m_name << std::endl;
	}
}
```

但是更好的方案是采用更加灵活的std::unique_lock，在不需要持有锁的时候对互斥量进行解锁(比如进行数据处理时)，这样可以减少线程持有锁的时间，让其他线程在当前线程处理数据时也有机会读取或者更新数据：

```cpp
void get_and_update_data()
{
	std::unique_lock ul(mutex);
	DataBlock& original_data = get_data();

	//在不需要持有锁时，对互斥量解锁
	ul.unlock();
	DataBlock processed_data = process_data(original_data);

	//在需要修改共享数据时，尝试获取锁
	ul.lock();
	update_data(original_data, processed_data);
}
```

**4.5 C++标准库提供的互斥量**

在4.2节中已经介绍了一种C++标准库提供的互斥量std::mutex，本节还会介绍一些标准库所提供的其它的互斥量。

**a.std::recursive_mutex**

std::recursive_mutex与std::mutex一样也只定义了lock，trylock，unlock和native_handle(用于返回底层实现定义的原生句柄)方法。

std::recursive_mutex与std::mutex的不同点在于std::recursive_mutex允许在一个已经锁定互斥量的线程上多次调用lock方法(与之对应的在一个已经锁定std::mutex的线程上，再次调用std::mutex的lock方法是未定义行为)，在已锁定互斥量的情况下再次调用lock方法会增加std::recursive_mutex的所有权等级。在调用std::recursive_mutex的unlock方法时，若lock与unlock调用次数匹配时(即所有权等级为1时)会解锁互斥量，否则会减少std::recursive_mutex的所有权等级。当一个线程锁定互斥量时，其他线程若尝试锁定互斥量就会被阻塞。(所有权的最大层数是未指定的。若超出此数，则可能抛[std::system_error](https://link.zhihu.com/?target=https%3A//zh.cppreference.com/w/cpp/error/system_error)类型异常。std::recursive_mutex的lock与unlock，有点类似与COM中的AddRef和release)

下面时std::recursive_mutex的使用示例：

```cpp
std::recursive_mutex rmutex;

void test()
{
	std::thread worker{ []() {
		//锁定互斥量，rmutex的所有权等级为1
		rmutex.lock();

		do_something();

		{
			//在锁定互斥量的情况下，再次调用lock，所有权等级增加1(为2)
			rmutex.lock();

			do_something_else();

			//所有权等级为2，不等于1，将所有权登记减少1，此次unlock调用后线程依然占有互斥量
			rmutex.unlock();
		}
		//所有权等级为1，此次unlock调用后线程解锁互斥量
		rmutex.unlock();
	} };

	worker.join();
}
```

**b.std::shared_mutex**

std::shared_mutex是c++17引入的共享互斥量。出了提供lock，trylock，unlock方法以支持互斥的单个线程独锁(排他)定互斥量外，还提供了lock_shared，try_lock_shared和unlock_shared方法以支持多个线程同时占有(共享锁定)互斥量。

std::shared_mutex的lock方法用于排他性的锁定互斥量，若当前线程已经以任何模式(排他或共享)占有互斥量则调用lock方法为未定义行为。std::shared_mutex的unlock方法可以解锁互斥量，若互斥量未被当前线程占有则调用unlock方法为未定义行为。

std::shared_mutex的lock_shared方法用于获取互斥量的共享所有权。若另一线程以排他性所有权保有互斥，则到lock_shared的调用将阻塞执行，直到能取得共享所有权。若在以已任何模式（排他性或共享）占有互斥量的线程调用lock_shared，则为未定义行为。std::shared_mutex的unlock_shared方法用于将当前线程占有的共享互斥所有权释放。若当前线程未以共享方式获得互斥量所有权，则unlock_shared调用为未定义行为。

std::shared_mutex多用于多个线程共享读取数据，而只有一个线程能够写入数据的情况。

**c.支持时限的互斥量**

标准库除了提供std::mutex，std::recursive_mutex和std::shared_mutex外，还提供了与之分别对应的支持时限的互斥量std::timed_mutex，std::recursive_timed_mutex和std::shared_timed_mutex。这些支持时限的互斥量除了支持原有互斥量的全部功能外，还提供了try_lock_for和try_lock_until方法。

try_lock_for为在一段时间内尝试锁定互斥量，若超过给定时间段任未获得锁(在此期间调用try_lock_for的线程一直处于阻塞状态)，则返回false，若在给定时间段内成功锁定互斥量则返回true。此方法与try_lock方法类似，可能会在满足条件的情况下虚假的返回false。

try_lock_until为在给定时间点之前尝试锁定互斥量，若在给定时间点之后任未获得锁(在此期间调用try_lock_for的线程一直处于阻塞状态)，则返回false，若在给定时间点之前成功锁定互斥量则返回true。此方法与try_lock方法类似，可能会在满足条件的情况下虚假的返回false。

此类支持时限的互斥量，由于调度或资源争议延迟等原因，可能调用对应方法的线程被阻塞的时间会超过给定时间段或超出给定时间点。

```cpp
std::timed_mutex tmutex;

void test()
{
	//主线程一直持有锁
	std::lock_guard lg(tmutex);

	std::thread worker([]() {
		auto start = std::chrono::steady_clock::now();

		//worker线程try_lock_until会失败返回false，worker至少会被阻塞1s
		tmutex.try_lock_until(start + std::chrono::seconds(1));

		auto end = std::chrono::steady_clock::now();
		std::chrono::duration<double> time_span = std::chrono::duration_cast<std::chrono::duration<double>>(end - start);
		std::cout << "Time Span: " << time_span.count() << std::endl;
	});

	worker.join();
}
```

以上代码的可能输出为Time Span: 1.00057

**4.5 C++标准库提供的锁管理工具**

在4.3节中已经介绍了C++标准库提供的锁管理工具std::scoped_lock，std::lock，std::lock_guard和std::unique_lock。std::unique_lock除4.3节中已经介绍的功能外，也支持时限的try_lock_for和try_lock_until方法，其功能与互斥量提供的try_lock_for和try_lock_until方法功能相同。

这里还会介绍std::shared_lock与std::call_once。

**a.std::shared_lock**

std::shared_lock类似与std::unique_lock，但通常是与std::shared_mutex一起使用:

```cpp
std::shared_mutex smutex;

int value = 1;

std::vector<int> results;

//共享读
void shared_read(int index)
{
	//多个线程可以同时共享地锁定互斥量
	std::shared_lock<std::shared_mutex> sl(smutex);
	results[index] = value;
}

//互斥写
void exclusive_write()
{
	//只有一个线程能够排他的锁定互斥量
	std::unique_lock<std::shared_mutex> ul(smutex);
	value = value * 2;
}

void test()
{
	results.resize(4);

	std::vector<std::thread> writers;
	std::vector<std::thread> readers;

	writers.emplace_back([]() {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(20ns);

		exclusive_write();
	});

	writers.emplace_back([]() {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(20ns);

		exclusive_write();
	});

	readers.push_back(std::thread([](int index) {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(20ns);

		shared_read(index);
	}
	, 0));
	
	readers.emplace_back([](int index) {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(20ns);

		shared_read(index);
	}
	, 1);

	readers.emplace_back([](int index) {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(20ns);

		shared_read(index);
	}
	, 2);

	readers.emplace_back([](int index) {
		using namespace std::chrono_literals;
		std::this_thread::sleep_for(20ns);

		shared_read(index);
	}
	, 3);
	
	for (auto &t : writers)
	{
		t.join();
	}

	for (auto &t : readers)
	{
		t.join();
	}

	for (auto &var : results)
	{
		std::cout << var << std::endl;
	}
}
```

上面代码的可能输出为：

```text
2
4
4
4
```

**b.std::call_once**

std::call_once用于在多线程环境下只执行一次的可调用对象。标准库还提供了一个辅助类std::once_flag用于指示是否已经调用可调用对象。

若调用std::call_once时，std::once_flag指示可调用对象已被调用，则立即返回，否则调用可调用对象。若调用可调用对象时出现异常，则传播异常给call_once的调用方，并且不翻转once_flag。若调用成功，则正常返回并翻转once_flag。

下面为std::call_once的使用示例：

```cpp
std::once_flag flag;

//只调用一次
void prepare_data()
{
	std::cout << "data prepared" << std::endl;
}

void process(int index)
{
	std::cout << "process data: " << index << std::endl;
}

void process_data(int index)
{
	std::call_once(flag, prepare_data);
	process(index);
}

void test()
{
	std::vector<std::thread> workers;

	workers.emplace_back([](int index) {
		process_data(index);
	}, 0);

	workers.emplace_back([](int index) {
		process_data(index);
	}, 1);

	workers.emplace_back([](int index) {
		process_data(index);
	}, 2);

	for (auto &t : workers)
	{
		t.join();
	}
}
```



**引用：**

[What is the difference between concurrency and parallelism?](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism)[stackoverflow.com](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism)[C++ 11 多线程--线程管理](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/wangguchangqing/p/6134635.html)

[www.cnblogs.com

![图标](https://pic3.zhimg.com/v2-41fa1cef3b42cf34ff53fd4435c54a5e_120x160.jpg)]

(https://link.zhihu.com/?target=https%3A//www.cnblogs.com/wangguchangqing/p/6134635.html)[使用 C++11 编写 Linux 多线程程序](https://link.zhihu.com/?target=https%3A//www.ibm.com/developerworks/cn/linux/1412_zhupx_thread/)

[www.ibm.com

![图标](https://pic4.zhimg.com/v2-d4f790c047b43769f7c543b031bad453_ipico.jpg)]

(https://link.zhihu.com/?target=https%3A//www.ibm.com/developerworks/cn/linux/1412_zhupx_thread/)

此外还参考了c++ concurrency in action的第1，2，3章节。

**如果你发现了本篇文章存在的错误，请指出，我会及时修正。**