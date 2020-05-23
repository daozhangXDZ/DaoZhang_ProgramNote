# 纹理爆炸（Texture Bombing）

## 

## 【章节概览】

这章介绍了纹理爆炸（Texture Bombing）和相关的细胞技术，它们能在Shader中增加视觉的丰富性，图像的多样性，并减少大块纹理图案的重复性。

## 

## 【核心要点】

纹理爆炸（Texture bombing）是一种程序化技术，它把小块图像以不规则的间隔放置。有助于减少团案的失真。

纹理爆炸的基本思想是把UV空间分为规则的单元栅格。然后使用噪声或者伪随机函数，把一个图像放在任意位置上的各个单元中。最终的结果是在背景上对这些图像的合成。

由于要组合数以百计的图像，因此实际上这种合成（composite）图像的方法效率并不高。而程序化（Procedural ）计算图像虽好，但是又不适合合成。这篇文章主要讲了图像合成和程序化生成这两种方法，可以发现他们各有优劣。

[
![img](TextureBombing.assets/1f4929be9428a7031b3cbb41fa74d4f5.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/1f4929be9428a7031b3cbb41fa74d4f5.png)

图 纹理爆炸效果图

很显然，纹理爆炸也可以扩展到3D中，即3D程序化爆炸（Procedural 3D Bombing）

[
![img](TextureBombing.assets/66a9323f26da5e154bda269c6618326a.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/66a9323f26da5e154bda269c6618326a.png)

图 程序化的3D纹理爆炸效果

纹理爆炸有一种有趣的变化是在平面上画Voronoi区域。简言之，给定一个平面和那个平面上的一系列的点，接近那个点的面积就是点的Voronoi区域。Voronoi图案类似于树叶和皮肤上的单元形状、龟裂的泥土或爬虫类的皮。如下图。

[
![img](TextureBombing.assets/345450849611257d2f711c7f1e4e398f.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/345450849611257d2f711c7f1e4e398f.png)

图 Voronoi区域

总之，纹理爆炸和相关的细胞技术可以给Shader增加视觉的多样性。使用存储在纹理中的伪随机数表和一个小程序，可以增大一个图像或一组图像的变化，并减少大块纹理区域的重复。

## 

## 【本章配套源代码汇总表】

Example 20-1 将采样扩展到四个单元格（Extending the Sampling to Four Cells）

Example 20-2 添加图像优先级（Adding Image Priority）

Example 20-3 使用程序化生成圆（Using a Procedurally Generated Circle）

Example 20-4 每个单元采样多个圆减少网格状图案（Sampling Multiple Circles per Cell Reduces Grid-Like Patterns）

Example 20-5 3D程序化爆炸（Procedural 3D Bombing）

Example 20-6 程序化3D纹理程序（The Procedural 3D Texture Program）

Example 20-7 计算Voronoi区域（Computing Voronoi Regions）

## 

## 【关键词提炼】

纹理爆炸（Texture Bombing）

3D程序化爆炸（Procedural 3D Bombing）

Voronoi区域（Voronoi Region）
