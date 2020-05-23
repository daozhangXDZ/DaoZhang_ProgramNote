# 虚幻4渲染编程（环境模拟篇）【第五卷：可交互物理植被模拟 - 上】



## **开篇综述**

这一卷将会开始研究可交互植被环境的模拟。我把可交互植被环境模拟这个大的课题拆解为几个部分。我挑选了几个森林模拟至关重要的几个要素并且实现它们。

【1】植被的交互

【2】植被渲染

【3】植被的生成

先看下交互效果吧，我这里只给了两层粒子，如果想交互得更细致可以把粒子段数给多点

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1119216366464442368?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



------

## **【1】植被的交互**

想要让玩家在游玩游戏的时候产生心流，首先就要让玩家沉浸到游戏里，环境交互将增强玩家的沉浸感。就森林环境而言，玩家需要和植被发生交互。目前制作植被交互效果大致有以下几种方式：

（1）动力学模拟：适用于枝叶明晰类的植被，如芭蕉，成人身高的树苗或灌木。

（2）UV纹理扰动，这种主要用于低矮的苔藓，水生藤蔓等。

（3）顶点偏移：适用于小草等植被。

（4）旋转位移：适用于20cm~120cm左右大小的植被，如树苗，灌木。

（5）纹理控制：适用于草丛，人走过时草丛被拨开，走过后草丛慢慢合上。

可以根据不同的情况选择或者组合相应的技术。



【动力学模拟】

做动力学模拟需要先抽象一个动力学模型模型出来，我把植物想象为若干粒子和约束组成的一个树状结构，如下图所示。下面就来介绍一下构建动力学网格的方法。



![img](https://pic2.zhimg.com/80/v2-323032fef9d076f6f4c5b8a01e8faaa5_hd.jpg)

我们可以使用动力学粒子+约束的方式+物理引擎碰撞解算来构建我们的动力学解算网格。关于动力学粒子和约束方式这部分内容我前面的图元汇编篇有详细介绍，传送门 : [虚幻4渲染编程（图元汇编篇）【第五卷：游戏中的动力学模拟】](https://zhuanlan.zhihu.com/p/39703910)

我们需要在动力学粒子网格的基础上加上引擎物理解算，然后用解算后的粒子去驱动数的网格最后实现交互。要实现这个，只需要在Verlet  Instigation和Constrain  Instigation解算之后加上物理解算即可，下面是一个最简单的动力学小球+物理解算后的运动结果：

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1052577822647898112?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



物理解算的代码如下：



![img](https://pic2.zhimg.com/80/v2-5e34cfdf406a81b1b0488ed3cb50fcd1_hd.png)



![img](https://pic1.zhimg.com/80/v2-021c1c96322ada9e16dcda9e917912f4_hd.jpg)

这里会调用引擎的物理模块，引擎的物理模块最终会去调用英伟达的PhysX物理引擎。

除了要使用物理引擎来解算，我们需要三种约束莱构建整颗树，PinConstrain，DistanceConstrain，AngularConstrain。下面是是PinConstrain，DistanceConstraint和Angular  Constrain的粒子和场景交互的效果：



![img](https://pic4.zhimg.com/v2-0d761d4b08130bd87a0baf06bbbabdcf_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

（上面这种约束可以用来做藤条等物体的动力学解算）



![img](https://pic3.zhimg.com/v2-71dd79090b3333cf19e2b48d8805df3e_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

（上面这种约束可以用来做如芭蕉叶之类的动力学解算，用来做弹簧绳也不错！）

不运动的质点为PinConstraint，蓝色为DistanceConstrain，绿色为AngularConstrain

下面是我的3DVerletAngularConstraint的代码：



![img](https://pic4.zhimg.com/80/v2-8094207ea158de5e17c9660d0433cd63_hd.jpg)

AngularConstraint需要先找到一个轴N作为旋转轴，旋转其实使用四元数也是可以的。我的方法是通过两个DistanceConstraint的向量得到。如下图所示：



![img](https://pic1.zhimg.com/80/v2-85cb0105fd24c46fe0436ea4f1c12f30_hd.jpg)

上面是构筑Angular Constraint的第一种方法，其实还有一种简便的算法



![img](https://pic1.zhimg.com/80/v2-feb1b5995a8f44a85433b0a8062a44ec_hd.jpg)

直接通过三角公式，用a，b和角度alpha把c算出来，然后给c边用DistanceConstraint，但是这个给c用的DistanceConstraint的ErrorFactor很小，以至于两端粒子无法在一帧内恢复给定长度，于是c就拥有了弹性。代码如下：

Q弹的棍子：



![img](https://pic1.zhimg.com/80/v2-8f99d30eec76e08ab7e35aeee8e6d62c_hd.jpg)

DistanceAngularConstraint：



![img](https://pic1.zhimg.com/80/v2-da32aaec579ebd8faf01dfd15206a828_hd.jpg)

DistanceAngularConstraint效果如下：



![img](https://pic1.zhimg.com/v2-efc534cee51ea534da644f090aad8690_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

总地来说，要构建一个动力学网格，首先需要动力学粒子，这个使用VerletInstigation解算就可以了，然后需要构建PinConstraint，DistanceConstraint，AngularConstraint，然后使用物理引擎再次解算约束器解算后的数据。粒子网格解算完成后，再基于粒子网格构建模型网格。



![img](https://pic3.zhimg.com/80/v2-d23e34f05d4f2b17114bb6ead3178416_hd.jpg)

最后完成上述工作后就可以让粒子网格和（场景&&人物）发生交互了。



下面先从一个简单的模型开始，构建一个动力学草丛。我们需要构建一个草丛粒子整列，两层粒子之间使用距离约束，让力的方向向上即可。增加粒子层数可以让草更柔软。



![img](https://pic4.zhimg.com/v2-fd86265395e1e717473fb382406d1f7f_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

下面是我的粒子网（注意粒子网不是模型，是粒子约束运动网）构建代码：



![img](https://pic1.zhimg.com/80/v2-09ea94951ed36f7a135059fa1717cf20_hd.jpg)

使用这种方式可以轻松实现多物体交互。下面开始构建模型网格。我这里就只是在两层粒子的基础上生成了一个草的面片模型。让草丛更加自然，加入了些随机值。如果觉得草的晃动持续过久，可以把加速度的值加大来解决这个问题。

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1055427648175579136?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



还可以更改一下VerletInstigation部分，让粒子的迭代速度变慢



![img](https://pic1.zhimg.com/80/v2-21adae879711c99cb100fa90830d2d58_hd.jpg)

然后就可以得到如下的碾压草丛的效果，效果如下：



![img](https://pic2.zhimg.com/v2-3299c94eea138f6bd78f0365adfcf1cd_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

这样就初步完成了物理草的动力学解算部分了。

上面使用了两层动力学粒子来模拟简单的草丛。如果想要模拟更加复杂的形状就需要在粒子动力学网格的构建，约束上下功夫了。



![img](https://pic1.zhimg.com/v2-6c3e201225aae15aedb4fdfccdb59404_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1055950598406467584?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



我重载了粒子动力学网格的加速度解算方法，让每个粒子都可以定义自己的加速度方向，这样就可以仅仅使用DistanceConstraint和pinConstraint就能方便支撑起整个动力学网格的形状啦。



![img](https://pic4.zhimg.com/80/v2-876d2c32790ab867c22236974236c5a3_hd.jpg)

这样一来就可以使用非常cheap的少量DistanceConstraint和PinConstraint来进行粒子网格的形状建模，避免使用非常expensive的AngularConstraint。但是如果想要强调枝干的韧性还是需要上AngularConstraint。



![img](https://pic2.zhimg.com/80/v2-b89904b659cfdf00fd91816fd13d688d_hd.jpg)



![img](https://pic3.zhimg.com/80/v2-7d96bfdf7c7d48db59411690944a0082_hd.jpg)



![img](https://pic4.zhimg.com/80/v2-696736f60a4852af38ef9b131a51689b_hd.jpg)

实现方式是我给Init函数多实现了一个版本，如果使用第二个init版本初始化粒子，那么粒子将默认开启使用自己的LocalForce而不是全局的。用代码建模实在太痛苦了，其实可以做个工具来实现BuildVerletparticleMesh里面的逻辑的。

利用动力学粒子来构建模型最主要的问题其实还是优化，可以考虑为植被使用两个IB和VB，这样就可以避免Buffer在读的时候GPU处于等待状态。这样就可以绘制大量物体了，效果如下：

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1060201911701082112?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



使用动力学模拟的方式来实现植物的动力学交互的步骤总的来说就是

（1）构建动力学粒子和动力学网格

（2）利用动力学网格构建模型网格

（3）在模型的基础上做shading

优点是限制少，因为这种方式是最接近真实的方式。但是缺点就是效率问题和自由度问题，在粒子网格上构建模型网格实在比较难。还有种思路是使用粒子网格驱动骨架网格。这种就解决了上述所有问题，但是效率堪忧，但是效果是最好的一种方式。驱动骨架的实现方法可以看我下面这篇文章

[小IVan：虚幻4渲染编程（动画篇）【第六卷：自定义动画节点】](https://zhuanlan.zhihu.com/p/52266316)



![img](https://pic4.zhimg.com/v2-357c99ea46f72e92fd2c278f1497ecdb_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

物理模拟的方式可以轻松实现多物体的交互，如果是使用RT或者是数组传到shader里的方式的话，在实现多人同时交互时就比较麻烦了。

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1062679680951377920?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



------

【UV纹理扰动】

这种方式来模拟植被的交互效果就比较简单了，这种方式适合青苔，水洼里的水藻之类的。

------

【顶点偏移】

这种方式被业内大量运用，这种方式能做到效率效果兼备而且自由度高，能方便美术师制作。最简单的方法就是把角色的位置传到cbuffer里，顶点着色器每帧取一下，然后给植被的顶点做个偏移。

最多给个曲线或者什么trcik公式控制一下幅度



![img](https://pic2.zhimg.com/v2-c95206c2170bfb2cc92fbaf148401dc5_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

------

【纹理控制的顶点偏移】

这种方式就是做一个RT用于记录当前草丛的信息，被拨开也好被扰动也好，然后把这个RT传到草丛模型Shader里做解读。



![img](https://pic4.zhimg.com/v2-41d1dee18d56d5d025eedf3e88cb4877_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

------

【旋转位移】

这种方式是在植被的Transform信息上下文章，非常适合draw   instance的植被，因为instance天生就有个transform信息，这种方式模拟出来的效果也非常自然，不需要来回画Rendertarget了，直接对instance进行操作（摆动，拨开等等）。主要开销在instance的查询上。

这种方法的具体做法我以前的CSDN博客上有详细描述



![img](https://pic3.zhimg.com/v2-80adcb51e7633ec8636bd1b6f5a8bbde_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

------

可交互物理植被模拟(1)主要是理论推导和实现，后面的shading和生成章节会有更进一步的效果完善。

Enjoy it！
