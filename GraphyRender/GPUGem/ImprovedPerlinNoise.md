# 改良的Perlin噪声实现（Implementing Improved Perlin Noise）

## 

## 【章节概览】

这章的作者是奥斯卡得主Ken Perlin。他提出的噪声算法（Perlin Noise）已在实时和离线计算机图形学中得到多方面运用。这篇文章详细阐述了最新进展，纠正了最初的两个缺陷，也提供了有效及稳定的框架结构，用于在现代可编程硬件上执行噪声运算。

## 

## 【核心要点】

首先，噪声函数的目的，是在三维空间中提供一种可以有效率地实现、可重复，伪随机的信号。其信号的能带有限（band-limited），大部分能量集中在一个空间频率附近，而视觉上是各向同性（isotropic）的，统计上不随旋转变化。

一般的想法是创建某种信号，类似于一个完全的随机信号（即白噪声），通过低通滤波后，滤除了所有的空间高频率而变得模糊。有如沙丘你缓慢上升的山包和下落的低谷。

[
![img](ImprovedPerlinNoise.assets/ce58e6d0901706ca3cf7f3a49bf0e354.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/ce58e6d0901706ca3cf7f3a49bf0e354.png)

图 沙丘与噪声

最初的噪声在1983年实现，1985 (Perlin 1985)发表，思想是使用埃尔米特-样条（Hermite spline）插值法等方法实现，原文中对此方法的步骤进行了描述。

[
![img](ImprovedPerlinNoise.assets/5ff8e22e8afe125e1fd305bf9f6bb89e.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/5ff8e22e8afe125e1fd305bf9f6bb89e.jpg)

图 使用使用埃尔米特-样条（Hermite spline）插值法，从常规3D格点的八个样本中插值

[
![img](ImprovedPerlinNoise.assets/7ae7fa8a3f40c0cf23a707d15f8fe87f.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/7ae7fa8a3f40c0cf23a707d15f8fe87f.jpg)

图 通过噪声函数产生的一个切片样条

这篇文章从两个方面对最初的噪声方法的不足进行了改进：

插值的特性以及伪随机斜率场（field of pseudo-random gradients）的特性。

[
![img](ImprovedPerlinNoise.assets/9806d02f14c9b03d2f8ddc68859d4b3a.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/9806d02f14c9b03d2f8ddc68859d4b3a.png)

图 四种基于噪声生成的纹理

而另外一个关于噪声的思路是，用体积噪声制造程序式纹理（Procedural texturing using volumetric noise），这样可以不创建显式的纹理图像，来得到自然的材质。这种方法在当年的大片《指环王》中，已经有了广泛应用。

## 

## 【本章配套源代码汇总表】

5-1 假设模型是单位半径球体，实现凹凸模式的示例代码（Assuming the model is a unit-radius  sphere, the expressions that implement these bump patterns sample Code）

## 

## 【关键词提炼】

Perlin噪声（Perlin Noise）

噪声函数（Noise function）

伪随机斜率场（Field of Pseudo-Random Gradients）

体积噪声( volumetric noise）

埃尔米特样条（Hermite spline）
