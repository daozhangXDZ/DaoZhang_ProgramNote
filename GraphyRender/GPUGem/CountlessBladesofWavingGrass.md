# 三、无尽波动的草地叶片的渲染（Rendering Countless Blades of Waving Grass）

## 

## 【章节概览】

这章关于巨量自然元素的渲染，特别是对于无尽波动的草地叶片的渲染。作者对Codecreatures demo中首次成形的技术进行了扩展，使其能够高性能的渲染，以更好地适应游戏引擎的需要。

[
![img](三、无尽波动的草地叶片的渲染（RenderingCountlessBladesofWavingGrass.assets/000e7d0e677c5cc7aaa92cbfc28e7b44.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/000e7d0e677c5cc7aaa92cbfc28e7b44.jpg)

图 Realistic Grass Field @Giovanni Baer

## 

## 【核心内容提炼】

### 

### 3.1 概述

首先，需要意识到，对单个草叶的细节建模意义不大，因为那样大片草地需要的多边形数目会太多。

所以，我们必须建立一个符合以下条件的简单而有用的替代方案：

- 许多草的叶片必须由少数多边形表示。
- 草地必须从不同的视线看起来显得密集。

而要做到让场景不依赖于摄像机的位置和方向，可以把一些草叶组合起来，表示在一个纹理中，并将多个纹理组合起来，且在结果中单个的多边形不应该引起注意。当观察者四处活动时，通过将草体加入混合操作或者移除混合操作，以在距离范围内增加或删去草体，来保证整个草地的渲染效果具有稳定的视觉质量。

### 

### 3.2 草的纹理

草的纹理，应该是一些一簇一簇聚集丛生的草，否则，会出现大片的透明区域。

需在透明的alpha通道上画实体草茎。在彩色通道中，用深浅不同的绿色和黄色，来较好地区别各个单独的叶片，也应该模拟不同情况的草叶：长得好的和长得差的、老的和嫩的，甚至区别叶片的前面与后面。

下图是一个草地纹理的示例。

[![fig07-02.jpg](三、无尽波动的草地叶片的渲染（Rendering Countless Blades of Waving Grass.assets/75eb9a7c7b47bfd883f3d2c15f1b1166.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPU%20Gems%201%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/75eb9a7c7b47bfd883f3d2c15f1b1166.png)

图 草地纹理的示意图

### 

### 3.3 草体

这一部分将探讨总结如何对多边形进行组合，并用上文提到的草地纹理进行映射，以模拟出茂密的草地，并且不凸显个别多边形。此技术也保证了单个多边形不可见。

因为用户能自由地在场景中游玩，下图所示的结构便不能产生令人信服的效果。

[![fig07-03.jpg](三、无尽波动的草地叶片的渲染（Rendering Countless Blades of Waving Grass.assets/2e621ba9c08c3c8d560175f594ab5cd8.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPU%20Gems%201%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/2e621ba9c08c3c8d560175f594ab5cd8.jpg)

图 线性排布

对于线性排布，如果从垂直于多边形的方向观看场景，就会立刻穿帮，看出草地多边形的结构是线性排布的。另外这种情况下草地会看起来非常稀疏。只有在摄像机自动导航，或者渲染无法到达的远距离草地时，才会考虑这样的排布。

为了保证独立于当前视线的良好视觉质量，我们必须交叉地排布草地多边形。已证明，使用星型结构是非常好的。下图给出了“草体”可能的两种变体。

他们由3个相交的方块构成。我们必须禁用背面剔除来渲染多边形，以保证双面都可见。为了得到合适的照明度，应该让所有顶点的法线方向与多边形的垂直边平行。这保证了位于斜坡上的所有草体都可以得到正确的光照，不会因为地形的亮度而出现差异。

[![fig07-04.jpg](三、无尽波动的草地叶片的渲染（Rendering Countless Blades of Waving Grass.assets/0e5096bbb70198af88449e17482a45d6.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPU%20Gems%201%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/0e5096bbb70198af88449e17482a45d6.jpg)

图 草体的交叉排布

如果把这些草地物体彼此相当靠近地设置在一个大的区域里，如下图。在运行期间把它们从后向前进行排序，使用alpha混合，并启用Draw Call中的z-testing/writing，那么就会得到自然而茂密的草地渲染效果。

[![fig07-05.jpg](三、无尽波动的草地叶片的渲染（Rendering Countless Blades of Waving Grass.assets/a6c9d7add4706057988add72188400ab.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPU%20Gems%201%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/a6c9d7add4706057988add72188400ab.jpg)

图 草地的扩展

### 

### 3.4 草地动画

关于草地的动画，基本思想是以三角函数（尤其是正弦和余弦）为基础进行计算，且计算应该考虑到移动的位置和当前时间、风向和强度。

以基本思想为基础，实现起来有几种方法：

1、每草丛草体的动画（Animation per Cluster of Grass Objects）

2、每顶点的动画（Animation per Vertex）

3、每草体的动画（Animation per Grass Object）

三种方法各有优缺点，而文中都给出了具体算法步骤和实现的Shader源码，这里因为篇幅原因，便不展开分析了。

最终可以实现的渲染效果。

[
![img](三、无尽波动的草地叶片的渲染（RenderingCountlessBladesofWavingGrass.assets/fb643b85c492b73c4ee4b7994a77ae9e.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/fb643b85c492b73c4ee4b7994a77ae9e.jpg)

图 Realistic Grass

## 

## 【核心要点总结】

1）草的纹理，应选取一簇一簇聚集丛生的草。在透明的alpha通道上画实体草茎。在彩色通道中，用深浅不同的绿色和黄色，区别各个单独的叶片。

2）草体的渲染，适合进行交叉排布，从后向前进行排序，使用alpha混合，并启用Draw Call中的z-testing/writing，便能得到自然而茂密的草地渲染效果。

3）草地的动画，以三角函数（尤其是正弦和余弦）为基础，且应该考虑到移动的位置和当前时间、风向和强度。实现起来有三种方法：

> 1、每草丛草体的动画（Animation per Cluster of Grass Objects）

> 2、每顶点的动画（Animation per Vertex）

> 3、每草体的动画（Animation per Grass Object）

## 

## 【本章配套源代码汇总表】

Example 7-1. 顶点着色器框架（Framework in the Vertex Shader）

Example 7-2. 对每草丛草体的动画的实现Shader代码（Code for Animation per Cluster of Grass Objects）

Example 7-3. 每顶点动画实现Shader代码（Code for Animation per Vertex）

Example 7-4. 每草体的动画实现Shader代码（Code for Animation per Grass Object）

## 

## 【关键词提炼】

草地渲染（Grass Rendering）

草地动画（Grass Animation）

草体（Grass Objects）
