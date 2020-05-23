# 最简单的迭代器

C++ 的迭代器与 Python 的迭代器不同，它并不提出一套新的接口，而是尽可能模仿指针的行为。而一个指针最基本的功能是访问它指向的元素。仅支持这一个功能还不够，为了能够 **迭代**，还需要至少支持指针的自增操作 `++i`。

我们可以为一个整数数组写一个最简单的迭代器，它仅提供访问数组元素和自增的功能：

```
class ArrayIterator {
 public:
  // 从一个数组创建一个迭代器，并且让迭代器指向 pos 指定的位置
  ArrayIterator(int* array, int pos): array_(array), pos_(pos) {}
  
  // 访问当前数组元素
  int& operator*() const {
    return array_[pos_];
  }
  
  // 移动到下一个数组元素
  ArrayIterator& operator++() {
    pos_++;
    return *this;
  }
 private:
  int* array_;
  int pos_;
};
```

下面，我们可以用这个迭代器来访问数组元素，就像使用指针一样，但功能比指针局限得多：

```
void access_array() {
  int array[] = { 1, 2, 3, 4 };
  ArrayIterator it(array, 0);
  printf("array[0] = %d\n", *it);  // 访问第0元素
  ++it;                            // 指向下一个元素
  printf("array[1] = %d\n", *it);  // 访问第1元素
}
```

从这个例子我们可以看出，**迭代器在接口上尽可能模拟指针的行为**。这正是 C++ 迭代器的主要设计思路。

## 迭代器的种类

指针非常灵活，不但可以指向某个内存位置，还可以加上一个偏移量来访问内存的其他位置。而不是所有的容器都支持这些操作，比如随机访问任意位置对于指针都是 O(1) 时间复杂度，而对于链表，则是 O(n) 时间复杂度。因此，让链表的迭代器支持加偏移量的操作就不合理，因为对于 `i + n` 这个运算，人们会默认它的复杂度为常数。

将所有功能一一去除，一个迭代器需要至少支持两个功能才有用：

1. 访问当前元素 `*i` 
2. 前缀自增操作 `++i` （前缀自增和后缀自增是两个操作符）

我们根据迭代器能够提供的额外功能，将其分成五类：

### 1. 输入迭代器 (input iterator)

输入迭代器用于从一个对象中不断读出元素。

除了迭代器基本操作，还需要支持：

1. 比较两个迭代器是否指向相同元素 `i == j` 和 `i != j` 
2. 访问元素的成员 `i->m` 
3. 后缀自增操作 `i++` 

输入迭代器不需要保证自增操作之后，之前的迭代器依然有意义。典型的例子是用于读取流文件的迭代器：每次自增之后，都无法回复到原来的位置。也包括随机数生成器的迭代器：每次自增之后，随机数生成器的状态都发生了变化。

### 2. 输出迭代器 (output iterator)

输出迭代器用于向一个对象不断添加元素。

除了迭代器基本操作，还需要支持：

1. 修改元素 `*i = v` 
2. 后缀自增操作 `i++` 

输出迭代器也不保证自增之后，之前的迭代器有意义，并且它还不保证修改元素之后访问元素有意义。典型的例子是用于写入流文件的迭代器和向容器中插入元素的 **插入迭代器 (insert iterator)**。

### 3. 前向迭代器 (forward iterator)

前向迭代器用于访问一个容器中的元素。

因此，它必须提供输入迭代器的所有操作，如果它用于访问一个非 const 容器，还需要支持输出迭代器的所有操作。

在此基础上，它需要保证自增之后，其他的迭代器仍然有意义（比输入迭代器要求更高）。它也需要保证可以不受限制地修改和访问当前元素（比输出迭代器要求更高）。

典型的例子包括各种容器的迭代器，比如 vector、list、map 的迭代器。

### 4. 双向迭代器 （bidirectional iterator）

双向迭代器首先是一个前向迭代器，除此之外，它还需要支持自减操作 `--i` 和 `i--` 。

一个线性存储元素的容器应该提供双向迭代器，例如 vector 和 list。

### 5. 随机访问迭代器 (random access iterator)

随机访问迭代器是所有迭代器种类中最强大的，它除了需要支持前向迭代器的所有操作，还支持加上任意偏移量并得到新的迭代器，即 `i + n`，其中 `n` 可以是正数也可以是负数，分别表示向前或向后随机访问。

它需要支持的完整操作包括：

1. 加上或减去一个偏移量 `i + n` 和 `i - n` 
2. 自加或自减一个偏移量 `i += n` 和 `i -= n` 
3. 计算两个迭代器的距离 `i - j` 
4. 使用下标形式的加上一个偏移量 `i[n]`，其效果等价于 `*(i + n)` 
5. 比较两个迭代器的先后顺序 `a < b` `a <= b` `a > b` `a >= b` 

我们可以发现，随机访问迭代器在功能上已经等价于指针。

一般来说，只有 vector 这类线性且连续存储元素的容器才会提供随机访问迭代器。

## 如何写出通用的操作函数

迭代器的用途是让程序员写出通用的操作函数。比如，不管是什么容器，我们通常都有将它的所有元素拷贝到另一容器的需求。在有迭代器之前，我们需要为每种容器都写一个循环，而有了迭代器，我们可以写出一个通用的拷贝函数。

为此，我们首先需要使用函数模版，因为迭代器的类型是未知的。我们需要两个输入迭代器，分别表示拷贝的起点和终点，以及一个输出迭代器。因此，我们的拷贝函数接受三个参数，其中前两个参数的类型是相同的。

```
template <class InputIt, class OutputIt>
// requires InputIterator<InputIt> && OutputIterator<OutputIt>
OutputIt copy(InputIt first, InputIt last, OutputIt d_first) {
  while (first != last) {
    *d_first++ = *first++;
  }
  return d_first;
}
```

如果将 InputIt 和 OutputIt 替换成指针，函数仍然可以编译，这说明我们的实现是正确的。

我们在 template 和函数名之间插入了一行注释，用于说明 InputIt 和 OutputIt 应该满足什么条件，即 InputIt 必须是输入迭代器，OutputIt 必须是输出迭代器。虽然目前该代码被注释掉，没有实际用途，但是 C++20 可能会支持 concepts，去掉注释之后，这行声明就是使用 concepts 约束模版类型的语法。使用 requires 表达式后，C++ 编译器会在模版实例化时帮助我们检查 InputIt 和 OutputIt 的具体类型是否满足这两类迭代器的条件。

C++ 已经为我们实现了一组通用的操作函数，定义在头文件 `<algorithm>` 中。常用的函数可以分成以下 7 类：

1. 计数：count count_if
2. 检查条件：all_of any_of none_of
3. 遍历：for_each for_each_n
4. 查找：find find_if find_if_not
5. 拷贝：copy copy_if copy_n
6. 填充同一元素：fill fill_n
7. 元素变换（map 操作）：transform

头文件 `<algorithm>` 中还定义了许多函数，在此不一一列出，可以浏览
 [C++ Reference](https://link.jianshu.com?t=http://en.cppreference.com/w/cpp/algorithm)
 来查看所有函数。

## C++ STL 风格迭代器

虽然我们了解了迭代器的种类，但我们到目前仍然无法写出完全符合 C++ STL 风格的迭代器。

对于一个迭代器类型 **T**，我们会关心和它相关的如下信息：

1. 它是哪种类型的迭代器；
2. 它指向的数据类型是什么；
3. 这个数据类型的引用类型是什么；
4. 这个数据类型的指针类型是什么；
5. 两个迭代器的距离用什么类型表示。

这些信息通过迭代器类的内部类型定义来呈现，因此，一个完整的迭代器应该包含如下定义：

```
#include <iterator>

class ArrayIterator {
 public:
  typedef std::random_access_iterator_tag iterator_category;  // 迭代器类型
  typedef int value_type;        // 数据类型
  typedef int& reference_type;   // 数据类型的引用
  typedef int* pointer_type;     // 数据类型的指针
  typedef std::ptrdiff_t difference_type;  // 距离类型

  // 迭代器的实现
};
```

然而，如果为每个迭代器都写这些类型定义又十分繁琐，因此，STL 提供了 **iterator** 类模版来简化迭代器的定义。我们可以将这四行类型定义用继承 **iterator** 类模版的方式来替代，如下所示：

```
#include <iterator>

class ArrayIterator : 
    public std::iterator<std::random_access_iterator_tag, int> {
  // 迭代器的实现
};
```

不过因为 **std::iterator** 的名字会让程序员误以为迭代器一定要继承这个类，以及误导程序员写出接受 **std::iterator** 类型的函数等原因，从 C++17 起，**std::iterator** 会被弃用 (deprecated)。因此，我们并不建议在实际场景中使用这个类模版，而建议自己定义一个类模版来用。

## 小结

1. C++ 的迭代器在接口上模拟指针；
2. 迭代器按功能分成五类： 
   1. 输入迭代器：从对象中不断读出元素
   2. 输出迭代器：向对象不断添加元素
   3. 前向迭代器：单向遍历容器中的元素
   4. 双向迭代器：双向遍历容器中的元素
   5. 随机访问迭代器：随机访问容器中任意位置的元素
3. 可以基于迭代器写出通用的容器操作；
4. 迭代器要求五个类型定义： 
   1. 迭代器类型 iterator_category
   2. 数据类型 value_type
   3. 数据类型的引用 reference_type
   4. 数据类型的指针 pointer_type
   5. 迭代器的距离类型 difference_type

作者：番茄吐司君

链接：https://www.jianshu.com/p/40e40aef2305

来源：简书

简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
