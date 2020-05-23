# 几何特征系列：Ambient Occlusion（环境光遮蔽）



2016-06-24



LEEMANCHIU



[1 Comment](http://lemonc.me/ambient-occlusion.html#comments)



[理工男](http://lemonc.me/category/science-engineering)

计算机图形学的项目中，经常会涉及到一些几何特征，于是打算写一系列关于几何特征的文章。这篇文章将介绍  Ambient  Occlusion，中文名译作「环境光遮蔽」，是一种光照模型，它会计算像素亮度与场景中的附近物体之间的关系，时常会出现在游戏或电影的渲染技术中，但同时它也可作为一种三维几何特征，度量三维模型点的遮挡情况。

## Ambient Occlusion 的介绍

Ambient Occlusion 是一种计算机图形学中描述环境光阴影的视觉效果，最早是在 [Siggraph](http://www.siggraph.org/) 2002年会上由 [Industrial Light and Magic](http://www.ilm.com/)（工业光魔）的技术主管 [Hayden Landis](http://www.ilm.com/people/hayden-landis/)   所展示。这项技术之所以重要是因为它解决或改善了场景中缝隙、褶皱、接触面以及细小物体靠近等的空间的层次感问题，通过综合改善暗部阴影，同时加强画面明暗对比，增强了画面的真实感。其工作原理简单来说，就是当某些物体阻挡了相当数量的本应投射到其他物体的光线时，被光线阻挡的地方亮度值便会降低。越多光线被阻挡，表面则变得越暗。

真实的图形画面为了逼真光影效果需要全局光照，而光线追踪是实现全局光照完美效果的最佳技术方式之一，其技术实现方式最接近现实的物理模型，但是由于效率较低，所以很难在游戏等实时场景中使用。目前，为了让游戏实现全局光照的效果，实际并不会使用光线追踪的方式，而是通过多种技术方式共同达成这一效果，其中就用到了  Ambient Occlusion。Ambient Occlusion  实现方式并未严格遵循现实的物理模型，但能给出精确和平滑的阴影去模拟全局照明的结果，因为效率高，因此被广泛地应用于游戏之中。它主要是通过改善阴影来现实更好的图像细节，尤其在场景物体很多从而到处阻挡着光线导致间接照明不足时，Ambient  Occlusion 的作用会更加明显。在一般的游戏中，Ambient Occlusion 可能会以 HBAO（Horizon Based  Ambient Occlusion）或 SSAO（Screen Space Ambient  Occlusion）列在图形选项菜单中，分别译作「水平基准环境光遮蔽」和「屏幕空间环境光遮蔽」。这两者均表示环境光遮蔽，而水平基准环境光遮蔽是屏幕空间环境光遮蔽的一种优化形式。

下面提供一个 Ambient Occlusion 实例。

![dragon](Ambient Occlusion.assets/dragon.jpg)

图片左边是一条的 [Standford Dragon](http://graphics.stanford.edu/data/3Dscanrep/) 的简单模型，呈现在一个均匀照明的环境中。尽管模型中有一些明暗不同的区域，但大部分光照都是均匀的。虽然模型有着相当复杂的几何形状，但看上去比较光滑平坦，没有明显的深度感觉。

而图片右边是启用了  Ambient Occlusion 的相同模型。使用了 Ambient Occlusion  后，明显的变化是图像中添加了一些包围模型的平滑阴影，基于 Ambient Occlusion  的阴影具有柔和、平滑的层次感。完全暴露在周围环境中的区域（如龙鳍）显得更亮，而光线受阻的区域（如龙的腹部）则显得更暗。

如果用 Ambient Occlusion 作为一个几何特征，值越高的地方就代表越光亮，值越低的地方代表越暗。可以根据 Ambient Occlusion 的几何意义，区分三维模型上有无遮挡的部分。

## Ambient Occlusion 的原理

Ambient Occlusion 采用快速而廉价的算法来模拟全局照明模式，下面将简单介绍算法的原理。

![Rays](Ambient Occlusion.assets/Rays.jpg)

其计算过程大致是在三维几何模型表面任意一点的上方，用半径预定的半球探测该点的外部区域，判定光线在该点处被几何体遮挡的情况。一旦各点的遮挡程度确定，三维模型表面将形成一张灰度级的映射图，反映了对环境光吸收的强弱程度。

表面上对于点 *p*¯ 且法向为 *n*^ 的遮蔽 *A**p*¯，可通过以下公式在半球面 Ω 范围内积分求得：





*A**p*¯=1*π*∫Ω*V**p*¯,*ω*^(*n*^⋅*ω*^)*d**ω*





其中 *V**p*¯,*ω*^ 为点 *p*¯ 的可见性函数，若点 *p*¯ 在方向 *ω*^ 上受到遮蔽，则该可见性函数定义为零，*d**ω* 为积分变量 *ω*^ 的立体角微分。

## Ambient Occlusion 的实现

在实际项目中，最简单也最为常用的实现方法是利用[蒙特卡罗方法](https://en.wikipedia.org/wiki/Monte_Carlo_method)的思路，从每个点在半球范围内投射一定数量的射线，并统计射线相交的数量占总射线的比例。参考伪代码如下：

For each triangle {     Compute center of triangle     Generate set of rays over the hemisphere there     Vector avgUnoccluded = Vector(0, 0, 0);     int numUnoccluded = 0;     For each ray {         if (ray doesn't intersect anything) {             avgUnoccluded += ray.direction;             ++numUnoccluded;         }     }     avgUnoccluded = normalize(avgUnoccluded);     accessibility = numUnoccluded / numRays; }

| 1234567891011121314 | For each triangle {    Compute center of triangle    Generate set of rays over the hemisphere there    Vector avgUnoccluded = Vector(0, 0, 0);    int numUnoccluded = 0;    For each ray {        if (ray doesn't intersect anything) {            avgUnoccluded += ray.direction;            ++numUnoccluded;        }    }    avgUnoccluded = normalize(avgUnoccluded);    accessibility = numUnoccluded / numRays;} |
| ------------------- | ------------------------------------------------------------ |
|                     |                                                              |

下面是实际项目程序中对三维模型采样后（采样点数数量：100000），用 Ambient Occlusion 作为每个点的几何特征值的可视化结果。归一化这些特征值后，红色代表 1.0（最亮），蓝色代表 0.0（最暗）。![samples_feature_AO](Ambient Occlusion.assets/samples_feature_AO-1024x784.png)

## 参考文献

Landis H. Production-ready global illumination[J]. Siggraph course notes, 2002, 16(2002): 11.

在游戏中启用环境光遮蔽（Ambient Occlusion）. <http://www.geforce.cn/whats-new/guides/ambient-occlusion>

Ambient occlusion. <https://en.wikipedia.org/wiki/Ambient_occlusion>

Chapter 17. Ambient Occlusion. <http://http.developer.nvidia.com/GPUGems/gpugems_ch17.html>

Understanding Ambient Occlusion. <http://blog.digitaltutors.com/understanding-ambient-occlusion/>
