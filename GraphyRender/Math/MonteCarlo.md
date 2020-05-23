# 蒙特卡洛（Monte Carlo）法求定积分



https://blog.csdn.net/baimafujinji/article/details/53869358

蒙特卡洛（Monte Carlo）法是一类随机算法的统称。随着二十世纪电子计算机的出现，蒙特卡洛法已经在诸多领域展现出了超强的能力。在机器学习和自然语言处理技术中，常常被用到的MCMC也是由此发展而来。本文通过蒙特卡洛法最为常见的一种应用——求解定积分，来演示这类算法的核心思想。

欢迎关注白马负金羁的CSDN博客 http://blog.csdn.net/baimafujinji，为保证公式、图表得以正确显示，强烈建议你从该地址上查看原版博文。本博客主要关注方向包括：数字图像处理、算法设计与分析、数据结构、机器学习、数据挖掘、统计分析方法、自然语言处理。
无意识统计学家法则（Law of the unconscious statistician）

这是本文后续会用到的一个定理。作为一个预备知识，我们首先来介绍一下它。先来看一下维基百科上给出的解释。
In probability theory and statistics, the law of the unconscious statistician (sometimes abbreviated LOTUS) is a theorem used to calculate the 期望值 of a function g(X)
of a 随机变量 X when one knows the probability distribution of X but one does not explicitly know the distribution of g(X). The form of the law can depend on the form in which one states the probability distribution of the 随机变量 X

.

    If it is a discrete distribution and one knows its PMF function ƒX

(but not ƒg(X)), then the 期望值 of g(X) is
E[g(X)]=∑xg(x)fX(x)
where the sum is over all possible values x of X
.
If it is a continuous distribution and one knows its PDF function ƒX
(but not ƒg(X)), then the 期望值 of g(X) is
E[g(X)]=∫∞−∞g(x)fX(x)dx

LOTUS到底表达了一件什么事呢？它的意思是：已知随机变量X
的概率分布，但不知道g(X)的分布，此时用LOTUS公式能计算出函数g(X)

的数学期望。LOTUS的公式如下：

    X

是离散分布时
E[g(X)]=∑xg(x)fX(x)
X
是连续分布时
E[g(X)]=∫∞−∞g(x)fX(x)dx

其实就是在计算期望时，用已知的X
的PDF（或PMF）代替未知的g(X)

的PDF（或PMF）。
蒙特卡洛求定积分（一）：投点法

这个方法也常常被用来求π
值。现在我们用它来求函数的定积分。如下图所示，有一个函数f(x)，若要求它从a到b的定积分，其实就是求曲线下方的面积。这时我们可以用一个比较容易算得面积的矩型罩在函数的积分区间上（假设其面积为Area）。然后随机地向这个矩形框里面投点，其中落在函数f(x)下方的点为绿色，其它点为红色。然后统计绿色点的数量占所有点（红色+绿色）数量的比例为r，那么就可以据此估算出函数f(x)从a到b的定积分为Area×r

。


注意由蒙特卡洛法得出的值并不是一个精确之，而是一个近似值。而且当投点的数量越来越大时，这个近似值也越接近真实值。
蒙特卡洛求定积分（二）：期望法

下面我们来重点介绍一下利用蒙特卡洛法求定积分的第二种方法——期望法，有时也成为平均值法。

任取一组相互独立、同分布的随机变量{Xi}
，Xi在[a,b]上服从分布律fX，也就是说fX是随机变量X的PDF（或PMF），令g∗(x)=g(x)fX(x)，则g∗(Xi)也是一组独立同分布的随机变量，而且（因为g∗(x)是关于x

的函数，所以根据LOTUS可得）
E[g∗(Xi)]=∫bag∗(x)fX(x)dx=∫bag(x)dx=I

由强大数定理
Pr(limN→∞1N∑i=1Ng∗(Xi)=I)=1

若选
I¯=1N∑i=1Ng∗(Xi)

则I¯依概率1收敛到I。平均值法就用I¯作为I的近似值。

假设要计算的积分有如下形式
I=∫bag(x)dx
其中被积函数g(x)在区间[a,b]内可积。任意选择一个有简便办法可以进行抽样的概率密度函数fX(x)，使其满足下列条件：

    当g(x)≠0

时，fX(x)≠0（a≤x≤b
）
∫bafX(x)dx=1

如果记
g∗(x)=⎧⎩⎨⎪⎪g(x)fX(x),0,fX(x)≠0fX(x)=0

那么原积分式可以写成
I=∫bag∗(x)fX(x)dx

因而求积分的步骤是：

    产生服从分布律fX

的随机变量Xi (i=1,2,⋯,N)
；
计算均值
I¯=1N∑i=1Ng∗(Xi)
并用它作为I的近似值，即I≈I¯

    。

如果a,b
为有限值，那么fX

可取作为均匀分布：
fX(x)=⎧⎩⎨1b−a,0,a≤x≤botherwise

此时原来的积分式变为
I=(b−a)∫bag(x)1b−adx

具体步骤如下：

    产生[a,b]

上的均匀分布随机变量Xi (i=1,2,⋯,N)
;
计算均值
I¯=b−aN∑i=1Ng(Xi)
并用它作为I的近似值，即I≈I¯

    。

平均值法的直观解释

下面是来自参考文献【1】的一个例子。注意积分的几何意义就是[a,b]区间内曲线下方的面积。


当我们在[a,b]之间随机取一点x时，它对应的函数值就是f(x)，然后变可以用f(x)×(b−a)来粗略估计曲线下方的面积（也就是积分），当然这种估计（或近似）是非常粗略的。


于是我们想到在[a,b]之间随机取一系列点xi时（xi满足均匀分布），然后把估算出来的面积取平均来作为积分估计的一个更好的近似值。可以想象，如果这样的采样点越来越多，那么对于这个积分的估计也就越来越接近。


按照上面这个思路，我们得到积分公式为
I¯=(b−a)1N∑i=0N−1f(Xi)=1N∑i=0N−1f(Xi)1b−a

注意其中的1b−a就是均匀分布的PMF。这跟我们之前推导出来的蒙特卡洛积分公式是一致的。

参考文献

【1】http://www.scratchapixel.com/lessons/mathematics-physics-for-computer-graphics/monte-carlo-methods-in-practice/monte-carlo-integration
--------------------- 
作者：白马负金羁 
来源：CSDN 
原文：https://blog.csdn.net/baimafujinji/article/details/53869358 
版权声明：本文为博主原创文章，转载请附上博文链接！
