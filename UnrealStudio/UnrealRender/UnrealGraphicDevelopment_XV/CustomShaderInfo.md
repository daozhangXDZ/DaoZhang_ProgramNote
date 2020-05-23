# 虚幻4渲染编程(Shader篇)【第三卷：第二卷代码解释】



这一节就是在解释第二卷的代码的。可以先看看我第二卷的文章

## **（声明一下，图片的水印是因为这个博客是直接从我的CSDN搬过来的，我不打算继续在CSDN写文章了所以打算搬到知乎来）**

虚幻4有一篇教你怎么写globalshader的文档，但是我看了一遍后，感觉还是没说核心原理，只是教你怎么复制粘贴。下面就用我们上一节的例子（约三百多行代码）来窥探一下虚幻的渲染流程。例子虽然只有300多行代码，但是麻雀虽小五脏俱全。引擎的fog啦，后期啦，都是globalshader写的。

首先来看一下ShadertestPlugin.Build.cs文件。

```
// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.  
 
using UnrealBuildTool;  
 
public class ShadertestPlugin : ModuleRules  
{  
    public ShadertestPlugin(ReadOnlyTargetRules Target) : base(Target)  
    {  
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;  
 
        PublicIncludePaths.AddRange(  
            new string[] {  
                "ShadertestPlugin/Public"  
                // ... add public include paths required here ...  
            }  
            );  
 
 
        PrivateIncludePaths.AddRange(  
            new string[] {  
                "ShadertestPlugin/Private",  
                // ... add other private include paths required here ...  
            }  
            );  
 
 
        PublicDependencyModuleNames.AddRange(  
            new string[]  
            {  
                "Core",  
                "CoreUObject",  
                "Engine",  
                "RHI",  
                "Engine",  
                "RenderCore",  
                "ShaderCore",  
                // ... add other public dependencies that you statically link with here ...  
            }  
            );  
 
 
        PrivateDependencyModuleNames.AddRange(  
            new string[]  
            {  
                "CoreUObject",  
                "Engine",  
                "Slate",  
                "SlateCore",  
                // ... add private dependencies that you statically link with here ...    
            }  
            );  
 
 
        DynamicallyLoadedModuleNames.AddRange(  
            new string[]  
            {  
                // ... add any modules that your module loads dynamically here ...  
            }  
            );  
    }  
}  
// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class ShadertestPlugin : ModuleRules
{
	public ShadertestPlugin(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
 
		PublicIncludePaths.AddRange(
			new string[] {
				"ShadertestPlugin/Public"
				// ... add public include paths required here ...
			}
			);
 
 
		PrivateIncludePaths.AddRange(
			new string[] {
				"ShadertestPlugin/Private",
				// ... add other private include paths required here ...
			}
			);
 
 
		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
                "CoreUObject",
                "Engine",
                "RHI",
                "Engine",
                "RenderCore",
                "ShaderCore",
				// ... add other public dependencies that you statically link with here ...
			}
			);
 
 
		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"CoreUObject",
				"Engine",
				"Slate",
				"SlateCore",
				// ... add private dependencies that you statically link with here ...	
			}
			);
 
 
		DynamicallyLoadedModuleNames.AddRange(
			new string[]
			{
				// ... add any modules that your module loads dynamically here ...
			}
			);
	}
}
```

这个文件主要是用来做路径配置的，和你需要增加的模块。只有这里引入了模块我们才能在头文件中include他们。虚幻这是在c++中实现了c#的模块编程的思路。需要什么功能，在这里写进来，不需要就不写。不禁感叹虚幻的牛逼。

下面再来看看ShadertestPlugin.uplugin，这个文件是一个配置文件，描述了我们插件的一些信息和最关键的加载顺序LoadingPhase.



可以去查一下LoadingPhase还有其他的。



看完这些之后，我们还需要再关注三个文件





我们先来看看MyShader.usf



一个是顶点着色器一个是像素着色器。还有声明了一个shader的float4变量。像素着色器和顶点着色器做的事情很简单，就是输出一个简单的颜色和位置。

最顶上那个#include "/Engine/Public/Platform.ush"可以不用包含的。如果你在shader中



这个ShouldCompilePermutation函数如果有判断平台的话，那么你就需要加上这个include了。

下面再来看看MyShaderTest.h



其实这个就是一个静态函数库，我们之所以能在蓝图脚本中调用这个函数就是因为这个是个静态函数库。为蓝图提供了一个直接调用的方法。



这个函数做的事情就是帮我们从蓝图脚本里传了一些数据到我们的shader里。

接下来看最重要的MyShaderTest.cpp文件了



首先包含了我们需要的头文件。这些头文件是因为我们在c#中引入了他们所在的模块我们才能include的。不然这些include操作都是非法的。



接下来是引入我们的自定义命名空间。对应的，在这个cpp文件的最末尾，必须配对一个end操作



接下来是蓝图函数库的构造函数。这里面什么也不需要写。





然后就是我们的shader类了

```
class FMyShaderTest : public FGlobalShader  
{  
public:  
 
    FMyShaderTest(){}  
 
    FMyShaderTest(const ShaderMetaType::CompiledShaderInitializerType& Initializer)  
        : FGlobalShader(Initializer)  
    {  
        SimpleColorVal.Bind(Initializer.ParameterMap, TEXT("SimpleColor"));  
    }  
 
    static bool ShouldCache(EShaderPlatform Platform)  
    {  
        return true;  
    }  
 
    static bool ShouldCompilePermutation(const FGlobalShaderPermutationParameters& Parameters)  
    {  
        //return IsFeatureLevelSupported(Parameters.Platform, ERHIFeatureLevel::SM4);  
        return true;  
    }  
 
    static void ModifyCompilationEnvironment(const FGlobalShaderPermutationParameters& Parameters, FShaderCompilerEnvironment& OutEnvironment)  
    {  
        FGlobalShader::ModifyCompilationEnvironment(Parameters, OutEnvironment);  
        OutEnvironment.SetDefine(TEXT("TEST_MICRO"), 1);  
    }  
 
    void SetParameters(  
        FRHICommandListImmediate& RHICmdList,  
        const FLinearColor &MyColor  
        )  
    {  
        SetShaderValue(RHICmdList, GetPixelShader(), SimpleColorVal, MyColor);  
    }  
 
    virtual bool Serialize(FArchive& Ar) override  
    {  
        bool bShaderHasOutdatedParameters = FGlobalShader::Serialize(Ar);  
        Ar << SimpleColorVal;  
        return bShaderHasOutdatedParameters;  
    }  
 
private:  
 
    FShaderParameter SimpleColorVal;  
 
};  
class FMyShaderTest : public FGlobalShader
{
public:

	FMyShaderTest(){}

	FMyShaderTest(const ShaderMetaType::CompiledShaderInitializerType& Initializer)
		: FGlobalShader(Initializer)
	{
		SimpleColorVal.Bind(Initializer.ParameterMap, TEXT("SimpleColor"));
	}

	static bool ShouldCache(EShaderPlatform Platform)
	{
		return true;
	}

	static bool ShouldCompilePermutation(const FGlobalShaderPermutationParameters& Parameters)
	{
		//return IsFeatureLevelSupported(Parameters.Platform, ERHIFeatureLevel::SM4);
		return true;
	}

	static void ModifyCompilationEnvironment(const FGlobalShaderPermutationParameters& Parameters, FShaderCompilerEnvironment& OutEnvironment)
	{
		FGlobalShader::ModifyCompilationEnvironment(Parameters, OutEnvironment);
		OutEnvironment.SetDefine(TEXT("TEST_MICRO"), 1);
	}

	void SetParameters(
		FRHICommandListImmediate& RHICmdList,
		const FLinearColor &MyColor
		)
	{
		SetShaderValue(RHICmdList, GetPixelShader(), SimpleColorVal, MyColor);
	}

	virtual bool Serialize(FArchive& Ar) override
	{
		bool bShaderHasOutdatedParameters = FGlobalShader::Serialize(Ar);
		Ar << SimpleColorVal;
		return bShaderHasOutdatedParameters;
	}

private:

	FShaderParameter SimpleColorVal;

};
```

其中有几个函数



shader类的默认构造函数和构造函数。在构造函数中，我们用bind方法把shader的私有成员变量SimpleColorVal和shader中的变量float4 SimpleColor做了绑定。



然后是者三个函数：



这三个函数的作用分别是：

static bool ShouldCache(EShaderPlatform Platform)主要是作用如下





对于这个函数 ModifyCompilationEnvironment，如果是看过我前面加shadingmode的博客的话就不会陌生了。它可以把宏塞进shader里。



SetParameters这个函数是自己定义的，你可以随便怎么给它命名。它的作用是把我们的颜色信息传到shader里。我们直接set



这个私有变量即可。它在构造函数的时候和shader的变量绑定了的。



这个函数就是序列化了，这个没啥好说的，如果不懂可以去看知乎上的关于虚幻序列化和反序列化的文章。可以理解为虚幻怎么从磁盘读取二进制数据。我们的shader是一个文件（敲过渲染器的化就应该知道这一点啦）。如果不清楚的话可以直接跳过它，毕竟虚幻的这套机制又是一个庞大的话题了。

然后是我们的VS和PS



这两个类里都没什么内容，主要是我们把代码都写FMyShaderTest里了。这样方便不用再写一次。这也是FMyShaderTest类存在的目的。当然你让PS和VS都继承自globalshader也是没问题的。



这个宏会帮我们把我们的shader加入到全局的shadermap中，这也是虚幻能识别到我们的shader然后编译它的关键。这个宏帮我们做了很多事情，反正总的来说就是让虚幻知道了，哦！这里有个shader，我要编译它，我要用它来做渲染啥的。如果你想深入了解，可以跟进去看看。



然后是这么两个宏。它的作用就是把shader文件和我们shader类绑定起来，然后指认它是什么shader，shader对应的HLSL入口代码是哪里。大概就是这么一个作用。

最后就是这两个函数了：





DrawTestShaderRenderTarget是MyShaderTest.h里蓝图函数库的实现，是逻辑线程这边调用draw方法的部分。



在这个函数中，我们首先判断，是不是逻辑线程在调用它，然后判断一下我们从蓝图输入的资源那个RT是不是空的，其实这里还应该判断一下Ac是不是空的。

然后获取到这个rendertarget在渲染线程的渲染资源。然后获取FeatureLevel。写过DX的设备初始化的话就对这个FeatureLevelhen会很熟悉了，这里就不赘述了，如果不清楚，就去百度搜dxd11设备初始化吧。

最后就是调用ENQUEUE_RENDER_COMMAND这个宏了。这个宏会向渲染线程压入一个渲染命令，调用我们在渲染线程的

DrawTestShaderRenderTarget_RenderThread方法。如果不清楚这里的语法的，去看一下c++的lambda表达式吧。



完成这里之后，就会调用我们渲染线程的DrawTestShaderRenderTarget_RenderThread函数了。

```
static void DrawTestShaderRenderTarget_RenderThread(  
    FRHICommandListImmediate& RHICmdList,   
    FTextureRenderTargetResource* OutputRenderTargetResource,  
    ERHIFeatureLevel::Type FeatureLevel,  
    FName TextureRenderTargetName,  
    FLinearColor MyColor  
)  
{  
    check(IsInRenderingThread());  
 
#if WANTS_DRAW_MESH_EVENTS  
    FString EventName;  
    TextureRenderTargetName.ToString(EventName);  
    SCOPED_DRAW_EVENTF(RHICmdList, SceneCapture, TEXT("ShaderTest %s"), *EventName);  
#else  
    SCOPED_DRAW_EVENT(RHICmdList, DrawUVDisplacementToRenderTarget_RenderThread);  
#endif  
 
    //设置渲染目标  
    SetRenderTarget(  
        RHICmdList,  
        OutputRenderTargetResource->GetRenderTargetTexture(),  
        FTextureRHIRef(),  
        ESimpleRenderTargetMode::EUninitializedColorAndDepth,  
        FExclusiveDepthStencil::DepthNop_StencilNop  
    );  
 
    //设置视口  
    //FIntPoint DrawTargetResolution(OutputRenderTargetResource->GetSizeX(), OutputRenderTargetResource->GetSizeY());  
    //RHICmdList.SetViewport(0, 0, 0.0f, DrawTargetResolution.X, DrawTargetResolution.Y, 1.0f);  
 
    TShaderMap<FGlobalShaderType>* GlobalShaderMap = GetGlobalShaderMap(FeatureLevel);  
    TShaderMapRef<FShaderTestVS> VertexShader(GlobalShaderMap);  
    TShaderMapRef<FShaderTestPS> PixelShader(GlobalShaderMap);  
 
    // Set the graphic pipeline state.  
    FGraphicsPipelineStateInitializer GraphicsPSOInit;  
    RHICmdList.ApplyCachedRenderTargets(GraphicsPSOInit);  
    GraphicsPSOInit.DepthStencilState = TStaticDepthStencilState<false, CF_Always>::GetRHI();  
    GraphicsPSOInit.BlendState = TStaticBlendState<>::GetRHI();  
    GraphicsPSOInit.RasterizerState = TStaticRasterizerState<>::GetRHI();  
    GraphicsPSOInit.PrimitiveType = PT_TriangleList;  
    GraphicsPSOInit.BoundShaderState.VertexDeclarationRHI = GetVertexDeclarationFVector4();  
    GraphicsPSOInit.BoundShaderState.VertexShaderRHI = GETSAFERHISHADER_VERTEX(*VertexShader);  
    GraphicsPSOInit.BoundShaderState.PixelShaderRHI = GETSAFERHISHADER_PIXEL(*PixelShader);  
    SetGraphicsPipelineState(RHICmdList, GraphicsPSOInit);  
 
    //RHICmdList.SetViewport(0, 0, 0.0f, DrawTargetResolution.X, DrawTargetResolution.Y, 1.0f);  
    PixelShader->SetParameters(RHICmdList, MyColor);  
 
    // Draw grid.  
    //uint32 PrimitiveCount = 2;  
    //RHICmdList.DrawPrimitive(PT_TriangleList, 0, PrimitiveCount, 1);  
    FVector4 Vertices[4];  
    Vertices[0].Set(-1.0f, 1.0f, 0, 1.0f);  
    Vertices[1].Set(1.0f, 1.0f, 0, 1.0f);  
    Vertices[2].Set(-1.0f, -1.0f, 0, 1.0f);  
    Vertices[3].Set(1.0f, -1.0f, 0, 1.0f);  
    static const uint16 Indices[6] =  
    {  
        0, 1, 2,  
        0, 2, 3  
    };  
    //DrawPrimitiveUP(RHICmdList, PT_TriangleStrip, 2, Vertices, sizeof(Vertices[0]));  
    DrawIndexedPrimitiveUP(  
        RHICmdList,  
        PT_TriangleList,  
        0,  
        ARRAY_COUNT(Vertices),  
        2,  
        Indices,  
        sizeof(Indices[0]),  
        Vertices,  
        sizeof(Vertices[0])  
    );  
 
    // Resolve render target.  
    RHICmdList.CopyToResolveTarget(  
        OutputRenderTargetResource->GetRenderTargetTexture(),  
        OutputRenderTargetResource->TextureRHI,  
        false, FResolveParams());  
}  
static void DrawTestShaderRenderTarget_RenderThread(
	FRHICommandListImmediate& RHICmdList, 
	FTextureRenderTargetResource* OutputRenderTargetResource,
	ERHIFeatureLevel::Type FeatureLevel,
	FName TextureRenderTargetName,
	FLinearColor MyColor
)
{
	check(IsInRenderingThread());

#if WANTS_DRAW_MESH_EVENTS
	FString EventName;
	TextureRenderTargetName.ToString(EventName);
	SCOPED_DRAW_EVENTF(RHICmdList, SceneCapture, TEXT("ShaderTest %s"), *EventName);
#else
	SCOPED_DRAW_EVENT(RHICmdList, DrawUVDisplacementToRenderTarget_RenderThread);
#endif

	//设置渲染目标
	SetRenderTarget(
		RHICmdList,
		OutputRenderTargetResource->GetRenderTargetTexture(),
		FTextureRHIRef(),
		ESimpleRenderTargetMode::EUninitializedColorAndDepth,
		FExclusiveDepthStencil::DepthNop_StencilNop
	);

	//设置视口
	//FIntPoint DrawTargetResolution(OutputRenderTargetResource->GetSizeX(), OutputRenderTargetResource->GetSizeY());
	//RHICmdList.SetViewport(0, 0, 0.0f, DrawTargetResolution.X, DrawTargetResolution.Y, 1.0f);

	TShaderMap<FGlobalShaderType>* GlobalShaderMap = GetGlobalShaderMap(FeatureLevel);
	TShaderMapRef<FShaderTestVS> VertexShader(GlobalShaderMap);
	TShaderMapRef<FShaderTestPS> PixelShader(GlobalShaderMap);

	// Set the graphic pipeline state.
	FGraphicsPipelineStateInitializer GraphicsPSOInit;
	RHICmdList.ApplyCachedRenderTargets(GraphicsPSOInit);
	GraphicsPSOInit.DepthStencilState = TStaticDepthStencilState<false, CF_Always>::GetRHI();
	GraphicsPSOInit.BlendState = TStaticBlendState<>::GetRHI();
	GraphicsPSOInit.RasterizerState = TStaticRasterizerState<>::GetRHI();
	GraphicsPSOInit.PrimitiveType = PT_TriangleList;
	GraphicsPSOInit.BoundShaderState.VertexDeclarationRHI = GetVertexDeclarationFVector4();
	GraphicsPSOInit.BoundShaderState.VertexShaderRHI = GETSAFERHISHADER_VERTEX(*VertexShader);
	GraphicsPSOInit.BoundShaderState.PixelShaderRHI = GETSAFERHISHADER_PIXEL(*PixelShader);
	SetGraphicsPipelineState(RHICmdList, GraphicsPSOInit);

	//RHICmdList.SetViewport(0, 0, 0.0f, DrawTargetResolution.X, DrawTargetResolution.Y, 1.0f);
	PixelShader->SetParameters(RHICmdList, MyColor);

	// Draw grid.
	//uint32 PrimitiveCount = 2;
	//RHICmdList.DrawPrimitive(PT_TriangleList, 0, PrimitiveCount, 1);
	FVector4 Vertices[4];
	Vertices[0].Set(-1.0f, 1.0f, 0, 1.0f);
	Vertices[1].Set(1.0f, 1.0f, 0, 1.0f);
	Vertices[2].Set(-1.0f, -1.0f, 0, 1.0f);
	Vertices[3].Set(1.0f, -1.0f, 0, 1.0f);
	static const uint16 Indices[6] =
	{
		0, 1, 2,
		0, 2, 3
	};
	//DrawPrimitiveUP(RHICmdList, PT_TriangleStrip, 2, Vertices, sizeof(Vertices[0]));
	DrawIndexedPrimitiveUP(
		RHICmdList,
		PT_TriangleList,
		0,
		ARRAY_COUNT(Vertices),
		2,
		Indices,
		sizeof(Indices[0]),
		Vertices,
		sizeof(Vertices[0])
	);

	// Resolve render target.
	RHICmdList.CopyToResolveTarget(
		OutputRenderTargetResource->GetRenderTargetTexture(),
		OutputRenderTargetResource->TextureRHI,
		false, FResolveParams());
}
```

还是先判断一下线程



然后就是设置渲染目标设置视口，设置管线的状态这些老生常谈的东西了。



这里是向shader里传值了。



这里就是实际的绘制了，会传入顶点和索引。这里DrawIndexedPrimitiveUP会从面片的顶端架一台摄像机然后拍这个面片然后把拍到的信息存到RT上



最后一步就是把渲染的RT拷贝到我们传入的那张RT上。

如果你发现拍出来的形状不对，请把Indices改一下



这个是错的。

改成



这样！！

至此第二卷的代码讲解就完成啦。后面我们会继续我们的探索之旅。

## **关于UE的Shader虚拟路径**

UE在4.21之后对于Shader的路径做了一些修改，导致之前的虚拟路径的写法会报错。



比如：

```
IMPLEMENT_SHADER_TYPE(, FVolumeCSShader, TEXT("/Plugin/VolumetricClouds/Private/VolumeCloudSky.usf"), TEXT("MainCS"), SF_Compute)
```

如果直接这么写的话4.21后的版本直接就过不了编译了。所以我研究了下UE的虚拟路径系统。

首先找到GetShaderSourceFilePath函数。这里便是在把我们的虚拟路径映射成真实路径的地方。



而在这个过程中会用到GShaderSourceDirectoryMappings。在4.21及之后这个Directory Mappings需要自己初始化。从此以后再也不需要为虚拟路径的写法烦恼了。



可能这么说有点抽象，我举个例子吧：

我如果把虚拟路径的名字写夸张点





点下F5后依然能完美运行！



其实4.21相对于4.20这一点实际上是个进步，我们能自己定义Shader的虚拟路径了。

Enjoy it !
