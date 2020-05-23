## 用于粒状遮挡剔除的分层项缓冲 | Hierarchical Item Buffers for Granular Occlusion Culling

剔除（Culling）算法是许多高效的交互式渲染技术的关键，所有剔除算法的共同目标都是从渲染管线的几乎所有阶段减少工作量。

最常用的算法是在应用阶段采用视锥剔除（frustum culling）和视口剔除（portal culling）来排除不可见的几何体，通常按层次数据结构组织。更复杂的算法会在昂贵的前期流程中预计算整个可见集，以实现高效的实时可见性计算。

这章提出了一种直接在GPU上运行的剔除方法，该方法对应用程序完全透明且实现起来非常简单，特别是在下一代硬件和图形API上。文中表明，只需很少的开销，每帧的渲染时间可以显着减少，特别是对于昂贵的着色器或昂贵的渲染技术。该方法特别针对像几何着色器这样的早期着色器阶段，且应用目标是多方面。例如，[Engelhardt  and Dachsbacher  09]展示了这种技术的应用，以加速每像素位移映射，但它也为基于可见性的LOD控制和曲面细分着色器中的剔除提供了可能性。

[
![img](HierarchicalItemBuffersforGranularOcclusionCulling.assets/9c2b071b069eda2e4df844b060909a87.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/9c2b071b069eda2e4df844b060909a87.png)

图 分层项缓冲区（Hierarchical Item Buffers）图示（a）确定可见度的实体;（b）光栅化后的项缓冲区（item buffer）;（c）项缓冲区的直方图。实体3没有计算任何内容，因此是不可见的。
