# 八、 Dawn Demo中的动画（Animation in the "Dawn" Demo）

## 

## 【章节概览】

这章主要讲到编程人员如何帮助美术同学对混合形状实行控制，从而创建不同的表情。主要是使用顶点Shader通过索引的蒙皮和变形网格对象（morph target）来使一个高分辨率网格变形，实现角色表情和动画等效果。也讨论了为实现实时动画而考虑的各种折中方案。

[
![img](AnimationintheDawn.assets/cafa26f19c54ca597045c5a047c3bb38.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/cafa26f19c54ca597045c5a047c3bb38.jpg)

图 Dawn Demo的实时屏幕截图

## 

## 【核心要点】

使用变形目标（Morph Target）是表现复杂网格变形的常用方法。NVIDIA Demo团队使用此技术创建的Zoltar等Demo从每秒插值30个网格开始，然后基于累计误差方案（Accumulated Error Scheme）去除关键帧。使得我们能够缩小文件并减少存储空间，最多可以将三分之二的原始关键帧，同时几乎不会出现可见的失真。在这种类型的网格插值中，任何给定时间中只有两个插值关键帧处于激活状态，而且他们是连续地执行的。另外，变形目标可以并行使用。

原文也中对变形目标（Morph Target）的具体实现进行了论述。

[
![img](AnimationintheDawn.assets/2230e081af4283a98249ba60e39e3c12.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/2230e081af4283a98249ba60e39e3c12.png)

图 表情的混合对象（混合形状）

而蒙皮（Skinning）是一种网格变形方法，对网格中的每个顶点指定一组带有权重的矩阵（权重最大可增加到1.0）。权重指明矩阵应该如何约束顶点。

为一个网格蒙皮做准备，通常要为网格创建一个中间状态，叫做绑定姿势（Bind Pose），这个姿势保持胳膊和腿略微分开，并且尽可能避免弯曲。

[
![img](AnimationintheDawn.assets/90fc18ee992be370b2d6597d2f70c5b4.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/90fc18ee992be370b2d6597d2f70c5b4.jpg)

图 Dawn的绑定姿势（Bind Pose）

## 

## 【本章配套源代码汇总表】

Example 4-1 以线性或连续样式运用到变形目标的示例代码（Applying morph targets in a linear or serial fashion sample code）

Example 4-2 单个"multiply-add"用于每个变形目标的示例代码（Single "multiply-add" instruction for each morph target sample code）

Example 4-3 变形目标的实现示例代码（Morph Target Implementation sample code）

Example 4-4 使用四根骨头蒙皮的示例代码（Application of four-bone skinning sample code）

## 

## 【关键词提炼】

面部表情模拟（Facial Expression Simulation）

网格动画（Mesh Animation）

变形目标（Morph Target）

蒙皮（Skinning）
