# 虚幻4渲染编程(Shader篇)【第十二卷：MeshDrawPipline】



## 简介：

Unreal engine的渲染模块是越来越复杂，最开始只有延迟管线，随后加入了mobile，现在又加了很多实时光线追踪的东西，各种DX12，VK新的RHI也纷纷加入。

虚幻4的4.22版本对渲染模块进行了较大重构，废弃了之前的DrawList&&Draw   Policy，取而代之的是MeshDrawPipline。与之前的DrawPolicy相比，MeshDraw更为简洁，灵活。新旧Pipline对比图如下：

4.22



![img](MeshDrawPipline.assets/v2-4741d01b86c2a0838f69f62994217103_hd.jpg)

<=4.22



![img](MeshDrawPipline.assets/v2-6842757d6cdbbe664bf881c9cc7e3eb0_hd.jpg)

我之前有写老的drawingpolicy的文章：[小IVan：虚幻4渲染编程(Shader篇)【第十卷：绘制策略】](https://zhuanlan.zhihu.com/p/43576669)。如有错误还请巨佬们斧正。

因为涉及到的细枝末节的东西很多，所以这篇文章我会在一个月内持续更新修改。

------

首先先过一下渲染过程中主要的类和步骤。

## 【1】FPrimitiveSceneProxy

这个类的功能没有什么改变，依然在通过GetDynamicMeshElements等函数从每个primitivecomponent中收集渲染资源



![img](MeshDrawPipline.assets/v2-080a2aeb3ed579f31529be4e4e34c893_hd.jpg)

## 【2】InitViews

FPrimitiveComponent的GetDynamicElements这个收集操作通过渲染器的InitViews在可见性剔除之后发起



![img](MeshDrawPipline.assets/v2-d6dabdcae9c1cf6622c7c99ba7db08ce_hd.jpg)



![img](MeshDrawPipline.assets/v2-189412e0445d583e8feead60ea730d3f_hd.png)

FMeshElementCollector会把场景里的渲染数据收集起来



最后会调用SetupMeshPass来创建MeshPassProcessor



## 【3】FMeshPassProcessor



![img](MeshDrawPipline.assets/v2-3b49a186b5f6ec56e0c6b1bea7547ded_hd.jpg)

FMeshPassProcessor有两个作用，第一个是选择绘制时所使用的shader，第二个是搜集这个pass绑定的顶点工厂，材质等。**可以从一个FMeshBatch创建多个FMeshDrawCommands**



![img](MeshDrawPipline.assets/v2-abdcff6aa0929355b1cba70dfa5fcec1_hd.jpg)

搜索引擎就会发现，每个pass都会有一个对应的FMeshPassProcessor。FMeshPassProcessor是所有pass的FXXXMeshPassProcessor基类。

在一个pass在初始化的时候，会往MeshPassProcessor里填充BatchMesh渲染单元。

以depthpass为例,DepthPass的PassProcessor创建代码如下：



![img](MeshDrawPipline.assets/v2-a3d4bd08a60bdbc4d62faf3731134541_hd.jpg)

在渲染管线重会调用Processor的AddBatchMesh把渲染资源加进去



![img](MeshDrawPipline.assets/v2-8ffbe4a6821ddd27a88f6f0065d392ed_hd.png)



在AddMeshBatch函数中会进行Passfilter和SelectShader，分别对应下图的1，2部分。



shader等设置好以后会通过BuildMeshDrawCommands创建command然后通过FinalizeCommand完成command的添加





## 【4】FMeshDrawCommand



代码注释已经解释得很清楚了。一个MeshDrawCommand描述了一次绘制所需要的所有资源。FMeshDrawCommand类中主要负责管理了三类资源：（1）ShaderBindings，记录了这次Command各个阶段绑定的参数集。（2）VertexStreams   记录了VertexBuffer的信息。IndexBuffer记录了IndexBuffer的相关纤细。CachedPipeline用于索引GraphicPipelineState。

## 【5】ShaderBindings



![img](MeshDrawPipline.assets/v2-b24e4393235cf5c91297d3a051b729e4_hd.jpg)

可以从新老方式中看到，新的方式是通过收集参数而不是直接设置RHICmdList来设置Paramerters了。ShaderBinding是作为MeshDrawCommand的组成部分之一，在这里面需要绑定管线所需要的所有参数集。



![img](MeshDrawPipline.assets/v2-4f60c34422624d137f243d4052b720ed_hd.jpg)

## 【GPUScene】



![img](MeshDrawPipline.assets/v2-1b3a12c20d2ad2417a785cc4f998cd23_hd.jpg)

GPUScene有一个PrimitiveBuffer，它会跟踪场景Primitive的添加，移除操作，会在GPU端有一个镜像场景。虚幻使用一个Computeshader来更新primitivebuffer给下一帧使用。Primitivedatabuffer要求一个primitive的所有shader只能有一个primitiveID



![img](MeshDrawPipline.assets/v2-cb0e8f3d3e65632c29c0d458180fbe3a_hd.jpg)

这个primitiveID只有LocalVertexFactory才有



![img](MeshDrawPipline.assets/v2-e71eeb565b7bcc312fb12336361528c3_hd.jpg)



![img](MeshDrawPipline.assets/v2-33cc1b62c9f081fa1773c1bcf77000e0_hd.png)

------

这里用CustomDepthPass作为一个例子看一下静态物体的绘制流程。

## 【CustomDepthPass】

首先准备好个空场景然后拖一个盒子进去



![img](MeshDrawPipline.assets/v2-681e8a20f22bd4567b5bec51b6dcb6c5_hd.jpg)

这时会调用AddPrimitive的逻辑



![img](MeshDrawPipline.assets/v2-04307e21e9f52dbfb84ac922fea5acf9_hd.jpg)

会创建场景代理，各种渲染数据，矩阵包围盒等。并且会更新GPUScene



并且会CacheMeshDrawCommands



然后创建PassProcessor然后AddMeshBatch，这个Processor会创建MeshDrawCommands



完成commands的创建后销毁这个Processor。这便完成了对Commands的添加。



要绘制时直接调用这些commands即可。这些commands会去调用RHI，RHI层会去调用各大图形接口。



最终就完成了绘制。

这里会发现，我们添加的时候是往TSet<FMeshDrawCommandStateBucket,  MeshDrawCommandKeyFuncs>  CachedMeshDrawCommandStateBuckets;里添加，真正使用的时候不会直接使用这个数据，而是经过剔除和各种处理后把一帧画面里所需要的数据放到ParallelMeshDrawCommandPasses里。

------

DrawCall的发起者ParallelMeshDrawCommandPasses

## 【ParallelMeshDrawCommandPasses】



DispatchPassSetup是一个关键函数，它负责为每个pass管理MeshDrawCommands，为绘制每个pass做准备。

可以看到我们有很多种pass类型。一个pass里有很多MeshCommand



![img](MeshDrawPipline.assets/v2-857a64092c73e4230104611eff74af34_hd.jpg)

在InitView的时候，我们把我们的command按照不同的pass类型分别塞倒ParallelMeshDrawCommandPasses里，这样就可以方便地统一调用command来完成各个pass的绘制了。



![img](MeshDrawPipline.assets/v2-3787a8f6fdf436b5da6cf2b486cdf66f_hd.jpg)

PrePass：



![img](MeshDrawPipline.assets/v2-43778ba03642bf6dd9e8824439f69660_hd.png)

DepthPass：



![img](MeshDrawPipline.assets/v2-00896070b0764ab7dc4f73915597432c_hd.png)

CustomDepthPass：



![img](MeshDrawPipline.assets/v2-d11c0c37b01246b35e6987cfb48c9e84_hd.png)

BasePass：



![img](MeshDrawPipline.assets/v2-d1d67f7a603d45151991197ad19c987b_hd.png)

还有很多我这里就不例举了。

我在视口中加入一个球一个盒子，他们的vertex buffer不一样材质一样，所以无法被加入到一个batchmesh中，所以可以理论上customdepthpass会有两次绘制



![img](MeshDrawPipline.assets/v2-cce48ca03b263974a80630a131d2e288_hd.jpg)



![img](MeshDrawPipline.assets/v2-4d98f33504f1e447ccca20aa432995f2_hd.jpg)

我在视口中再拖了一个盒子，现在视口中有两个盒子一个球体。BasePass只画了两次，因为两个盒子被DrawInstance了，然而CustomDepthPass却画了三次：



![img](MeshDrawPipline.assets/v2-43af65d28c7ccd21bcef0244947a57f3_hd.jpg)



![img](MeshDrawPipline.assets/v2-047dea6113aca7e691d55118406d1ef9_hd.jpg)

对于美术制作层面来说，如果是做端游，我们可以把模型切成碎块然后搭建场景不需要batch，因为虚幻的basepass已经dynamicbatch了的（前提是这些碎片的vertexbuffer和材质是一样的）比如搭建一个木头结构的房子其实也就用几个木头模型罢了。这样切模型和非在DCC中batch模型的区别在于，其它有些pass不会以dynamicbatch规则去合并这些dc。

------

综上虚幻的渲染模块经过这次重构后，灵活性更强，逻辑更加紧凑。



![img](MeshDrawPipline.assets/v2-520e526b6d25884e480f0d1e6695bb66_hd.jpg)

Enjoy it.
