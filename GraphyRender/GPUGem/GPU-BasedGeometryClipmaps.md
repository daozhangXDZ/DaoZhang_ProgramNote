# 几何体实例化的内幕（Inside Geometry Instancing）

## 

## 【章节概览】

本章讨论了在Direct3D中渲染一个几何体的许多独特实例（Instance）的技术细节问题，对几何体实例（Geometry Instancing）的技术内幕进行了分析。

## 

## 【核心要点】

使用几何体实例（Geometry Instancing）的优势在于可以对渲染性能进行优化（最小化花费在提交渲染批次上的CPU时间）。

想要使用应用程序最小化状态和纹理变化次数，并在一次Direct3D调用中把统一批次中的同一个三角形渲染多次。这样就能最小化花费在提交批次上的CPU时间。

这章描述了4种不同的技术来实现Geometry Batch：

- 静态批次（Static batching）。最快的实例化几何体的方法。每个实例一旦转换到世界空间，则应用它的属性，然后每一帧把已经转换的数据发送给GPU。虽然简单，但静态批次是最不具灵活性的技术。
- 动态批次（Dynamic batching）。最慢的实例化几何体的方法。每个实例在每帧都流向GPU存储器，已经转换并应用了属性。动态批次无缝地支持蒙皮并提供了最灵活的实现。
- 顶点常量实例（Vertex constants instancing）。每个实例的几何体有多份副本一次复制到GPU存储器中的混合实现。然后实例属性在每一帧通过顶点常量设置，而由于顶点着色器完成几何体的实例化。
- 通过几何体实例化API的批次（Batching with Geometry Instancing API）。使用DirectX等图形API提供并支持的几何体实例化，此实现提供了灵活快速的几何体实例化解决方案。与其他方法不同的是，这不需要在Direct3D顶点流中复制几何体包

高效地渲染相同的几何体（静态批次、动态批次、顶点常量实例化，通过几何体实例化API的批次），他们各有优劣，根据应用和渲染的物体类型分别选取。一些建议：

- 有相同几何体的许多静态实例的室内场景，很少或从不移动的实例（比如墙壁或家具），采用静态批次较为理想。
- 有许多动画物体实例的一个室外景物，如策略游戏中有上百个士兵的大战场，在这种情况下，动态批次或许是最好的解决方案。
- 有许多植被和树以及许多粒子系统的室外场景，其中有很多经常需要修改的属性（例如，树和草随风摇摆），几何体实例API可能是最好的解决方案。

[
![img](GPU-BasedGeometryClipmaps.assets/793e100cfc7a336d5c367063417968c5.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/793e100cfc7a336d5c367063417968c5.jpg)

图 在真实场景中将静态批次和几何体实例化结合起来

## 

## 【关键词】

几何体实例（Geometry Instancing）

静态批次（Static batching）

动态批次（Dynamic batching）

顶点常量实例（Vertex constants instancing）

通过几何体实例化API的批次（Batching with Geometry Instancing API）
