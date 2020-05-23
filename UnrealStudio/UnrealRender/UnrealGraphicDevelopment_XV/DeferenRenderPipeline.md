# 虚幻4渲染编程【第一卷：虚幻自身的延迟渲染管线】

文章



## **我的专栏目录：**

![图标](DeferenRenderPipeline.assets/v2-adfc32ab6d1929ce6ebb6863da9e0f0f_180x120.jpg)

## **简介：**

因为虚幻的架构，我们美术做一个效果只能使用材质编辑器。这让我很不舒服，稍微想做点特别点的效果就没办法了。我又是天天在公司用自研引擎的人，这种限制让人很不舒服。所以我开始修改了虚幻的shadingmode之类的。但是感觉自己还是不满足，想调个多pass虚幻都不让我做，所以我打算加个pass什么的。但是虚幻加pass可不像unity那么简单，只有操刀去改源码了。然后我又反观了一下我前几篇博客，只简单讲了一下怎么改代码，没说原理。所以这个系列我打算系统说一下虚幻的一个架构。当然虚幻如此庞大，我也有很多不知道的地方。

​      其实我写博客的目的很简单，就是想记录一下自己做的东西，有时候自己翻一下，再把问题再想一下，也许会有新的发现。虚幻的渲染方面的资料也是少得可怜，研究的人也少得可怜。大部分牛人都自己去造轮子去了。我只是个技术美术，造轮子的事情还是交给图形程序吧。不过研究虚幻4的确学到很多。如果有大牛看到我的文章中有错误，还请留言斧正。

首先在看这个系列之前，你需要具备以下：

（1）至少要敲过简单的渲染器，不管是拿dx敲还是拿gl敲或者vk之类的。

（2）对虚幻引擎有一定了解，对虚幻的渲染有一定了解。可以看我前几篇文章，或许可以有所帮助。

（3）C++基础。其实本人c++水平也是一般般（常常受到公司程序大牛的鄙视，不过我是美术）。

（4）至少一块RTX显卡可以用来做实时光线追踪（2019年）

随着引擎版本的更新，后续会逐步加入新版本。那么下面就正式开始吧！

## **【概览虚幻4渲染管线】**



![img](DeferenRenderPipeline.assets/v2-22128d79c885d1fe1d99d8fe6d576fca_r.jpg)



![img](https://pic1.zhimg.com/v2-08f11139f8888ff018aee74a229ff90c_r.jpg)

首先，虚幻有很多个管线的。Mobile管线和Deferred管线。首先找到



![img](https://pic1.zhimg.com/80/v2-b01943154ac4971cadb819c320827918_hd.jpg)

在这个函数里你将会看到很多熟悉的函数名称



![img](https://pic2.zhimg.com/v2-79365eb5ed9f7a86511ae8688a3d7cb5_r.jpg)

虚幻就是通过调用这些函数来一步步绘制的。是不是很眼熟？这个就是各大论坛啦，博客啦讲的虚幻渲染流程的真面目。

下面就是官方的DrawOrder了。那么这个顺序是怎么来的呢。就是上面那个函数的调用顺序。



![img](DeferenRenderPipeline.assets/v2-f9c233f06579279d759ee7f76d1d87d3_r.jpg)

再打开这个Render函数，你就将看到延迟渲染一帧所调用的各个函数。（反正我看了半天就看到个大概的渲染顺序之外，还是啥也不知道）



![img](https://pic2.zhimg.com/v2-2f80522a5ef41b9858277cee2726f53d_r.jpg)

那么当我们把一个模型托到场景里，这个模型被渲染出来的整个流程到底是什么样的呢？这个流程其实是非常庞大的。下面我就来一个一个拆分。

（1）第一步：资源准备阶段。这个阶段包括顶点缓冲区的准备，索引缓冲区的准备。这一步由场景代理管理完成。当然从磁盘里读取模型资源这些就涉及到StaticMesh这些了。想了解这一步可以去看我以前的博客，或者直接去看UPrimitiveComponent，UMeshComponent，UStaticMeshComponent，UCableComponent，UCustomMeshComponent。当你把这些源码全部研究一遍后，这个阶段算是了解了。这个阶段我不打算再描述了，因为已经有了很多现成的代码了。

（2）第二步就是shader资源的准备了，这个又是一个非常大的话题了。可以去看我以前关于给改材质编辑器和加shadingmode的文章便可以有个大概的了解。这一步我还会进一步阐述。

（3）第三步就是绘制了。

我们先不看Render函数那些复杂的调用，我们把精力先集中到shader层面来。一张画面是怎么开始绘制的呢？





![img](DeferenRenderPipeline.assets/v2-c1e60fc31db469462deaf519452720aa_hd.jpg)



通过这个我们便能知道一个大概的绘制流程（千万别以为虚幻只有这几步，不过主要的大概的流程是这样）。先绘制那些深度啊，初始化视口啦我们先不管。我们来看下这个BasePass。这个BasePass干的事情就是把GBuffer画出来。



![img](https://pic2.zhimg.com/v2-e9b47830309669b8e7b5b941e7842a79_r.jpg)

这里就是像素着色器的入口。绘制完这一步后，我们就有了GBuffer然后再绘制剩下的。环境遮罩骤就先不说了。来看看最重要的光照部分。

光照部分的入口在这里：



![img](https://pic1.zhimg.com/v2-636bcab8823640a0c6a27f53af6c68f8_r.jpg)

虚幻的TiledDeferredLighting的渲染方式。不知道这个的去看毛星云的RTR3的博客的光照那节，讲得特别好。这里给个传送门：

[https://blog.csdn.net/poem_qianmo/article/details/77142101](https://link.zhihu.com/?target=https%3A//blog.csdn.net/poem_qianmo/article/details/77142101)

这里会调用



![img](DeferenRenderPipeline.assets/v2-c70eae1048c6162206d5b474bfe981cf_r.jpg)

GetDynamicLighting这个函数会调用



![img](DeferenRenderPipeline.assets/v2-7fbb0cbfb3b9df9e669443140ec243e2_r.jpg)

这里会接着调用



![img](DeferenRenderPipeline.assets/v2-f949410bac2fd37074974d1d7df2be3f_r.jpg)

看到这里就很熟悉了，看过前面我修改shadingmode的博客应该会对这里很熟悉。

lighting绘制完了之后就会绘制一些反射啊之类的东西了，然后就是透明物体啊后期啊。这些后面会慢慢分析他们。我们先把两个最重量级的研究了。

接下来我们研究一下fog渲染阶段。找到FogRendering.cpp你就会发现，其实绘制fog的是一个globalshader。前面绘制各个物体的是materialshader。



![img](DeferenRenderPipeline.assets/v2-041f009f82343271db98d1c8f658acc7_r.jpg)



![img](https://pic1.zhimg.com/v2-912f6613411e7febc76d6a04a360f4b8_r.jpg)

你会发现绘制fog的是一个globalshader。虚幻一共有这么几种shader：Globalshader  materialshader和meshshader。

这篇博客只是一个概述性和引导性的。只是说明一下虚幻绘制的一个大概情况。下一卷我将演示一下怎么自己写个shader，引擎识别它，编译它，然后如何cpu和gpu进行信息交流的

4.20的Unreal渲染模块有了较大改动。



![img](https://pic2.zhimg.com/v2-ff846341921de5e2603cdf8fbb07e72d_r.jpg)

主要是为了配合引擎新增特性和性能优化。不过大体上的流程还是和上个版本的保持一致。

为了给LTC让道，所以shader做了大面积重构。



![img](DeferenRenderPipeline.assets/v2-8a8ebea188a277f2f7186ba2b9400533_r.jpg)

ShadingModel改为了IntergrateBxDF



![img](https://pic1.zhimg.com/v2-a0306824caeff694627c0b10992d5a38_r.jpg)

下面会对绘制流水线详细写一遍，由于量巨大所以我会慢慢更新。

## （1）【InitView】



![img](https://pic2.zhimg.com/v2-579f87c2f5d7426774e0faf91828f1ad_r.jpg)



![img](https://pic2.zhimg.com/v2-281e12fd30c5afbb307c2e38d89e02ed_r.jpg)

引擎代码注释写得非常简单：Initialize scene's views.Check visibility, build visible mesh commands, etc.

这是渲染管线的开始，这步是为渲染管线准备绘制当前帧所需要各种资源。后面的管线就是判断一下画不画，绑定一下状态和RT然后就画画画就好了。这一阶段做的事情非常多也非常杂。首先来看看一些主要的

### ComputeVisibility



![img](https://pic1.zhimg.com/v2-413887eb219612529fad23a791cdffe4_r.jpg)

可见性剔除有很多种技术，引擎会使用多种方法进行组合剔除，把没必要渲染的东西剔除干净，最大限度在渲染之前就做到最省。

虚幻提供了几种剔除方法



![img](DeferenRenderPipeline.assets/v2-fa3aa8b0d64ec933f51e6d53cf8c1962_hd.jpg)

他们各有优劣，可以根据不同平台和情况进行选择。

**VisibilityMap**

在后面会把视口中可见性属性是非可见的物体剔除掉。



![img](DeferenRenderPipeline.assets/v2-3e6a3d6795ee883095316aad2d84de6e_r.jpg)

**PrecomputedVisibilit**

在场景中可以使用预烘焙的可见性数据。



![img](https://pic2.zhimg.com/v2-338fa423f32cc89fc61d49d52a3f9c6d_r.jpg)

如果当前视口场景中有可见性烘焙数据就会启用可见性烘焙的剔除方式



![img](DeferenRenderPipeline.assets/v2-90003f837c79f232abd9cd8d256c926b_r.jpg)

**ViewFrustomCulled**

做完前面的步骤后，还会进行视锥体剔除，并且大部分情况下，视口会使用视锥体剔除



![img](https://pic2.zhimg.com/v2-6a73aecb905f86fe35e609d48d22030d_r.jpg)



![img](https://pic2.zhimg.com/v2-a132e9e92fc49242fedcfcfdbf9bbf81_r.jpg)

进行视锥体剔除后可以减少大部分没必要绘制的图元



![img](https://pic2.zhimg.com/v2-633af0986b124f9de75572fc72f934f1_r.jpg)

这时再配合各种其它的剔除方法就可以进一步剔除



![img](DeferenRenderPipeline.assets/v2-9508c4c49a170086ad0324b21ab0952b_r.jpg)



![img](https://pic2.zhimg.com/v2-7a06cfb0ddb034c3de3fe90d41261999_r.jpg)

而这里的“其它的剔除方法”包括但不限于PrecomputedVisibility，Distance，DynamicOcclusion

**DistanceOcclusion**



![img](DeferenRenderPipeline.assets/v2-f03bccf5cee359508ffe4f35226c3ff3_r.jpg)

不在距离范围内就不绘制，非常简单有效的绘制方式。这种剔除方式挺适合地面上摆的小物件，摆的一些decal或者小道具，对大型建筑不适合。

**Hardware Occlusion Queries**

硬件的可见性剔除。这种方法将每帧的可见性检查作为每个Actor的查询发出。  Actor的可见度在一帧之后被回读 - 如果相机移动得非常快，有时会产生不利影响，导致它们“弹出”。  硬件遮挡的成本随着在GPU上执行的查询的数量而变化。 使用距离和预计算可见性方法可以减少GPU每帧执行的查询次数。

在各种剔除后，在InitView的最后会根据这些数据建立MeshPass



![img](DeferenRenderPipeline.assets/v2-f8f8a5da3c83bf414cc298ed873e4fc3_r.jpg)

## （2）【EarlyZ-PrePass】



![img](DeferenRenderPipeline.assets/v2-20b0db727695cf52011890e382b141f7_r.jpg)



![img](DeferenRenderPipeline.assets/v2-c4431b89c91a80c03c2b6262e15b2faf_r.jpg)

EarlyZ由硬件实现，我们的渲染管线只需要按照硬件要求渲染就可以使用earlyz优化了，具体步骤如下：

（1）首先UE4会把场景中所有的Opaque和Mask的材质做一遍Pre-Pass，只写深度不写颜色，这样可以做到快速写入，先渲染Opaque再渲染Mask的物体，渲染Mask的时候开启Clip。

（2）做完Pre-pass之后，这个时候把深度测试改为Equal，关闭写深度渲染Opaque物体。然后再渲染Mask物体，同样是关闭深度写，深度测试改为Equal，但是这个时候是不开启clip的，因为pre-pass已经把深度写入，这个时候只需要把Equal的像素写入就可以了。

关于EarlyZ的具体详解可以去看参考文章【1】

首先渲染prepass的第一步肯定是渲染资源的准备啦。primitive资源会在InitView的时候准备好。

然后会再BeginRenderingPrePass函数中设置各种绘制管线的绑定，包括关闭颜色写入，绑定Render target



![img](https://pic2.zhimg.com/v2-b7bc93523a89f8a71fdcbaff1c5f7741_r.jpg)

然后再调用draw之前会把各种UniformBuffer和渲染状态设置好



![img](DeferenRenderPipeline.assets/v2-2335f9e9be8296914c75dcc0143dc20e_r.jpg)



![img](https://pic1.zhimg.com/v2-222b71e8428210b332c7af6630f59734_r.jpg)

然后调用draw



![img](https://pic2.zhimg.com/v2-2bf33be4490056844784e7f7ca614789_r.jpg)

最后完成PrePass的绘制



![img](DeferenRenderPipeline.assets/v2-f46c8f5ca6bfebefeeb5309fd4da63ba_r.jpg)

## （3）【ShadowDepthPass】

根据不同的灯光类型会绘制不同种类的shadowmap。总的来说绘制shadowmap的时候不会使用遮挡剔除。

Unreal渲染shadowmap目前我就找到个视锥剔除



![img](https://pic1.zhimg.com/80/v2-76d5a2f790384aa5c172157eda0fb760_hd.png)



![img](DeferenRenderPipeline.assets/v2-4b239cf4bbdce108af1929b27542fa8e_r.jpg)

shadowdepthpass可能是在basepass之前，也可以是之后，具体看EarlyZ的方式



![img](DeferenRenderPipeline.assets/v2-c1d630e5e5349a8133c907a4d845c0d7_r.jpg)



![img](https://pic1.zhimg.com/v2-7be01e95ea13f36f1a1e979637691570_r.jpg)

我们的灯光种类繁多大致可以分为两类，一类使用2Dshadowmap的，一类使用Cubemapshadowmap的



![img](https://pic1.zhimg.com/v2-322e5c8413568369be9fa332612372c0_r.jpg)

上图的1部分就是渲染2DshadowMap，2部分渲染的就是Cubemapshadowmap，这一步只是渲染出shadowmap供后面的Lightingpass使用。

## （4）【BasePass】



![img](https://pic1.zhimg.com/v2-975568166609af0c7721fbaca1464828_r.jpg)

BasePass使用了MRT技术一次性渲染出GBuffer。



![img](DeferenRenderPipeline.assets/v2-f7018c22976e094d9a2faf24a82467bb_hd-1559760125135.png)

再上一次GBuffer的数据分布



![img](https://pic1.zhimg.com/v2-7122e9e374b7824897153f0d30716304_r.jpg)

BasePass把GBuffer渲染出来之后就可以供后面的LightingPass使用了。我们的材质编辑器再Surface模式下也是在生成MaterialShader为BasePass服务



![img](DeferenRenderPipeline.assets/v2-08e5687122396117ca2ec8c91364cb1f_hd-1559760125136.jpg)

这部分可以去看看我的材质编辑器篇有详细介绍。

也是通过一系列设置绑定渲染状态资源等，最后调用dispatchdraw



![img](https://pic2.zhimg.com/v2-7b3ca3b430be474df968dbefa78b3a31_r.jpg)



![img](https://pic1.zhimg.com/v2-7cfc98b15cddeae69f7ce2c082ff1554_r.jpg)

可以注意到，MRT0是SceneColor而不是BaseColor



![img](https://pic2.zhimg.com/v2-5d21e50dd500c5a2767beee0e1d46af1_r.jpg)

Scene在BasePass中做了简单的漫反射计算



![img](DeferenRenderPipeline.assets/v2-387c26c1874b87fcc347f1ae4e8a59db_r.jpg)

这一步用到了，这个测试场景我是烘焙过的，我把烘焙数据去掉，SceneColor其实是这样的：



![img](DeferenRenderPipeline.assets/v2-8eaeaf082a3a834c4c171ed747c5d12f_r.jpg)

啥也没有黑的

BasePass会在这个阶段把预烘焙的IndirectLiting计算到SceneColor这张RT上供后面的pass使用



![img](DeferenRenderPipeline.assets/v2-e1057d96b87a69bd1b0348192e7d3743_r.jpg)

## （5）【CustomDepthPass】



![img](DeferenRenderPipeline.assets/v2-02c2ea20f0faf7498f929d3db4a53d1f_r.jpg)



![img](DeferenRenderPipeline.assets/v2-d3979c189f927d9df8ba9c0f1f8eec32_r.jpg)



![img](https://pic2.zhimg.com/v2-e840d7c19ad4236635107d43600857e5_r.jpg)

上面的图渲染了一个球的customdepth（在红圈处可以看到一个球，可能不是很明显哈）。CustomDepth没啥特别的，就是把需要绘制CustomDepth的物体的深度再绘制一遍到CustomDepthBuffer上。

## （6）PreLightingPass

虚幻封装了一套方便画PostPass的机制，后面的绘制SSAO，Lighting，SSR，Bloom等各种pass都是用的这逃Context的机制。



![img](DeferenRenderPipeline.assets/v2-dd100189736dd2fbc0bf7fcd04c602c7_r.jpg)



![img](DeferenRenderPipeline.assets/v2-27ce6dcd474432309e921ff6a4c5dd3a_r.jpg)

PreLighting这步主要是在用前面的GBuffer算decals和SSAO为后面的Lighting做准备。



![img](https://pic1.zhimg.com/v2-3e9ecfb1b2b3b30bedbf036a96e95424_r.jpg)

SSAO使用的是FPostProcessBasePassAOPS这个C++shader类。



![img](https://pic2.zhimg.com/v2-71ec0c87347da589f9fdd1a996245211_r.jpg)

对应的USF是PostProcessAmbientOcclusion



![img](DeferenRenderPipeline.assets/v2-3bb3b9be4b24b7e6f72a81ac4374a49a_r.jpg)

并且使用Computeshader来加速计算。

## （7）【DirectLightPass】



![img](DeferenRenderPipeline.assets/v2-9c628b0deac61c8f85fdf9e737bbee36_r.jpg)

LightPass也非常复杂，整个pass的代码有几千行，shader代码也有几千行非常恐怖的系统。我们先找到入口函数：



![img](https://pic2.zhimg.com/v2-ae2cf511c90d31bdc8f1fd5b51e775e5_r.jpg)

### （1）方向光

根据不同的情况，使用不同的渲染策略

渲染不同情况下的灯光大体分类如下。还会根据不同的渲染方式分类。



![img](DeferenRenderPipeline.assets/v2-a1333d04a291ebbcb02b00e3aee9e20f_r.jpg)

比如一般的方向光：



![img](https://pic1.zhimg.com/v2-e81159b5659a27db7d517ed13c75add0_r.jpg)



![img](DeferenRenderPipeline.assets/v2-d92700e7edb10534ee05525828eb2953_r.jpg)



![img](DeferenRenderPipeline.assets/v2-ea5721ab9ef2dd6b2142de91fc8d25fb_r.jpg)

在渲染方向光的时候因为不需要考虑分块，所以直接把每盏灯挨个画出来就可以了



![img](DeferenRenderPipeline.assets/v2-24d0336562057e6775d29cc3c816ce87_r.jpg)

下面我只放了一盏方向光



![img](https://pic1.zhimg.com/v2-61121b057c63138f11f098d20e221154_r.jpg)

下面我放三盏方向光：



![img](https://pic2.zhimg.com/v2-1611d5f40ce987c51300b20a8a5bc5dd_r.jpg)

### （2）TileDeferredLighting

如果灯光不渲染阴影，并且灯光没用IES并且灯光数目达到80盏以上（4.22）并且启用了TileDeferred管线，那么虚幻4就会使用TileDeferredLight来计算光照，虚幻实现TileDeferrdLight使用的是一个Computeshader



![img](DeferenRenderPipeline.assets/v2-921f7b112ed427ba1c620d175427af67_r.jpg)



![img](DeferenRenderPipeline.assets/v2-d48819345cfedd485228613f01978203_r.jpg)



![img](https://pic2.zhimg.com/v2-b6c3467da49e57487a68713c3b426481_r.jpg)

有很多灯光使用的潜规则。

## （8）【ScreenSpaceReflectionPass】



![img](DeferenRenderPipeline.assets/v2-70188de95d3495fb079b443ae6c7dcf2_r.jpg)



![img](DeferenRenderPipeline.assets/v2-09ba59cff82192d6da7a5a162719a6f6_r.jpg)



## （9）【TranslucencyPass】



![img](DeferenRenderPipeline.assets/v2-d1f1d40bdd60db0e92b278cfa9728eae_r.jpg)



![img](DeferenRenderPipeline.assets/v2-94b0640d438e3161dbeaec70cf3f1582_r.jpg)

透明物体会放在最后渲染，但是在后期的前面。需要看是否在DOF(景深)后合并。

对于这个上图的那个场景来说，透明物体渲染的buffer是长下面这样的：



![img](DeferenRenderPipeline.assets/v2-6c05f557dc872163ce7f9b1f554222af_r.jpg)

最后在后期中组合



![img](https://pic2.zhimg.com/v2-7aceba7b907363239ee4127cae52b7dd_r.jpg)

如果没有启用r.ParallelTranslucency透明物体只能挨个渲染。



![img](DeferenRenderPipeline.assets/v2-f171cd98a584a4d84d496fdbf8b23ec7_hd-1559760125402.jpg)



![img](DeferenRenderPipeline.assets/v2-bd2be1695a6910da54f2365ffaaf5b2b_r.jpg)



![img](DeferenRenderPipeline.assets/v2-0186407aafeca4d0bb4b0c89367d2d7b_r.jpg)

如果启用了就可以走上面的并行渲染分支。

透明物体的渲染在实时渲染中一直比较迷，会有各种问题。比如排序等等。在默认情况下是走AllowTranslucentDOF的。AllowTranslucentDOF是什么意思呢，代码的注释里有解释。



![img](https://pic1.zhimg.com/v2-2b17bd6e094be3f7032fc8b5a34a8d80_r.jpg)

Translucent物体的渲染有几种模式：



![img](https://pic1.zhimg.com/v2-6b669646aa731d2e62198ecdd6f72c88_r.jpg)

这里的代码我们在BasePassPixelShader.usf里能找到



![img](https://pic2.zhimg.com/v2-45338166686e8f83ea1ad2afe022a049_r.jpg)

对于非透明物体来说basepass是渲染GBuffer的，但是对于透明物体来说，BasePass是渲染基础的+Lighting的，会在这里一次性渲染完，如果我们想改透明物体的shading方式，就需要用在这里改了。

Enjoy it

## **Next：**

参考文章：

【1】[fengliancanxue：深入剖析GPU Early Z优化](https://zhuanlan.zhihu.com/p/53092784)

【2】[Visibility and Occlusion Culling](https://link.zhihu.com/?target=https%3A//docs.unrealengine.com/en-us/Engine/Rendering/VisibilityCulling)

