# [C++任务队列与多线程](https://www.cnblogs.com/zhiranok/archive/2013/01/14/task_queue.html)

### 摘要：

   很多场合之所以使用C++，一方面是由于C++编译后的native  code的高效性能，另一方面是由于C++优秀的并发能力。并行方式有多进程  和多线程之分，本章暂且只讨论多线程，多进程方面的知识会在其他章节具体讨论。多线程是开发C++服务器程序非常重要的基础，如何根据需求具体的设计、分配线程以及线程间的通信，也是服务器程序非常重要的部分，除了能够带来程序的性能提高外，若设计失误，则可能导致程序复杂而又混乱，变成bug滋生的温床。所以设计、开发优秀的线程组件以供重用，无论如何都是值得的。

​    线程相关的api并不复杂，然而无论是linux还是windows系统，都是c风格的接口，我们只需简单的封装成对象，方便易用即可。任务队列是设计成用来进行线程间通信，使用任务队列进行线程间通信设计到一些模式，原理并不难理解，我们需要做到是弄清楚，在什么场景下选用什么样的模式即可。

#### 任务队列的定义：

​    任务队列对线程间通信进行了抽象，限定了线程间只能通过传递任务，而相关的数据及操作则被任务保存。任务队列这个名词可能在其他场景定义过其他意义，这里讨论的任务队列定义为：能够把封装了数据和操作的任务在多线程间传递的线程安全的先入先出的队列。其与线程关系示意图如下：

|      |                                                              |
| ---- | ------------------------------------------------------------ |
|      | [![clip_image001](Task_And_multithreading.assets/14221931-2c40b86b81ba476a850e3b1a6283218c.gif)](https://images0.cnblogs.com/blog/282357/201301/14221931-eb26d8a176994c2c904f07d61a3a045e.gif) |

   注：两个虚线框分别表示线程A和线程B恩能够访问的数据边界，由此可见 任务队列是线程间通信的媒介。

#### 任务队列的实现：

##### 任务的定义

​    生产者消费者模型在软件设计中是极其常见的模型，常常被用来实现对各个组件或系统解耦合。大到分布式的系统交互，小到网络层对象和应用层对象的通讯，都会应用到生产者消费者模型，在任务队列中，生产和消费的对象为“任务”。这里把任务定义为组合了数据和操作的对象，或者简单理解成包含了void (void*) 类型的函数指针和void* 数据指针的结构。我们把任务定义成类task_t，下面来分析一下task_t的实现。

插入代码：

[![复制代码](Task_And_multithreading.assets/copycode.gif)](javascript:void(0);)

```
class task_impl_i
{
public:
    virtual ~task_impl_i(){}
    virtual void run()          = 0;
    virtual task_impl_i* fork() = 0;
};

class task_impl_t: public task_impl_i
{
public:
    task_impl_t(task_func_t func_, void* arg_):
        m_func(func_),
        m_arg(arg_)
    {}

    virtual void run()
    {
        m_func(m_arg);
    }

    virtual task_impl_i* fork()
    {
        return new task_impl_t(m_func, m_arg);
    }

protected:
    task_func_t m_func;
    void*       m_arg;
};

struct task_t
{
    static void dumy(void*){}
    task_t(task_func_t f_, void* d_):
        task_impl(new task_impl_t(f_, d_))
    {
    }
    task_t(task_impl_i* task_imp_):
        task_impl(task_imp_)
    {
    }
    task_t(const task_t& src_):
        task_impl(src_.task_impl->fork())
    {
    }
    task_t()
    {
        task_impl = new task_impl_t(&task_t::dumy, NULL);
    }
    ~task_t()
    {
        delete task_impl;
    }
    task_t& operator=(const task_t& src_)
    {
        delete task_impl;
        task_impl = src_.task_impl->fork();
        return *this;
    }
    
    void run()
    {
        task_impl->run();
    }
    task_impl_i*    task_impl;
};
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

​    Task最重要的接口是run，简单的执行保存的操作，具体的操作保存在task_impl_i的基类中，由于对象本身就是数据加操作的集合，所以构造task_impl_i的子类对象时，为其赋予不同的数据和操作即可。这里使用了组合的方式实现了接口和实现的分离。这么做的优点是应用层只需知道task的概念即可，对应task_impl_i不需要了解。由于不同的操作和数据可能需要构造不同task_impl_i子类，我们需要提供一些泛型函数，能够将用户的所有操作和数据都能轻易的转换成task对象。task_binder_t 提供一系列的gen函数，能够转换用户的普通函数和数据为task_t对象。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
struct task_binder_t
{
    //! C function
    
    static task_t gen(void (*func_)(void*), void* p_)
    {
        return task_t(func_, p_);
    }
    template<typename RET>
    static task_t gen(RET (*func_)(void))
    {
        struct lambda_t
        {
            static void task_func(void* p_)
            {
                (*(RET(*)(void))p_)();
            };
        };
        return task_t(lambda_t::task_func, (void*)func_);
    }
    template<typename FUNCT, typename ARG1>
    static task_t gen(FUNCT func_, ARG1 arg1_)
    {
        struct lambda_t: public task_impl_i
        {
            FUNCT dest_func;
            ARG1  arg1;
            lambda_t(FUNCT func_, const ARG1& arg1_):
                dest_func(func_),
                arg1(arg1_)
            {}
            virtual void run()
            {
                (*dest_func)(arg1);
            }
            virtual task_impl_i* fork()
            {
                return new lambda_t(dest_func, arg1);
            }
        };
        return task_t(new lambda_t(func_, arg1_));
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

##### 生产任务

   函数封装了用户的操作逻辑，需要在某线程执行特定操作时，需要将操作对应的函数转换成task_t，投递到目的线程对应的任务队列。任务队列使用起来虽然像是在互相投递消息，但是根本上仍然是共享数据式的数据交换方式。主要步骤如下：

l 用户函数转换成task_t对象

l 锁定目的线程的任务队列，将task_t 放到任务队列尾，当队列为空时，目的线程会wait在条件变量上，此时需要signal唤醒目的线程

实现的关键代码如下：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
void produce(const task_t& task_)
    {        
        lock_guard_t lock(m_mutex);
        bool need_sig = m_tasklist.empty();

        m_tasklist.push_back(task_);
        if (need_sig)
        {
            m_cond.signal();
        }
    }
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

##### 消费任务

消费任务的线程会变成完全的任务驱动，该线程只有一个职责，执行任务队列的所有任务，若当前任务队列为空时，线程会阻塞在条件变量上，重新有新任务到来时，线程会被再次唤醒。实现代码如下：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
int   consume(task_t& task_)
    {
        lock_guard_t lock(m_mutex);
        while (m_tasklist.empty())
        {
            if (false == m_flag)
            {
                return -1;
            }
            m_cond.wait();
        }

        task_ = m_tasklist.front();
        m_tasklist.pop_front();

        return 0;
} 
int run()
    {
        task_t t;
        while (0 == consume(t))
        {
            t.run();
        }
        return 0;
    }
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

#### 任务队列的模式

##### 单线程单任务队列方式

任务队列已经提供了run接口，绑定任务队列的线程只需执行此函数即可，此函数除非用户显示的调用任务队列的close接口，否则run函数永不返回。任务队列的close接口是专门用来停止任务队列的工作的，代码如下：

```
void close()
    {
        lock_guard_t lock(m_mutex);
        m_flag = false;
        m_cond.broadcast();
}
```

首先设置了关闭标记，然后在条件变量上执行broadcast，  任务队列的run函数也会由此退出。在回头看一下run接口的代码你会发现，检查任务队列是否关闭（m_flag  变量）的代码是在任务队列为空的时候才检测的，这样能够保证任务队列被全部执行后，run函数才返回。

下面是一个使用任务队列的helloworld的示例：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
class foo_t
{
public:
    void print(int data)
    {
        cout << "helloworld, data:" <<data << " thread id:"<< ::pthread_self() << endl;
    }
    void print_callback(int data, void (*callback_)(int))
    {
        callback_(data);
    }
    static void check(int data)
    {
        cout << "helloworld, data:" <<data << " thread id:"<< ::pthread_self() << endl;
    }
};

//  单线程单任务队列
void test_1()
{
    thread_t thread;
    task_queue_t tq;

    thread.create_thread(task_binder_t::gen(&task_queue_t::run, &tq), 1);

    foo_t foo;
    for (int i = 0; i < 100; ++i)
    {
        cout << "helloworld, thread id:"<< ::pthread_self() << endl;
        tq.produce(task_binder_t::gen(&foo_t::print, &foo, i));
        sleep(1);
    }
    thread.join();
}
int main(int argc, char* argv[])
{
    test_1();
    return 0;
}
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

本例使用单线程单任务队列的方式，由于只有一个线程绑定在任务队列上，所以任务的执行会严格按照先入先出的方式执行。优点是能够保证逻辑操作的有序性，所以最为常用。

##### 多线程多任务队列方式

如果想利用更多线程，那么创建更多线程的同时，仍然保证每个任务队列绑定在单线程上。让不同的任务队列并行执行就可以了。

下面几种情况适用此模式：

l 比如网游中数据库一般会创建连接池，用户的操作数据库都是有数据库线程池完成，在将结果投递给逻辑层。对每个用户的数据增删改查操作都必须是有序的，所以每个用户绑定一个固定的任务队列。而不同的用户的数据修改互不干扰，不同的用户分配不同的任务队列即可。

l 比如网络层中的多个socket的读写是互不干扰的，可以创建两个或更多线程，每个对应一个任务队列，不同的socket的操作可以随机的分配一个任务队列（注意分配是随机的，一旦分配了，单个socket的所有操作都会由这个任务队列完成，保证逻辑有序性）。

示例代码：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
//! 多线程多任务队列
void test_2()
{
    thread_t thread;
    task_queue_t tq[3];

    for (unsigned int i = 0; i < sizeof(tq)/sizeof(task_queue_t); ++i)
    {
        thread.create_thread(task_binder_t::gen(&task_queue_t::run, &(tq[i])), 1);
    }

    foo_t foo;
    cout << "helloworld, thread id:"<< ::pthread_self() << endl;
    for (unsigned int j = 0; j < 100; ++j)
    {
        tq[j % (sizeof(tq)/sizeof(task_queue_t))].produce(task_binder_t::gen(&foo_t::print, &foo, j));
        sleep(1);
    }
    thread.join();
}
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

##### 多线程单任务队列方式

有时候可能并不需要逻辑操作的完全有序，而是要求操作尽可能快的执行，只要有空闲线程，任务就投递到空闲线程立刻执行。如果时序不影响结果，这种模式会更有效率，下面几种情况可能用到这种模式：

l 比如social  game中的好友是从platform的api获取的，需要http协议通讯，若采用curl等http库同步通讯时，会阻塞线程，这是可以使用多线程单队列方式，请求投递到任务队列后，只要有空闲线程立马执行，用户A虽然比用户B先到达任务队列，但是并不能保证A比B一定先获取到好友列表，如果A有2k好友，而B只有两个呢，当然有可能B请求更快。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
//! 多线程单任务队列
void test_3()
{
    thread_t thread;
    task_queue_t tq;

    thread.create_thread(task_binder_t::gen(&task_queue_t::run, &tq), 3);

    foo_t foo;
    cout << "helloworld, thread id:"<< ::pthread_self() << endl;
    for (unsigned int j = 0; j < 100; ++j)
    {
        tq.produce(task_binder_t::gen(&foo_t::print, &foo, j));
        sleep(1);
    }
    thread.join();
}
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

#### 任务队列的高阶用法

##### 异步回调

任务队列的模式中列举的例子都是线程间单项通讯，线程A将请求投递给了B，但B执行完毕后A并没有检测结果。实际中往往都是需要将执行结果进行额外处理或者投递到另外任务队列。异步回调可以很好的解决这个问题，原理就是投递任务时，同时包含检查任务执行结果的函数。示例代码：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
//! 异步回调
void test_4()
{
    thread_t thread;
    task_queue_t tq;

    thread.create_thread(task_binder_t::gen(&task_queue_t::run, &tq), 1);

    foo_t foo;
    cout << "helloworld, thread id:"<< ::pthread_self() << endl;
    for (unsigned int j = 0; j < 100; ++j)
    {
        tq.produce(task_binder_t::gen(&foo_t::print_callback, &foo, j, &foo_t::check));
        sleep(1);
    }
    thread.join();
}
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

异步是性能优化非常重要的手段，下面如下场合可以使用异步：

l 服务器程序要求很高的实时性，几乎逻辑层不执行io操作，io操作通过任务队列被io线程执行成功后再通过回调的方式传回逻辑层。

l 网游中用户登录，需呀从数据库载入用户数据，数据库层不需要知晓逻辑层如何处理用户数据，当接口被调用时必须传入回调函数，数据库层载入数据后直接调用回调函数，而数据作为参数。

##### 隐式任务队列

使用任务队列可以解耦多线程的设计。更加优秀的使用是将其封装在接口之后。前边的例子中都是显示的操作了任务队列对象。但这就限制了用户必须知道某个接口需要绑定哪个任务队列上，尤其是多线程多任务队列的例子，如果当用户操作socket接口时还要知道socket对应哪个任务队列就显得不够优雅了。Socket自己本身可以保存对应任务队列的引用，这样使用者只需调用socket的接口，而接口内部再将请求投递到争取的任务队列。示例代码：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
void socket_impl_t::async_send(const string& msg_)
{
    tq.produce(task_binder_t::gen(&socket_impl_t::send, &this, msg_));
}
void socket_impl_t::send(const string& msg_)
{
    //do send code
}
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

#### 总结：

l 设计多线程程序时，往往设计使用任务队列是关键，好用、高效、灵活的任务队列组件十分必需，本节介绍的实现支持多种多线程模式，易用易理解。

l 异步回调在多线程程序中非常常见，异步往往是为了提高性能和系统吞吐量的，但是异步其不可避免的会带来复杂性，所以尽量保证异步相关的步骤简单。

l 任务队列封装对象接口的内部更佳，使用者直接调用接口，仿佛没有任务队列这回事，让他在看不见的地方默默运行。

l 本节设计的任务队列是线程安全的，并且关闭时已经投递的任务能够保证被 。

代码：http://code.google.com/p/ffown/source/browse/trunk/#trunk%2Ffflib%2Finclude

## 相关连接

1. 文档 [http://h2cloud.org](http://h2cloud.org/)
2. 源码 https://github.com/fanchy/h2engine
3. 介绍 http://www.cnblogs.com/zhiranok/p/ffengine.html