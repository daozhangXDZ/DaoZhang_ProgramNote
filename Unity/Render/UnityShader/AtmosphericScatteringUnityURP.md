# 基于物理的大气散射 in Unity URP

背景资料

# 基于物理的大气渲染

## **# 要解决的问题**



以下我们推导**单次散射（single scattering）**的气渲染模型，即光线从太阳发出过、只经过一次散射被改变方向后射入我们的眼睛。



下图显示了我们观察大气时的观察路径***AB\***，我们想知道***B\***点的大气颜色：



![img](AtmosphericScatteringUnityURP.assets/v2-a2dc765da25ec0f3b23eac3e4c1719ea_720w.jpg)来源：https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-1/



这个过程实际上就是对视线路径***AB\***上每一点的光照贡献进行一个积分，下面我们把问题一步步拆分。



**## 问题一：P点的光照是什么？**



由于我们关心的是单级散射，那么唯一的一次散射发生在路径***AB***上的每一点***P***，那么该点的光照强度***Ip***要怎么求呢？它可以理解成是，从***P\***点出发沿着光照方向与大气边缘的交点为***C\***，从***C\***点的光照（我们认为大气层边缘的光照就是太阳发出的光照）经过路径***CP\***衰减后到达***P\***点的光照：



![img](AtmosphericScatteringUnityURP.assets/v2-bb58473846466bfd4c05c7cfc6432e5b_720w.jpg)来源：https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-1/

用公式表示就是：

![img](AtmosphericScatteringUnityURP.assets/v2-d1d381f22ff6867dbea8731a05a8d635_720w.jpg)

其中，***T项\***是**衰减系数（Transmittance）**，它表示在某段路径上的对光照的衰减程度。该公式也可以被认为是**零级散射（zero scattering）**，即不考虑任何散射事件、直接考虑经过衰减后光强。



**## 问题二：在P点发生了什么？**



我们已知到达***P\***点的光照强度为***Ip\***，那么光线在***P\***点经过一次散射后、经路径***PA\***其他大气粒子的衰减后，最终到达人眼的光照强度***Ipa\***为：

![img](AtmosphericScatteringUnityURP.assets/v2-db2deaeefb5790830b272d49993f9228_720w.jpg)

其中，***λ\***是波长，***θ***是图中所示的光线入射方向和观察方向的夹角，***h***是***P\***点的高度。通俗解释下，***S项***是**散射系数（Scattering）**，它表示此次散射事件中有多少光被反射到了***θ\***方向上，***T项\***是衰减系数（Transmittance），它表示在***PA\***路径上的对光照的衰减程度。它们之间是有联系的，简单来说正是因为大气对光线不断发生散射（***S项\***）才导致经过一定路径后光线会发生衰减（***T项***）。接下来对每一项进行解释。



**(1) 散射系数： \*S(λ,θ,h)\***



散射系数和粒子的大小和折射率有关，这里就得解释一下大气粒子的分类。我们知道大气中有很多不同种类的大气分子/粒子，一般在大气渲染模型里把它们分成两大类。一种是小分子，例如氮气和氧气分子等，另一种是大粒子，例如各种尘埃粒子。之所以要进行分类是因为它们对光线有着不一样的行为（这里忽略对光的吸收，只考虑散射）：

- 小分子：指大小远小于光线波长的粒子。小分子对光的散射在前后方向上分布比较均匀，通常会使用**Rayleigh散射（Rayleigh Scattering）**对它们进行建模。由于这些分子大小比波长还要小很多，因此光的波长也会影响Rayleigh散射的程度。
- 大粒子：指大小远大于光线波长的粒子。大粒子在发生散射的时候会把更多的光散射到前向，通常会使用**Mie散射（Mie Scattering）**对它们进行建模。由于光的波长相较于这些粒子大小来说是可以忽略的，因此我们认为Mie散射跟光线波长无关。

![img](AtmosphericScatteringUnityURP.assets/v2-3f42a14f9dfbc1c1f47527136d979365_720w.jpg)



下面以Rayleigh散射为例，解释***S(λ,θ,h)\***的含义。这里直接给出公式，在Rayleigh散射模型中，散射到***θ\***方向上的比例为：

![img](AtmosphericScatteringUnityURP.assets/v2-d37a2d1523117479b2c216803f2853df_720w.jpg)

其中，***λ***是光的波长，***n***是粒子折射率，***N***是海平面处的大气密度，***ρ(h)\***是高度***h\***处的相对大气密度（即相对于海平面的密度，可以理解成***h\***处真正的大气密度与海平面处大气密度的比值，因此它在海平面处值为1，随着***h\***增加不断减小），我们一般会使用指数函数对它的真实曲线进行数学拟合（是一种近似拟合，不要和后面提到的指数函数弄混）：

![img](AtmosphericScatteringUnityURP.assets/v2-c7f4772d09c0ee6f4fb7d85dc21353c6_720w.jpg)

其中，***H\***是大气的整体厚度。



可以看出Rayleigh散射大致和波长的4次幂的成反比，波长越小（越靠近紫光）的光被散射得越厉害。所以白天的时候天空为蓝色，因为蓝光在大气里不断被散射，黄昏的时候天空会变红，因为相比于白天，阳光此时要穿越更厚得多的大气层，在到达人眼之前，大多数蓝光都被散射到其他方向，所以剩下来的就是红光了。



**(2) 衰减系数：\*T(PA)\***



对于大气粒子对光的散射，在传播路径***PA\***上光线会继续衰减。***S(λ,θ,h)\***关心的是被反射到某一特定角度上的光线比例，那么现在我们就需要考虑经过一次散射后，在入射方向上还“剩下来”多少光。



我们先来看一次衰减。假设***I0\***在经过一次散射后损失了***β\***比例的能量，则剩余的能量***I1\***为：

![img](AtmosphericScatteringUnityURP.assets/v2-80f17765f7d7d5f9daeb960159fbb8d3_720w.jpg)

那么经过一段传播路径***PA\***后，余下的能量为：

- 简单情况：如果***β\***为定值，我们可以直接通过微积分得到衰减一段距离***x\***后的剩余能量：

![img](AtmosphericScatteringUnityURP.assets/v2-af72dff7e15b935378c65f6605fe6480_720w.jpg)

- 复杂情况：复杂情况是***β\***是与波长***λ\***和高度***h\***都相关，即不能简单地当成定值。此时，我们就需要用积分来表示了：

![img](AtmosphericScatteringUnityURP.assets/v2-4b51dbc91f62175286092870ee162fc9_720w.jpg)



那么问题是，***β\***是什么？在简单情况下，也是很多游戏里雾效的实现方法中，就拿一个类似雾效密度的参数来代替***β\***。在复杂情况下，我们就需要考虑真实的***β\***是如何计算的。



之前我们一直在讨论的***S(λ,θ,h)\***是在某方向上的散射系数，那么***β\***就是在所有方向上的**总散射系数**。我们还是以Rayleigh散射为例，如果我们对Rayleigh散射的***S(λ,θ,h)\***做球面积分，得到总散射系数***β(λ,h)\***为：

![img](AtmosphericScatteringUnityURP.assets/v2-5c16f047198bb2c5cfd86540273e2bf0_720w.jpg)



终于，我们的公式长度缩短成了两项，不用再看密密麻麻的符号了！上式可以理解成，***β(λ)\***是海平面处的散射系数，随着高度增加，散射强度也不断减小。因为大气相对密度***ρ(h)\***不断减小。据此，我们可以改写***T(PA)\***部分，可以看出，***β(λ)\***其实只跟波长相关，在传播路径上不需要进行积分，因此可以提到积分外部：

![img](AtmosphericScatteringUnityURP.assets/v2-2abd6459f5e2ae486c16856eaad49220_720w.jpg)



我们可以进一步改写其中的积分项。对比简单情况下的公式，积分项对应的其实就是路径长度***x\***，而这部分积分可以理解成**光学距离——Optical Depth**：

![img](AtmosphericScatteringUnityURP.assets/v2-51b550e4b1c594aac75d9b442423c39d_720w.jpg)



同样，我们也可以改写***S(λ,θ,h)\***部分：

![img](AtmosphericScatteringUnityURP.assets/v2-13f86f63fb6c18fdb8a2d54b64e48dc8_720w.jpg)



其中，***P(θ)\***表示在这些被散射的能量中，有多少比例被反射到了***θ\***方向上，它有一个专有名字——**相位函数（Phase Function）**，也被称为**Scattering Geometry**。所以对于Rayleigh散射来说，它的相位函数就是：

![img](AtmosphericScatteringUnityURP.assets/v2-1fc28d073b75b49d9270059264be0686_720w.jpg)



至此，我们简单推导了***S项\***和***T项\***，这样一开始的公式就可以写成：

![img](AtmosphericScatteringUnityURP.assets/v2-e2652c509fd2d33d700ee6437ab36124_720w.jpg)



总结起来，公式表示的含义就是，计算观察路径***AB\***上某一点***P\***的光照贡献：

1. 光线从太阳出发，到达大气边缘的***C\***点
2. 经过路径***CP\***上的衰减到达***P\***点（**0级散射**）
3. 在***P\***点发生一次散射，将一部分光散射到了观察方向上（**1级散射**）
4. 这部分光又经过***AP\***路径上的衰减最终到达了我们的眼睛



**## 问题三：路径AB之间发生了什么？**

![img](AtmosphericScatteringUnityURP.assets/v2-eac80fde9f6e203d3b3402ab99352e56_720w-1588830107198.jpg)来源：https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-1/



***P\***只是***AB\***上的某一点，我们需要对路径***AB\***上的每一点进行积分：

![img](AtmosphericScatteringUnityURP.assets/v2-e8dadefdbb1966bb7ccb4533fad372be_720w.jpg)



其中涉及到了散射系数***β(λ)\***、相位函数***P(θ)\***、光学距离***D(PA)\***等。



**## 小结**



至此，我们完成了单级散射模型的简单推导。但实际情况要复杂得多，在到达人眼之前，光线已经在大气里被散射了无数次，而更高一级的散射总是可以靠它前一级的散射来定义，即是一个**递归定义**：

![img](AtmosphericScatteringUnityURP.assets/v2-ab28709c7fe9f96548a48d80b588a329_720w.jpg)



上式的含义是，在***A***点、从观察方向***v\***、光线入射方向***s\***贡献的第***i+1\***级散射（左侧）等于，对观察路径***AB\***上的每一点***P\***的贡献度进行积分：

1. 在***P***点处发生最后一次散射，把光线从积分方向***v'\***散射到观察方向***v\***上（***β(v,v')\***），然后经过***T(PA)\***衰减后到达***A\***点
2. 在最后一次散射前，对之前发生在***P***点、从方向***v'\***、光线入射方向***s\***贡献的第***i\***级散射做球面积分，表示从各个方向***v'\***贡献的第***i\***级散射



回顾我们之前对单级散射的推导过程，其实就是***i=0***的情况。对于第0级散射来说，由于***v'\***不等于***s\***的方向来说，第0级散射都为0，所以我们省略了公式里做球面积分部分。而在***A\***点、从观察方向***v\***、光线入射方向***s\***最后的光照结果应该是把所有级的散射都加起来：

![img](AtmosphericScatteringUnityURP.assets/v2-a6e4161099ec9d3dcbd48980deb61c96_720w.jpg)



如果是离线渲染，理论上我们可以求得上述公式的精确解。但对于实时渲染来说，第0级和第1级散射都是可以较为快速的求得精确解的，而更高级的散射要计算起来就非常划不来了。在早期的大气渲染资料（例如GPU Gems 2）里，都是对第0级和第1级散射的求解和渲染。直到2008 Precomputed Atmospheric  Scattering的提出，我们也可以实时计算更高级别散射的近似解了。



## **# 大气渲染模型**



具体应用到游戏渲染里，我们一般会把大气渲染分为两个部分：一是天空背景的渲染，即skybox，二是大气透视的渲染，也是我们俗称的大气雾效。在渲染的时候需要考虑光线入射方向***s\***上的遮挡（阴影），通常使用传统的shadow map就可以了。这样我们就可以得到god ray效果。



**## 天空背景**



我们之前推导的公式可以直接拿来渲染天空盒，这里就不重复了。多说一句，第0级散射可以理解成对“sun disk”的渲染。



**## 大气透视**



**大气透视（aerial perspective）**是渲染场景里物体距离摄像机远近的很重要的效果，也是所谓的雾效。与渲染天空盒略微不同的是，我们还需要考虑反射地表颜色等。

![img](AtmosphericScatteringUnityURP.assets/v2-4a37c498da54c483f1ab7eab30251739_720w.jpg)



依然是考虑在***A\***点、沿着观察路径***AB***接收到的光照。这部分光照可以分为两个部分：一是***B\***点反射的地表颜色***Rb\***经过路径***AB\***衰减后的光照，也就是**第0级反射**，二是路径***AB***上由于散射贡献的光照：

![img](AtmosphericScatteringUnityURP.assets/v2-f13c08b5c742c419455a037747897a0f_720w.jpg)

***Textinction\***就是我们之前推导的***T(AB)\***，***Iinscattter\***则是之前推导的多级散射模型。



**## 优化**



核心是使用LUT，例如可以***T(AB)\***存到一张2D纹理里。



**## 例子：简化模型**



大部分游戏的视角只会在地表附近，因此可以使用简化模型来渲染大气雾效。简化模型有两个最明显的特征：

- 使用直线距离***d\***直接代替光学距离***D(AB)\***
- 基于上一点，我们可以使用恒定的散射系数***β\***



**（1）Unity的Exponential Fog**



最简单的例子应该就是**Unity的Exponential Fog**（[https://docs.unity3d.com/Manual/GlobalIllumination.html](https://link.zhihu.com/?target=https%3A//docs.unity3d.com/Manual/GlobalIllumination.html)）了，公式表示就是：

![img](AtmosphericScatteringUnityURP.assets/v2-5be1c751ff7c152070a29253f19fe90e_720w.jpg)



其中的exp部分就是***Textinction\***，即使用恒定的散射系数的简化模型。但后面计算***Iinscattter\***的部分其实是不准确的，可以说是“不怎么基于物理”。



**（2）The Blacksmith中的大气散射**



Unity的The Blacksmith给出了大气散射部分的代码（[https://blogs.unity3d.com/cn/2015/05/28/atmospheric-scattering-in-the-blacksmith/](https://link.zhihu.com/?target=https%3A//blogs.unity3d.com/cn/2015/05/28/atmospheric-scattering-in-the-blacksmith/)，[https://assetstore.unity.com/packages/essentials/the-blacksmith-atmospheric-scattering-39939](https://link.zhihu.com/?target=https%3A//assetstore.unity.com/packages/essentials/the-blacksmith-atmospheric-scattering-39939)）。这部分以后再补吧。



**# 参考资料**



推荐阅读顺序即为排序顺序：

- 入门（理解渲染方程）

- - Atmospheric Scattering系列教程：[https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-1/](https://link.zhihu.com/?target=https%3A//www.alanzucconi.com/2017/10/10/atmospheric-scattering-1/)，详细解释了基本原理和原始的“暴力解法”
  - 2003 Modeling Skylight and Aerial Perspective：[http://mathinfo.univ-reims.fr/IMG/pdf/PreethamSig2003CourseNotes.pdf](https://link.zhihu.com/?target=http%3A//mathinfo.univ-reims.fr/IMG/pdf/PreethamSig2003CourseNotes.pdf)，主要是用来理解大气渲染方程的
  - 2002 Rendering Outdoor Light Scattering in Real Time：[http://developer.amd.com/wordpress/media/2012/10/ATI-LightScattering.pdf](https://link.zhihu.com/?target=http%3A//developer.amd.com/wordpress/media/2012/10/ATI-LightScattering.pdf)，[http://developer.amd.com/wordpress/media/2012/10/ATI-LightScattering.pdf](https://link.zhihu.com/?target=http%3A//developer.amd.com/wordpress/media/2012/10/ATI-LightScattering.pdf)，加上之前的两篇，这三篇看完对渲染方程应该就可以有比较深刻的理解了，可以自己手推

- 进阶（实现渲染方程）

- - GPU Gems 2：[https://developer.nvidia.com/gpugems/GPUGems2/gpugems2_chapter16.html](https://link.zhihu.com/?target=https%3A//developer.nvidia.com/gpugems/GPUGems2/gpugems2_chapter16.html)，经典文章，求解single scattering，虽然文章给出的代码是比较原始的“暴力解法”，但后面给出了关键的优化思想，就是使用LUT
  - 2008 Precomputed Atmospheric Scattering：[https://hal.inria.fr/file/index/docid/288758/filename/article.pdf](https://link.zhihu.com/?target=https%3A//hal.inria.fr/file/index/docid/288758/filename/article.pdf)，[https://ebruneton.github.io/precomputed_atmospheric_scattering/](https://link.zhihu.com/?target=https%3A//ebruneton.github.io/precomputed_atmospheric_scattering/)，除了single scattering还可以得到multiple scattering的近似解，性能也很好，目前是各大3A游戏的标配，缺点是论文写得太难懂，各种数学符号。好在作者给了源码，在2017年的时候甚至优化了代码，增加了可读性和健壮性，良心作者

- 实际应用（GDC）



Unity有很多插件的实现都是基于2008年的Precomputed Atmospheric Scattering，例如uSky（[https://www.assetstore.unity3d.com/#!/content/24830](https://link.zhihu.com/?target=https%3A//www.assetstore.unity3d.com/%23!/content/24830)）、Azure（[https://assetstore.unity.com/packages/tools/particles-effects/azure-sky-dynamic-skybox-36050](https://link.zhihu.com/?target=https%3A//assetstore.unity.com/packages/tools/particles-effects/azure-sky-dynamic-skybox-36050)）等，可以参考和优化。



实现

## 前言**

最近一直在研究大气散射，同时也想验证一下Unity的URP是否好用。目前开始能见到一些效果了，如下：

![img](AtmosphericScatteringUnityURP.assets/v2-5e6124ca86975e76f3cd1ee07db053b8_720w.jpg)项目效果截图



打算开文章写一下实现细节，实现到哪写到哪，本文将会不定期更新。当前Github工程如下：

[PZZZB/Atmospheric-Scattering-URP](https://link.zhihu.com/?target=https%3A//github.com/PZZZB/Atmospheric-Scattering-URP)[github.com![图标](AtmosphericScatteringUnityURP.assets/v2-f113d7c6cec80257366f442b2c5423e7_ipico.jpg)](https://link.zhihu.com/?target=https%3A//github.com/PZZZB/Atmospheric-Scattering-URP)

要求：

- Unity2019.3.4
- Universal Rendering Pipeline 7.3.1

大气散射在游戏中的重要性不必多说，不管是营造真实的氛围，还是掩盖细节都不可或缺，往往一个好的全局氛围可以马上提升游戏整体的表现力。

说到大气散射，就必须先了解其理论和模型。这里不作太多解释，有更详细的资料可以学习，我个人十分推荐先从Zucconi的这一系列教程 （共8篇）开始：

[Zucconi 的 Volumetric Atmospheric Scattering](https://link.zhihu.com/?target=https%3A//www.alanzucconi.com/2017/10/10/atmospheric-scattering-1)[[1\]](https://zhuanlan.zhihu.com/p/127026136#ref_1)

关于公式的推导过程，可以参考冯乐乐的这一篇，每一步都讲解的非常清楚：

[冯乐乐的基于物理的大气渲染 ](https://zhuanlan.zhihu.com/p/36498679)[[2\]](https://zhuanlan.zhihu.com/p/127026136#ref_2)

仔细看这几篇包括里面引用的论文，并自己推导一遍公式，就可以有一个比较完善的认识了。



这里我简要仅简要总结一下散射理论和模型。

## **散射理论**

根据大气层中粒子的直径分布，散射又分为三种：

**Rayleigh散射**（粒子直径远小于波长)

**Mie散射**（粒子直径和波长相当）

**Geometry散射**（粒子直径大于波长）



如果不考虑云层的情况，那么大气中散射基本以Rayleigh和Mie散射为主。



**Scattering Equation 散射函数**用于描述入射光散射到特定方向上的大小，

以Rayleight散射为例，其散射函数为：



![[公式]](AtmosphericScatteringUnityURP.assets/equation-1588828832235.svg) 

![image-20200511111323586](AtmosphericScatteringUnityURP.assets/image-20200511111323586.png)



在这个公式里面除了密度百分比和角度以外，其他都是可以提前确定的常数。

粒子密度百分比在海平面上为1，随着高度的上升而指数下降，可以用指数函数来拟合：

![[公式]](AtmosphericScatteringUnityURP.assets/equation-1588828832253.svg) 

其中表示Scale Height，是一个常数。

并且可以看到Rayleigh散射与光的波长的4次幂的成反比，波长越小（靠近光谱的紫色端）的光被散射得越厉害。这也是为什么白天的时候天空为蓝色，因为蓝光在大气里散射后充满整个天空。黄昏的时候天空呈现红色，因为此时阳光需要穿过更厚的大气层，在到达人眼之前，大多数蓝光都被散射到其他方向，剩下来的就是红光了。



![img](AtmosphericScatteringUnityURP.assets/v2-b473e3cf6e17ba71df4df928de818576_720w.jpg)



Rayleigh Scattering 来源：https://en.wikipedia.org/wiki/Rayleigh_scattering

Mie散射和光的波长无关，但它在某些方向散射更强，它是造成太阳周围形成光晕的主要原因。

显然，对散射函数作球面积分，就得到一次散射过程丢失的总能量，也叫**Scattering Coefficient散射系数**，

记作：

![[公式]](AtmosphericScatteringUnityURP.assets/equation-1588828832243.svg) 

常数部分放一起，就成了常数乘密度函数，显然散射系数和方向是无关的。

将散射函数除以散射系数，就得到了**Phase Function（相位函数）**，他表示散射出去的能量中，在每个方向的分布比例，Rayleigh和Mie的相位函数如下：

![image-20200511110944877](AtmosphericScatteringUnityURP.assets/image-20200511110944877.png)



![img](AtmosphericScatteringUnityURP.assets/v2-97b869421c44a70ea99a97c7a5d4e8cc_720w.jpg)左：Rayleigh Phase Function。右：Mie Phase Function，从左往右代表g=0.75，0.5，0，-0.5，-0.75的分布

## **大气散射模型**

大气散射模型分为两种：Single Scattering和Multi Scattering。

Single Scattering，即只考虑太阳光经过**一次散射**后抵达我们的眼睛。

Multi Scattering，考虑光线**多次散射**过程的模型。显然这更符合现实世界的情况，但下一级的散射取决于与上一级散射的结果，也就是说这是一个递归方程，实现起来并不太容易。Eric Bruneton给出了一种方法 [[3\]](https://zhuanlan.zhihu.com/p/127026136#ref_3)通过使用LUT把当前一级散射结果存起来，下一级散射从上一级LUT读取结果再计算，能够视线实时渲染Multi Scattering，这也是目前主要实现Multi Scattering 的方法。

由于第二次散射以上的能量较少，对最终视觉的影响程度有限，所以目前Single Scattering还是一种相对实现简单效果也不会差很多的模型，本文实现的也是Single Scattering：

![img](AtmosphericScatteringUnityURP.assets/v2-eac80fde9f6e203d3b3402ab99352e56_720w.jpg)来源：https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-1/

假设我们在点A看向点B，Single Scattering指的是路径上的每一个点，比如P0,P1,P2，每个点都会收到太阳穿过大气入射的光线，并将光散射到点A方向后被我们看到，这个过程我们叫做**In Scattering**。对路径上所有的点的In Scattering的光都累加（P0,P1,P2...) 起来（积分），就形成了我们看到的点B经过散射效应后的样子。

现在我们只看路径上的一个点，如点P0，阳光在抵达点P0的这段路程，会因为散射发生一定的损耗，这叫做**Out Scattering**，损耗之后还剩下的能量比例，由**Beer–Lambert law（比尔-朗伯定律）**决定：

![image-20200511141119898](AtmosphericScatteringUnityURP.assets/image-20200511141119898.png)

指数部分的术语，叫做**Transmittance ，或者Optical Length（光学长度）**，其中 ![[公式]](AtmosphericScatteringUnityURP.assets/equation-1588828832219.svg) 表示**散射系数**， ![[公式]](AtmosphericScatteringUnityURP.assets/equation-1588828832248.svg) 为大气密度函数。我们把这一项记作T，即:

![image-20200511141246071](AtmosphericScatteringUnityURP.assets/image-20200511141246071.png)

对于点P0来说，太阳光从宇宙空间出发，穿过地球大气层，抵达P0（此过程发生Out Scattering) 用公式就表示为:

![image-20200511141326716](AtmosphericScatteringUnityURP.assets/image-20200511141326716.png)

接着，抵达点P的光还要散射到我们的视觉方向，也就是乘以一个散射函数：

![image-20200511141342033](AtmosphericScatteringUnityURP.assets/image-20200511141342033.png)

然后，这部分光抵达我们的眼睛，路径上还需要经过Out Scattering：

![image-20200511141353683](AtmosphericScatteringUnityURP.assets/image-20200511141353683.png)

最后，我们要把视线上每个点贡献的都加起来，也就是对路径AB积分，最终得到：

![image-20200511141405292](AtmosphericScatteringUnityURP.assets/image-20200511141405292.png)

这是Single Scattering的一般式，所谓一般是指大气密度处处不均匀。这时候，光学长度T是一个积分，因此整体很难得到简单的解析式。可以暴力遍历路径上的点计算积分，即Ray Marching，也就是Alan的教程中[[1\]](https://zhuanlan.zhihu.com/p/127026136#ref_1)使用的方法。优化方法就是提前把一些数据比如光学长度计算到Look Up Table中。

## **空中透视模型**

在实际人站在地球表面的情况，视线触及的范围（不包括天空）相比地球的规模可以忽略不记，因此我们可以把地表的大气密度看作是常数，这样光学长度就只和距离有关了，经此假设我们可以化简一般式为：

![image-20200511141429640](AtmosphericScatteringUnityURP.assets/image-20200511141429640.png)

如果同时考虑Rayleigh和Mie散射，最终得到In scattering的公式为：

![image-20200511141440328](AtmosphericScatteringUnityURP.assets/image-20200511141440328.png)

由于我们假设了场景规模相较于地球忽略不计， ![[公式]](AtmosphericScatteringUnityURP.assets/equation-1588828832286.svg) 其实就等于Main Light了，是一个可以提前确定的常数。公式中唯一的变量是s，即物体到摄像机的距离。

![img](AtmosphericScatteringUnityURP.assets/v2-f4afceb1e6c6d35613c270ba1781391e_720w.jpg)



考虑在近地面观察一个物体，物体本身发出的光是要经过Out Scattering才能达到我们的眼睛的，

于是有：

![image-20200511141512567](AtmosphericScatteringUnityURP.assets/image-20200511141512567.png)

把C的乘数称作Extinction项，In即In Scattering项。即：

![image-20200511141539552](AtmosphericScatteringUnityURP.assets/image-20200511141539552.png) 

本文的实现**

用Single Scattering实现的In Scattering作为天空，对地表的物体运用大气密度恒定的空中透视模型。

参考文献：

[Rendering Parametrizable Planetary Atmospheres with Multiple Scattering in Real-Time](https://link.zhihu.com/?target=http%3A//www.cescg.org/CESCG-2009/papers/PragueCUNI-Elek-Oskar09.pdf)[[4\]](https://zhuanlan.zhihu.com/p/127026136#ref_4)

[Rendering Outdoor Light Scattering in Real Time](https://link.zhihu.com/?target=http%3A//citeseerx.ist.psu.edu/viewdoc/download%3Fdoi%3D10.1.1.192.1514%26rep%3Drep1%26type%3Dpdf)[[5\]](https://zhuanlan.zhihu.com/p/127026136#ref_5)

参考项目：

[SlightMad的Atmospheric Scattering for Unity 5](https://link.zhihu.com/?target=https%3A//github.com/SlightlyMad/AtmosphericScattering)[[6\]](https://zhuanlan.zhihu.com/p/127026136#ref_6)

[Unity的Atmospheric Scattering in The Blacksmith](https://link.zhihu.com/?target=https%3A//blogs.unity3d.com/cn/2015/05/28/atmospheric-scattering-in-the-blacksmith/)[[7\]](https://zhuanlan.zhihu.com/p/127026136#ref_7)

SlightMad这一篇是完全全程用不均匀密度的Single Scattering计算的。他的完成度很高，并且提供RayMarching和预计算LUT两种方法，很适合学习。

Unity的这一篇则是典型的空中透视模型。并且它的参数设置比较偏向美术，初次学习看不太懂，但是效果非常不错。此外他还额外叠加了“指数高度雾”，用于弥补大气密度恒定带来的问题。



根据空中透视模型的公式： ![image-20200511141620157](AtmosphericScatteringUnityURP.assets/image-20200511141620157.png)

Extinction项：

![img](AtmosphericScatteringUnityURP.assets/v2-06a9dfa2337e2b64342cfdeb8d5fe870_720w.jpg)

In Scattering项：

![img](AtmosphericScatteringUnityURP.assets/v2-d718e69c08dea4b915902169a1c18cd4_720w.jpg)

叠加结果：

![img](AtmosphericScatteringUnityURP.assets/v2-4fb739ce675ad330350174b595a8ea8c_720w.jpg)

## **Sun**

在In Scattering中渲染太阳的方法，可以叠加多一次Mie Scattering的方法实现[[4\]](https://zhuanlan.zhihu.com/p/127026136#ref_4)，Phase Function中的g需要选用较高的值。

![img](AtmosphericScatteringUnityURP.assets/v2-ba7db23aef09e377b0bb9428d7430362_720w.jpg)

上，g=0.99；下：g=0.98

## **Light Shafts**

Light Shafts，或者叫体积光，由于存在阴影的关系，光在抵达视线的过程中还需要考虑遮挡的问题。

![img](AtmosphericScatteringUnityURP.assets/v2-578e5b19f6a87c01d4d9eb74622bc1f1_720w.jpg)

上：不考虑阴影。下：在阴影处形成体积光

一般的实现方法就是在屏幕空间，从Depth Map重建像素的世界坐标，再从世界坐标到摄像机进行Ray Marching N次，每个点转到Shadow map空间后判断可见性，叠加起来后就得到Light Shafts。

这种方法最大的问题就是效率，因为屏幕上的每个点都要计算N次。如果N过小，效果不太好。

一种优化的思路就是进行Down Sample，然后通过Dithering抖动采样，并进行模糊处理，可以在N较小的情况下得到不错的结果。

![img](AtmosphericScatteringUnityURP.assets/v2-9f8c0b0c9543ef0eb8091ba5cb92ee75_720w.jpg)

上：每像素64次采样。中：每像素16次采样。下：每像素16次Dithering采样

不过目前还有一些效率更高的方法，一个是针对采样方法的优化[[8\]](https://zhuanlan.zhihu.com/p/127026136#ref_8)。

还有另外一种通过构造网格实现的方法[[9\]](https://zhuanlan.zhihu.com/p/127026136#ref_9)。

以后有机会实现的话再研究吧。

### **Look Up Table**

根据实际需要。如果是静态的天空盒则很容易，把In Scattering烘焙到Cube Map中作为天空盒：

![img](AtmosphericScatteringUnityURP.assets/v2-02f86f807b7aca75a527ad746f26d582_720w.jpg)

利用Reflection Probe烘焙成HDRI CubeMap



如果说需要动态的天空，那么为了优化需要将In Scattering计算到LUT中。In Scattering和3个参数有关：视线方向，太阳方向和高度，需要3维的LUT。如果摄像机的高度不会改变，那么可以排除掉高度只需要2维的LUT。这就取决于实际情况了。

### **确定主平行光和环境光**

随着太阳角度的变化，也会跟着变化，并且环境光也会跟着变化。

为了保证整个环境的物理一致性，我们需要控制当前的Main Light Color和Ambient。

这些数据可以利用Compute Shader提前计算出来。

由于我们已经假设了地表上大气密度恒定，因此其实就是阳光经过Out Scattering抵达摄像机处的结果。

对于环境光，我们需要对In Scattering乘法线点乘方向做半球积分：

![image-20200511141745193](AtmosphericScatteringUnityURP.assets/image-20200511141745193.png)

其中N表示法线，可以直接用world up表示。

利用`UnityEngine.Random.onUnitSphere`可以快速生成随机的单位方向向量。

在Compute Shader中计算之后，要把结果读取回CPU并序列化起来，以便在后续渲染中直接使用。借助一张临时的Texture2D，从Render Texture中拷贝内容：

```csharp
RenderTexture currentActiveRT = RenderTexture.active;
RenderTexture.active = src;
dst.ReadPixels(new Rect(0, 0, dst.width, dst.height), 0, 0);
RenderTexture.active = currentActiveRT;
```

### **缺点**

缺陷在于本来大气密度是随着海平面升高呈指数降低的，这会造成山脚下雾气浓厚的效果，或者也叫“指数高度雾”。在比较大规模的场景中，或者从山上眺望的场景中，恒定的大气密度就会比较假。

Unity的Black Smith[[7\]](https://zhuanlan.zhihu.com/p/127026136#ref_7)专门额外叠加了一个指数高度雾来解决此问题。

### **关于Universal Render Pipeline**

鉴于URP灵活的架构，整体实现来说还是比较方便的。不过目前的URP还是有不少小毛病，我自己就遇到了好几个莫名其妙的问题，并且都是确定或还未确定的bug，等待官方的进一步提高稳定性吧。

关于自定义后处理。目前是还不能嵌入到默认的Volume 系统中。需要自行实现一个ScriptableRenderFeature，可以参考官方的 [Universal Rendering Example]:

 ([https://github.com/Unity-Technologies/UniversalRenderingExamples](https://link.zhihu.com/?target=https%3A//github.com/Unity-Technologies/UniversalRenderingExamples))

## 参考

1. ^[a](https://zhuanlan.zhihu.com/p/127026136#ref_1_0)[b](https://zhuanlan.zhihu.com/p/127026136#ref_1_1)Zicconi17 https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-1
2. [^](https://zhuanlan.zhihu.com/p/127026136#ref_2_0)Feng18 https://zhuanlan.zhihu.com/p/36498679
3. [^](https://zhuanlan.zhihu.com/p/127026136#ref_3_0)Eric08 https://hal.inria.fr/inria-0028
4. ^[a](https://zhuanlan.zhihu.com/p/127026136#ref_4_0)[b](https://zhuanlan.zhihu.com/p/127026136#ref_4_1)Elek09 https://old.cescg.org/CESCG-2009/papers/PragueCUNI-Elek-Oskar09.pdf
5. [^](https://zhuanlan.zhihu.com/p/127026136#ref_5_0)Hoffman http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.192.1514&rep=rep1&type=pdf
6. [^](https://zhuanlan.zhihu.com/p/127026136#ref_6_0)SlightMad16 https://github.com/SlightlyMad/AtmosphericScattering
7. ^[a](https://zhuanlan.zhihu.com/p/127026136#ref_7_0)[b](https://zhuanlan.zhihu.com/p/127026136#ref_7_1)Unity15 https://blogs.unity3d.com/cn/2015/05/28/atmospheric-scattering-in-the-blacksmith/
8. [^](https://zhuanlan.zhihu.com/p/127026136#ref_8_0)Yusov13 https://software.intel.com/sites/default/files/managed/b9/1d/gdc2013-lightscattering-final.pdf
9. [^](https://zhuanlan.zhihu.com/p/127026136#ref_9_0)Hoobler16 https://developer.nvidia.com/sites/default/files/akamai/gameworks/downloads/papers/NVVL/Fast_Flexible_Physically-Based_Volumetric_Light_Scattering.pdf