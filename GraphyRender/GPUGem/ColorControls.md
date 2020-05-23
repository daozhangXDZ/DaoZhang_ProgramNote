# 颜色控制（Color Controls）

## 

## 【章节概览】

这章将在游戏中图像处理的讨论，扩展到技术和艺术上控制颜色的方法和应用，包括将图像从一些的色彩空间中移入移出，以及快速地给任何2D或3D场景加上精美的色调。

## 

## 【核心要点】

色彩校正（Color Correction）是几乎所有印刷和胶片成像应用的一部分。 色彩校正可用于将彩色图像从一个色彩空间移动到另一个色彩空间。

我们在电视、杂志和电影中剪刀的大部分图像，都经过了非常小心的彩色校正和控制。对于这个过程的理解，可以帮助开发者在实时应用程序中得到同样华美的视觉效果。

色彩校正通常有两种做法：一是各个通道的校正，分别是改变红色、绿色和蓝色各成分；二是混色操作，基于红、绿、蓝各个成分的同时操作，得到每个通道的输出值。

色彩校正的机理可以简洁而容易地在一个shader中描述。重要的是，美术和程序员使用的普通工具就能有效地控制他们。在这章中，运用Photoshop创建控制资源，然后通过像素shader应用到实时程序中。

在Photoshop中提供了一些基于通道校正的工具。如级别（levels）和曲线（Curves）工具。

其中曲线是仿制了化学中的交叉处理（cross-processing）外观，确切地说，就是在C41化合物中处理E6叫绝所产生的假颜色外观。这样的处理已在印刷、电影和电视领域使用多年。

[
![img](ColorControls.assets/b95941c57ca75f5ad2a48ff7a453376b.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/b95941c57ca75f5ad2a48ff7a453376b.png)

图 重新创建交叉处理效果的Photoshop曲线

[
![img](ColorControls.assets/b2d6a1dbc10f3a3f6b0b8a24a97df7f2.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/b2d6a1dbc10f3a3f6b0b8a24a97df7f2.png)

图 伪交叉处理 

（a）原始图 （b）曲线调节之后

可以使用下面几行shader代码运用于输出颜色，使用色彩校正纹理映射，可以随意地用曲线工具重新创建任何色彩变化：

float3 InColor = tex2D(inSampler, IN.UV).xyz;

float3 OutColor;

OutColor.r = tex1D(ColorCorrMap, InColor.r).r;

OutColor.g = tex1D(ColorCorrMap, InColor.g).g;

OutColor.b = tex1D(ColorCorrMap, InColor.b).b;

也就是说，使用每个原始的红、绿和蓝像素的灰度值，确定在梯度纹理中我们寻找的相关位置，然后由梯度纹理本身定义对新颜色的重映射，即由复杂曲线调节所定义的新颜色，如下图。

[
![img](ColorControls.assets/d01cd3f0054bd4178d7561b61e7c5f01.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/d01cd3f0054bd4178d7561b61e7c5f01.png)

图 对红、绿、蓝通道重映射结果

## 

## 【本章配套源代码汇总表】

原文仅存在无编号的代码片段若干，具体详见原文。

## 

## 【关键词提炼】

颜色控制（Color Controls）

色彩校正（Color Correction）

基于通道的颜色校正（Channel-Based Color Correction）

灰度变换（Grayscale Conversion）

色彩空间变换（Color-Space Conversions）

图像处理（Image Processing）
