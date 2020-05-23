# c++ chrono：处理时间的类

# 1. 用std::chrono::duration表示一段时间。

## duration的定义方式

```C++
typedef duration<long long> seconds;
typedef duration<int, ratio<60> > minutes;
```

第一个参数`int`表示用类型保存**时间间隔**，第二个参数`ratio<60>`是个有理数，表示一个**时间间隔**等于多少秒。这里一分钟就定义为60秒。库里面定义了常用的类型，毫秒，秒，小时等等。

## 定义一个心跳的duration，然后不同的duration可以互相换算

定义心跳的duration: `using heartbeats = std::chrono::duration < int, std::ratio < 3, 4 >>;`，`std::ratio < 3, 4 >`表示每四分之三秒跳一次。
 定义一个用浮点计数的`minutes`类型，计算跳动123次等于多少分钟。

```C++
    using minutes = std::chrono::duration<double, ratio<60> >;
    heartbeats beat(123);
    cout << minutes(beat).count() << endl;
```

计算每小时跳动多少次，std::chrono::hours为标准库预定义好的类型。

```c++
    std::chrono::hours hour(1);
    cout << heartbeats(hour).count() << endl;
```

## duration的计算。

```C++
    std::chrono::seconds s(10);
    std::chrono::minutes m(2);
```

duration可以是负数：`std::chrono::seconds s(-10);`
 两个duration可以加减，结果是共同的类型，秒。秒可以表示分 `cout << (m + s).count();`
 duration可以乘除一个数字，结果还是duration;`s *= 3;`
 duration可以除和%另外一个duration，返回一个数值. `cout << m / s;`。等同于2分钟包含多少个10秒钟。

```C++
    using namespace std::chrono;
    seconds sec(10);
    minutes minu(-2);
    sec += minu;
```

定义一个十秒的duration: `std::chrono::seconds sec(10);`

## C++14，chrono literals。方便的表示时间。

```C++
    using namespace std::chrono_literals;
    auto day = 24h;
    auto halfhour = 0.5h;
```

# 2. Clock记时的方法，由一个时钟起点和计时单位组成。

### system_clock，系统时钟，用来处理真实的时间的，可是和`time_t`类型互相转换。

```C++
    system_clock::time_point today = system_clock::now();
    system_clock::time_point tomorrow = today + hours(24);
```

### steady_clock 是稳定的时钟，用来计算时间间隔的。

`system_clock`不适合来计算时间间隔，因为系统时间可以改变的。
 `steady_clock::period`是个有理数，表示`steady_clock`计时最短时间间隔，单位为秒。这里打印出来的是1和10000000，也就是1/10,000,000之一秒，100 nano seconds。

```c++
 cout << steady_clock::period::num << endl;
 cout << steady_clock::period::den << endl;
```

`end - start`的结果是duration类型，`elapsed.count()`可以等同理解为经过了多少`100 nano seconds`.

```C++
    steady_clock::time_point start = steady_clock::now();
    std::this_thread::sleep_for(std::chrono::seconds(2));
    steady_clock::time_point end = steady_clock::now();
    
    auto elapsed = end - start;
    cout << endl << elapsed.count() << endl;
    cout << duration<double>(elapsed).count() << endl; // converts to seconds
```

### high_resolution_clock 高精度时钟

和steady_clock没本质区别，也许和stead_clock是一样的实现。

# 3. Time points表示具体的某个时间点。

`time_point`类用两个参数组成，Clock和Duration。
 比如`steady_clock::time_point`的定义就是`typedef chrono::time_point time_point;`。这里模板参数`Duration`省略了，使用了默认的值`typename _Clock::duration`
 Time point可以互相比较大小，可以和duration做加减运算得到一个新的Time point.

```c++
system_clock::time_point tomorrow = system_clock::now() + hours(24);
```

# 4. 用std::get_time和std::put_time处理时间和字符串。

```C++
    using namespace std::chrono;
    auto now = system_clock::now();
    time_t t = system_clock::to_time_t(now);
    std::tm tm = *std::localtime(&t);
    auto time = std::put_time(&tm, "%b %d %Y %H:%M:%S");
```

`std::localtime`返回的指针不需要delete。因为它指向的是某个static对象，所以`localtime`是线程不安全的。可以考虑使用非标准函数`localtime_s`
 `put_time`可以把`std::tm`变成一个特殊的对象。这个对象可以根据不同的场景转换成需要的对象。

```C++
    std::cout << time << std::endl;
    std::stringstream ss;
    ss << time;
```

利用`std::get_time`可以把string变回`system_clock`

```C++
ss >> std::get_time(&tm, "%b %d %Y %H:%M:%S");
auto now2 = std::chrono::system_clock::from_time_t(std::mktime(&tm));
```

可以看到两次转换以后，损失了小于一秒的部分。

```C++
    duration<double> diff = now - now2;
    std::cout << diff.count() << std::endl;
```