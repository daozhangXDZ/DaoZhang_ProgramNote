# TLSALLOC



为什么要有TLS？原因在于，进程中的全局变量与函数内定义的静态(static)变量，是各个线程都可以访问的共享变量。在一个线程修改的内存内容，对所有线程都生效。这是一个优点也是一个缺点。说它是优点，线程的数据交换变得非常快捷。说它是缺点，一个线程死掉了，其它线程也性命不保; 多个线程访问共享数据，需要昂贵的同步开销，也容易造成同步相关的BUG。

如果需要在一个线程内部的各个函数调用都能访问、但其它线程不能访问的变量（被称为static memory local to a thread 线程局部静态变量），就需要新的机制来实现。这就是TLS。

[线程局部存储](http://baike.baidu.com/view/598128.htm)在不同的平台有不同的实现，可移植性不太好。幸好要实现线程局部存储并不难，最简单的办法就是建立一个全局表，通过当前线程ID去查询相应的数据，因为各个线程的ID不同，查到的数据自然也不同了。

大多数平台都提供了线程局部存储的方法，无需要我们自己去实现：

**linux:**

int pthread_key_create(pthread_key_t *key, void (*destructor)(void*));

int pthread_key_delete(pthread_key_t key);

void *pthread_getspecific(pthread_key_t key);

int pthread_setspecific(pthread_key_t key, const void *value);

**Win32**

方法一：每个线程创建时系统给它分配一个LPVOID指针的数组（叫做TLS数组），这个数组从C编程角度是隐藏着的不能直接访问，需要通过一些C API函数调用访问。首先定义**一些**DWORD线程全局变量或函数静态变量,**准备**作为各个线程访问自己的TLS数组的索引变量。一个线程使用TLS时，第一步在线程内调用TlsAlloc()函数，为一个TLS数组索引变量与这个线程的TLS数组的某个槽(slot）关联起来，例如获得一个索引变量：

global_dwTLSindex=TLSAlloc();

注意，此步之后，当前线程实际上访问的是这个TLS数组索引变量的线程内的拷贝版本。也就说，不同线程虽然看起来用的是同名的TLS数组索引变量，但实际上各个线程得到的可能是不同DWORD值。其意义在于，每个使用TLS的线程获得了一个DWORD类型的**线程局部静态变量**作为TLS数组的索引变量。C/C++原本没有直接定义**线程局部静态变量**的机制，所以在如此大费周折。

第二步，为当前线程动态分配一块内存区域（使用LocalAlloc()函数调用），然后把指向这块内存区域的指针放入TLS数组相应的槽中(使用TlsValue()函数调用)。

第三步，在当前线程的任何函数内，都可以通过TLS数组的索引变量，使用TlsGetValue()函数得到上一步的那块内存区域的指针，然后就可以进行内存区域的读写操作了。这就实现了在一个线程内部这个范围处处可访问的变量。

最后，如果不再需要上述线程局部静态变量，要动态释放掉这块内存区域(使用LocalFree()函数)，然后从TLS数组中放弃对应的槽(使用TlsFree()函数）。

 

 

TLS 是一个良好的Win32 特质，让多线程程序设计更容易一些。TLS 是一个机制，经由它，程序可以拥有全域变量，但处于「每一线程各不相同」的状态。也就是说，进程中的所有线程都可以拥有全域变量，但这些变量其实是特定对某个线程才有意义。例如，你可能有一个多线程程序，每一个线程都对不同的文件写文件（也因此它们使用不同的文件handle）。这种情况下，把每一个线程所使用的文件handle 储存在TLS 中，将会十分方便。当线程需要知道所使用的handle，它可以从TLS 获得。重点在于：线程用来取得文件handle 的那一段码在任何情况下都是相同的，而从TLS中取出的文件handle 却各不相同。非常灵巧，不是吗？有全域变数的便利，却又分属各线程。  

 

  虽然TLS 很方便，它并不是毫无限制。在Windows NT 和Windows 95 之中，有64 个DWORD slots 供每一个线程使用。这意思是一个进程最多可以有64 个「对各线程有不同意义」的DWORDs。 虽然TLS 可以存放单一数值如文件handle，更常的用途是放置指针，指向线程的私有资料。有许多情况，多线程程序需要储存一堆数据，而它们又都是与各线程相关。许多程序员对此的作法是把这些变量包装为C 结构，然后把结构指针储存在TLS 中。当新的线程诞生，程序就配置一些内存给该结构使用，并且把指针储存在为线程保留下来的TLS 中。一旦线程结束，程序代码就释放所有配置来的区块。既然每一个线程都有64 个slots 用来储存线程自己的数据，那么这些空间到底打哪儿来？在线程的学习中我们可以从结构TDB中看到，**每一个****thread database** **都有****64** **个****DWORDs** **给****TLS** **使用**。当你以TLS 函式设定或取出数据，事实上你真正面对的就是那64 DWORDs。好，现在我们知道了原来那些“对各线程有不同意义的全局变量”是存放在线程各自的TDB中阿。 

 

​    接下来你也许会问：我怎么存取这64个DWORDS呢？我又怎么知道哪个DWORDS被占用了，哪个没有被占用呢？首先我们要理解这样一个事实：系统之所以给我们提供TLS这一功能，就是为了方便的实现“对各线程有不同意义的全局变量”这一功能；既然要达到“全局变量”的效果，那么也就是说每个线程都要用到这个变量，既然这样那么我们就不需要对每个线程的那64个DWORDS的占用情况分别标记了，因为那64个DWORDS中的某一个一旦占用，是所有线程的那个DWORD都被占用了，于是KERNEL32 使用两个DWORDs（总共64 个位）来记录哪一个slot 是可用的、哪一个slot 已经被用。这两个DWORDs 可想象成为一个64 位数组，如果某个位设立，就表示它对应的TLS slot 已被使用。这64 位TLS slot 数组存放在process database 中（在进程一节中的PDB结构中我们列出了那两个DWORDs）。 

##  操作

下面的四个函数就是对TLS进行操作的：  

（1）TlsAlloc  

上面我们说过了KERNEL32 使用两个DWORDs（总共64 个位）来记录哪一个slot 是可用的、哪一个slot 已经被用。当你需要使用一个TLS slot 的时候，你就可以用这个函数将相应的TLS slot位置１。  

（2）TlsSetValue  

*TlsSetValue* 可以把数据放入先前配置到的TLS slot 中。两个参数分别是TLS slot 索引值以及欲写入的数据内容。*TlsSetValue* 就把你指定的数据放入64 DWORDs 所组成的数组（位于目前的thread database）的适当位置中。  

（3）TlsGetValue  

这个函数几乎是*TlsSetValue* 的一面镜子，最大的差异是它取出数据而非设定数据。和*TlsSetValue* 一样，这个函数也是先检查TLS 索引值合法与否。如果是，*TlsGetValue* 就使用这个索引值找到64 DWORDs 数组（位于thread database 中）的对应数据项，并将其内容传回。  

（4）TlsFree  

这个函数将*TlsAlloc* 和*TlsSetValue* 的努力全部抹消掉。*TlsFree* 先检验你交给它的索引值是否的确被配置过。如果是，它将对应的64 位TLS slots 位关闭。然后，为了避免那个已经不再合法的内容被使用，*TlsFree* 巡访进程中的每一个线程，把0 放到刚刚被释放的那个TLS slot 上头。于是呢，如果有某个TLS 索引后来又被重新配置，所有用到该索引的线程就保证会取回一个0 值，除非它们再调用*TlsSetValue*。

 

##  互斥

互斥（Mutex）是一种用途非常广泛的内核对象。能够保证多个线程对同一共享资源的互斥访问。同临界区有些类似，只有拥有互斥对象的线程才具有访问资源的权限，由于互斥对象只有一个，因此就决定了任何情况下此共享资源都不会同时被多个线程所访问。当前占据资源的线程在任务处理完后应将拥有的互斥对象交出，以便其他线程在获得后得以访问资源。与其他几种内核对象不同，互斥对象在操作系统中拥有特殊代码，并由操作系统来管理，操作系统甚至还允许其进行一些其他内核对象所不能进行的非常规操作。为便于理解，可参照图3.8给出的互斥内核对象的工作模型：

 

图3.8 使用互斥内核对象对共享资源的保护

图（a）中的箭头为要访问资源（矩形框）的线程，但只有第二个线程拥有互斥对象（黑点）并得以进入到共享资源，而其他线程则会被排斥在外（如图（b）所示）。当此线程处理完共享资源并准备离开此区域时将把其所拥有的互斥对象交出（如图（c）所示），其他任何一个试图访问此资源的线程都有机会得到此互斥对象。

以互斥内核对象来保持线程同步可能用到的函数主要有CreateMutex、OpenMutex、ReleaseMutex、WaitForSingleObject和WaitForMultipleObjects等。在使用互斥对象前，首先要通过CreateMutex或OpenMutex创建或打开一个互斥对象。CreateMutex函数原型如下：

HANDLE CreateMutex(

LPSECURITY_ATTRIBUTES lpMutexAttributes,     // 安全属性指针

BOOL bInitialOwner,                                            // 初始拥有者

LPCTSTR lpName                                               // 互斥对象名

);

参数bInitialOwner主要用来控制互斥对象的初始状态。一般多将其设置为FALSE，以表明互斥对象在创建时并没有为任何线程所占有。如果在创建互斥对象时指定了对象名，那么可以在本进程其他地方或是在其他进程通过OpenMutex函数得到此互斥对象的句柄。OpenMutex函数原型为：

HANDLE OpenMutex(

DWORD dwDesiredAccess, // 访问标志

BOOL bInheritHandle, // 继承标志

LPCTSTR lpName // 互斥对象名

);

当目前对资源具有访问权的线程不再需要访问此资源而要离开时，必须通过ReleaseMutex函数来释放其拥有的互斥对象，其函数原型为：

BOOL ReleaseMutex(HANDLE hMutex);

其惟一的参数hMutex为待释放的互斥对象句柄。至于WaitForSingleObject和WaitForMultipleObjects等待函数在互斥对象保持线程同步中所起的作用与在其他内核对象中的作用是基本一致的，也是等待互斥内核对象的通知。但是这里需要特别指出的是：在互斥对象通知引起调用等待函数返回时，等待函数的返回值不再是通常的WAIT_OBJECT_0（对于WaitForSingleObject函数）或是在WAIT_OBJECT_0到WAIT_OBJECT_0+nCount-1之间的一个值（对于WaitForMultipleObjects函数），而是将返回一个WAIT_ABANDONED_0（对于WaitForSingleObject函数）或是在WAIT_ABANDONED_0到WAIT_ABANDONED_0+nCount-1之间的一个值（对于WaitForMultipleObjects函数），以此来表明线程正在等待的互斥对象由另外一个线程所拥有，而此线程却在使用完共享资源前就已经终止。除此之外，使用互斥对象的方法在等待线程的可调度性上同使用其他几种内核对象的方法也有所不同，其他内核对象在没有得到通知时，受调用等待函数的作用，线程将会挂起，同时失去可调度性，而使用互斥的方法却可以在等待的同时仍具有可调度性，这也正是互斥对象所能完成的非常规操作之一。

在编写程序时，互斥对象多用在对那些为多个线程所访问的内存块的保护上，可以确保任何线程在处理此内存块时都对其拥有可靠的独占访问权。下面给出的示例代码即通过互斥内核对象hMutex对共享内存快g_cArray[]进行线程的独占访问保护。下面是示例代码：

// 互斥对象

HANDLE hMutex = NULL;

char g_cArray[10];

UINT ThreadProc1(LPVOID pParam)

{

// 等待互斥对象通知

WaitForSingleObject(hMutex, INFINITE);

// 对共享资源进行写入操作

for (int i = 0; i < 10; i++)

{

g_cArray[i] = 'a';

Sleep(1);

}

// 释放互斥对象

ReleaseMutex(hMutex);

return 0;

}

UINT ThreadProc2(LPVOID pParam)

{

// 等待互斥对象通知

WaitForSingleObject(hMutex, INFINITE);

// 对共享资源进行写入操作

for (int i = 0; i < 10; i++)

{

g_cArray[10 - i - 1] = 'b';

Sleep(1);

}

// 释放互斥对象

ReleaseMutex(hMutex);

return 0;

}

线程的使用使程序处理能够更加灵活，而这种灵活同样也会带来各种不确定性的可能。尤其是在多个线程对同一公共变量进行访问时。虽然未使用线程同步的程序代码在逻辑上或许没有什么问题，但为了确保程序的正确、可靠运行，必须在适当的场合采取线程同步措施。

### 3.2.6 **线程局部存储**

线程局部存储（thread-local storage, TLS）是一个使用很方便的存储线程局部数据的系统。利用TLS机制可以为进程中所有的线程关联若干个数据，各个线程通过由TLS分配的全局索引来访问与自己关联的数据。这样，每个线程都可以有线程局部的静态存储数据。

用于管理TLS的数据结构是很简单的，Windows仅为系统中的每一个进程维护一个位数组，再为该进程中的每一个线程申请一个同样长度的数组空间，如图3.9所示。

 

图3.9 TSL机制在内部使用的数据结构

运行在系统中的每一个进程都有图3.9所示的一个位数组。位数组的成员是一个标志，每个标志的值被设为FREE或INUSE，指示了此标志对应的数组索引是否在使用中。Windodws保证至少有TLS_MINIMUM_AVAILABLE（定义在WinNT.h文件中）个标志位可用。

动态使用TLS的典型步骤如下。

（1）主线程调用TlsAlloc函数为线程局部存储分配索引，函数原型为：

DWORD TlsAlloc(void); // 返回一个TLS索引

如上所述，系统为每一个进程都维护着一个长度为TLS_MINIMUM_AVAILABLE的位数组，TlsAlloc的返回值就是数组的一个下标（索引）。这个位数组的惟一用途就是记忆哪一个下标在使用中。初始状态下，此位数组成员的值都是FREE，表示未被使用。当调用TlsAlloc的时候，系统会挨个检查这个数组中成员的值，直到找到一个值为FREE的成员。把找到的成员的值由FREE改为INUSE后，TlsAlloc函数返回该成员的索引。如果不能找到一个值为FREE的成员，TlsAlloc函数就返回TLS_OUT_OF_INDEXES（在WinBase.h文件中定义为－1），意味着失败。

例如，在第一次调用TlsAlloc的时候，系统发现位数组中第一个成员的值是FREE，它就将此成员的值改为INUSE，然后返回0。

当一个线程被创建时，Windows就会在进程地址空间中为该线程分配一个长度为TLS_MINIMUM_AVAILABLE的数组，数组成员的值都被初始化为0。在内部，系统将此数组与该线程关联起来，保证只能在该线程中访问此数组中的数据。如图3.7所示，每个线程都有它自己的数组，数组成员可以存储任何数据。

（2）每个线程调用TlsSetValue和TlsGetValue设置或读取线程数组中的值，函数原型为：

BOOL TlsSetValue(

DWORD dwTlsIndex,     // TLS 索引

LPVOID lpTlsValue                   // 要设置的值

);

LPVOID TlsGetValue(DWORD dwTlsIndex );       // TLS索引

TlsSetValue函数将参数lpTlsValue指定的值放入索引为dwTlsIndex的线程数组成员中。这样，lpTlsValue的值就与调用TlsSetValue函数的线程关联了起来。此函数调用成功，会返回TRUE。

调用TlsSetValue函数，一个线程只能改变自己线程数组中成员的值，而没有办法为另一个线程设置TLS值。到现在为止，将数据从一个线程传到另一个线程的惟一方法是在创建线程时使用线程函数的参数。

TlsGetValue函数的作用是取得线程数组中索引为dwTlsIndex的成员的值。

TlsSetValue和TlsGetValue分别用于设置和取得线程数组中的特定成员的值，而它们使用的索引就是TlsAlloc函数的返回值。这就充分说明了进程中惟一的位数组和各线程数组的关系。例如，TlsAlloc返回3，那就说明索引3被此进程中的每一个正在运行的和以后要被创建的线程保存起来，用以访问各自线程数组中对应的成员的值。

（3）主线程调用TlsFree释放局部存储索引。函数的惟一参数是TlsAlloc返回的索引。

利用TLS可以给特定的线程关联一个数据。比如下面的例子将每个线程的创建时间与该线程关联了起来，这样，在线程终止的时候就可以得到线程的生命周期。整个跟踪线程运行时间的例子的代码如下：

|      |
| ---- |
|      |



`#include <stdio.h>                                   // 03UseTLS工程下`

`\#include <windows.h>`            

`\#include <process.h>`

`// 利用TLS跟踪线程的运行时间`

`DWORD g_tlsUsedTime;`

`void InitStartTime();`

`DWORD GetUsedTime();`

`UINT __stdcall ThreadFunc(LPVOID)`

`{       int i;`

​         `// 初始化开始时间`

​         `InitStartTime();`

​         `// 模拟长时间工作`

​         `i = 10000*10000;`

​         `while(i--){}`

​         `// 打印出本线程运行的时间`

​         `printf(" This thread is coming to end. Thread ID: %-5d, Used Time: %d \n",`

​                                                                                                       `::GetCurrentThreadId(), GetUsedTime());`

​         `return 0;`

`}`

`int main(int argc, char* argv[])`

`{       UINT uId;`

​         `int i;`

​         `HANDLE h[10];`

​         `// 通过在进程位数组中申请一个索引，初始化线程运行时间记录系统`

​         `g_tlsUsedTime = ::TlsAlloc();`

​         `// 令十个线程同时运行，并等待它们各自的输出结果`

​         `for(i=0; i<10; i++)`

​         `{       h[i] = (HANDLE)::_beginthreadex(NULL, 0, ThreadFunc, NULL, 0, &uId);         }`

​         `for(i=0; i<10; i++)`

​         `{       ::WaitForSingleObject(h[i], INFINITE);`

​                   `::CloseHandle(h[i]);      }`

​         `// 通过释放线程局部存储索引，释放时间记录系统占用的资源`

​         `::TlsFree(g_tlsUsedTime);`

​         `return 0;`

`}`

`// 初始化线程的开始时间`

`void InitStartTime()`

`{       // 获得当前时间，将线程的创建时间与线程对象相关联`

​         `DWORD dwStart = ::GetTickCount();`

​         `::TlsSetValue(g_tlsUsedTime, (LPVOID)dwStart);`

`}`

`// 取得一个线程已经运行的时间`

`DWORD GetUsedTime()`

`{       // 获得当前时间，返回当前时间和线程创建时间的差值`

​         `DWORD dwElapsed = ::GetTickCount();`

​         `dwElapsed = dwElapsed - (DWORD)::TlsGetValue(g_tlsUsedTime);`

​         `return dwElapsed;`

### `}`

GetTickCount函数可以取得Windows从启动开始经过的时间，其返回值是以毫秒为单位的已启动的时间。

一般情况下，为各线程分配TLS索引的工作要在主线程中完成，而分配的索引值应该保存在全局变量中，以方便各线程访问。上面的例子代码很清除地说明了这一点。主线程一开始就使用TlsAlloc为时间跟踪系统申请了一个索引，保存在全局变量g_tlsUsedTime中。之后，为了示例TLS机制的特点同时创建了10个线程。这10个线程最后都打印出了自己的生命周期，如图3.10所示。

 

### 3.10 各线程的生命周期

这个简单的线程运行时间记录系统仅提供InitStartTime和GetUsedTime两个函数供用户使用。应该在线程一开始就调用InitStartTime函数，此函数得到当前时间后，调用TlsSetValue将线程的创建时间保存在以g_tlsUsedTime为索引的线程数组中。当想查看线程的运行时间时，直接调用GetUsedTime函数就行了。这个函数使用TlsGetValue取得线程的创建时间，然后返回当前时间和创建时间的差值。

 

来自 <<https://www.cnblogs.com/findumars/p/5625075.html>> 

 

# 
