# "上帝说要有光"——游戏真实感光照技术



711501594                     

**1****、****引言**

光照技术一直是计算机图形学中最为活跃的分支之一,它在真实感渲染中扮演着举足轻重的角色.伴随着计算机硬件机能的日益提高,尤其是GPU技术的日新月异,应用于游戏开发实的时光照技术也有了长足进展,从最初简单的局部光照,到基于全局光照算法的静态光照技术的应用,再到今天对动态全局光照的实时近似模拟.

我们知道,人类对物体的视觉感知来源于从物体发射和(或)反射并进入人眼的光线,光照运算正是着眼于通过各种方法估算从光源发出的光线和物体发生交互最后到达观察点时的能量强弱.

本文分为基础篇和应用篇两个部份,其中基础篇介绍真实感光照运算的基础理论,应用篇则是基于光照运算的基础理论简介图形渲染中的经典和常用的光照算法.希望通过这两篇的介绍,使大家能对计算机图形渲染中的光照技术的研究内容和发展方向和现状有一个基本的了解.

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image001.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.001.1433145964.jpeg)

局部光照

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image002.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.002.1433145965.jpeg)

基于全局光照的Lightmap

![](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.003.1433145965.jpeg)

CryEngine3中的动态全局光照

**2****、****基础篇**

无论是强调定性研究的简单如Lambert/Phong等的局部光照模型,还是PRT/RSM等对全局光照的实时近似模拟,甚或是复杂如Path Tracing/Photon Mapping等强调定量分析的离线渲染器的核心算法,其理论基础和参考/评估原型都是以下要介绍到的光能量的度量及其传递原理.

**2.1****、****光能量的度量**

要计算一种物理量首先需要知道它的度量方法.光是一种电磁波,以电磁辐射通用的辐射线测定法( Radiometry )作为其能量的度量方法.

**2.1.1****、****辐射能量( Radiant energy )**

单位为焦耳(J),一般以大写字母Q表示.

**2.1.2****、****辐射通量( Radiant flux )**

辐射通量是单位时间通过表面( Surface )的辐射能量,这里的***表面***是一个广义的概念,既可以是实际的物质表面,也是可以是空间中一个假想的表面,***通过***包括能量的出射和入射两种情况.辐射通量的单位是焦耳/秒(![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image004.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.004.1433145965.png))即瓦特( W ),一般以符号Ф表示.

​      

**2.1.3****、****辐射照度( Irradiance )**

辐射照度指的是单位面积的表面***入射***的辐射通量,也即表面接受的辐射通量的密度,其单位为 瓦特/平方米![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image005.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.005.1433145965.png).我们以大写字母E表示辐射照度,大写字母A表示辐射通量通过的表面的面积,由定义易知其计算公式为:

​       E = ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image006.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.006.1433145965.png)

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image007.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.007.1433145965.png)

内圈的辐射照度大于外圈的辐射照度

**2.1.4****、****辐射度( Radiosity )**

辐射度和辐射照度是相对的概念,指的是单位面积的表面***出射***的辐射通量,其单位和计算公式都与辐射照度一致,一般以大写字母B表示:

​       B = ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image006.png](http://gameweb-img.qq.com/gad/20150601/f198a0c8dd9142f0a018467290e7be02.006.1433145965.png)

**2.1.5****、****辐射率( Radiance )**

辐射率是非常重要的一个概念,前文提到的光照运算的结果:到达观察点的光能量的***强弱***就是以辐射率来衡量的.在正式介绍辐射率的定义之前需要引入另外两个重要的概念:投影面积( Projected area )和立体角( Solid angle ).

投影面积指的是原始表面(在光照运算中一般是发射光能的表面)在目标表面(在光照运算中一般是接受光能的表面)的投影区域的面积,我们以符号 ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image008.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.008.1433145965.png)表示投影面积,θ表示初始表面法线和目标表面法线之间的夹角,A表示初始表面面积,则![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image008.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.008.1433145965.png)的公式为:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image009.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.009.1433145965.png)

​    ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image010.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.010.1433145965.png)                       倾斜表面的能量分布到了更大的区域上

立体角是基于点(在光照运算中一般是观察点的目标点)及表面(在光照运算中一般是以观察方向为法线的微表面)来说的:在以这个点为中心的单位球体中,以球心为视角,表面所覆盖的球体表面积即为立体角,虽然数学和物理学都没有定义立体角的单位,但为了表示方便,通常我们以sr作为立体角的单位.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image011.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.011.1433145965.png)

c在单位球面上占据表面积s

有了以上两个概念作为基础,就能顺理成章的引出辐射率的定义了:对于表面上给定的方向,单位投影面积,单位立体角的辐射通量.单位为(![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image012.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.012.1433145965.png)).我们以大写字母L表示辐射率,ω表示立体角,则辐射率的公式为:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image013.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.013.1433145966.png)

直观的讲,辐射率描述了沿着某一方向***通过***一个点(微平面)的能量强弱.和辐射通量的定义一样, ***通过***包括能量的出射和入射两种情况,通常我们以下标表示不同的情况:![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image014.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.014.1433145966.png)表示入射辐射率( Incident radiance ),![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image015.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.015.1433145966.png)表示出射辐射率( exitant radiance ).

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image016.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.016.1433145966.png)

​                                                                 辐射率

总结以上的讨论,我们可以得出一个有趣的结论,辐射率实际上是一个关于位置(p)和方向(![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image017.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.017.1433145966.png))的函数即L(p,![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image018.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.018.1433145966.png)).如果计算出了场景中每一个点通过每一个方向的辐射率,那么也就得到了这个场景的外观(出于效率的考虑,在实际渲染中我们仅需计算在当前观察点下场景可见部份的辐射率).

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image019.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.019.1433145966.png)

出射/入射辐射率

另外需要说明的是,光的颜色是由其波长分布所决定的,我们平常所观察到的光一般是复色光,是由各种不同波长的单色光混合叠加而成的.因此,要正确估算出光的颜色,就需要分别计算出各波长单色光的能量强弱即辐射率.幸运的是,人类的视网膜只对三种特定波长分布的光能量最为敏感,视神经根据这三种光能量的强弱比例来确定光的颜色.出于这个原因,我们只要分别计算出三种特定颜色(原色)的光的辐射率就可以了,在计算机图形学领域,我们取红绿蓝(RGB)为原色.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image020.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.020.1433145966.jpeg)

可见光及其波长

**2.2****、****光能的传递**

在了解了光能量的度量方法之后,我们就可以开始研究光能和物体的具体交互过程了,本文主要围绕光照运算中最基本也是最重要的一种情况进行讨论,即对于给定的点(微平面),其出射辐射率(![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image015.png](http://gameweb-img.qq.com/gad/20150601/f198a0c8dd9142f0a018467290e7be02.015.1433145966.png))和入射辐射率(![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image014.png](http://gameweb-img.qq.com/gad/20150601/f198a0c8dd9142f0a018467290e7be02.014.1433145966.png))之间的函数映射关系.

**2.2.1****、** **BRDF**

BRDF是bidirectional reflectance distribution function的首字母缩写,即双向表面反射分布函数,它描述的是在给定点(微平面)处,入射辐射照度和出射辐射率之间的比例关系,其公式为 :

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image021.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.021.1433145966.png)

​     其中![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image022.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.022.1433145966.png)是BRDF的符号,x是点p的位置,![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image023.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.023.1433145966.png),![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image024.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.024.1433145966.png)分别表示入射光和出射光的方向

​       根据辐射照度和辐射率之间的关系,我们可以进一步得到:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image025.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.025.1433145967.png)

其中![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image026.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.026.1433145967.png)是入射辐射率方向和给定点处表面法线的夹角,![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image027.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.027.1433145967.png)是入射光立体角的微分.

物体的外观属性即材质正是由BRDF来描述的,常见的漫反射,高光反射,镜面反射等其实都可以表述为一种特定的BRDF.

BRDF具有如下一些重要性质:

1.波长相关性( Wavelength dependency ):BRDF一般是波长相关的,对于不同波长(即不同的颜色)的光能量材质对其的反射属性一般也是不同的,基于此,物体才有了各异的颜色外观,呈现给我们一个五彩缤纷的世界.

2.对等性( Reciprocity ):BRDF中交换入射方向和出射方向的位置,其函数值保持不变,即![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image028.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.028.1433145967.png)

3.能量守恒( Energy conservation ):光照过程实际上是一个能量传递的过程,自然而然的,该过程应满足能量守恒定律,即在给定点(微平面)处,出射的光能量必然小于等于入射的光能量(有可能被吸收一部份).

4.各向同性( isotropic )和各向异性( Anisotropy ):在BRDF中,保持x,![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image029.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.029.1433145967.png)三个参数的值不变.让该BRDF描述的表面绕其法线旋转,如果BRDF函数值保持不变,则该BRDF是各向同性的,反之则是各向异性的.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image030.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.030.1433145967.png)

BRDF决定出射光能与入射光能的关系

**2.2.2****、****光能的本地反射方程**

有了BRDF作为基础,光能本地反射的方程就很容易描述了:在给定点(微平面)处,某一个方向的出射辐射率和该点所处的光环境即所有方向(一般是该点所处的正半球空间)的辐射照度或入射辐射率之间的关系,它是一个积分式:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image031.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.031.1433145967.png)

这里,![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image032.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.032.1433145967.png)表示的是一个定积分,积分区间是该点所处的正半球空间.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image033.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.033.1433145967.png)

​                                                        点p所处的半球面

光能的本地反射方程决定了表面在特定光环境中的外观,是图形学中一个非常重要的公式,虽然它很难直接计算,但它是一切实用的图形渲染光照算法的理论基础,评判一个基于物理的光照算法的优劣,很大程度上就是分析其计算方法和该公式的匹配程度.

**2.2.3****、****延伸**

BRDF仅仅描述了光能从某个方向到达表面的给定点处并从同一位置从某些方向反射回全部或部份光能的规律.那折射(水,玻璃等),次表面散射(皮肤,玉石等)的情况又该怎样去描述呢?答案很简单,其实只要对BRDF函数进行扩展就可以了:1.BRDF中的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image034.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.034.1433145967.png)可以和![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image035.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.035.1433145967.png)分别位于不同的半球空间, 且![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image035.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.035.1433145967.png)的取值可以覆盖整个球面.2.BRDF中的位置信息x,分成独立的两个:![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image036.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.036.1433145967.png),![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image037.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.037.1433145967.png),分别表示光能入射位置和出射位置.

经过了这些扩展后,BRDF已经不能准确的表达函数的作用了,因此,这个函数又有了BTDF(bidirectional  transmission distribution function),BSDF(bidirectional scattering  distribution function),BSSRDF(bidirectional scattering surface  reflectance distribution function )等新名称.另外,我们还可以统称此类描述光能和表面交互规律的函数为BxDF.

另外需要提到的是,我们经常用到的用来计算光能被反射和折射所占比例的Fresnel方程也是BRDF的组成部份.

**3****、****应用篇**

在基础篇中我们已经讲到,光能传递方程是一个积分式,并且在数学上一般无法用解析的方法估算其精确值.那么在实际的渲染程序中,尤其是实时渲染中,光能传递方程是如何估值,从而准确的表现出材质的视觉外观的呢?

本篇将由浅入深,首先介绍光照算法中常用的BRDF,然后分别介绍局部光照和全局光照中的常用技术.

**3.1****、****常用BRDF**

要估算光能传递方程,首先要解决的是,BRDF该如何定义以适应复杂多变的材质外观属性的问题.

**3.1.1****、****Lambert**

Lambert是最简单的BRDF之一,它描述的是理想漫反射表面与光能的交互作用,即入射光能会均匀的向整个半球空间反射回去,Lambert一般用于表现拥有粗糙表面的物体材质,其公式为:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image038.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.038.1433145968.png) 

其中![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image039.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.039.1433145968.png)指代材质的反照率(albedo)函数,通常可将其理解为漫反射颜色,容易看到,在给定点处,Lambert BRDF就是一个常数,这完全符合我们对漫反射的直观理解.

这里的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image040.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.040.1433145968.png)是一个能量守恒系数,需要说明的是,在Phong等本地光照模型公式中一般看不到这个系数,因为它一般会被笼统的合入”光源颜色与亮度 ”一类的系数中,以减少运行时运算开销并使得公式更加简略易懂.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image041.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.041.1433145968.png)

Lambert漫反射光照

**3.1.2****、****Specular reflection**

镜面反射直观上很容易理解,即任意方向的出射辐射率与从该方向的理想反射方向入射的辐射率是一个正比例关系.因为发生镜面反射的物体表面是光滑表面,这个比例系数就是Fresnel系数,即![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image042.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.042.1433145968.png).

根据![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image043.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.043.1433145968.png)与![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image044.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.044.1433145968.png)的关系式,我们可以确定,镜面反射满足Dirac delta分布规律,即

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image045.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.045.1433145968.png)且![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image046.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.046.1433145968.png)

简单的讲就是只有当光能出射方向和入射方向满足理想反射定律时,镜面反射BRDF的值才不为0.

基于以上的基础,我们得出镜面反射BRDF的公式为:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image047.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.047.1433145968.png)

​     其中,R是理想反射向量计算函数,n是面法线.

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image048.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.048.1433145968.png)

镜面反射

**3.1.3****、****Refraction**

折射描述的是光能在两种介质的交接面处发生的传播方向的改变,折射和镜面反射的规律类似,只是光能的出射和入射方向遵守理想反射定律而是Snell法则:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image049.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.049.1433145968.png)

​     其中η指带介质的折射率,T是计算折射向量的函数.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image050.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.050.1433145969.png)

折射

**3.1.4****、****Microfacet**

以上介绍的BRDF只能描述自然界中一些特殊,简单的物体的材质,我们需要根据这些基本BRDF函数推导出一些更通用的BRDF函数.

微表面模型将物质表面抽象为由符合理想漫反射和理想镜面反射的微观表面构成的复杂宏观表面,并通过统计学方法考察光能和大量微观理想表面的总体交互规律(仅基于几何光学),以此来描述复杂材质与光能的交互作用.

Microfacet模型假定构成宏观表面和微观表面具有如下一些性质:

\1.       微观表面成对排列为V型凹槽,因此光能间接传递只能发生在这两个成对的微观表面之间,以此简化运算.

\2.       微观表面的面积远小于与之交互的光波波长.(几何光学的要求)

\3.       微观表面的面积远小于一个着色点(像素).

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image051.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.051.1433145969.png)

Microfacet假定宏观表面由特定分布的微观表面构成

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image052.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.052.1433145969.jpeg)

光能在微观表面之间传递:间接反射,遮挡,投影

依据微观表面选择的理想反射模型的不同,Microfacet模型分为以下两种:

**3.1.4.1****、****Oren-Nayar**

Oren-Nayar模型主要用来描述粗糙表面材质,它假定构成宏观表面的微观表面都是理想漫反射表面,用微观表面朝向的标准差![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image053.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.053.1433145969.png)来描述微观表面的朝向分布情况也即是宏观表面的粗糙程度,标准差越趋于0则表面越粗糙,当标准差为0时,Oren-Nayar退化为理想漫反射模型,其BRDF函数为:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image054.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.054.1433145969.png)

​      其中:

​      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image055.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.055.1433145969.png)

​      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image056.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.056.1433145969.png)

​      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image057.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.057.1433145969.png)

​      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image058.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.058.1433145969.png)

​      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image059.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.059.1433145969.png)是入射向量和出射向量在反射表面上的投影向量的夹角

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image060.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.060.1433145969.png)

Oren-Nayar漫反射

**3.1.4.2****、****Torrance-Sparrow**

和Oren-Nayar相对的,Torrance-Sparrow模型主要用来描述光泽(glossy)表面材质,它假定构成宏观表面的微观表面都是理想镜面反射表面.Torrance-Sparrow模型中最重要的部份当属理想微表面分布函数![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image061.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.061.1433145969.png),它决定对于给定的光能出射和入射方向在宏观表面上符合理想镜面反射的微表面的比例,其BRDF函数为:

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image062.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.062.1433145969.png)

其中![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image063.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.063.1433145969.png)是几何衰减项,即微观表面的相互遮挡对反射光能的衰减效果.

微表面分布函数让Torrance-Sparrow拥有灵活的表现,常用的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image061.png](http://gameweb-img.qq.com/gad/20150601/f198a0c8dd9142f0a018467290e7be02.061.1433145969.png)有以下两种:

**3.1.4.2.1****、****Blinn**

使用Blinn微表面分布函数的Torrance-Sparrow模型适于表现一般的具有高光反射属性的材质,它用一个指数衰减函数来描述微表面法线的分布:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image064.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.064.1433145970.png)

​     其中e越大,表面越光滑.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image065.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.065.1433145970.png)

应用Blinn分布的高光

**3.1.4.2.2****、****Ashikhmin Shirley**

使用Ashikhmin Shirley微表面分布函数的Torrance-Sparrow模型主要用来描述各向异性的光泽表面:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image066.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.066.1433145970.png)

有别于Blinn分布,该分布函数分别用两个参数![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image067.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.067.1433145970.png),![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image068.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.068.1433145970.png)控制微观表面在两个水平方向上的指数衰减型分布,其中![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image069.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.069.1433145970.png)是实际分布方向的方位角(与X分布方向的水平夹角).

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image070.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.070.1433145970.jpeg)

应用Ashikhmin Shirley分布的各向异性高光

**3.2****、****局部光照技术简介**

局部光照是游戏渲染中使用的最为悠久的光照技术,并且由于运行效率的原因,至今仍被广泛的使用着.局部光照主要有下列特性:

\1.       使用的光照模型一般都是简单的,计算量很小的物理不正确的经验模型.

\2.       一般使用方向光源和点光源等假想光源而不是物理正确的面光源.

\3.       主要考虑光能在光源与物体表面之间的直接传递,在物体与物体之间的间接传递一般笼统的用环境光来粗略模拟.

**3.2.1****、****Phong光照模型**

Phong光照模型是应用的最为广泛的局部光照模型,在固定管线时代,它获得了硬件层面的直接支持,在如今的可编程管线时代,依然被广泛的在Shader层面支持着.

Phong是一种经验模型,其一般形式为:

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image071.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.071.1433145970.png)![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image072.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.072.1433145970.jpeg)

其中![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image073.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.073.1433145970.png)表示视线v方向的辐射率,在具体光照运算中,这就是我们要计算的顶点(像素)颜色值,![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image074.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.074.1433145970.png),![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image075.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.075.1433145970.png)分别是光源向量和视线方向关于该表面的反射向量,![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image076.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.076.1433145970.png),![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image077.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.077.1433145970.png)分别是该表面材质的漫反射颜色和高光反射颜色，![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image078.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.078.1433145971.png)描述表面光泽度,![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image079.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.079.1433145971.png)是光源颜色.下划线表示将点积结果限定到[0,1].

虽然是一个物理不正确(能量不守恒等)的经验公式,但通过与光能传递方程对比,我们还是能够发现一些它们之间的关联:

\1.      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image080.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.080.1433145971.png)和光能传递方程中的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image081.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.081.1433145971.png)相对应.

\2.      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image076.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.076.1433145970.png)与Lambert BRDF中的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image082.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.082.1433145971.png)(x)对应.

\3.      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image083.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.083.1433145971.png)与Torrance-Sparrow BRDF中的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image084.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.084.1433145971.png)相对应.

\4.      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image085.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.085.1433145971.png)与Blinn分布公式中的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image086.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.086.1433145971.png)相对应.

\5.      ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image079.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.079.1433145971.png)与光能传递方程中的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image087.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.087.1433145971.png)相对应.

这即是为什么Phong模型看起来***大概正确***的原因.

**3.2.2****、****Phong光照模型的改良**

Phong光照模型虽然性价比很高,也能满足实时渲染对光照效果的一般要求.但由于其仅是一个经验公式, 在某些情况下难免会有一些与实际不符的现像发生.随着硬件的进步,特别是GPU可编程管线的出现和发展,我们能通过参考光能传递公式以少量的运行时开销为代价来修正这些瑕疵,使得Phong模型更加符合物理规律,并使改进后的Phong模型参数更加易于调整,改进都是针对Phong光照模型中的高光分量:

\1.       强行钳住高光分量是物理不正确的,且会产生生硬分割线,其实将![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image080.png](http://gameweb-img.qq.com/gad/20150601/f198a0c8dd9142f0a018467290e7be02.080.1433145971.png)作为高光分量的衰减系数,更加契合光能传递公式,且不再产生生硬分割线:

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image088.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.088.1433145971.jpeg)

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image089.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.089.1433145971.png)

强行钳住高光形成的瑕疵

\2.       与高光分量计算式中的![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image085.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.085.1433145971.png)相比Blinn分布函数中![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image090.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.090.1433145972.png)更为符合物理学规律:虽然在大多数情况下![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image091.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.091.1433145972.png)能与Blinn取得极为相似的结果,但我们发现在近水平观察视角下![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image090.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.090.1433145972.png)呈拉伸形状的高光区域更为接近于现实世界中的高光反射现象:

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image092.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.092.1433145972.png)

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image093.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.093.1433145972.jpeg)

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image094.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.094.1433145972.jpeg)

Blinn高光的表现更贴近于现实世界

\3.       由于原始的Phong光照模型中的高光分量不满足能量守恒定律,使得![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image078.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.078.1433145971.png)的数值不但控制了高光光斑的大小还影响总的高光反射能量(本该是恒定的),![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image095.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.095.1433145972.png)光斑的亮度随着![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image078.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.078.1433145971.png)的增大反而会减小，这使得光泽物体的高光强度和光滑度产生了错误的关联性.通过对Torrance-Sparrow 和Blinn模型的考察，不难发现问题出在Phong忽略了高光分量的归一化系数，通过简化的Torrance-Sparrow 和Blinn模型，我们得出这个归一化系数为:![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image096.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.096.1433145972.png).

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image097.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.097.1433145972.png)

归一化后高光的表现更加符合物理规律

有了以上的改进再引入对普遍存在的Fresnel效应考虑，我们得到了最终改良版的Phong光照模型中的高光分量:

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image098.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.098.1433145972.png)

 其中，Fresnel的计算也比较高效:

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image099.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.099.1433145973.png)

**3.3****、****全局光照技术简介**

与局部光照相比，全局光照还会考虑光能在物体之间的传递现象，包括光能的间接传递(如Color  Bleeding现象),光能在物质内部的散射(Subsurface  scattering)等.且全局光照能够使用物理正确的面光源,从而应用全局光照技术的渲染一般能够得到比仅仅应用局部光照技术的渲染更为真实可信的渲染结果.借用RenderingTime  Rendering中的一句话来形容:”Let the form of an object be what it may, light,  shade, and perspective will always make it beautiful”.

**3.3.1****、****非实时全局光照算法**

因为不考虑实时性,这类全局光照算法一般采用比较直接的方式去计算光能传递方程,很少引入会影响视觉效果的简化技巧,因此,由它们生成的全局光照结果最为接近现实世界中的真实情况,且常被用来作为其余全局光照简化技巧的参考,以衡量其优劣.

非实时的全局光照算法一般是渐进式(Progressive)算法,通过收敛速度(接近精准结果的快慢)来描述性能.

**3.3.1.1****、****Radiosity**

Radiosity基于有限元方法(Finite  element method)计算光能传递方程:将场景中的物体表面划分为分片(Patch),通过一个系数(Form  factor)确定分片之间的光能传递关系,通过求解由Form  factor和Patch辐射度(包括已知的和未知的)构成的线性方程组求得光能传递的结果.

Radiosity仅能计算光能在场景中与漫反射表面的交互,因此它是视点无关的,只要光源,物体的状态都保持不变,就无需重复运算.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image100.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.100.1433145973.png)

局部光照与Radiosity方法漫反射光照的对比

**3.3.1.2****、****Ray Tracing类算法**

这类算法通过光线跟踪获取大量的场景信息采样(Sample)并基于蒙特卡罗数值积分法(Monte Carlo methods)和这些采样计算出光能传递方程的值.

Ray Tracing类算法的一个核心研究问题是如何优化采样分布,以获取更快的收敛速度.

因为基于统计学的方法,所以该类算法又分为两大类:无偏的(Unbiased)和有偏的(biased),其中无偏算法以Path  Tracing为代表,有偏算法以Photon  Mapping为代表,因为有偏算法可以引入一些简化计算量的技巧(如IrradianceCache算法假定在某些情况下样点的漫反射可以通过插值附近已知的样点漫反射得到),所以一般来说,有偏算法的性能要优于无偏算法.

因为此类的全局光照算法能完整的描述光能与场景的一切交互现象,因此其使用的比Radiosity方法更为广泛,且相关研究也活跃的多.

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image101.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.101.1433145973.jpeg)

​                                                                                    Path Tracing渲染的结果

**3.3.2****、****全局光照的实时近似**

由于运行时效率上的原因,基于光线跟踪的全局光照技术一般无法直接应用于游戏渲染,但随着硬件的发展,越来越多的简化的全局光照技术在实时渲染程序中发挥了良好的作用,以下是一些最具代表性的实时全局光照算法,绝大多数其它的实时全局光照技术都是基于以下描述的基本算法的改良/整合.

**3.3.2.1****、****GI Based Lightmap**

基于全局光照(GI)技术的光照贴图技术是通过非实时全局光照算法预先计算出场景中的静态的,视点无关的光照信息并保存为贴图,供运行时使用.

这种算法的优势是主要的计算量都可以预先完成,运行时开销极小,缺点是仅能应用于场景静态元素的漫反射光照.且存储开销较大,特别是对于广阔的场景.

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image102.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.102.1433145973.jpeg)

Lightmap

**3.3.2.2****、****Environment Maps**

环境映射技术是将定点处的来自所有方向的入射辐射率信息记录下来,作为一个环境光源以满足环境镜面反射,环境光照明等假想光源(方向光源/点光源)无法满足的应用场合的需求.

环境映射数据多数时候预先生成即可,但有时也需动态生成(如应用于赛车类游戏的车身镜面反射时).环境映射数据的载体可以是贴图(如Cubemap),有时也可以用Spherical harmonics等基函数来近似表示(如作为漫反射环境光源等无需高频率光照信息时),以节省存储开销.

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image103.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.103.1433145973.jpeg)

镜面反射,漫反射,高光反射的环境映射

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image104.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.104.1433145973.png)

应用环境映射的渲染

**3.3.2.3****、****AmbientOcclusion**

环境遮挡是对场景中某点被遮挡程度的描述(如角落处的环境遮档程度大于开阔处的环境遮程度).环境遮档可以大大增强环境光照的真实感和场景的立体感.

环境遮挡可以预先生成(如AO Map),也可以实时生成(如SSAO)以适应动态场景的需求.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image105.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.105.1433145973.jpeg)

应用SSAO前

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image106.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.106.1433145973.jpeg)

应用SSAO后

**3.3.2.4****、****Light Volume**

Light   Volume是一类算法的通称,这类算法的核心是将场景按某种规律划分为栅格,并计算每个栅格处的光照环境信息,即是将连续的光照环境采样为离散的光照环境,以供光照算法使用.此类算法的代表是IrradianceVolume,它在栅格中存储DiffuseEnvironmentMap,一般供场景动态物体使用,使动态物体得以融入场景光照环境.

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image107.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.107.1433145973.jpeg)

​                            IrradianceVolume,站在蓝色墙壁下的角色拥有视觉上正确的光照环境

**3.3.2.5****、****PRT**

PRT是Precomputed  Radiance Transfer的简称.场景的光照过程其实就是场景将入射光(Source Radiance)转换(传递)为出射光(Exit  Radiance)的过程.PRT正是一种将这一过程预先计算出来,以供实时渲染时使用的技术.

因为场景对光能的传递转换过程可以预先计算,使得实现一些较为复杂的光能传递现象成为可能,如间接光照,次表面散射等.

​       ![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image108.png](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.108.1433145973.png)

同样是因为预计算的原因,PRT的计算对象只能是场景的静态元素,但光照环境(Source Radiance)可以动态的变化,因为我们预计算的是光能的传递过程而非结果,在这一点上,PRT是要优于Lightmap的(PRT的运行时开销高于Lightmap).

此外,PRT借助Spherical harmonic基函数来存储预计算的数据,加之光照环境也是预先分解为Spherical harmonic级数的形式,一般仅适用于表现低频率的光照信息:漫反射,软阴影等.

![http://avocado.oa.com/fconv/files/201101/89dfec7d-ce39-4083-b233-a3f9011df146_files/image109.jpg](the technology of realistic lighting in games.assets/f198a0c8dd9142f0a018467290e7be02.109.1433145973.jpeg)

局部光照和PRT光照的漫反射效果对比

**3.3.2.6****、****RSM**

人们发现,对于绝大多数场景和光照环境来讲,光能只要间接传递一次就能很好的表现出Color Bleeding等全局光照效果了.这一简化设想,为实现实时的全局光照效果提供了重要思路.

RSM正是基于这一简化设想的技术,它是Reflective   ShadowMap的简称.众所周知,ShadowMap记录了直接光源对场景的可见性,而直接光源能到达的地方就是间接反射的源头(间接光源).很自然的想到,我们可以基于直接光源的ShadowMap中的信息生成一些虚拟光源,然后使这些虚拟光源作用于场景,就能近似模拟出光能一次间接传递的效果了.当然,为了完成间接光照运算,Reflective  ShadowMap中还需存储光源可达处的光能量强度.

RSM是全动态的,这是一个巨大的优势。

著名的CryEngine3引擎中采用的实时全动态全局光照技术Light Propagation Volumes就是由RSM扩展衍生而来的
