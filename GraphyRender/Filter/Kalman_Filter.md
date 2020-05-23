## [图说卡尔曼滤波，一份通俗易懂的教程](https://zhuanlan.zhihu.com/p/39912633)

![图说卡尔曼滤波，一份通俗易懂的教程](Kalman_Filter.assets/v2-954bea3147c72502022920b95819621b_hd.jpg)

作者：[Bzarg](http://link.zhihu.com/?target=http%3A//www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/)编译：Bot编者按：卡尔曼滤波（Kalman   filter）是一种高效的自回归滤波器，它能在存在诸多不确定性情况的组合信息中估计动态系统的状态，是一种强大的、通用性极强的工具。它的提出者，鲁道夫.E.卡尔曼，在一次访问NASA埃姆斯研究中心时，发现这种方法能帮助解决阿波罗计划的轨道预测问题，后来NASA在阿波罗飞船的导航系统中确实也用到了这个滤波器。最终，飞船正确驶向月球，完成了人类历史上的第一次登月。

![img](Kalman_Filter.assets/v2-e7fade003119539cd2892c23ff924ca1_b.jpg)



本文是国外博主Bzarg在2015年写的一篇图解。虽然是几年前的文章，但是动态定位、自动导航、时间序列模型、卫星导航——卡尔曼滤波的应用范围依然非常广。那么，作为软件工程师和机器学习工程师，你真的了解卡尔曼滤波吗？什么是卡尔曼滤波？对于这个滤波器，我们几乎可以下这么一个定论：只要是存在不确定信息的动态系统，卡尔曼滤波就可以对系统下一步要做什么做出有根据的推测。即便有噪声信息干扰，卡尔曼滤波通常也能很好的弄清楚究竟发生了什么，找出现象间不易察觉的相关性。因此卡尔曼滤波非常适合不断变化的系统，它的优点还有内存占用较小（只需保留前一个状态）、速度快，是实时问题和嵌入式系统的理想选择。如果你曾经Google过卡尔曼滤波的教程（如今有一点点改善），你会发现相关的算法教程非常可怕，而且也没具体说清楚是什么。事实上，卡尔曼滤波很简单，如果我们以正确的方式看它，理解是很水到渠成的事。本文会用大量清晰、美观的图片和颜色来解释这个概念，读者只需具备概率论和矩阵的一般基础知识。我们能用卡尔曼滤波做什么？让我们举个例子：你造了一个可以在树林里四处溜达的小[机器人](http://link.zhihu.com/?target=http%3A//www.jqr.com/)，为了让它实现导航，机器人需要知道自己所处的位置。

![img](Kalman_Filter.assets/v2-f712a1162871053ea130215f313226fb_b.jpg)

也就是说，机器人有一个包含位置信息和速度信息的状态



 ![[公式]](http://www.zhihu.com/equation?tex=%5Cvec%7Bx%7D_k) ：![img](Kalman_Filter.assets/v2-e536756c4f6489c542a611c76caaea91_b.jpg)

注意，在这个例子中，状态是位置和速度，放进其他问题里，它也可以是水箱里的液体体积、汽车引擎温度、触摸板上指尖的位置，或者其他任何数据。我们的小机器人装有GPS**传感器**，定位精度10米。虽然一般来说这点精度够用了，但我们希望它的定位误差能再小点，毕竟树林里到处都是土坑和陡坡，如果机器人稍稍偏了那么几米，它就有可能滚落山坡。所以GPS提供的信息还不够充分。

![img](Kalman_Filter.assets/v2-9067328eb93cbb9f49dae46561ed3b5f_b.jpg)



我们也可以**预测**机器人是怎么移动的：它会把指令发送给控制轮子的马达，如果这一刻它始终朝一个方向前进，没有遇到任何障碍物，那么下一刻它可能会继续坚持这个路线。但是机器人对自己的状态不是全知的：它可能会逆风行驶，轮子打滑，滚落颠簸地形……所以车轮转动次数并不能完全代表实际行驶距离，基于这个距离的预测也不完美。这个问题下，GPS为我们提供了一些关于状态的信息，但那是间接的、不准确的；我们的预测提供了关于机器人轨迹的信息，但那也是间接的、不准确的。但以上就是我们能够获得的全部信息，在它们的基础上，我们是否能给出一个完整预测，让它的准确度比机器人搜集的单次预测汇总更高？用了卡尔曼滤波，这个问题可以迎刃而解。卡尔曼滤波眼里的机器人问题还是上面这个问题，我们有一个状态，它和速度、位置有关：

![img](Kalman_Filter.assets/v2-a1a901c6aad3d87b47b148a3e5cdddbe_b.jpg)



我们不知道它们的实际值是多少，但掌握着一些速度和位置的可能组合，其中某些组合的可能性更高：

![img](Kalman_Filter.assets/v2-20ad3b88677b04dbd054432e61229828_b.jpg)



卡尔曼滤波假设两个变量（在我们的例子里是位置和速度）都应该是**随机的**，而且符合**高斯分布**。每个变量都有一个**均值** ![[公式]](http://www.zhihu.com/equation?tex=%CE%BC) ，它是随机分布的中心；有一个方差 ![[公式]](http://www.zhihu.com/equation?tex=%CF%83%5E2) ，它衡量组合的不确定性。



在上图中，位置和速度是**不相关**的，这意味着我们不能从一个变量推测另一个变量。那么如果位置和速度相关呢？如下图所示，机器人前往特定位置的可能性取决于它拥有的速度。

![img](Kalman_Filter.assets/v2-d474e950b50b865fec1cd454b3059b57_b.jpg)



这不难理解，如果基于旧位置估计新位置，我们会产生这两个结论：如果速度很快，机器人可能移动得更远，所以得到的位置会更远；如果速度很慢，机器人就走不了那么远。这种关系对目标跟踪来说非常重要，因为它提供了更多信息：一个可以衡量可能性的标准。这就是卡尔曼滤波的目标：从不确定信息中挤出尽可能多的信息！为了捕获这种相关性，我们用的是协方差矩阵。简而言之，矩阵的每个值是第 ![[公式]](Kalman_Filter.assets/equation.svg) 个变量和第 ![[公式]](Kalman_Filter.assets/equation.svg) 个变量之间的相关程度（由于矩阵是对称的， ![[公式]](Kalman_Filter.assets/equation.svg) 和 ![[公式]](Kalman_Filter.assets/equation.svg) 的位置可以随便交换）。我们用 ![[公式]](http://www.zhihu.com/equation?tex=%CE%A3) 表示协方差矩阵，在这个例子中，就是 ![[公式]](http://www.zhihu.com/equation?tex=%CE%A3_%7Bij%7D) 。

![img](Kalman_Filter.assets/v2-c0d94558ba4ee781291cefc855ea53f0_b.jpg)



用矩阵描述问题为了把以上关于状态的信息建模为高斯分布（图中色块），我们还需要 ![[公式]](Kalman_Filter.assets/equation.svg) 时的两个信息：最佳估计 ![[公式]](http://www.zhihu.com/equation?tex=%5Chat%7Bx%7D_k) （均值，也就是 ![[公式]](http://www.zhihu.com/equation?tex=%CE%BC) ），协方差矩阵 ![[公式]](http://www.zhihu.com/equation?tex=P_k) 。

（虽然还是用了位置和速度两个变量，但只要和问题相关，卡尔曼滤波可以包含任意数量的变量）

![img](Kalman_Filter.assets/v2-2ac6f7823c6e340805cce06b61c8fa16_b.jpg)

接下来，我们要通过查看当前状态（k-1时）来预测下一个状态（k时）。这里我们查看的状态不是真值，但预测函数无视真假，可以给出新分布：

![img](Kalman_Filter.assets/v2-4aa0fa34f4d423f6cfca39b48fde03e4_b.jpg)



我们可以用矩阵 ![[公式]](Kalman_Filter.assets/equation.svg) 表示这个预测步骤：

![img](Kalman_Filter.assets/v2-1aeabc85ef432999b6126536be07d845_b.jpg)

它从原始预测中取每一点，并将其移动到新的预测位置。如果原始预测是正确的，系统就会移动到新位置。这是怎么做到的？为什么我们可以用矩阵来预测机器人下一刻的位置和速度？

下面是个简单公式：

![img](Kalman_Filter.assets/v2-03ed134b88639dbfe347012511440a3a_b.jpg)

换成矩阵形式：

![img](Kalman_Filter.assets/v2-2916712c805c703b37fce364549dadf6_b.jpg)

这是一个预测矩阵，它能给出机器人的下一个状态，但目前我们还不知道协方差矩阵的更新方法。这也是我们要引出下面这个等式的原因：如果我们将分布中的每个点乘以矩阵A，那么它的协方差矩阵会发生什么变化

![img](Kalman_Filter.assets/v2-69a02c2142ed47d086a9a948cb8b17b1_b.jpg)

把这个式子和上面的最佳估计 ![[公式]](http://www.zhihu.com/equation?tex=%5Chat%7Bx%7D_k) 结合，可得：

![img](Kalman_Filter.assets/v2-dbf13375a23f07e1040adf38ea186aa7_b.jpg)

外部影响**但是，除了速度和位置，外因也会对系统造成影响。比如模拟火车运动，除了列车自驾系统，列车操作员可能会手动调速。在我们的机器人示例中，导航软件也可以发出停止指令。对于这些信息，我们把它作为一个向量 ![[公式]](http://www.zhihu.com/equation?tex=%5Cvec%7Bu%7D_k) ，纳入预测系统作为修正。假设油门设置和控制命令是已知的，我们知道火车的预期加速度 ![[公式]](http://www.zhihu.com/equation?tex=a) 。**

**根据运动学基本定理，我们可得：

![img](Kalman_Filter.assets/v2-e0cd414e3b6d4ef4f8a57c8b156a5103_b.jpg)

把它转成矩阵形式：

![img](Kalman_Filter.assets/v2-64e50bf118c8039f6228b5c817490601_b.jpg)![[公式]](Kalman_Filter.assets/equation.svg)

 是控制矩阵， ![[公式]](http://www.zhihu.com/equation?tex=%5Cvec%7Bu%7D_k) 是控制向量。如果外部环境异常简单，我们可以忽略这部分内容，但是如果添加了外部影响后，模型的准确率还是上不去，这又是为什么呢？**外部不确定性**当一个国家只按照自己的步子发展时，它会自生自灭。当一个国家开始依赖外部力量发展时，只要这些外部力量是已知的，我们也能预测它的存亡。但是，如果存在我们不知道的力量呢？当我们监控[无人机](http://link.zhihu.com/?target=https%3A//www.jqr.com/service/company%3Fbusiness%3D16)时，它可能会受到风的影响；当我们跟踪轮式机器人时，它的轮胎可能会打滑，或者粗糙地面会降低它的移速。这些因素是难以掌握的，如果出现其中的任意一种情况，预测结果就难以保障。这要求我们在每个预测步骤后再加上一些新的不确定性，来模拟和“世界”相关的所有不确定性：

![img](Kalman_Filter.assets/v2-7cc51be5e269b579c4588db25daf995f_b.jpg)

如上图所示，加上外部不确定性后， ![[公式]](http://www.zhihu.com/equation?tex=%5Chat%7Bx%7D_%7Bk-1%7D) 的每个预测状态都可能会移动到另一点，也就是蓝色的高斯分布会移动到紫色高斯分布的位置，并且具有协方差 ![[公式]](Kalman_Filter.assets/equation.svg) 。换句话说，我们把这些不确定影响视为协方差 ![[公式]](Kalman_Filter.assets/equation.svg) 的噪声。

![img](Kalman_Filter.assets/v2-9f3e50aa57cf224319b6c8e50560c595_b.jpg)

这个紫色的高斯分布拥有和原分布相同的均值，但协方差不同。

![img](Kalman_Filter.assets/v2-e3a93c5aaae676913f37d08ca50fda7a_b.jpg)

我们在原式上加入 ![[公式]](Kalman_Filter.assets/equation.svg) ：![img](Kalman_Filter.assets/v2-2c8b709435f6c99ef9b00bba18d32b09_b.jpg)简而言之，

这里：

![[公式]](http://www.zhihu.com/equation?tex=%5Ccolor%7Bmagenta%7D%7B%5Ctext%7B%E6%96%B0%E7%9A%84%E6%9C%80%E4%BD%B3%E4%BC%B0%E8%AE%A1%7D%7D%5C) 是基于 ![[公式]](http://www.zhihu.com/equation?tex=%5Ccolor%7Bblue%7D%7B%5Ctext%7B%E5%8E%9F%E6%9C%80%E4%BD%B3%E4%BC%B0%E8%AE%A1%7D%7D%5C) 和 ![[公式]](http://www.zhihu.com/equation?tex=%5Ccolor%7Borange%7D%7B%5Ctext%7B%E5%B7%B2%E7%9F%A5%E5%A4%96%E9%83%A8%E5%BD%B1%E5%93%8D%7D%7D%5C) 校正后得到的预测。![[公式]](http://www.zhihu.com/equation?tex=%5Ccolor%7Bmagenta%7D%7B%5Ctext%7B%E6%96%B0%E7%9A%84%E4%B8%8D%E7%A1%AE%E5%AE%9A%E6%80%A7%7D%7D%5C) 是基于 ![[公式]](http://www.zhihu.com/equation?tex=%5Ccolor%7Bblue%7D%7B%5Ctext%7B%E5%8E%9F%E4%B8%8D%E7%A1%AE%E5%AE%9A%E6%80%A7%7D%7D%5C) 和 ![[公式]](http://www.zhihu.com/equation?tex=%5Ccolor%7Bturquoise%7D%7B%5Ctext%7B%E5%A4%96%E9%83%A8%E7%8E%AF%E5%A2%83%E7%9A%84%E4%B8%8D%E7%A1%AE%E5%AE%9A%E6%80%A7%7D%7D%5C) 得到的预测。

现在，有了这些概念介绍，我们可以把传感器数据输入其中。通过测量来细化估计值我们可能有好几个传感器，它们一起提供有关系统状态的信息。传感器的作用不是我们关心的重点，它可以读取位置，可以读取速度，重点是，它能告诉我们关于状态的间接信息——它是状态下产生的一组读数。

![img](Kalman_Filter.assets/v2-e7aa23b6558800eb17567244f6f7b12d_b.jpg)

请注意，读数的规模和状态的规模不一定相同，所以我们把传感器读数矩阵设为 ![[公式]](Kalman_Filter.assets/equation.svg) 。

![img](Kalman_Filter.assets/v2-114204d0be573afac8df2630fbf43374_b.jpg)

把这些分布转换为一般形式：

![img](Kalman_Filter.assets/v2-531d486ddd0875207e79b16d19006ca5_b.jpg)

卡尔曼滤波的一大优点是擅长处理传感器噪声。换句话说，由于种种因素，传感器记录的信息其实是不准的，一个状态事实上可以产生多种读数。

![img](Kalman_Filter.assets/v2-2cc213523368e5b0c551522fa917f507_b.jpg)

我们将这种不确定性（即传感器噪声）的协方差设为 ![[公式]](http://www.zhihu.com/equation?tex=R_k) ，读数的分布均值设为 ![[公式]](Kalman_Filter.assets/equation.svg) 。现在我们得到了两块高斯分布，一块围绕预测的均值，另一块围绕传感器读数。

![img](Kalman_Filter.assets/v2-501fb01035bdb4d503fa61591f9cc2dc_b.jpg)

如果要生成靠谱预测，模型必须调和这两个信息。也就是说，对于任何可能的读数 ![[公式]](http://www.zhihu.com/equation?tex=%28z_1%2Cz_2%29) ，这两种方法预测的状态都有可能是准的，也都有可能是不准的。重点是我们怎么找到这两个准确率。最简单的方法是两者相乘：

![img](Kalman_Filter.assets/v2-5abf2cf6004b9387464b2da41ae62bb7_b.jpg)

两块高斯分布相乘后，我们可以得到它们的重叠部分，这也是会出现最佳估计的区域。换个角度看，它看起来也符合高斯分布：![img](Kalman_Filter.assets/v2-15bdb8527c724044528cdaf118480614_b.jpg)

事实证明，当你把两个高斯分布和它们各自的均值和协方差矩阵相乘时，你会得到一个拥有独立均值和协方差矩阵的新高斯分布。最后剩下的问题就不难解决了：我们必须有一个公式来从旧的参数中获取这些新参数！结合高斯让我们从一维看起，设方差为 ![[公式]](http://www.zhihu.com/equation?tex=%CF%83%5E2) ，均值为 ![[公式]](http://www.zhihu.com/equation?tex=%CE%BC) ，一个标准一维高斯钟形曲线方程如下所示：

![img](Kalman_Filter.assets/v2-97fd17b2ea76d5452a22725f19f99580_b.jpg)

那么两条高斯曲线相乘呢？![img](Kalman_Filter.assets/v2-95a639e3feb8773757a4a74e45e477c5_b.jpg)

![img](Kalman_Filter.assets/v2-44fae648700cd28c6ed7c82e91c864a9_b.jpg)

把这个式子按照一维方程进行扩展，可得：

![img](Kalman_Filter.assets/v2-f3119ec5da2279746e27b0e2e31ccfb9_b.jpg)

如果有些太复杂，我们用k简化一下：

![img](Kalman_Filter.assets/v2-2881114c10fc274482b013e408df9ce9_b.jpg)
以上是一维的内容，如果是多维空间，把这个式子转成矩阵格式：

![img](Kalman_Filter.assets/v2-1c02a4b31a146aba44c5082079df1e8c_b.jpg)

这个矩阵 ![[公式]](Kalman_Filter.assets/equation.svg) 就是我们说的**卡尔曼增益**，easy！把它们结合在一起截至目前，我们有用矩阵 ![[公式]](http://www.zhihu.com/equation?tex=+%28%CE%BC_0%2C%CE%A3_0%29%3D%28H_k%5Chat%7Bx%7D_k%2CH_kP_kH_%7Bk%7D%5E%7BT%7D%29) 预测的分布，有用传感器读数 ![[公式]](http://www.zhihu.com/equation?tex=%28%CE%BC_1%2C%CE%A3_1%29%3D%28%5Cvec%7Bz%7D_k%2CR_k%29) 预测的分布。把它们代入上节的矩阵等式中：

![img](Kalman_Filter.assets/v2-9cb02f4cb340f4bee98bf8fdef80867b_b.jpg)

相应的，卡尔曼增益就是：

![img](Kalman_Filter.assets/v2-c2a3f0e191354e598e09d4fdd59b8d25_b.jpg)

考虑到 ![[公式]](Kalman_Filter.assets/equation.svg) 里还包含着一个 ![[公式]](Kalman_Filter.assets/equation.svg) ，我们再精简一下上式：

![img](Kalman_Filter.assets/v2-47b92e3442751ff8266b4d18e30bda2a_b.jpg)

最后， ![[公式]](http://www.zhihu.com/equation?tex=%5Chat%7Bx%7D_k%5E%E2%80%B2) 是我们的最佳估计值，我们可以把它继续放进去做另一轮预测：

![img](Kalman_Filter.assets/v2-c4db49174bd28fa7634be3858a368e26_b.jpg)

希望这篇文章能对你有用！