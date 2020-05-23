# 实现照片级真实感的虚拟植物（Toward Photorealism in Virtual Botany）

## 

## 【内容概览】

众所周知，植物的渲染需要很多的视觉深度和细节才能令人信服。

本章即关于渲染逼真自然场景的技术，描述了对实时游戏引擎友好的、用于渲染更真实的自然场景的策略。讲述了在不需要大量CPU或GPU占用的前提下渲染出包含大量植物和树组成的绿色植物场景。

内容安排方面，这章从管理大型户外环境场景数据这一基础开始描述。然后，提供一些细节，例如关于如何最大化GPU吞吐量，以便可以看到密集的草丛。接下来扩展这些技术，增加地面杂物和大型植物，如树，将阴影和环境影响组合进去。

一些真实感植物渲染的效果图：

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/e66658a5ca10fc9b5728471d4ffd6fd5.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/e66658a5ca10fc9b5728471d4ffd6fd5.jpg)

图 真实感植物渲染 @UE4

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/8da1e9a983bce8f97f98d62fd48e4188.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/8da1e9a983bce8f97f98d62fd48e4188.png)

图 真实感植物渲染 @UE4

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/996601e8702197b5eb9a68526eeb1c73.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/996601e8702197b5eb9a68526eeb1c73.png)

图 真实感植物渲染@UE4

## 

## 【核心内容提炼】

### 

### 1.1 场景管理（Scene Management）

任何3D游戏引擎都应该有环境相关渲染技术的管理和组织。

游戏引擎必须管理其渲染技术，以适合于它们希望看到的环境范围。以自然场景为主的游戏由上千棵树，灌木和可能上百万片草叶组成。直接分开渲染会出现数据管理问题，只有解决了这一问题才能以交互的帧率实时渲染。

我们的目标是在一个逼真的室外场景中大范围地移动游戏相机，而不需要在任务管理上花费过多的存储器资源。

#### 

#### 1.1.1 种植栅格（The Planting Grid）

场景管理方面，首先是使用了虚拟栅格的思路。

我们在相机周围建立一个世界空间固定的栅格，来管理每一层的植物和其他自然物体的种植数据。每个栅格单元包含渲染它所在物理空间层的所有数据。特别是，单元数据结构存储了对应的顶点、索引缓冲区和材质信息来再现需要绘制的内容。

对植物的每个层，建立相机到层的距离，层需要用它来产生视觉效果，这决定了虚拟栅格的大小。相机移动，虚拟栅格也随之移动。当一个栅格单元不再在虚拟栅格中时，丢弃它，并在需要维护完整栅格结构的地方添加新的单元。在添加每个单元格时，用一种种植算法把渲染所需的数据填充到层。如下图。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/8f2f9167f2775cfd70f2c978ce49ad6f.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/8f2f9167f2775cfd70f2c978ce49ad6f.jpg)

图 一个虚拟栅格

图注：每层有一个世界空间对齐的固定大小的栅格。深绿的单元表现为活动单元。当相机向前移动时，丢弃标记为X的单元，添加新的单元（显示为亮绿色）以维持虚拟栅格的大小，实现过程中有用的改进是使用栅格单元池且循环使用，因为当一个旧单元被丢弃时，总会增加一个新单元。

#### 

#### 1.1.2 种植策略（Planting Strategy）

对于充满自然物体的每个单元，需要在地面上选择要放置物体的适当位置。采用试探的方法根据被放置对象的类型来选择这些点。通常，需要的密度随机选点，然后看地面上的对应点是否适合于要种植的东西。而地面多边形的材质决定了一个层是否适用。

最显然的方式是在单元体中随机发射光线，直达地面，每当击中一个多边形，检查它是否适合种植（判断：草能种在这里吗？斜度会不会太大？），如果成功，那么就得到了一个种植点，继续这个过程，直到到达合适的密度。

这种方法不能处理重叠地形，且在少数栅格单元中，可能会花费过多的CPU时间。

比较好的方法是，选择所有与单元相交的多边形，丢弃所有不合适种植的多边形，然后扫描并转换它们来寻找合适的种植点。这与渲染管线中的光栅化一个多边形类似。

#### 

#### 1.1.3 实时优化（Real-Time Optimization）

实时优化种植策略的方法包括，选择一个栅格单元中的多边形可以通过使用AABB树或类似的数据结构来快速完成。而由于相机的连续运动，许多单元可能要突然种植，所以它也可以高效地让这个任务排队，使任务在每帧中只占用相对固定的CPU资源。而通过扩大栅格，可以确保在单元的内容进入视野之前，所有的种植就已完成。

### 

### 1.2 草地层（The Grass Layer）

实时渲染出无边的草地需要GPU技术和算法的细心平衡，主要的挑战是在相对低的计算和渲染开销下产生高度复杂的视觉外观。

这章的这一节中介绍了一种和[ Pelzer 2004 ]“渲染无数波动的草叶”相似的技术，且这章的技术以更低的GPU和CPU负载产生更高质量和更稳定的结果。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/04e8e2bee126a22e4ae4fa30fe71a1bf.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/04e8e2bee126a22e4ae4fa30fe71a1bf.jpg)

图 真实感草地渲染

首先，需要保证批次的最大化。该技术的目标是如何用相对较少的渲染API调用来绘制出尽可能多的草地，合理的方式是基于公告板。但其实更好的方式是在一次绘制调用中渲染尽可能多的内容（即一次draw call渲染多个公告板）。

为实现这个目的，草的每一层（即使用相同纹理和其他参数的所有草）的每个栅格单元由一个顶点和一个索引缓冲区对表现。如下图。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/a41e3afc06a8bc473d899e62d9257bbf.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/a41e3afc06a8bc473d899e62d9257bbf.jpg)

图：绘制每个栅格的单元结构

对种植的每个草丛（或公告板），将其位置写入顶点缓冲区并更新对应的索引缓冲区。每个公告板需要4个顶点和6个索引。对每个顶点，将位置设置为已经种植草丛的点。

一旦顶点缓冲区建立并发送到显存，就可以用单次调用画出每个栅格单元的植物。

与Pelzer的方法不同的是，这里使用面向相机的公告板代替每丛3个方形，而且其方法没有进行屏幕对齐。面向屏幕的公告板在所有的视角下（即便向下看）创建一个固定的深度。而相机越是由上往下看草丛，3个方形丛的方法就越会失效。所以本文提到的方法，更加灵活，适用更多相机角度的情况。

#### 

#### 1.2.1 通过溶解模拟Alpha透明（Simulating Alpha Transparency via Dissolve）

在渲染草的时候，想要使用透明来改善视觉混合和在接近虚拟栅格边界时的淡出。然而，基于Alpha的透明并不理想，因为它需要排序且速度很慢。虽然可以利用草较为杂乱的性质最小化一些排序技术，但实际上可以完全忽略这种做法。

为此，采取溶解效应（dissolve effect），也称纱门效应（screen-door effect）的方法，代替Alpha混合来模拟透明。首先，用一个噪音纹理调制草纹理的Alpha通道，然后使用Alpha测试从渲染中去除像素，通过从0到1调节Alpha测试数值，纹理表现出溶解的现象。这一过程如下图所示。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/ed41e45d2906640097c5db3421fe53aa.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/ed41e45d2906640097c5db3421fe53aa.jpg)

图 草纹理的构成

（a）漫反射纹理； （b）美工创建的alpha通道； （c）Perlin噪音纹理； （d）Perlin噪音与Alpha相乘的结果。这可以在像素着色器，或固定的Alpha测试值产生淡出。

这项技术的有点是Alpha测试的速度快而且与顺序无关。我们不再需要排序，草依然可以在远处淡出。虽然溶解在正常的情况下看起来不像真实的Alpha透明那么好，但可以利用自然的分形属性来完全掩饰任何溶解技术的视觉失真。

而实验表明，使用Perlin噪音纹理（Perlin 2002）代替随机的噪音纹理，则溶解效应与环境的适配程度几乎与Alpha透明一样好。

#### 

#### 1.2.2 变化

为增加真实感，需引入一些变化。一种方式是使用多种草的图像，但分批方法限制我们在每个绘制调用中只能用一张纹理。好在可以使用大纹理，把多种草排布在上面，在建立顶点的时候，可以调整UV坐标以旋转纹理的不同子区域（即可以建立一个纹理图集）。

每个公告板也能带有颜色信息。如果在种植时也为每个草丛建立一种颜色，那么对渲染灰度纹理或在顶点着色器中做细微的颜色偏移非常有用。Perlin噪声在这里也可以使用，而且很容易，例如，草可以从健康的颜色过渡到垂死的褐色染色，以获得宽广的颜色变化并减少草的重复性。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/8cdea6b4c4d2dc48fea0d9326739933d.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/8cdea6b4c4d2dc48fea0d9326739933d.jpg)

图 使用RGB信息来增加草地的真实感 @ GeNa @Unity5

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/93ca6ad54cad71c2042c8bf40669aceb.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/93ca6ad54cad71c2042c8bf40669aceb.jpg)

图 使用RGB信息来增加草地的真实 @ GeNa @Unity5

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/49090fe6638902bc41a55a8275982a42.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/49090fe6638902bc41a55a8275982a42.jpg)

图 使用RGB信息来增加草地的真实感 @ GAIA @Unity 5

【注：每颗草的顶点中都包含RGB的信息。在此场景中，颜色值来自Perlin噪声函数，模拟了比较绿的草，并修补了不太健康的褐色】

#### 

#### 1.2.3 光照

光照在草的外观上扮演了重要的角色。对于公告板草，要确保草和下面的地面一样受光。而地面自然起伏，并因此获得了不同角度的光照。我们需要通过减弱草的亮度来模拟这点，因此，需要知道草所在的地面角度，一个简单方法是在顶点定义中通过另一个向量传递这一信息。

在种植的时候，确定正在种植的草的多边形法线并把它带入公告板定义中。通过这种方式，顶点着色器就可以进行和草下多边形一样的光照计算、从而减弱它的彩色。在多丘陵的地形上，这会导致草和地面一样也有细微的到光的角度信息变化。

遗憾的是，这种方式导致草有一面一面的着色现象，即使地面的多边形是几乎平滑着色（如Gouraud着色）。为了避免这个问题，在种植处理期间必须平滑地插值通过顶点着色器的法线。

而如果太阳的角度是动态的，可以假设地面法线都大致向上，然后基于此法线和光的角度来计算光照。这样，就不一定要将地面的多边形法线带入顶点的定义和后续计算。这是一个画质的权衡，但这种方式对于应用程序来说已经完全足够。

#### 

#### 1.2.4 风

当风吹过，草地泛起涟漪，草变得鲜活起来了。

通过每一帧偏移草方形顶部的两个顶点，可以使方形在风中摇摆。可以使用一个正弦近似的和计算这个偏移，类似计算水表面的波动[Finch 2004]。这个技巧是在顶点定义中带一个混合权重，草方形的顶部两个顶点被设为1，底部两个顶点为0，然后把这一数值乘以风的缩放系数，底部的顶点仍然牢牢地依附在地上。

对于另外的变化，可以在种植期间略微随机变换顶部的两个顶点权重。这模拟了草的软硬区别。

在风中摇曳的时候，草叶时常改变其对光的方向，导致它们变亮或变暗，我们可以使用专门的风项来增加光照变化，以模拟这一现象。这极大地改善了风的视觉效果，甚至也能改善远处草丛的效果，虽然那里的物理摇摆变形以及变成子像素大小了。

然而，不允许风系数使草方形变形太多，否则产生的形变将会显得滑稽而不真实。谨记细微是关键。

### 

### 1.3 地面杂物层（The Ground Clutter Layer）

地面不仅只有随风摆动的草，细枝、小植物、岩石和其他碎片共同组成了具有自然复杂性的效果。其中，一些杂物和草一样可以当做公告板表现。

而但当我们混入混合各种几何对象物体时，环境的复杂度也就增加了。

和处理草公告板的方法一样，对于每个栅格元素，可以把3D网格数据解开到顶点和索引缓冲区中，以使它们可以在单次调用中绘制。我们必须把地面杂物分组为使用相同的纹理和着色器的层。可以像选择种植点那样，应用随机变换来改变它们的大小和方向，但是变换必须依据网格的特性，例如岩石是可以颠倒过来的，但是灌木颠倒就不行了。对于另外的变化，如同处理草多边形一样，可以通过传递RGB信息来给物体染色。

另外，用于处理顺序无关透明特效的溶解技术在3D网格和公告板上工作起来完全一样。把perlin噪声纹理调制到纹理的alpha通道，并使用到相机的衰减距离，然后alpha测试溶解3D网格，类似处理草公告板。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/d85c811d58e5187cf445614dc8d69988.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/d85c811d58e5187cf445614dc8d69988.png)

图 使用地面杂物来增加密集的细节@UE4 @Landscape Auto Material

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/8544048f8a6586cfbb57ce993dc8df9c.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/8544048f8a6586cfbb57ce993dc8df9c.jpg)

图 使用地面杂物来增加密集的细节@UE4

### 

### 1.4 树和灌木层（The Tree and Shrub Layers）

树的树干和主要的树枝应该建模成3D网格。次级树枝可以用公告板来模拟，以增加视觉的复杂性。因为树的枝叶繁茂，所以可以用类似于草的技术，用面向相机的公告板建立树叶丛。

因为树需要在长距离上维护它们的基本体积，但高细节渲染又很昂贵，所以必须使用层次细节（LOD）策略。当树退到一定距离后，可以使用较大但较少的叶丛公告板。对于较大的公告板，使用带有较多但较小树叶的纹理。

而在一个适当的距离之外，最后想要用一个面向相机的公告板表现一颗树。当树的轮廓不对称时，会相对困难。为了避免这个问题，可以为公告板产生树在各种不同角度的图片，然后根据树和相机的角度混合它们。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/841bf927d977d170d5f0d84cbc5a8ab3.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/841bf927d977d170d5f0d84cbc5a8ab3.png)

图 树的多级LOD与公告板 @UE4

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/568e67e4033f0a64316448f2fe5b2714.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/568e67e4033f0a64316448f2fe5b2714.png)

图 树的多级LOD与公告板 @UE4

灌木和叶片可作为另一种类型的树，和普通的树使用相同的技术。例如，一个茂盛的灌木可以看做一棵树干很小，或者不存在树干的树。此外，我们可以翻转一棵树，去掉树叶，并获得一个精心制作的暴露的根系，去嫁接上一棵正常的树。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/4e41bccf539ae7775743a71915dd858b.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/4e41bccf539ae7775743a71915dd858b.png)

图 灌木LOD与billboard @UE4

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/eb9fcfe97c4cba0c610e4d4ea21a3140.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/eb9fcfe97c4cba0c610e4d4ea21a3140.png)

图 灌木的渲染 @UE4

### 

### 1.5 阴影（Shadowing）

因为传递了草和地面杂物的RGB颜色，所以可以为阴影的区域选择较暗的颜色。这需要知道植物是否在阴影中。为了在自然环境中有效，这种阴影只需要非常接近正确的阴影即可。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/797d666a9b58c2d3d47893880e8eca5d.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/797d666a9b58c2d3d47893880e8eca5d.jpg)

图 草在树产生的阴影中 @UE4

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/af224ad22b30dbaa0fa4914937ebfb05.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/af224ad22b30dbaa0fa4914937ebfb05.png)

图 草在树产生的阴影中 @UE4 @Landscape Auto Material

一种方法是在种植时确定阴影。只需从植物位置向主要光源（太阳）投射一道阴影试探光线（shadow feeler ray），看看是否有相交。如果有，根据周围场景的环境颜色调整RGB值。记住投射阴影试探光线只考虑是否有相交（不只是最近的），所以其可以比标准的碰撞光线投射高效得多。

软阴影（Soft shadows）,在上下文中叫抗锯齿阴影（antialiased shadows）其实更合适，可以通过投射一个以上的阴影试探（shadow feeler）来实现。下图演示了这一方法，通过细微地偏移每道光线的开始位置，在一个给定点上可以进行3~5次光线投射。击中的部分用来在漫反射太阳光的和场景的环境光之间减弱光照。偏移越宽，阴影就越模糊。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/40f3733de4873b15f5d733bc3445c90f.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/40f3733de4873b15f5d733bc3445c90f.jpg)

图 使用光线投射的可见性测试

图注：从种植点向光源（在这个例子中是方向光）投射阴影试探光线。几乎发生的任何碰撞都可以表明这个点是在阴影中。为得到一个模糊阴影，需要投射另外的偏移阴影试探光线，并使用击中的部分决定多少环境光的颜色。需要注意的是，不要让阴影试探光线立刻与种植点的地平面相交吗，否则这次试探就没有意义了。

这些阴影不是动态的，但是对于移动缓慢的光源来说，可以很快地在间隔中重新计算（如太阳的移动）。一般来说，它们提供了充分的视觉信息，把风景变得更栩栩如生。

当投过树的大部分时，可以使用树叶茂密部分的球体或树干的圆柱体碰撞。对于树叶茂密部分，使用一个基于树叶茂密的随机函数来确定光线是否相交。虽然这种阴影技术是粗糙的，但和正确的解决方案没有明显的差别。

如果种植是作为离线处理预计算的，那么可以极大地提高阴影逼真度。一种可能比阴影试探光线方法更好的方法是获取光照图（light map）的纹素来确定阴影。如果光照图不在系统内存中，在实时处理方面可能有困难。

### 

### 1.6 后处理（Post-Processing）

后处理方面，辉光（glow）和泛光（bloom ），以及用高斯（Gaussian）模糊实现自然柔和的效果，都是比较合适进行照片级真实感植物渲染的后处理效果。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/ceb6e7e3a1c2db8d78220b20433a26d5.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/ceb6e7e3a1c2db8d78220b20433a26d5.jpg)

图 使用了多种后处理效果的渲染图 @UE4

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/d6f5fcf758bd46d7c1072ed88c86033e.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/d6f5fcf758bd46d7c1072ed88c86033e.jpg)

图 使用了多种后处理效果的渲染图 @UE4

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/63f1635a48edb1b4bb6ca456d2d27531.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/63f1635a48edb1b4bb6ca456d2d27531.png)

图 使用了多种后处理效果的渲染图 @UE4

### 

### 1.7 业界领先的植物渲染解决方案SpeedTree

也需要提到的是，SpeedTree是很优秀的树与灌木层的中间件，是植物渲染方面业界领先的解决方案。自2008年以来的各种一线3A游戏，如《蝙蝠侠》、《使命召唤》、《神秘海域》系列，包括近期的《彩虹六号》、《孤岛惊魂5》、《地平线：黎明》、《絶地求生》、《最终幻想15》等游戏，都使用了SpeedTree作为树木植物相关渲染的解决方案。

电影方面，包括最近的《复仇者联盟3》、《黑豹》在内的好莱坞大片，以及早一些的《速度与激情8》《魔兽》《星球大战：原力觉醒》等大片，也都使用了SpeedTree作为树木植物相关渲染的解决方案。

SpeedTree官网：<https://store.speedtree.com/>

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/32a152dc4d4886903745739c829e4af3.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/32a152dc4d4886903745739c829e4af3.png)

图 SpeedTree · CINEMA的宣传图

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/b80e73a6bad6f9b460d91e3ef121e6a3.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/b80e73a6bad6f9b460d91e3ef121e6a3.png)

图 SpeedTree · GAME的宣传图

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/1b92464b7a254a80459eac04f750e68b.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/1b92464b7a254a80459eac04f750e68b.png)

图 电影《星球大战 原力觉醒》中的speed tree @<https://www.speedtree.com/starwars.php>

## 

## 【核心要点总结】

【场景管理方面】

采用虚拟栅格的思路，实时优化种植的策略是使用AABB树类似的数据结构来选择一个栅格单元中的多边形。

【草地渲染方面】

基于公告板进行渲染，保证渲染批次的最大化、通过溶解模拟Alpha透明。

调整UV坐标以旋转纹理、使用RGB信息等方法来减少重复，增加真实感

草地的光照：多边形法线并把它带入公告板定义中，参与光照计算。滑地插值通过顶点着色器的法线，来解决草有一面一面的着色的现象。也可以假设地面法线都大致向上，然后基于此法线和光的角度来计算光照。

草地与风的交互：使用一个正弦近似的和计算这个偏移，类似计算水表面的波动[Finch 2004]，也可以使用专门的风项来模拟草地因风而出现的光照变化。

【地面杂物层方面】

3D网格结合公告板的渲染、通过溶解模拟Alpha透明。

【阴影方面】

基于阴影试探光线（shadow feeler ray）、基于树叶茂密的随机函数来确定光线是否相交、基于光照图（light map）的纹素来确定阴影。

【树与灌木层】

树干和主要树枝建模成3D网格，次级树枝用公告板。LOD。多个角度的公告板混合。

【后处理】

辉光（glow）、泛光（bloom ）、高斯（Gaussian）模糊

最后再上几张渲染图，都来自虚幻4引擎的渲染：

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/884517e8ec7d2aef0b5ad1bd7c8e8503.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/884517e8ec7d2aef0b5ad1bd7c8e8503.jpg)

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/9f4b87b3064801c621bcb3ce2dfe9e76.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/9f4b87b3064801c621bcb3ce2dfe9e76.jpg)

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/b952ace0a5917201fb0c6d551ba468ab.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/b952ace0a5917201fb0c6d551ba468ab.png)

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/34baace7f0a13911171a220a8609ce34.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/34baace7f0a13911171a220a8609ce34.png)

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/3dd03483e84361d405a7570f2df8c088.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/3dd03483e84361d405a7570f2df8c088.png)

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/1bc80b240f19e0200e0fa47401f7fbb5.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/1bc80b240f19e0200e0fa47401f7fbb5.png)

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/107f5ac68224623ee428576c95850ca3.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/107f5ac68224623ee428576c95850ca3.jpg)

## 

## 【关键词提炼】

真实感植物渲染（Photorealistic Botany Rendering）

场景管理（Scene Management）
