# 阴影贴图抗锯齿（Shadow Map Antialiasing）

## 

## 【章节概览】

这章介绍了如何通过邻近百分比过滤方法（Percentage-Closer Filtering , PCF）有效减少阴影贴图的反走样。

## 

## 【核心要点】

阴影贴图（Shadow Map，又译作阴影映射）是渲染阴影的常见方法，也是渲染阴影领域的两大流派之一，但是它存在走样的问题。通常使用高分率的阴影贴图和增加阴影贴图的分辨率来反走样，也就是使用Stamminger和Drettakis 2002年提出的“透视阴影贴图（ perspective shadow maps）”技术。但是，当光与表面接近于平行的时候，使用“透视阴影贴图”技术和增加阴影贴图分辨率就不起作用了，因为放大的倍数接近于无穷大。

高端渲染软件使用“临近的百分比过滤（Percentage-Closer Filtering,PCF）”技术解决走样问题。最初的PCF算法由Reeves等人1987年提出。其计算的是靠近光源表面的百分比，而不是在阴影中表面的百分比，具体是多次比较阴影贴图的每个像素，求其平均值。

且文中对传统的PCF算法做了改进，不再计算阴影贴图空间中被遮挡的区域，只是简单地在各处使用一个 4 x 4个texel（纹素）的样本块。这个块应该大到能够有效地减少走样，但是不能达到要求大量样本和随机取样的程度。如下图。

[![fig11-09a.jpg](Shadow Map Antialiasing.assets/cf872a841af5cb1643e04ed813be7ca3.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPU%20Gems%201%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/cf872a841af5cb1643e04ed813be7ca3.png)

图 （a）每像素取1个样本  （b）每像素取4个样本  （c）每像素取16个样本

可以看到3幅图中的显示效果区别很明显，图（c）中每像素取16个样本，效果最为出色，达到了反走样的预期。

## 

## 【本章配套源代码汇总表】

PS:原文中没有对代码片段进行编号，这里的编号为附加。

Example 11-1 暴风(Brute Force)算法16采样版本的片元程序实现代码

Example 11-2 阴影贴图反走样的4采样实现版本代码

## 

## 【关键词提炼】

反走样/抗锯齿（Antialiasing）

邻近百分比过滤（Percentage-Closer Filtering , PCF）

透视阴影贴图（ perspective shadow maps）
