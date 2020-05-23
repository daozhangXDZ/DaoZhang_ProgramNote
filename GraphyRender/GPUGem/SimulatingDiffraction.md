# 衍射的模拟（Simulating Diffraction）

## 

## 【章节概览】

这章讲述了简化的Jos衍射光照模型（最初在SIGGRAPH 1999上发表），此模型以光的物理性质为基础，将光当做波来进行建模，从而创建出多彩的干涉条纹。

## 

## 【核心要点】

什么是衍射（Diffraction）？小尺度的表面细节引起反射波彼此干扰，这个现象就是衍射。

首先，计算机绘图的大多数表面反射模型都忽略自然光的波动效果。当表面的细节比光的波长（约1um）大许多时，不存在问题。但对于小尺寸的细节，例如一个光盘的表面，波效应就不能忽略了。所以，对于小尺度的表面细节引起反射波彼此干扰的现象，即为衍射。

衍射使这些表面的反射光呈现五彩缤纷的图案，由光盘的精细反射可以看到这一现象。

[
![img](SimulatingDiffraction.assets/5561904e298f41f28747bd98b9e7688a.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/5561904e298f41f28747bd98b9e7688a.jpg)

图 光盘的衍射

衍射的实现，可以在Shader的顶点着色器上，也可以在片元着色器上，且实现可以在任何网格上进行，只需提供一个“切线向量”，和每顶点的法线及位置。而切线向量提供表面上窄条带的局部方向。对于一个光盘，其为轨道的方向，如下图。

[
![img](SimulatingDiffraction.assets/682310461e6d8b4e23a2984cb2ff34a8.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/682310461e6d8b4e23a2984cb2ff34a8.png)

图 光盘的切线向量

对应给定衍射波长的颜色，可以使用简单近似的彩虹贴图。贴图从紫到红排列，而且提供彩虹的大部分颜色，用三个理想凹凸函数（峰值分别在蓝、绿和红的区域）简单混合而成。

[
![img](SimulatingDiffraction.assets/a0aabb93a265e9d258848657aefa8228.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/a0aabb93a265e9d258848657aefa8228.png)

图 用于shader的彩虹彩色贴图

而最终的衍射颜色是彩色的衍射图案和各项异性高光的简单相加的和。

[
![img](SimulatingDiffraction.assets/aab296674959b3b442794016332e3e4a.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/aab296674959b3b442794016332e3e4a.png)

图 光盘衍射实时的3个快照

[
![img](SimulatingDiffraction.assets/2b00f10637fef6861756d4a5669a8296.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/2b00f10637fef6861756d4a5669a8296.png)

图 用纹理映射各项异性主要方向表面的3个快照

## 

## 【本章配套源代码汇总表】

Example 8-1. 衍射的顶点着色器代码（The Diffraction Shader Vertex Program）

## 

## 【关键词提炼】

衍射模拟（Simulating Diffraction）

各项异性（Anisotropy）
