# 带位移映射的细分表面自适应镶嵌（Adaptive Tessellation of Subdivision Surfaces with Displacement Mapping）

## 

## 【章节概览】

这章介绍了如何使用可选的位移贴图（Displacement Mapping）执行Catmull-Clark细分曲面（Catmull-Clark Subdivision Surfaces）的视图相关的自适应镶嵌（Adaptive Tessellation）。使用GPU进行镶嵌计算，这可以节省图形总线带宽，并且比使用CPU快许多倍。

## 

## 【核心要点】

文中通过重复细分（repeated subdivision）的方法来实现镶嵌，通过渲染到2D纹理来实现。细分，平坦度测试（（Flatness Test））和最终顶点属性计算使用片元着色器（也称像素着色器）完成。该方法假设细分曲面控制网格的顶点数据存储在纹理贴图中。中间结果也渲染到纹理贴图并从纹理贴图读取，并且最终的镶嵌结果（位置，法线等）被渲染到一个顶点数组中，以被渲染图元（render-primitives）如glDrawElements()函数使用。

[
![img](SurfaceswithDisplacementMapping.assets/4cb9e4f55f54345baf193a7d27e9efff.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/4cb9e4f55f54345baf193a7d27e9efff.jpg)

图 对立方体的Catmull-Clark细分

[
![img](SurfaceswithDisplacementMapping.assets/cf81c02e293590e733309bcc776c7019.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/cf81c02e293590e733309bcc776c7019.jpg)

图 自适应镶嵌（Adaptive Tessellation） vs. 均匀镶嵌（Uniform Tessellation）

总之，这章介绍了一个结合使用广度优先递归（breadth-first recursion algorithm）细分算法在GPU上镶嵌细分表面的方法。文中描述了执行平坦度测试、实现细分和计算极限表面属性所需的着色器。而且解释了如何修改着色器来添加位移映射的支持，以增加细分表面模型的几何细节。

## 

## 【关键词】

Catmull-Clark细分 （Catmull-Clark subdivision）

位移贴图（Displacement Mapping）

平坦度测试（Flatness Test）

GPU镶嵌（GPU Tessellation ）

自适应镶嵌（Adaptive Tessellation）
