# 基于图像的光照（Image-Based Lighting）

### 

### 【章节概览】

这篇文章打破了当时立方体贴图环境（Cube-Map  Environment）用法的桎梏，深入研究了更多可能的逼真光照效果。文章主要研究了基于图像的光照（Image-Based  Lighting，IBL），包括局部化的立方体映射，类似于使用基于图像的局部光照（Localizing Image-Based Lighting），然后介绍了如何把哪些重要的技巧用于着色模型，包括逼真的反射、阴影和漫反射/环境项。

### 

### 【核心要点】

立方体贴图通常用于创建无限远环境的反射效果。但是使用少量Shader算法，我们可以将物体放置在特定大小和位置的反射环境中，从而提供高质量的基于图像的光照（Image-Based Lighting，IBL）。

在室内环境移动模型时，最好是使用近距离的立方体贴图，距离的大小与当前的房间类似。当模型在房间移动时，根据模型在房间中的位置，适当地放大或缩小放射。这种方法得到的模拟效果使人感到更为可靠和逼真。尤其在包含窗户，屏幕和其他可识别光源的环境中。而只要加入很少的Shader数学就能将反射局部化。具体可以看原文贴出的Shader源码。

[
![img](Image-BasedLighting.assets/406e4997427e4959de16ad7676327ca1.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/406e4997427e4959de16ad7676327ca1.png)

图 不同位置上的局部反射

另外，我们可以将3D几何体做成立方体贴图，并且在正常地渲染环境的时候，把贴图应用到该环境的物体上。也可以使用贴图作为环境，把它投射到较简单的几何体上。

立方体贴图也能用来决定漫反射光照。Debevec的HDRShop程序能够从映射立方体光照环境积分出全部的漫反射贡献度，那么通过把表面法线带入预先卷积的立方体贴图，能够简单地查询漫反射贡献。

基于图像的光照为复杂的光照计算提供了综合而廉价的替代品，将一点数学加入纹理方法，可以大大拓宽“简单”IBL效果，给3D图像提供更强的的方位感。

## 

## 【本章配套源代码汇总表】

Example 19-1生成世界空间和光照空间坐标的顶点着色器代码（Vertex Shader to Generate World-Space and Lighting-Space Coordinates）

Example 19-2 本地化反射像素着色器代码（Localized-Reflection Pixel Shader）

Example 19-3 用于背景立方体对象的顶点着色器代码（Vertex Shader for Background Cube Object）

Example 19-4 用于背景立方体对象的像素着色器代码（Pixel Shader for Background Cube Object）

## 

## 【关键词提炼】

基于图像的光照（Image-Based Lighting，IBL）

立方体贴图环境（Cube-Map Environment ）

基于图像的局部光照（Localizing Image-Based Lighting）
