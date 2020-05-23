# 标准库头文件 <chrono>

此头文件是[日期和时间](https://zh.cppreference.com/w/cpp/chrono)库的一部分。

###  类

| 定义于命名空间 `std::chrono`                                 |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [ duration](https://zh.cppreference.com/w/cpp/chrono/duration)(C++11) | 时间区间   (类模板)                                          |
| [ system_clock](https://zh.cppreference.com/w/cpp/chrono/system_clock)(C++11) | 来自系统范畴实时时钟的挂钟时间   (类)                        |
| [ steady_clock](https://zh.cppreference.com/w/cpp/chrono/steady_clock)(C++11) | 决不会调整的单调时钟   (类)                                  |
| [ high_resolution_clock](https://zh.cppreference.com/w/cpp/chrono/high_resolution_clock)(C++11) | 拥有可用的最短嘀嗒周期的时钟   (类)                          |
| [ time_point](https://zh.cppreference.com/w/cpp/chrono/time_point)(C++11) | 时间中的点   (类模板)                                        |
| [ treat_as_floating_point](https://zh.cppreference.com/w/cpp/chrono/treat_as_floating_point) | 指示时长可转换为拥有不同嘀嗒周期的时长   (类模板)            |
| [ duration_values](https://zh.cppreference.com/w/cpp/chrono/duration_values) | 构造给定类型的嘀嗒计数的零、最小及最大值   (类模板)          |
| 便利 typedef                                                 |                                                              |
| 定义于命名空间 `std::chrono`                                 |                                                              |
| [std::chrono::nanoseconds](https://zh.cppreference.com/w/cpp/chrono/duration) | Period 为 [std::nano](https://zh.cppreference.com/w/cpp/numeric/ratio/ratio) 的时长类型 |
| [std::chrono::microseconds](https://zh.cppreference.com/w/cpp/chrono/duration) | Period 为 [std::micro](https://zh.cppreference.com/w/cpp/numeric/ratio/ratio) 的时长类型 |
| [std::chrono::milliseconds](https://zh.cppreference.com/w/cpp/chrono/duration) | Period 为 [std::milli](https://zh.cppreference.com/w/cpp/numeric/ratio/ratio) 的时长类型 |
| [std::chrono::seconds](https://zh.cppreference.com/w/cpp/chrono/duration) | Period 为 [std::ratio](http://zh.cppreference.com/w/cpp/numeric/ratio/ratio)<1> 的时长类型 |
| [std::chrono::minutes](https://zh.cppreference.com/w/cpp/chrono/duration) | Period 为 [std::ratio](http://zh.cppreference.com/w/cpp/numeric/ratio/ratio)<60> 的时长类型 |
| [std::chrono::hours](https://zh.cppreference.com/w/cpp/chrono/duration) | Period 为 [std::ratio](http://zh.cppreference.com/w/cpp/numeric/ratio/ratio)<3600> 的时长类型 |
| 特化                                                         |                                                              |
| 定义于命名空间 `std`                                         |                                                              |
| [ std::common_type](https://zh.cppreference.com/w/cpp/chrono/duration/common_type) | 特化 [std::common_type](https://zh.cppreference.com/w/cpp/types/common_type) 特征   (类模板特化) |
| [ std::common_type](https://zh.cppreference.com/w/cpp/chrono/time_point/common_type) | 特化 [std::common_type](https://zh.cppreference.com/w/cpp/types/common_type) 特征   (类模板特化) |

###  函数

| duration                                                     |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 定义于命名空间 `std::chrono`                                 |                                                              |
| [ operator+operator-operator*operator/operator%](https://zh.cppreference.com/w/cpp/chrono/duration/operator_arith4) | 实现以时长为实参的算术运算   (函数模板)                      |
| [ operator==operator!=operatoroperator>=](https://zh.cppreference.com/w/cpp/chrono/duration/operator_cmp) | 比较两个时长   (函数模板)                                    |
| [ duration_cast](https://zh.cppreference.com/w/cpp/chrono/duration/duration_cast) | 转换时长到另一个拥有不同嘀嗒间隔的时长   (函数模板)          |
| [ floor(std::chrono::duration)](https://zh.cppreference.com/w/cpp/chrono/duration/floor)(C++17) | 以向下取整的方式，将一个时长转换为另一个时长    (函数模板)   |
| [ ceil(std::chrono::duration)](https://zh.cppreference.com/w/cpp/chrono/duration/ceil)(C++17) | 以向上取整的方式，将一个时长转换为另一个时长    (函数模板)   |
| [ round(std::chrono::duration)](https://zh.cppreference.com/w/cpp/chrono/duration/round)(C++17) | 转换时长到另一个时长，就近取整，偶数优先   (函数模板)        |
| [ abs(std::chrono::duration)](https://zh.cppreference.com/w/cpp/chrono/duration/abs)(C++17) | 获取时长的绝对值    (函数模板)                               |
| time_point                                                   |                                                              |
| 定义于命名空间 `std::chrono`                                 |                                                              |
| [ operator+operator-](https://zh.cppreference.com/w/cpp/chrono/time_point/operator_arith2) | 实施涉及时间点的加法和减法运算   (函数模板)                  |
| [ operator==operator!=operatoroperator>=](https://zh.cppreference.com/w/cpp/chrono/time_point/operator_cmp) | 比较两个时间点   (函数模板)                                  |
| [ time_point_cast](https://zh.cppreference.com/w/cpp/chrono/time_point/time_point_cast) | 转换时间点为同一时钟上拥有不同时长的另一时间点   (函数模板)  |
| [ floor(std::chrono::time_point)](https://zh.cppreference.com/w/cpp/chrono/time_point/floor)(C++17) | 转换 time_point 到另一个，向下取整   (函数模板)              |
| [ ceil(std::chrono::time_point)](https://zh.cppreference.com/w/cpp/chrono/time_point/ceil)(C++17) | 转换 time_point 到另一个，向上取整   (函数模板)              |
| [ round(std::chrono::time_point)](https://zh.cppreference.com/w/cpp/chrono/time_point/round)(C++17) | 转换 time_point 到另一个，就近取整，偶数优先   (函数模板)    |
| 字面量                                                       |                                                              |
| 定义于内联命名空间 `std::literals::chrono_literals`          |                                                              |
| [ operator""h](https://zh.cppreference.com/w/cpp/chrono/operator""h)(C++14) | 表示小时的 [std::chrono::duration](https://zh.cppreference.com/w/cpp/chrono/duration) 字面量   (函数) |
| [ operator""min](https://zh.cppreference.com/w/cpp/chrono/operator""min)(C++14) | 表示分钟的 [std::chrono::duration](https://zh.cppreference.com/w/cpp/chrono/duration) 字面量   (函数) |
| [ operator""s](https://zh.cppreference.com/w/cpp/chrono/operator""s)(C++14) | 表示秒的 [std::chrono::duration](https://zh.cppreference.com/w/cpp/chrono/duration) 字面量   (函数) |
| [ operator""ms](https://zh.cppreference.com/w/cpp/chrono/operator""ms)(C++14) | 表示毫秒的 [std::chrono::duration](https://zh.cppreference.com/w/cpp/chrono/duration) 字面量   (函数) |
| [ operator""us](https://zh.cppreference.com/w/cpp/chrono/operator""us)(C++14) | 表示微秒的 [std::chrono::duration](https://zh.cppreference.com/w/cpp/chrono/duration) 字面量   (函数) |
| [ operator""ns](https://zh.cppreference.com/w/cpp/chrono/operator""ns)(C++14) | 表示纳秒的 [std::chrono::duration](https://zh.cppreference.com/w/cpp/chrono/duration) 字面量   (函数) |

###  概要

```c++
namespace std {
  namespace chrono {
    // 类模板 duration
    template <class Rep, class Period = ratio<1>> class duration;
    // 类模板 time_point
    template <class Clock, class Duration = typename Clock::duration> class time_point;
  }
  // common_type 特化
  template <class Rep1, class Period1, class Rep2, class Period2>
  struct common_type<chrono::duration<Rep1, Period1>,
                     chrono::duration<Rep2, Period2>>;
  template <class Clock, class Duration1, class Duration2>
  struct common_type<chrono::time_point<Clock, Duration1>,
                     chrono::time_point<Clock, Duration2>>;
  namespace chrono {
    // 定制的特征
    template <class Rep> struct treat_as_floating_point;
    template <class Rep> struct duration_values;
    template <class Rep>
    constexpr bool treat_as_floating_point_v = treat_as_floating_point<Rep>::value;
    // duration 算术
    template <class Rep1, class Period1, class Rep2, class Period2>
    common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
    constexpr operator+(const duration<Rep1, Period1>& lhs,
                        const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
    common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
    constexpr operator-(const duration<Rep1, Period1>& lhs,
                        const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period, class Rep2>
    duration<common_type_t<Rep1, Rep2>, Period>
    constexpr operator*(const duration<Rep1, Period>& d,
                        const Rep2& s);
    template <class Rep1, class Rep2, class Period>
    duration<common_type_t<Rep1, Rep2>, Period>
    constexpr operator*(const Rep1& s,
                        const duration<Rep2, Period>& d);
    template <class Rep1, class Period, class Rep2>
    duration<common_type_t<Rep1, Rep2>, Period>
    constexpr operator/(const duration<Rep1, Period>& d,
                        const Rep2& s);
    template <class Rep1, class Period1, class Rep2, class Period2>
    common_type_t<Rep1, Rep2>
    constexpr operator/(const duration<Rep1, Period1>& lhs,
                        const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period, class Rep2>
    duration<common_type_t<Rep1, Rep2>, Period>
    constexpr operator%(const duration<Rep1, Period>& d,
                        const Rep2& s);
    template <class Rep1, class Period1, class Rep2, class Period2>
    common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
    constexpr operator%(const duration<Rep1, Period1>& lhs,
                        const duration<Rep2, Period2>& rhs);
    // duration 比较
    template <class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator==(const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator!=(const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator< (const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator<=(const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator> (const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
    constexpr bool operator>=(const duration<Rep1, Period1>& lhs,
                              const duration<Rep2, Period2>& rhs);
    // duration_cast
    template <class ToDuration, class Rep, class Period>
    constexpr ToDuration duration_cast(const duration<Rep, Period>& d);
    template <class ToDuration, class Rep, class Period>
    constexpr ToDuration floor(const duration<Rep, Period>& d);
    template <class ToDuration, class Rep, class Period>
    constexpr ToDuration ceil(const duration<Rep, Period>& d);
    template <class ToDuration, class Rep, class Period>
    constexpr ToDuration round(const duration<Rep, Period>& d);
    // 便利 typedef
    using nanoseconds = duration</* 至少 64 位的有符号整数类型 */ , nano>;
    using microseconds = duration</* 至少 55 位的有符号整数类型 */ , micro>;
    using milliseconds = duration</* 至少 45 位的有符号整数类型 */ , milli>;
    using seconds = duration</* 至少 35 位的有符号整数类型 */ >;
    using minutes = duration</* 至少 29 位的有符号整数类型 */ , ratio< 60>>;
    using hours = duration</* 至少 23 位的有符号整数类型 */ , ratio<3600>>;
    // time_point 算术
    template <class Clock, class Duration1, class Rep2, class Period2>
    constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
    operator+(const time_point<Clock, Duration1>& lhs,
              const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Clock, class Duration2>
    constexpr time_point<Clock, common_type_t<duration<Rep1, Period1>, Duration2>>
    operator+(const duration<Rep1, Period1>& lhs,
              const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Rep2, class Period2>
    constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
    operator-(const time_point<Clock, Duration1>& lhs,
              const duration<Rep2, Period2>& rhs);
    template <class Clock, class Duration1, class Duration2>
    constexpr common_type_t<Duration1, Duration2>
    operator-(const time_point<Clock, Duration1>& lhs,
              const time_point<Clock, Duration2>& rhs);
    // time_point 比较
    template <class Clock, class Duration1, class Duration2>
    constexpr bool operator==(const time_point<Clock, Duration1>& lhs,
                              const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
    constexpr bool operator!=(const time_point<Clock, Duration1>& lhs,
                              const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
    constexpr bool operator< (const time_point<Clock, Duration1>& lhs,
                              const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
    constexpr bool operator<=(const time_point<Clock, Duration1>& lhs,
                              const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
    constexpr bool operator> (const time_point<Clock, Duration1>& lhs,
                              const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
    constexpr bool operator>=(const time_point<Clock, Duration1>& lhs,
                              const time_point<Clock, Duration2>& rhs);
    // time_point_cast
    template <class ToDuration, class Clock, class Duration>
    constexpr time_point<Clock, ToDuration>
    time_point_cast(const time_point<Clock, Duration>& t);
    template <class ToDuration, class Clock, class Duration>
    constexpr time_point<Clock, ToDuration>
    floor(const time_point<Clock, Duration>& tp);
    template <class ToDuration, class Clock, class Duration>
    constexpr time_point<Clock, ToDuration>
    ceil(const time_point<Clock, Duration>& tp);
    template <class ToDuration, class Clock, class Duration>
    constexpr time_point<Clock, ToDuration>
    round(const time_point<Clock, Duration>& tp);
    // 特化的算法
    template <class Rep, class Period>
    constexpr duration<Rep, Period> abs(duration<Rep, Period> d);
    // 时钟
    class system_clock;
    class steady_clock;
    class high_resolution_clock;
  }
  inline namespace literals {
    inline namespace chrono_literals {
      // duration 字面量后缀
      constexpr chrono::hours operator "" h(unsigned long long);
      constexpr chrono::duration</* 未指明 */,
                                 ratio<3600,1>> operator "" h(long double);
      constexpr chrono::minutes operator "" min(unsigned long long);
      constexpr chrono::duration</* 未指明 */,
                                 ratio<60,1>> operator "" min(long double);
      constexpr chrono::seconds operator "" s(unsigned long long);
      constexpr chrono::duration</* 未指明 */ > operator "" s(long double);
      constexpr chrono::milliseconds operator "" ms(unsigned long long);
      constexpr chrono::duration</* 未指明 */,
                                 milli> operator "" ms(long double);
      constexpr chrono::microseconds operator "" us(unsigned long long);
      constexpr chrono::duration</* 未指明 */,
                                 micro> operator "" us(long double);
      constexpr chrono::nanoseconds operator "" ns(unsigned long long);
      constexpr chrono::duration</* 未指明 */, 
                                 nano> operator "" ns(long double);
    }
  }
  namespace chrono {
    using namespace literals::chrono_literals;
  }
```

####  [std::chrono::treat_as_floating_point](http://zh.cppreference.com/w/cpp/chrono/treat_as_floating_point)

```c++
template <class Rep> struct treat_as_floating_point : is_floating_point<Rep> { };
```

####  [std::chrono::duration_values](http://zh.cppreference.com/w/cpp/chrono/duration_values)

```c++
template <class Rep>
struct duration_values {
public:
  static constexpr Rep zero();
  static constexpr Rep min();
  static constexpr Rep max();
};
```

####  [std::chrono::duration](http://zh.cppreference.com/w/cpp/chrono/duration)

```c++
template <class Rep, class Period = ratio<1>>
class duration {
public:
  using rep = Rep;
  using period = Period;
private:
  rep rep_; // 仅用于阐释
public:
  // 构造/复制/销毁
  constexpr duration() = default;
  template <class Rep2>
  constexpr explicit duration(const Rep2& r);
  template <class Rep2, class Period2>
  constexpr duration(const duration<Rep2, Period2>& d);
  ~duration() = default;
  duration(const duration&) = default;
  duration& operator=(const duration&) = default;
  // 探察函数
  constexpr rep count() const;
  // 算术
  constexpr duration operator+() const;
  constexpr duration operator-() const;
  constexpr duration& operator++();
  constexpr duration operator++(int);
  constexpr duration& operator--();
  constexpr duration operator--(int);
  constexpr duration& operator+=(const duration& d);
  constexpr duration& operator-=(const duration& d);
  constexpr duration& operator*=(const rep& rhs);
  constexpr duration& operator/=(const rep& rhs);
  constexpr duration& operator%=(const rep& rhs);
  constexpr duration& operator%=(const duration& rhs);
  // 特殊值
  static constexpr duration zero();
  static constexpr duration min();
  static constexpr duration max();
};
```

####  [std::chrono::time_point](http://zh.cppreference.com/w/cpp/chrono/time_point)

```c++
template <class Clock, class Duration = typename Clock::duration>
class time_point {
public:
  using clock = Clock;
  using duration = Duration;
  using rep = typename duration::rep;
  using period = typename duration::period;
private:
  duration d_; // 仅用于阐释
public:
  // 构造
  constexpr time_point(); // 拥有纪元值
  constexpr explicit time_point(const duration& d); // 同 time_point() + d
  template <class Duration2>
  constexpr time_point(const time_point<clock, Duration2>& t);
  // 探察函数
  constexpr duration time_since_epoch() const;
  // 算术
  constexpr time_point& operator+=(const duration& d);
  constexpr time_point& operator-=(const duration& d);
  // 特殊值
  static constexpr time_point min();
  static constexpr time_point max();
};
```

####  [std::chrono::system_clock](http://zh.cppreference.com/w/cpp/chrono/system_clock)

```c++
class system_clock {
public:
  using rep = /* 见说明 */ ;
  using period = ratio</* 未指明 */, /* 未指明 */ >;
  using duration = chrono::duration<rep, period>;
  using time_point = chrono::time_point<system_clock>;
  static constexpr bool is_steady = /* 未指明 */ ;
  static time_point now() noexcept;
  // 映射到 C API
  static time_t to_time_t (const time_point& t) noexcept;
  static time_point from_time_t(time_t t) noexcept;
};
```

####  [std::chrono::steady_clock](http://zh.cppreference.com/w/cpp/chrono/steady_clock)

```c++
class steady_clock {
public:
  using rep = /* 未指明 */ ;
  using period = ratio</* 未指明 */, /* 未指明 */ >;
  using duration = chrono::duration<rep, period>;
  using time_point = chrono::time_point</* 未指明 */, duration>;
  static constexpr bool is_steady = true;
  static time_point now() noexcept;
};
```

####  [std::chrono::high_resolution_clock](http://zh.cppreference.com/w/cpp/chrono/high_resolution_clock)

```c++
class high_resolution_clock {
public:
  using rep = /* 未指明 */ ;
  using period = ratio</* 未指明 */, /* 未指明 */ >;
  using duration = chrono::duration<rep, period>;
  using time_point = chrono::time_point</* 未指明 */, duration>;
  static constexpr bool is_steady = /* 未指明 */ ;
  static time_point now() noexcept;
};
```