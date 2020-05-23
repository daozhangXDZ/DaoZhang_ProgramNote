# 动态辐照度环境映射实时计算（Real-Time Computation of Dynamic Irradiance Environment Maps）

## 

## 【章节概览】

环境映射（Environment Maps）是常用的基于图像的渲染技术，用来表现以空间上不变的球面函数。本章描述了一种完全GPU加速的方法，来生成一个环境映射在图形上特别有趣的类型——辐照度环境映射（Irradiance Environment maps）。

## 

## 【核心要点】

本技术使应用程序可以在动态环境下（如来自动态关和动态对象的辐射度）快速地模拟复杂的全局光照效果。

辐照度环境映射的渲染非常高效，漫反射只用一次，漫反射+镜面反射只用两次。

[
![img](DynamicIrradianceEnvironmentMaps.assets/82bda2bfc3ebdd3fc3dd1031c69f7f99.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/82bda2bfc3ebdd3fc3dd1031c69f7f99.jpg)

图 一个由单个方向光（左）和实时辐照度环境映射（右）照亮的物体

[
![img](DynamicIrradianceEnvironmentMaps.assets/c135b4f7854a5a36cc313ca4fbcf8014.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/c135b4f7854a5a36cc313ca4fbcf8014.jpg)

图 辐照度环境映射

（a）一个圣彼得教堂的立方体映射；（b）漫反射结果；（c）镜面映射结果。圣彼得教堂的光照探测。

而通过片元着色和浮点纹理，可以把球面调和卷积映射到GPU上变成简单的两个通道的操作：第一个pass中把光照换行转换成它的球面调和表示，另一个pass把它和反射函数进行卷积并把它转换为空域。且让环境映射的每个面有一个独立的查找表(Lookup Table)。

[
![img](DynamicIrradianceEnvironmentMaps.assets/e6d39172c6c96651c542230f730d3ddf.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/e6d39172c6c96651c542230f730d3ddf.jpg)

图 10-3 将输出系数映射到一个面的分块输入查找表上

## 

## 【关键词】

环境映射（Environment Maps）

动态辐照度环境映射（Dynamic Irradiance Environment Maps）

球面调和卷积(Spherical Harmonic Convolution)
