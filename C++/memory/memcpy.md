# 比memcpy更快的内存拷贝

   偶然间看到一个叫xmemcpy的工具，用做内存拷贝。号称在拷贝120字节以内时，比glibc提供的memcpy快10倍，并且有实验数据。

     这让人感觉很诧异。一直以来都觉得memcpy是很高效的。相比于strcpy等函数的逐字节拷贝，memcpy是按照机器字长逐字进行拷贝的，一个字等于4（32位机）或8（64位机）个字节。CPU存取一个字节和存取一个字一样，都是在一条指令、一个内存周期内完成的。显然，按字拷贝效率更高。
    
     那么，这个xmemcpy是靠什么来实现比memcpy“快10倍”的呢？
     看了一下xmemcpy的实现，原来它速度快的根据是：“小内存的拷贝，使用等号直接赋值比memcpy快得多”。
     这下就更纳闷了，内存拷贝不就是把一块内存一部分一部分地拷贝到另一块内存去吗？难道逐字拷贝还有性能提升的空间？

写了一段代码：

#include <stdio.h>
#define TESTSIZE        128
struct node {
char buf[TESTSIZE];
};
void main()
{
char src[TESTSIZE] = {0};
char dst[TESTSIZE];
*(struct node*)dst = *(struct node*)src;
}
然后反汇编：

......
00000000004004a8 <main>:
4004a8:       55                      push   %rbp
4004a9:       48 89 e5                mov    %rsp,%rbp
4004ac:       48 81 ec 00 01 00 00    sub    $0x100,%rsp
4004b3:       48 8d 7d 80             lea    0xffffffffffffff80(%rbp),%rdi
4004b7:       ba 80 00 00 00          mov    $0x80,%edx
4004bc:       be 00 00 00 00          mov    $0x0,%esi
4004c1:       e8 1a ff ff ff          callq 4003e0 <>
4004c6:       48 8b 45 80             mov    0xffffffffffffff80(%rbp),%rax
4004ca:       48 89 85 00 ff ff ff    mov    %rax,0xffffffffffffff00(%rbp)
4004d1:       48 8b 45 88             mov    0xffffffffffffff88(%rbp),%rax
......
400564:       48 89 85 70 ff ff ff    mov    %rax,0xffffffffffffff70(%rbp)
40056b:       48 8b 45 f8             mov    0xfffffffffffffff8(%rbp),%rax
40056f:       48 89 85 78 ff ff ff    mov    %rax,0xffffffffffffff78(%rbp)
400576:       c9                      leaveq 
400577:       c3                      retq   
400578:       90                      nop    
......

再将libc反汇编，并找到memcpy的实现，以作比较：

......
0006b400 <memcpy>:
6b400:       8b 4c 24 0c             mov    0xc(%esp),%ecx
6b404:       89 f8                   mov    %edi,%eax
6b406:       8b 7c 24 04             mov    0x4(%esp),%edi
6b40a:       89 f2                   mov    %esi,%edx
6b40c:       8b 74 24 08             mov    0x8(%esp),%esi
6b410:       fc                      cld    
6b411:       d1 e9                   shr    %ecx
6b413:       73 01                   jae    6b416 <memcpy+0x16>
6b415:       a4                      movsb %ds:(%esi),%es:(%edi)
6b416:       d1 e9                   shr    %ecx
6b418:       73 02                   jae    6b41c <memcpy+0x1c>
6b41a:       66 a5                   movsw %ds:(%esi),%es:(%edi)
6b41c:       f3 a5                   repz movsl %ds:(%esi),%es:(%edi)
6b41e:       89 c7                   mov    %eax,%edi
6b420:       89 d6                   mov    %edx,%esi
6b422:       8b 44 24 04             mov    0x4(%esp),%eax
6b426:       c3                      ret    
6b427:       90                      nop    
......

      原来两者都是通过逐字拷贝来实现的。但是“等号赋值”被编译器翻译成一连串的MOV指令，而memcpy则是一个循环。“等号赋值”比memcpy快，并不是快在拷贝方式上，而是快在程序流程上。
   （另外，测试发现，“等号赋值”的长度必须小于等于128，并且是机器字长的倍数，才会被编译成连续MOV形式，否则会被编译成调用memcpy。当然，具体怎么做是编译器决定的。）

     而为什么同样是按机器字长拷贝，连续的MOV指令就要比循环MOV快呢？
     在循环方式下，每一次MOV过后，需要：1、判断是否拷贝完成；2、跳转以便继续拷贝。
     每拷贝一个字长，CPU就需要多执行以上两个动作。
    
     循环除了增加了判断和跳转指令以外，对于CPU处理流水产生的影响也是不可不计的。CPU将指令的执行分为若干个阶段，组成一条指令处理流水线，这样就能实现在一个CPU时钟周期完成一条指令，使得CPU的运算速度得以提升。
     指令流水只能按照单一的指令路径来执行，如果出现分支（判断+跳转），流水就没法处理了。
     为了缓解分支对于流水的影响，CPU可能会采取一定的分支预测策略。但是分支预测不一定就能成功，如果失败，其损失比不预测还大。
    
     所以，循环还是比较浪费的。如果效率要求很高，很多情况下，我们需要把循环展开（比如在本例中，每次循环拷贝N个字节），以避免判断与跳转占用大量的CPU时间。这算是一种以空间换时间的做法。GCC就有自动将循环展开的编译选项（如：-funroll-loops）。
     但是，循环展开也是应该有个度的，并不是越展开越好（即使不考虑对空间的浪费）。因为CPU的快速执行很依赖于cache，如果cache不命中，CPU将浪费不少的时钟周期在等待内存上（内存的速度一般比CPU低一个数量级）。而小段循环结构就比较有利于cache命中，因为重复执行的一段代码很容易被硬件放在cache中，这就是代码局部性带来的好处。而过度的循环展开就打破了代码的局部性，所以xmemcpy一开始就提到拷贝120字节以内。如果要拷贝的字节更多，则全部展开成连续的MOV指令的做法未必会很高效。
    
     综上所述，“等号赋值”之所以比memcpy快，就是因为它省略了CPU对于判断与跳转的处理，消除了分支对CPU流水的影响。而这一切都是通过适度展开内存拷贝的循环来实现的。
---------------------
版权声明：本文为CSDN博主「ctthuangcheng」的原创文章，遵循CC 4.0 by-sa版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ctthuangcheng/article/details/8915070