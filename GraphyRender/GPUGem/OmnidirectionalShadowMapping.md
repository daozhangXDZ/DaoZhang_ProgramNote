# 十五、全方位阴影贴图（Omnidirectional Shadow Mapping）

## 

## 【章节概览】

在这章中，把阴影贴图的思路扩展到正确处理全方位的（点）光源中，其中包括了实现细节，也涉及到基本硬件能力不足时的低效运行策略。

## 

## 【核心要点】

首先，这篇文章也谈到了在实时计算机图形学中产生可见阴影的两个流行方法是：

- 模板阴影（stencil shadows）/ 阴影体(Shadow Volume)
- 阴影贴图（shadow mapping）

模板阴影（Stencil Shadows，也被称Shadow Volume，阴影体）作在《Doom  3》中有所应用，优点是得到大量的GPU支持、独立于光源的种类、产生的阴影质量很高。但缺点是严重依赖于CPU，只能产生清晰的影子，需要很高的填充率，而且不能与硬件（hardware-tessellated）的表面一起使用。

阴影贴图（Shadow Mapping,也译作阴影映射）由Lance  Williams于1978年引入计算机图形学，文章发布当时多数好莱坞电影都在使用这个方法，包括计算机渲染和特效。为了计算阴影，阴影映射在场景几何体上投射特殊的动态创建的纹理。它可以渲染清晰和模糊的影子，以及由不同类型的光源产生的阴影，它还可以与硬件镶嵌的表面以及GPU动画的网格（例如蒙皮网格）一起使用。

该文章主要介绍了全方位阴影贴图（Omnidirectional Shadow Mapping）方法，该方法有两个主要步骤：

- 创建阴影贴图
- 进行阴影投射

在创建阶段，对所有把阴影投射到阴影贴图纹理上的物体，渲染它们到光源的距离的平方。而在投射结算，渲染所有接受阴影的物体，并比较所渲染的像素到光源的距离的平方。以下为全方位阴影映射算法的伪代码：

```
for (iLight = 0; iLight < NumberOfLights; iLight++) 

{

  // Fill the shadow map.

  for (iObject = 0; iObject < NumberOfObjects; iObject++)

 {

    RenderObjectToShadowMap(iLight, iObject);

  }

  // Lighting and shadow mapping.

  for (iObject = 0; iObject < NumberOfObjects; iObject++) 

  {

    LightAndShadeObject (iLight, iObject);

  }

}
```

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/0b975daa48ea7ab00e8e82ac74275661.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/0b975daa48ea7ab00e8e82ac74275661.png)

图 Omnidirectional Shadow Mapping @Merlin3d

## 

## 【本章配套源代码汇总表】

Example 12-1 全方位阴影映射算法的伪代码（Pseudocode for the Omnidirectional Shadow-Mapping Algorithm）

Example 12-2 仅渲染深度（Depth-Only Rendering）

Example 12-3 产生一个软阴影（Making a Softer Shadow）

## 

## 【关键词提炼】

阴影渲染（Shadow Rendering）

阴影贴图（Shadow Mapping）

模板阴影（stencil shadows）/ 阴影体（Shadow volume）

全方位阴影映射（Omnidirectional Shadow Mapping）
