

# _vsnprintf

_vsnprintf是[C语言库函数](https://baike.baidu.com/item/C%E8%AF%AD%E8%A8%80%E5%BA%93%E5%87%BD%E6%95%B0)之一，属于可变参数。用于向字符串中打印数据、数据格式用户自定义。头文件是#include <stdarg.h>。

 

- 中文名

   _vsnprintf [1]  

- 类    型

   [C语言库函数](https://baike.baidu.com/item/C%E8%AF%AD%E8%A8%80%E5%BA%93%E5%87%BD%E6%95%B0)之一 

- 隶    属

   可变参数 

- 作    用

   向字符串中打印数据等 

## 目录

1.  1 [函数简介](https://baike.baidu.com/item/_vsnprintf#1) 
2.  2 [参数说明](https://baike.baidu.com/item/_vsnprintf#2) 
3.  3 [用法实例](https://baike.baidu.com/item/_vsnprintf#3) 
4.  4 [返回值用法](https://baike.baidu.com/item/_vsnprintf#4) 

​    

## 函数简介

编辑

头文件:

\#include <stdarg.h>

函数声明:

int _vsnprintf(char* str, size_t size, const char* format, va_list ap);

​    

## 参数说明

编辑

1. char *str [out],把生成的格式化的字符串存放在这里.
2. size_t size [in], str可接受的最大字符数 [1]  (非字节数，UNICODE一个字符两个字节),防止产生[数组](https://baike.baidu.com/item/%E6%95%B0%E7%BB%84)越界.
3. const char *format [in], 指定输出格式的字符串，它决定了你需要提供的可变参数的类型、个数和顺序。
4. va_list ap [in], va_list变量. va:variable-argument:可变参数

函数功能：将可变参数格式化输出到一个字符数组。

用法类似于vsprintf，不过加了size的限制，防止了内存溢出（size为str所指的存储空间的大小）。

返回值：执行成功，返回最终生成字符串的长度，若生成字符串的长度大于size，则将字符串的前size个字符复制到str，同时将原串的长度返回（不包含终止符）；执行失败，返回负值，并置[*errno*](https://baike.baidu.com/item/errno). [2]  

备注:

linux环境下是:vsnprintf

VC6环境下是:_vsnprintf

​    

## 用法实例

编辑

```c
`#include <stdio.h>``#include <stdarg.h>``int` `mon_log(``char``* format, ...)``{``char` `str_tmp[50];``int` `i=0;``va_list` `vArgList;                            ``//定义一个va_list型的变量,这个变量是指向参数的指针.``va_start` `(vArgList, format);                 ``//用va_start宏初始化变量,这个宏的第二个参数是第一个可变参数的前一个参数,是一个固定的参数``i=_vsnprintf(str_tmp, 50, format, vArgList); ``//注意,不要漏掉前面的_``va_end``(vArgList);                            ``//用va_end宏结束可变参数的获取``return` `i;                                    ``//返回参数的字符个数中间有逗号间隔``}``//调用上面的函数``void` `main()　``{``    ``int` `i=mon_log(``"%s,%d,%d,%d"``,``"asd"``,2,3,4);``    ``printf``(``"%d\n"``,i);``}`
```

输出 9。

asd,2,3,4

123456789 （共9个字符，间隔符逗号计算在内） [2]  

​    

## 返回值用法

编辑

```c
`#include <stdio.h>``#include <stdlib.h>``#include <stdarg.h>``char` `*make_message(``const` `char` `*fmt, ...) ``{``    ``/* 初始时假设我们只需要不超过100字节大小的空间 */``    ``int` `n, size = 100;``    ``char` `*p;``    ``va_list` `ap;``    ``if` `( (p = (``char` `*) ``malloc``(size*``sizeof``(``char``))) == NULL)``    ``return` `NULL;``    ``while` `(1) ``    ``{``        ``/* 尝试在申请的空间中进行打印操作 */``        ``va_start``(ap, fmt);``        ``n = vsnprintf (p, size, fmt, ap);``        ``va_end``(ap);``        ``/* 如果vsnprintf调用成功，返回该字符串 */``        ``if` `(n > -1 && n < size)``        ``return` `p;``        ``/* vsnprintf调用失败(n<0)，或者p的空间不足够容纳size大小的字符串(n>=size)，尝试申请更大的空间*/``        ``size *= 2; ``/* 两倍原来大小的空间 */``        ``if` `((p = (``char` `*)``realloc``(p, size*``sizeof``(``char``))) == NULL)``        ``return` `NULL;``    ``}``}``int` `main() ``{``    ``/* 调用上面的函数 */``    ``char``* str = make_message(``"%d,%d,%d,%d"``,5,6,7,8);``    ``printf``(``"%s\n"``,str);``    ``free``(str);``    ``/* we allocate the memory in the make_message function, so we should release it by caller(main function). */``    ``return` `0;``}`
```

代码在vc6.0下调试通过。
