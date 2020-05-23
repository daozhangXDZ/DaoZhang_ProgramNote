# 景深 （Depth of Field）

## 

## 【章节概览】

本章主要介绍如何使用GPU创建实时的景深（Depth of Field）效果。
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/f74d7a2718b91518d938208f750b8b74.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/f74d7a2718b91518d938208f750b8b74.png)

图 实时景深效果 @Crysis 2

## 

## 【核心要点】

物体在距离镜头的一个范围之内能够清晰成像（经过聚焦），在那个范围之外（或近或远）则成像模糊，这种效果就是景深。在相机业和电影业中，景深经常用来指示对场景的注意范围，并且提供场景深度的感觉。在本章中，把这个聚焦范围远的区域称为背景（background），在这个范围前的区域称为前景（foreground），而在范围外的面积称为中景（midground）。

景深效果由透镜的物理性质产生。若要穿过摄像机透镜（或人眼镜的晶体）的光辉聚到胶片（或人的视网膜）上的一个点，光源必须与透镜有着特定的距离。在这个距离上的平面称为焦平面（plane in focus）。不在这个精确距离上的任何东西，投影到胶片上的区域（而不是一个点）称为模糊圈（circle of confusion，CoC）。Coc的直径与透镜尺寸和偏离焦平面的距离成正比。偏离距离小到一定程度，CoC会变得比胶片的分辨率更小，摄影师和摄影师称这个距离为聚焦（in focus），而在这个范围之外的任何东西都是没有对准聚点的（out of focus，模糊的）。如下图。

[
![img](DepthofField.assets/d3fa2f5dbd2291d8094d263c446db246.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/d3fa2f5dbd2291d8094d263c446db246.png)

图 薄的透镜

[
![img](DepthofField.assets/b261554c6c79c1f2e1675e709d1d16e4.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/b261554c6c79c1f2e1675e709d1d16e4.png)

图 模糊圈（circle of confusion）

这章中主要综述了5种近似景深效果的技术。

1、基于光线追踪的景深（Ray-Traced Depth of Field）[Cook et al. 1984]

2、基于累积缓冲的景深（Accumulation-Buffer Depth of Field）[Haeberli and Akeley 1990]

3、分层景深（Layered Depth of Field）[Scofield 1994]

4、前向映射的Z缓冲景深（Forward-Mapped Z-Buffer Depth of Field） [Potmesil and Chakravarty 1981]

5、反向映射的Z缓冲景深（Reverse-Mapped Z-Buffer Depth of Field）[ Arce and Wloka 2002, Demers 2003]

## 

## 【本章配套源代码汇总表】

原文仅存在无编号的代码片段若干，具体详见原文。

## 

## 【关键词提炼】

景深（Depth of Field）

基于光线追踪的景深（Ray-Traced Depth of Field）

基于累积缓冲的景深（Accumulation-Buffer Depth of Field）

分层景深（Layered Depth of Field）

前向映射的Z缓冲景深（Forward-Mapped Z-Buffer Depth of Field）

反向映射的Z缓冲景深（Reverse-Mapped Z-Buffer Depth of Field）

图像处理（Image Processing）
