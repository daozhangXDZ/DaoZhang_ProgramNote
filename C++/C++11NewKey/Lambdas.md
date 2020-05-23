# [C++11 带来的新特性 （4）—— 匿名函数（Lambdas）](https://www.cnblogs.com/sword03/p/10022964.html)             

## 1 语法

Lambdas并不是新概念，在其它语言中已经烂大街了。直接进入主题，先看语法：

```
[ captures ] ( params ) specifiers exception attr -> ret { body }    (1) 
[ captures ] ( params ) -> ret { body }                              (2) 
[ captures ] ( params ) { body }                                     (3) 
[ captures ] { body }                                                (4) 
```

- captures：捕获参数。详细格式见下图。

| 格式    | 意义                                            |
| ------- | ----------------------------------------------- |
| []      | 默认不捕获任何变量                              |
| [=]     | 默认以值捕获所有变量                            |
| [&]     | 默认以引用捕获所有变量                          |
| [x]     | 仅以值捕获x，其它变量不捕获                     |
| [&x]    | 仅以引用捕获x，其它变量不捕获                   |
| [=, &x] | 默认以值捕获所有变量，但是x是例外，通过引用捕获 |
| [&, x]  | 默认以引用捕获所有变量，但是x是例外，通过值捕获 |
| [this]  | 通过引用捕获当前对象（其实是复制指针）          |
| [*this] | 通过传值方式捕获当前对象                        |

- params：参数列表。
- ret：返回类型。
- body：函数体。
- specifiers：限定符列表。比如mutable。
- exception：异常规定。比如noexcept。
- attr：属性规定，[详见](https://zh.cppreference.com/w/cpp/language/attributes)。

## 2 使用

Lambdas重在使用，所以下面直接上实例，由浅入深的介绍使用方法。

### 2.1 打印字符串

- 定义一个匿名函数

```
[]{
    std::cout<< "hello world!" <<std::endl;
}
```

- 调用匿名函数

```
[]{
    std::cout<< "hello world!" <<std::endl;
}();
```

- 传递匿名函数给一个变量

```
auto l = []{
    std::cout<< "hello world!" <<std::endl;
};
l();
```

### 2.2 带参数列表的匿名函数

```
auto l = [](const std::string &s){
    std::cout<< s <<std::endl;
};
l("hello world!");
```

### 2.3 指定返回值类型的匿名函数

```
[] -> double{
    return 42;
}
```

等价于

```
[]{
    return 42;
}
```

如果不指定返回类型，C++11也可以自动推断类型。

### 2.4 带捕获参数的匿名函数

- 捕获变量值+捕获变量引用

```
int x = 0;
int y = 42;
auto f = [x, &y] {
            std::cout<<"x:" << x << std::endl;
            std::cout<<"y:" << y << std::endl;
            ++y;
            //++x;//Error
         };
x = y = 77;
f();
f();
std::cout<< "final y: " << y <<std::endl;
```

输出

```
x:0
y:77
x:0
y:78
final y: 79
```

- 捕获所有变量值

```
int x = 0;
int y = 42;
auto f = [=] {
            std::cout<<"x:" << x << std::endl;
            std::cout<<"y:" << y << std::endl;
            //++y;//Error
            //++x;//Error
         };
x = y = 77;
f();
f();
std::cout<< "final y: " << y <<std::endl;
```

输出

```
x:0
y:42
x:0
y:42
final y: 77
```

- 捕获所有变量引用

```
int x = 0;
int y = 42;
auto f = [&] {
            std::cout<<"x:" << x << std::endl;
            std::cout<<"y:" << y << std::endl;
            ++y;//Error
            ++x;//Error
         };
x = y = 77;
f();
f();
std::cout<< "final x: " << x <<std::endl;
std::cout<< "final y: " << y <<std::endl;
```

输出

```
x:77
y:77
x:78
y:78
final x: 79
final y: 79
```

### 2.5 使用匿名函数统计容器中所有元素的值之和

```
std::vector<int> vec = { 1, 2, 3, 4, 5 };
double total = 0;

//inclucde 'algorithm' for foreach
std::foreach(begin(vec), end(vec),
    [&](int x) {
        total += x;
    });
std::cout<<"total:"<< total <<std::endl;
```

输出：

```
total:15
```

### 2.6 使用匿名函数对容器中的元素排序

```
struct Point{
    double x,y;
    Point(){
        x = (rand() % 10000) - 5000;
        y = (rand() % 10000) - 5000;
    }

    void Print(){
        std::cout<<"["<<x<<","<<y<<"]"<<std::endl;
    }
};


int count = 10;
std::vector<Point> points;
for( auto i = 0; i < 10 ; i++ ) points.push_back(Point());

cout<<"Unsorted:"<<endl;
for( auto i = 0; i < 10 ; i++ ) points[i].Print();

std::sort(points.begin(), points.end(),
    [](const Point& a, const Point& b) -> bool{
        return (a.x * a.x) + (a.y * a.y) < (b.x * b.x) + (b.y * b.y);
    });
cout<<"Sorted:"<<endl;
for( auto i = 0; i < 10 ; i++ ) points[i].Print();
```

输出：

```
Unsorted:
[4383,-4114]
[-2223,1915]
[2793,3335]
[386,-4508]
[1649,-3579]
[-2638,-4973]
[3690,-4941]
[2763,-1074]
[-4460,-1574]
[4172,736]
Sorted:
[-2223,1915]
[2763,-1074]
[1649,-3579]
[4172,736]
[2793,3335]
[386,-4508]
[-4460,-1574]
[-2638,-4973]
[4383,-4114]
[3690,-4941]
```

### 2.7 返回匿名函数类型

```
//include<functional>
std::function<int(int,int)> returnLambda (){
    return [](int x, int y){
                return x*y;
            };
}

auto lf = returnLambda();
std::cout<< lf(6,7) << std::endl;
```

### 2.8 奇怪的捕获变量作用域

```
void PerformOperation( function<void()> f ){
    f();
}

int main(){
    int x = 100;
    auto func = [&](){ x++;};
    PerformOperation(func);
    std::cout<< "x:" << x << std::endl;
    return 0;
}
```

输出：

```
x:101
```