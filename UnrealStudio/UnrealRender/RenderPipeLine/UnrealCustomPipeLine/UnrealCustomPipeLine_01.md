

# 虚幻4渲染编程（重写渲染管线篇）【第三卷：在虚幻中搭建渲染器---上】

有了第一卷的铺垫之后，我们就可以开始写渲染器了（虽然是用虚幻的框架和接口）。下面我们就来一步一步在虚幻中敲一个自己的渲染器。我使用的环境是：4.19源码版引擎，windows10，vs2017社区版。我这里只是举个例子，有兴趣的美术也可以照着这个办法把各种自己常用的离线渲染器搬到引擎里。 

 

【第一步】定义一条新的渲染path 

首先第一件事情是我们需要定义一条我们自己的渲染路径，现在引擎有两条渲染路径，一条是Mobile的一条是deferred，并且它是根据渲染质量来决定的 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132728.jpeg)

所以我打算使用SM3_1这个等级作为我们渲染器的使用等级，所以我把这个函数改为了下面这个样子,在SceneInterface.h中 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132725.jpeg)

 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132721.jpeg)

使用SM4或者SM5的话会多需要考虑可见性剔除的东西。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132717.jpeg)

如果我们写forward但是又用到了上面这部分分支的代码的话，ViewInfo在析构的时候会出发断言。 

然后还要在SceneRenderTargets.h里加上自己的渲染路径所对应的RT格式 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132713.jpeg)

【第二步】自定义渲染器 

然后再到SceneRendering.h中加入声明一个我们的渲染器 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132709.jpeg)

在创建渲染器的地方new它 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132705.jpeg)

【第三步】 

我们在引擎的Render模块里新建一个MyRenderer.cpp，然后到工程目录下ReGenerate一下工程，然后你将会看到： 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132701.jpeg)

然后在MyRenderer中敲入如下代码 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132655.jpeg)

【第四步】 

然后我们就可以点F5起引擎然后去泡杯茶啦。如果你电脑配置不太好，那就可以去泡两杯。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132652.jpeg)

推荐澳洲葵花蜜+绿茶。 

【第五步】 

打开引擎后切换到SM3 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132648.jpeg)

不出意外的话我们将只能看到上一个渲染器给我们留下的最后一帧画面。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132644.jpeg)

打个断点，的确引擎在跑我们的渲染器，不过现在Render函数啥也没干，所以什么也没有，接下来我们来完成Render函数。如果以后有面试官问你引擎的渲染顺序，现在我们可以从容不迫地告诉他，我们想先渲染啥就先渲染啥，因为一切渲染顺序都在我们的掌控之中。 

【第六步】完善Render函数 

下面我们就来完善这个Render函数，如果你之前有敲过软光栅渲染器或者是光线追踪渲染器的话，对下面的过程应该会很熟悉，如果没有也不必担心，我们一步一步来。 

经过刚才的步骤，现在我们使用了自己的渲染器但是此时RenderTarget上面显示的是上一个渲染器最后一帧的画面残留，我们想要渲染自己的东西，所以第一步是先把上一帧的残留给从我们的“画布”上清理掉 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132638.jpeg)

键入如下代码，我们将清理掉每帧的画面重新画新东西上去，当然我们这里什么也没画。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132634.jpeg)

为了更明显，我Clear一个蓝色上去，或者什么别的颜色。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132629.jpeg)

 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132625.jpeg)

记得包含头文件，因为我们这步只对views[0]做了操作，所以当有多个视口时就会出问题，不过暂时先不考虑这个问题啦。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132621.jpeg)

【第七步】初始化渲染参数 

现在我们有了一条非常简单的管线，那么下一步当然是该把模型拿进来渲染啦。为了这一步，我们需要模型数据，需要各种矩阵，需要各种设置渲染状态，还需要各种Shader，并且把前面说到的各种数据传到GPU里给Shader跑。这么多数据，这么多步骤应该如何开始着手渲染呢。 

其实可以把整个渲染想象成我们美术画原画的过程，稍微画过画的都应该清楚，绘画之前我们需要收集素材，参考（也就是前期准备过程）。同理我们在渲染一个场景之前我们需要准备各种资源。这个准备过程其实编辑器已经帮我们做了一大半了。编辑器把各种资源导入引擎，场景编辑器把各种模型资源，贴图材质全部组织好了，并且给场景了一个绘制列表。各种lightmap，可见性烘焙，全部都准备好了。材质编辑器把shader也给我们编译好了。下面就是需要我们把这些海量的资源取过来使用。 

首先我们要准备好我们的“画布”RenderTargets 

【第八步】渲染剔除 

在准备好画布以后，面对一个庞大的美术师搭建的世界我们需要把需要绘画的东西挑出来，不可能什么都画。山后面的村庄我们根本看不到，所以我们不应该先画村庄然后再画山把村庄覆盖掉，这不是多此一举么，所以我们需要一个剔除机制。现实生活中绘制的剔除很简单，我们看到了就是看到了，把它画下来，可是计算机可不知道这些，所以我们需要想个办法告诉它，你看到了它，你需要绘制它。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132617.jpeg)

我们在我们的渲染器中加一个InitViews函数来做这剔除这件事情，并且把最后需要绘制的图元收集出来。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132611.jpeg)

实现了InitViews之后，我们画面里依然什么都没有，我们目前只是决定了要画什么，还什么都没画呢。 

往场景里托一些模型进去然后再在View上打个断点我们可以看到 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132606.jpeg)

 



Views里面已经有了可见性信息。 

PreVisibilityFrameSetup(RHICmdList); 

ComputeViewVisibility(RHICmdList); 

PostVisibilityFrameSetup(ILCTaskData); 

这三个函数便是虚幻用于可见性剔除的函数了。它包括几部分：视锥体剔除，距离剔除，可见性剔除。可见性剔除又包含于预烘焙可见性剔除。 

首先视锥体剔除会把摄像机范围外的物体全部剔除掉 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132454.jpeg)

 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132448.jpeg)

然后是可见性剔除，会把看不到的物体剔除掉 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132442.jpeg)

距离剔除可以选择一个距离区间，剔除掉物体。过远或者过近的物体都可以被剔除掉。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132435.jpeg)

可见性剔除完以后，View里面的这些可见性表格就会被填充了，在绘制的时候我们就可以不需要去绘制那些看不见的物体了。 

【第九步】设置渲染目标 

设置渲染管线 

现在我们需要配置渲染管线，比如RenderTraget，顶点索引缓冲，视口等等 

// Dynamic vertex and index buffers need to be committed before rendering. 
	FGlobalDynamicVertexBuffer::Get().Commit(); 
	FGlobalDynamicIndexBuffer::Get().Commit(); 
 

UpdateViewCustomData(); 
 

GRenderTargetPool.VisualizeTexture.OnStartFrame(Views[0]); 
 

FViewInfo& View = Views[0]; 
 

//视口列表 
	TArray<const FViewInfo*> ViewList; 
	for (int32 ViewIndex = 0; ViewIndex < Views.Num(); ViewIndex++) 
	{ 
		if (Views[ViewIndex].StereoPass != eSSP_MONOSCOPIC_EYE) 
		{ 
			ViewList.Add(&Views[ViewIndex]); 
		} 
	} 
 

FTextureRHIParamRef SceneColor = nullptr; 
	//获取到BackBuffer然后把它Set到渲染管线 
	SceneColor = GetMultiViewSceneColor(SceneContext); 
 	const FTextureRHIParamRef SceneDepth = (View.bIsMobileMultiViewEnabled)  ?  SceneContext.MobileMultiViewSceneDepthZ->GetRenderTargetItem().TargetableTexture  :  static_cast<FTextureRHIRef>(SceneContext.GetSceneDepthTexture()); 
	SetRenderTarget(RHICmdList, SceneColor, SceneDepth, ESimpleRenderTargetMode::EClearColorAndDepth); 
 

【第十步】快速渲染BasePass 

这一步就是渲染BasePass，我们把模型渲染到BackBuffer上。为了快速得到效果，这里暂时使用Mobile管线的BasePass渲染函数。 

![](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132427.jpeg)

 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132422.jpeg)

 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132416.jpeg)

最后： 

这时我的代码是这样的： 

SceneInterface.h 

class FMySceneRenderer : public FMobileSceneRenderer 
{ 
public: 
 

FMySceneRenderer(const FSceneViewFamily* InViewFamily, FHitProxyConsumer* HitProxyConsumer); 
 

// FSceneRenderer interface 
	virtual void Render(FRHICommandListImmediate& RHICmdList) override; 
 

protected: 
 

void InitViews(FRHICommandListImmediate& RHICmdList); 
}; 
 

SceneRenderTargets.h 

ESceneColorFormatType GetSceneColorFormatType() const 
	{ 
		if (CurrentShadingPath == EShadingPath::Mobile) 
		{ 
			return ESceneColorFormatType::Mobile; 
		} 
 		else if (CurrentShadingPath == EShadingPath::Deferred &&  (bRequireSceneColorAlpha || GetSceneColorFormat() == PF_FloatRGBA)) 
		{ 
			return ESceneColorFormatType::HighEndWithAlpha; 
		} 
		else if (CurrentShadingPath == EShadingPath::Deferred && !bRequireSceneColorAlpha) 
		{ 
			return ESceneColorFormatType::HighEnd; 
		} 
 

//给自己的渲染path加上对应的渲染格式 
 		else if (CurrentShadingPath ==EShadingPath::MyRenderPath &&  (bRequireSceneColorAlpha || GetSceneColorFormat() == PF_FloatRGBA)) 
		{ 
			return ESceneColorFormatType::HighEndWithAlpha; 
		} 
		else if (CurrentShadingPath == EShadingPath::MyRenderPath && !bRequireSceneColorAlpha) 
		{ 
			return ESceneColorFormatType::HighEnd; 
		} 
 

check(0); 
		return ESceneColorFormatType::Num; 
	} 
 

MyRenderer.cpp 

\#include "SceneRendering.h" 
\#include "ClearQuad.h" 
\#include "ScenePrivate.h" 
 

\#include "CoreMinimal.h" 
\#include "Stats/Stats.h" 
\#include "Misc/MemStack.h" 
\#include "HAL/IConsoleManager.h" 
\#include "EngineGlobals.h" 
\#include "RHIDefinitions.h" 
\#include "RHI.h" 
\#include "RenderResource.h" 
\#include "RendererInterface.h" 
\#include "SceneUtils.h" 
\#include "UniformBuffer.h" 
\#include "Engine/BlendableInterface.h" 
\#include "ShaderParameters.h" 
\#include "RHIStaticStates.h" 
\#include "Shader.h" 
\#include "StaticBoundShaderState.h" 
\#include "PostProcess/SceneRenderTargets.h" 
\#include "GlobalShader.h" 
\#include "PostProcess/SceneFilterRendering.h" 
\#include "FXSystem.h" 
\#include "PostProcess/RenderingCompositionGraph.h" 
\#include "PostProcess/PostProcessing.h" 
\#include "PostProcess/PostProcessMobile.h" 
\#include "PostProcess/PostProcessUpscale.h" 
\#include "PostProcess/PostProcessCompositeEditorPrimitives.h" 
\#include "PostProcess/PostProcessHMD.h" 
\#include "IHeadMountedDisplay.h" 
\#include "IXRTrackingSystem.h" 
\#include "SceneViewExtension.h" 
\#include "ScreenRendering.h" 
\#include "PipelineStateCache.h" 
\#include "MobileSeparateTranslucencyPass.h" 
 

uint32 GetShadowQuality(); 
 

static TAutoConsoleVariable<int32> CVarMobileAlwaysResolveDepth( 
	TEXT("r.Mobile.AlwaysResolveDepth"), 
	0, 
	TEXT("0: Depth buffer is resolved after opaque pass only when decals or modulated shadows are in use. (Default)\n") 
	TEXT("1: Depth buffer is always resolved after opaque pass.\n"), 
	ECVF_Scalability | ECVF_RenderThreadSafe); 
 

static TAutoConsoleVariable<int32> CVarMobileForceDepthResolve( 
	TEXT("r.Mobile.ForceDepthResolve"), 
	0, 
	TEXT("0: Depth buffer is resolved by switching out render targets. (Default)\n") 
	TEXT("1: Depth buffer is resolved by switching out render targets and drawing with the depth texture.\n"), 
	ECVF_Scalability | ECVF_RenderThreadSafe); 
 

FMySceneRenderer::FMySceneRenderer(const FSceneViewFamily* InViewFamily, FHitProxyConsumer* HitProxyConsumer) 
	: FMobileSceneRenderer(InViewFamily, HitProxyConsumer) 
{ 
 

} 
 

void FMySceneRenderer::Render(FRHICommandListImmediate& RHICmdList) 
{ 
	//调整视口 
	PrepareViewRectsForRendering(); 
 

//统计使用 
	QUICK_SCOPE_CYCLE_COUNTER(STAT_FMySceneRenderer_Render); 
 

if (!ViewFamily.EngineShowFlags.Rendering) 
	{ 
		return; 
	} 
 

//获取渲染级别 
	const ERHIFeatureLevel::Type ViewFeatureLevel = ViewFamily.GetFeatureLevel(); 
 

//初始化并获取系统全局的渲染纹理 
	GSystemTextures.InitializeTextures(RHICmdList, ViewFeatureLevel); 
	FSceneRenderTargets& SceneContext = FSceneRenderTargets::Get(RHICmdList); 
 

//为当前视图系列分配最大场景渲染目标空间 
	SceneContext.Allocate(RHICmdList, this); 
 

//保证需要使用到的RenderTarget全部是可写入的 
	GRenderTargetPool.TransitionTargetsWritable(RHICmdList); 
 

// Find the visible primitives. 
	FMobileSceneRenderer::InitViews(RHICmdList); 
 

if (IsRunningRHIInSeparateThread()) 
	{ 
		// we will probably stall on occlusion queries, so might as well have the RHI thread and GPU work while we wait. 
		// Also when doing RHI thread this is the only spot that will process pending deletes 
		FRHICommandListExecutor::GetImmediateCommandList().ImmediateFlush(EImmediateFlushType::FlushRHIThreadFlushResources); 
	} 
 

// Dynamic vertex and index buffers need to be committed before rendering. 
	FGlobalDynamicVertexBuffer::Get().Commit(); 
	FGlobalDynamicIndexBuffer::Get().Commit(); 
 

UpdateViewCustomData(); 
 

GRenderTargetPool.VisualizeTexture.OnStartFrame(Views[0]); 
 

FViewInfo& View = Views[0]; 
 

//视口列表 
	TArray<const FViewInfo*> ViewList; 
	for (int32 ViewIndex = 0; ViewIndex < Views.Num(); ViewIndex++) 
	{ 
		if (Views[ViewIndex].StereoPass != eSSP_MONOSCOPIC_EYE) 
		{ 
			ViewList.Add(&Views[ViewIndex]); 
		} 
	} 
 

FTextureRHIParamRef SceneColor = nullptr; 
	//获取到BackBuffer然后把它Set到渲染管线 
	SceneColor = GetMultiViewSceneColor(SceneContext); 
 	const FTextureRHIParamRef SceneDepth = (View.bIsMobileMultiViewEnabled)  ?  SceneContext.MobileMultiViewSceneDepthZ->GetRenderTargetItem().TargetableTexture  :  static_cast<FTextureRHIRef>(SceneContext.GetSceneDepthTexture()); 
	SetRenderTarget(RHICmdList, SceneColor, SceneDepth, ESimpleRenderTargetMode::EClearColorAndDepth); 
 

//清理BackBuffer为青色 
	if (GIsEditor && !View.bIsSceneCapture) 
	{ 
		DrawClearQuad(RHICmdList, FLinearColor(0.5, 0.8, 0.7, 1.0)); 
	} 
 

//渲染BasePass 
	RenderMobileBasePass(RHICmdList, ViewList); 
 

for (int32 ViewExt = 0; ViewExt < ViewFamily.ViewExtensions.Num(); ++ViewExt) 
	{ 
		for (int32 ViewIndex = 0; ViewIndex < ViewFamily.Views.Num(); ++ViewIndex) 
		{ 
			ViewFamily.ViewExtensions[ViewExt]->PostRenderMobileBasePass_RenderThread(RHICmdList, Views[ViewIndex]); 
		} 
	} 
 

// Make a copy of the scene depth if the current hardware doesn't support reading and writing to the same depth buffer 
	ConditionalResolveSceneDepth(RHICmdList, View); 
 

if (ViewFamily.IsMonoscopicFarFieldEnabled() && ViewFamily.Views.Num() == 3) 
	{ 
		TArray<const FViewInfo*> MonoViewList; 
		MonoViewList.Add(&Views[2]); 
 

RenderMonoscopicFarFieldMask(RHICmdList); 
		RenderMobileBasePass(RHICmdList, MonoViewList); 
		RenderTranslucency(RHICmdList, MonoViewList); 
		CompositeMonoscopicFarField(RHICmdList); 
	} 
 

if (!View.bIsMobileMultiViewDirectEnabled) 
	{ 
		CopyMobileMultiViewSceneColor(RHICmdList); 
	} 
 

RenderFinish(RHICmdList); 
} 
 

void FMySceneRenderer::InitViews(FRHICommandListImmediate& RHICmdList) 
{ 
	SCOPED_DRAW_EVENT(RHICmdList, InitViews) 
 

SCOPE_CYCLE_COUNTER(STAT_InitViewsTime); 
 

FILCUpdatePrimTaskData ILCTaskData; 
	PreVisibilityFrameSetup(RHICmdList); 
	ComputeViewVisibility(RHICmdList); 
	PostVisibilityFrameSetup(ILCTaskData); 
 

const bool bDynamicShadows = ViewFamily.EngineShowFlags.DynamicShadows; 
	if (bDynamicShadows && !IsSimpleForwardShadingEnabled(GetFeatureLevelShaderPlatform(FeatureLevel))) 
	{ 
		InitDynamicShadows(RHICmdList); 
	} 
 

for (int32 ViewIndex = 0; ViewIndex < Views.Num(); ViewIndex++) 
	{ 
		FViewInfo& View = Views[ViewIndex]; 
		View.InitRHIResources(); 
	} 
 

OnStartFrame(RHICmdList); 
} 
 

至此我们初步搭建了一个我们自己的渲染器（算是吧），但是很多函数和功能是用Mobile管线的，后面的章节将逐步实现我们自己的版本，替代掉引擎自己的。 

什么？客户端业务逻辑？去做个小游戏放松一下。 

![img](UnrealCustomPipeLine_01.assets/Thu, 08 Aug 2019 132403.jpeg)

Enjoy it ！ 

 