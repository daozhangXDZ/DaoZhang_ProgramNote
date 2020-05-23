# 穿越大气的旅程

#### 大气密度比

我们还没有解决的是大气密度比的作用![\ rho](JourneyThroughTheAtmosphere.assets/quicklatex.com-e8e197a6f1572ae9b5a16039ea626388_l3.svg)。从逻辑观点来看，散射强度与大气密度成正比是有意义的。每平方米更多的分子意味着更多的光子被散射的机会。挑战在于，大气的组成非常复杂，由具有不同压力，密度和温度的几层组成。幸运的是，大多数瑞利散射发生在大气层的前60公里。在**对流层中**，温度呈线性下降，压力呈指数下降。

下图显示了低层大气中密度与高度之间的关系。

![image-20200507184112594](JourneyThroughTheAtmosphere.assets/image-20200507184112594.png)

的值![\ rho \ left（h \ right）](JourneyThroughTheAtmosphere.assets/quicklatex.com-7585ec6ce953852ce36339593219662d_l3.svg)表示海拔高度处的大气测量值![H](JourneyThroughTheAtmosphere.assets/quicklatex.com-2ce27f7d2d82e3b238176ec7e7ee9118_l3.svg)，已对其进行归一化，使其从零开始。

在许多科学论文中，![\ rho](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e8e197a6f1572ae9b5a16039ea626388_l3.svg)也称为**密度比，**因为它也可以定义为：

![image-20200507184130358](JourneyThroughTheAtmosphere.assets/image-20200507184130358.png)

通过将实际密度![密度\左（0 \右）](JourneyThroughTheAtmosphere.assets/quicklatex.com-091537319820e5c5fc0c39664d99ff5b_l3.svg)的原因![\ rho \ left（h \ right）](JourneyThroughTheAtmosphere.assets/quicklatex.com-86d0f8588bf7283124da427642f482bf_l3.svg)是![1个](JourneyThroughTheAtmosphere.assets/quicklatex.com-69a7c7fb1023d315f416440bca10d849_l3.svg)海平面。但是，如前所述，计算![密度\左（h \右）](JourneyThroughTheAtmosphere.assets/quicklatex.com-803b2fca578f6b2f23aa1b8b5f0ecb6c_l3.svg)远非平凡。我们可以用指数曲线来近似。你们中的一些人实际上可能已经认识到较低大气层中的密度随**指数衰减而变化**。

如果我们想用指数曲线来近似密度比，我们可以这样做：

![image-20200507184141695](JourneyThroughTheAtmosphere.assets/image-20200507184141695.png)

其中![H_0](JourneyThroughTheAtmosphere.assets/quicklatex.com-a81c61d64246a6d7aacbca7b00d54378_l3.svg)的比例因子称为**比例高度**。对于在地球较低层大气中的瑞利散射，通常假定为![高= 8500](JourneyThroughTheAtmosphere.assets/quicklatex.com-cb1b4728b1894070d9570126f0c10342_l3.svg)米（下图）。对于米氏散射，它通常在![1200](JourneyThroughTheAtmosphere.assets/quicklatex.com-49826c597725bfd80ff939399decbc11_l3.svg)米附近。

![image-20200507184201950](JourneyThroughTheAtmosphere.assets/image-20200507184201950.png)

用于的值![H](JourneyThroughTheAtmosphere.assets/quicklatex.com-a7cedbc00aa5531f310166df85e3a9bb_l3.svg)不能给出的最佳近似值![\ rho \ left（h \ right）](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-86d0f8588bf7283124da427642f482bf_l3.svg)。但是，这并不是真正的问题。本教程中介绍的大多数数量都经过严格的近似。为了获得最佳效果，调整可用参数以匹配参考图像将更加有效。

#### 指数衰减

在本教程的前面部分中，我们导出了一个方程式，该方程式显示了如何解释与单个粒子相互作用后光线受到的向外散射。用于模拟这种现象的数量称为**散射系数** ![\ beta](JourneyThroughTheAtmosphere.assets/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)。我们引入了系数![\ beta](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)以考虑到这一点。

在瑞利散射的情况下，我们还提供了一种封闭形式来计算每次单次相互作用受到大气散射的光量：

![image-20200507184253288](JourneyThroughTheAtmosphere.assets/image-20200507184253288.png)

在海平面上进行评估（即使用）时![h = 0](JourneyThroughTheAtmosphere.assets/quicklatex.com-fd16c23a91f843528cf3a40daf6ad564_l3.svg)，它将产生以下结果：

![image-20200507184307768](JourneyThroughTheAtmosphere.assets/image-20200507184307768.png)

其中![680](JourneyThroughTheAtmosphere.assets/quicklatex.com-e96d8ba2a90cb8fd4abbb464ad4cc091_l3.svg)，![550](JourneyThroughTheAtmosphere.assets/quicklatex.com-a87236ae98ef2cd78744e2d07c79e257_l3.svg)并且![440](JourneyThroughTheAtmosphere.assets/quicklatex.com-ae158198eb2584747dcc17fbf1d44334_l3.svg)是松散地映射到红色，绿色和蓝色波长。

这些数字是什么意思？它们表示与粒子的单次交互所损失的光的比率。如果我们假设一束光线具有初始强度，![I_0](JourneyThroughTheAtmosphere.assets/quicklatex.com-a388cb824462284238cced83860611ce_l3.svg)并且以（通用）散射系数穿过大气层![\ beta](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)，则*没有*被散射损失的光量为：

![image-20200507184319723](JourneyThroughTheAtmosphere.assets/image-20200507184319723.png)

虽然这仅适用于一次碰撞，但我们有兴趣了解在一定距离内散布了多少能量。这意味着，在每个点上，其余的光都要经过此过程。

当光穿过具有散射系数的均匀介质时![\ beta](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)，如何计算一定距离后仍能存活的光？

对于那些学习微积分的人来说，这听起来很耳熟。每当![\ left（1- \ beta \ right）](JourneyThroughTheAtmosphere.assets/quicklatex.com-e1a9a40535e8050314c59fb31784f552_l3.svg)在连续段上重复进行类似乘法的过程时，**欧拉数** 就大放异彩。行进![X](JourneyThroughTheAtmosphere.assets/quicklatex.com-7e5fbfa0bbbd9f3051cd156a0f1b5e31_l3.svg)米后幸存下来的光量为：

![image-20200507184337391](JourneyThroughTheAtmosphere.assets/image-20200507184337391.png)

再一次，我们遇到一个指数函数。这与用于描述密度比的指数函数没有任何关系![\ rho](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e8e197a6f1572ae9b5a16039ea626388_l3.svg)。两种现象都用指数函数描述的原因是它们都经历了指数衰减。除此之外，它们之间没有其他联系。

**exp exp**来自哪里？

#### 均匀透射率

在本教程的第二部分中，我们介绍了**透射** ![Ť](JourneyThroughTheAtmosphere.assets/quicklatex.com-7e093fd43ad2c244140c11afe4d4bdff_l3.svg)率的概念，即穿过大气后在散射过程中幸存下来的光的比率。现在，我们拥有了最终导出描述它的方程式所需的所有元素。

让我们看一下下面的图，看看如何计算该段的透射系数![\ overline {CP}](JourneyThroughTheAtmosphere.assets/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)。可以很容易地看到到达的光线![C](JourneyThroughTheAtmosphere.assets/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)穿过空的空间。因此，它们不会受到散射。![C](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)因此，处的光量是**太阳强度** ![I_S](JourneyThroughTheAtmosphere.assets/quicklatex.com-8267520f1a54784637e791b96ef239b8_l3.svg)。在到达的过程中![P](JourneyThroughTheAtmosphere.assets/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)，一些光从路径散开了。因此，光到达量![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)，![I_P](JourneyThroughTheAtmosphere.assets/quicklatex.com-e64a7aa5bd064613a51ee137be78ab61_l3.svg)将比较低![I_S](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8267520f1a54784637e791b96ef239b8_l3.svg)。

![img](JourneyThroughTheAtmosphere.assets/scattering_07.png)

散射的光量取决于行进的距离。路程越长，衰减越大。根据指数衰减定律，![I_P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e64a7aa5bd064613a51ee137be78ab61_l3.svg)可以计算出的光量如下：

![image-20200507184353752](JourneyThroughTheAtmosphere.assets/image-20200507184353752.png)

其中![\ overline {CP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)是从![C](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)到的段的长度![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)，![\ exp {\ left \ {x \ right \}}](JourneyThroughTheAtmosphere.assets/quicklatex.com-ccf3a9e878d038b9be6564d12bd1fccc_l3.svg)是**指数函数** ![e ^ {x}](JourneyThroughTheAtmosphere.assets/quicklatex.com-8a16a1815027984f11ade6873b398cc2_l3.svg)。

#### 大气透过率

我们基于以下假设建立方程，即沿的每个点偏转的机会（**散射系数** ![\ beta](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)）都相同![\ overline {CP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)。可悲的是，事实并非如此。

散射系数在很大程度上取决于大气密度。每立方米更多的空气分子意味着更高的撞击机会。行星大气的密度不是均匀的，而是随高度而变化的。这也意味着我们无法![\ overline {CP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)在单个步骤中计算出向外散射。为了克服这个问题，我们需要使用其自身的散射系数来计算每个点的向外散射。

要了解其工作原理，让我们从一个近似值开始。该段 ![\ overline {CP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)分为两部分， ![\ overline {CQ}](JourneyThroughTheAtmosphere.assets/quicklatex.com-cb73d88297fb8cad93709dd990038acb_l3.svg)和 ![\ overline {QP}](JourneyThroughTheAtmosphere.assets/quicklatex.com-e94d672a8559c5e3ff645bbf1ecd35e2_l3.svg)。

![img](JourneyThroughTheAtmosphere.assets/scattering_10a.png)

我们首先计算![C](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)到达的光量![问](JourneyThroughTheAtmosphere.assets/quicklatex.com-dd440a7af28975f52f03607a49307d46_l3.svg)：

​    ![\ [I_Q = I_S \ exp {\ left \ {-\ beta {\ left（\ lambda，h_0 \ right）} \ overline {CQ} \ right \}} \]]](JourneyThroughTheAtmosphere.assets/quicklatex.com-bed106a65f8c0a1e2cb10230fa87ea31_l3.svg)

然后，我们使用相同的方法来计算![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)来自的光量![问](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-dd440a7af28975f52f03607a49307d46_l3.svg)：

​    ![\ [I_P = \ boxed {I_Q} \ exp {\ left \ {-\ beta {\ left（\ lambda，h_1 \ right）} \ overline {QP} \ right \}} \]]](JourneyThroughTheAtmosphere.assets/quicklatex.com-f407f4c9bae5534c63499f9e227f95c0_l3.svg)

如果我们![I_Q](JourneyThroughTheAtmosphere.assets/quicklatex.com-22187d11c373ce6e54fd04beccb15ebe_l3.svg)用第二个等式代替并简化，我们得到：

![image-20200507184414008](JourneyThroughTheAtmosphere.assets/image-20200507184414008.png)

如果两者 ![\ overline {CQ}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-cb73d88297fb8cad93709dd990038acb_l3.svg)和 ![\ overline {QP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e94d672a8559c5e3ff645bbf1ecd35e2_l3.svg)具有相同的长度![ds](JourneyThroughTheAtmosphere.assets/quicklatex.com-0793eaa7d07ca060bd29efdb05f4ed82_l3.svg)，我们可以进一步简化表达式：

![image-20200507184426713](JourneyThroughTheAtmosphere.assets/image-20200507184426713.png)

在两个长度相等的段具有不同的散射系数的情况下，可以通过将各个段的散射系数相乘，再乘以段长度来计算外向散射。

我们可以使用任意数量的细分重复此过程，越来越接近实际值。这导致以下等式：

​    ![\ [I_P = I_S \ exp \ left \ {-\ boxed {\ sum_ {Q \ in \ overline {CP}}} {\ beta \ left（\ lambda，h_Q \ right）} \，ds} \ right \} \ ]](JourneyThroughTheAtmosphere.assets/quicklatex.com-b905c9ea8533efb981594e6b6933ca08_l3.svg)

![h_Q](JourneyThroughTheAtmosphere.assets/quicklatex.com-7a3a1c59e6cc8a5cca87b71d61c1c074_l3.svg)该点的高度在哪里![问](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-dd440a7af28975f52f03607a49307d46_l3.svg)。

就像我们所做的那样，将一条线分成多个段的方法称为**数值积分**。

如果我们假设接收到的初始光量等于![1个](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-69a7c7fb1023d315f416440bca10d849_l3.svg)，则可以得出任意段上的大气透射率方程：

![image-20200507184443825](JourneyThroughTheAtmosphere.assets/image-20200507184443825.png)

我们可以通过用![\ beta](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)Rayleigh散射所使用的实际值替换泛型来进一步扩展该表达式![\ beta](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)：

​    ![\ [T \ left（\ overline {CP} \ right）= \ exp \ left \ {-\ sum_ {Q \ in \ overline {CP}}} {\ boxed {\ frac {8 \ pi ^ 3 \ left（n ^ 2-1 \ right）^ 2} {3} \ frac {\ rho \ left（h_Q \ right）} {N} \ frac {1} {\ lambda ^ 4}}} \，ds \ right \} \ ]](JourneyThroughTheAtmosphere.assets/quicklatex.com-8b74c7ad117f46cc1a67a39d281a6d74_l3.svg)

的许多因素![\ beta](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)是恒定的，可以从总和中排除：

![image-20200507184459395](JourneyThroughTheAtmosphere.assets/image-20200507184459395.png)

由总和表示的量称为**光学深度** ![D \ left（\ overline {CP} \ right）](JourneyThroughTheAtmosphere.assets/quicklatex.com-89fca4cb7ebad0f197124801f47e3362_l3.svg)，这是我们将在着色器中实际计算的量。其余部分是一个只能计算一次的乘法系数，它对应**于海平面**上的**散射系数**。在最终的着色器中，我们将仅计算光学深度，并提供海平面的散射系数![\ beta](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)作为输入。

把它们加起来：

![image-20200507184510684](JourneyThroughTheAtmosphere.assets/image-20200507184510684.png)

如果您对此主题感兴趣，我还建议您阅读[Carl Davidson](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://davidson16807.github.io/tectonics.js//2019/03/24/fast-atmospheric-scattering.html&usg=ALkJrhguC5ChKh6ZD-c1TeYI4319ttUqaQ)关于大气散射的文章，他在其中使用了该迭代方法的改进版本。