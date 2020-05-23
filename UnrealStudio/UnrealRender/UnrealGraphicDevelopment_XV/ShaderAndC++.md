# 虚幻4渲染编程(Shader篇)【第四卷：虚幻4C++层和Shader层的简单数据通讯】

文章

本章将会在前几张的基础上进行讲解，如果你没看过前几章的话建议先看下虚幻4渲染编程（shader篇）的前几篇的内容

先上效果图如下。我们在虚幻里实现了自己的shader的贴图映射。



![img](https://pic2.zhimg.com/v2-6b11ab22f9a04ac80234b0e8fc635da9_r.jpg)

为啥我们要这么麻烦敲代码做这些事情，而不是直接用虚幻的材质编辑器呢。因为这是为我们自己定制我们自己的shader管线做准备！

经过前几卷的探索，我们现在已经可以通过自己的shader和Draw调用，在一个RenderTarget上绘制东西了。虽然最后还是通过材质编辑器才传到场景的render  target上，不过随着“旅行”的进行，我们揭开的谜团越来越多了。下一步我们将一起来向shader传入更多数据来完成一些更复杂的绘制。

​    我们现在只有一个颜色，我们来尝试一下把一张贴图传入shader吧。如果一个shader需要采一张贴图，需要一个Texture资源，需要一个sampler，还需要UV信息。我们先在HLSL代码里做如下工作：

```
#include "/Engine/Public/Platform.ush"  
Texture2D MyTexture;  
SamplerState MyTextureSampler;  
  
float4 SimpleColor;  
  
void MainVS(  
    in float4 InPosition : ATTRIBUTE0,  
    in float2 InUV : ATTRIBUTE1,  
    out float2 OutUV : TEXCOORD0,  
    out float4 OutPosition : SV_POSITION  
    )  
{  
    // screenspace position from vb  
    OutPosition = InPosition;  
    OutUV = InUV;  
  
}  
  
void MainPS(  
    in float2 UV : TEXCOORD0,  
    out float4 OutColor : SV_Target0  
    )  
{  
    OutColor = float4(MyTexture.Sample(MyTextureSampler, UV.xy).rgb, 1.0f);  
    OutColor *= SimpleColor;  
}  
```

我们给顶点着色器增加一个UV的输入输出，然后给像素着色器增加一个UV输入和一点简单的计算。因为加入了更多的顶点输入信息，所以我们要开始管理顶点输入布局了。



让我们定义一个顶点数据的结构体FMyTextureVertex，然后声明一个顶点输入布局类，在InitRHI种进行顶点输入布局的初始化。



虚幻自己实现了一个ATRIBUTE语义（HLSL并没有这个语义估计是虚幻自己实现的）。这个插槽和顶点输入布局的对应关系如上图所示。

​    完成了顶点输入布局后，下面我们需要把顶点输入布局给渲染管线。



完成指认后，我们需要把顶点UV数据传进draw函数，接下来



我们在原来的代码基础上增加了UV数据。至此UV数据算是完全完成了。下面我们来传贴图数据和sampler数据

首先在FMyShaderText类中加入新的成员变量



然后在构造函数把他们和shader里的变量绑定：



完成这个之后就是需要CPU端传渲染资源到GPU端了：



这里截图没截图完，不过不用担心，后面我会把所有代码再贴一遍，现在只需要关心的是再原有代码基础上的改动。主要是从UTexture中拿到渲染资源。

然后在渲染线程的函数中set一下即可：





至此整个代码就完成啦。再在蓝图脚本中完成资源指认即可。



至此完成了一个shader基本的需求。至于要传一些比较复杂的数据结构，如结构体buffer什么的，以后再作介绍。后面是完整的代码：

MyShader.usf

```
#include "/Engine/Public/Platform.ush"  
  
Texture2D MyTexture;  
SamplerState MyTextureSampler;  
  
float4 SimpleColor;  
  
void MainVS(  
    in float4 InPosition : ATTRIBUTE0,  
    in float2 InUV : ATTRIBUTE1,  
    out float2 OutUV : TEXCOORD0,  
    out float4 OutPosition : SV_POSITION  
    )  
{  
    // screenspace position from vb  
    OutPosition = InPosition;  
    OutUV = InUV;  
  
}  
  
void MainPS(  
    in float2 UV : TEXCOORD0,  
    out float4 OutColor : SV_Target0  
    )  
{  
    OutColor = float4(MyTexture.Sample(MyTextureSampler, UV.xy).rgb, 1.0f);  
    OutColor *= SimpleColor;  
}  
```

MyShaderTest.h(这里面的Struct是暂时没用的，以后介绍传复杂的buffer的时候会用到)

```
#pragma once  
  
#include "CoreMinimal.h"  
#include "UObject/ObjectMacros.h"  
#include "Classes/Kismet/BlueprintFunctionLibrary.h"  
#include "MyShaderTest.generated.h"  
  
USTRUCT(BlueprintType)  
struct FMyShaderStructData  
{  
    GENERATED_USTRUCT_BODY()  
  
    UPROPERTY(BlueprintReadWrite, VisibleAnywhere, Category = ShaderData)  
    FLinearColor ColorOne;  
    UPROPERTY(BlueprintReadWrite, VisibleAnywhere, Category = ShaderData)  
    FLinearColor ColorTwo;  
    UPROPERTY(BlueprintReadWrite, VisibleAnywhere, Category = ShaderData)  
    FLinearColor Colorthree;  
    UPROPERTY(BlueprintReadWrite, VisibleAnywhere, Category = ShaderData)  
    FLinearColor ColorFour;  
};  
  
UCLASS(MinimalAPI,meta = (ScriptName = "TestShaderLibary"))  
class UTestShaderBlueprintLibrary : public UBlueprintFunctionLibrary  
{  
    GENERATED_UCLASS_BODY()  
  
    UFUNCTION(BlueprintCallable, Category = "ShaderTestPlugin", meta = (WorldContext = "WorldContextObject"))  
    static void DrawTestShaderRenderTarget(class UTextureRenderTarget2D* OutputRenderTarget, AActor* Ac, FLinearColor MyColor, UTexture* MyTexture);  
};  
```

MyShader.cpp

```
// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.  
  
#include "MyShaderTest.h"  
  
#include "Classes/Engine/TextureRenderTarget2D.h"  
#include "Classes/Engine/World.h"  
#include "Public/GlobalShader.h"  
#include "Public/PipelineStateCache.h"  
#include "Public/RHIStaticStates.h"  
#include "Public/SceneUtils.h"  
#include "Public/SceneInterface.h"  
#include "Public/ShaderParameterUtils.h"  
#include "Public/Logging/MessageLog.h"  
#include "Public/Internationalization/Internationalization.h"  
#include "Public/StaticBoundShaderState.h"  
  
#include "RHICommandList.h"  
#include "UniformBuffer.h"  
  
#define LOCTEXT_NAMESPACE "TestShader"  
  
//BEGIN_UNIFORM_BUFFER_STRUCT(MyStructData, )  
//DECLARE_UNIFORM_BUFFER_STRUCT_MEMBER(FVector4, ColorOne)  
//DECLARE_UNIFORM_BUFFER_STRUCT_MEMBER(FVector4, ColorTwo)  
//DECLARE_UNIFORM_BUFFER_STRUCT_MEMBER(FVector4, ColorThree)  
//DECLARE_UNIFORM_BUFFER_STRUCT_MEMBER(FVector4, ColorFour)  
//END_UNIFORM_BUFFER_STRUCT(MyStructData)  
//typedef TUniformBufferRef<MyStructData> MyStructDataRef;  
  
UTestShaderBlueprintLibrary::UTestShaderBlueprintLibrary(const FObjectInitializer& ObjectInitializer)  
    : Super(ObjectInitializer)  
{  
  
}  
  
class FMyShaderTest : public FGlobalShader  
{  
public:  
  
    FMyShaderTest(){}  
  
    FMyShaderTest(const ShaderMetaType::CompiledShaderInitializerType& Initializer)  
        : FGlobalShader(Initializer)  
    {  
        SimpleColorVal.Bind(Initializer.ParameterMap, TEXT("SimpleColor"));  
        TestTextureVal.Bind(Initializer.ParameterMap, TEXT("MyTexture"));  
        TestTextureSampler.Bind(Initializer.ParameterMap, TEXT("MyTextureSampler"));  
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
        const FLinearColor &MyColor,  
        FTextureRHIParamRef &MyTexture  
        )  
    {  
        SetShaderValue(RHICmdList, GetPixelShader(), SimpleColorVal, MyColor);  
        SetTextureParameter(  
            RHICmdList,  
            GetPixelShader(),  
            TestTextureVal,  
            TestTextureSampler,  
            TStaticSamplerState<SF_Trilinear, AM_Clamp, AM_Clamp, AM_Clamp>::GetRHI(),  
            MyTexture);  
    }  
  
    virtual bool Serialize(FArchive& Ar) override  
    {  
        bool bShaderHasOutdatedParameters = FGlobalShader::Serialize(Ar);  
        Ar << SimpleColorVal << TestTextureVal;  
        return bShaderHasOutdatedParameters;  
    }  
  
private:  
  
    FShaderParameter SimpleColorVal;  
  
    FShaderResourceParameter TestTextureVal;  
    FShaderResourceParameter TestTextureSampler;  
  
};  
  
class FShaderTestVS : public FMyShaderTest  
{  
    DECLARE_SHADER_TYPE(FShaderTestVS, Global);  
  
public:  
    FShaderTestVS(){}  
  
    FShaderTestVS(const ShaderMetaType::CompiledShaderInitializerType& Initializer)  
        : FMyShaderTest(Initializer)  
    {  
  
    }  
};  
  
  
class FShaderTestPS : public FMyShaderTest  
{  
    DECLARE_SHADER_TYPE(FShaderTestPS, Global);  
  
public:  
    FShaderTestPS() {}  
  
    FShaderTestPS(const ShaderMetaType::CompiledShaderInitializerType& Initializer)  
        : FMyShaderTest(Initializer)  
    {  
  
    }  
};  
  
  
IMPLEMENT_SHADER_TYPE(, FShaderTestVS, TEXT("/Plugin/ShadertestPlugin/Private/MyShader.usf"), TEXT("MainVS"), SF_Vertex)  
IMPLEMENT_SHADER_TYPE(, FShaderTestPS, TEXT("/Plugin/ShadertestPlugin/Private/MyShader.usf"), TEXT("MainPS"), SF_Pixel)  
  
struct FMyTextureVertex  
{  
    FVector4    Position;  
    FVector2D   UV;  
};  
  
class FMyTextureVertexDeclaration : public FRenderResource  
{  
public:  
    FVertexDeclarationRHIRef VertexDeclarationRHI;  
  
    virtual void InitRHI() override  
    {  
        FVertexDeclarationElementList Elements;  
        uint32 Stride = sizeof(FMyTextureVertex);  
        Elements.Add(FVertexElement(0, STRUCT_OFFSET(FMyTextureVertex, Position), VET_Float4, 0, Stride));  
        Elements.Add(FVertexElement(0, STRUCT_OFFSET(FMyTextureVertex, UV), VET_Float2, 1, Stride));  
        VertexDeclarationRHI = RHICreateVertexDeclaration(Elements);  
    }  
  
    virtual void ReleaseRHI() override  
    {  
        VertexDeclarationRHI->Release();  
    }  
};  
  
static void DrawTestShaderRenderTarget_RenderThread(  
    FRHICommandListImmediate& RHICmdList,   
    FTextureRenderTargetResource* OutputRenderTargetResource,  
    ERHIFeatureLevel::Type FeatureLevel,  
    FName TextureRenderTargetName,  
    FLinearColor MyColor,  
    FTextureRHIParamRef MyTexture  
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
  
    FMyTextureVertexDeclaration VertexDec;  
    VertexDec.InitRHI();  
  
    // Set the graphic pipeline state.  
    FGraphicsPipelineStateInitializer GraphicsPSOInit;  
    RHICmdList.ApplyCachedRenderTargets(GraphicsPSOInit);  
    GraphicsPSOInit.DepthStencilState = TStaticDepthStencilState<false, CF_Always>::GetRHI();  
    GraphicsPSOInit.BlendState = TStaticBlendState<>::GetRHI();  
    GraphicsPSOInit.RasterizerState = TStaticRasterizerState<>::GetRHI();  
    GraphicsPSOInit.PrimitiveType = PT_TriangleList;  
    GraphicsPSOInit.BoundShaderState.VertexDeclarationRHI = VertexDec.VertexDeclarationRHI;  
    GraphicsPSOInit.BoundShaderState.VertexShaderRHI = GETSAFERHISHADER_VERTEX(*VertexShader);  
    GraphicsPSOInit.BoundShaderState.PixelShaderRHI = GETSAFERHISHADER_PIXEL(*PixelShader);  
    SetGraphicsPipelineState(RHICmdList, GraphicsPSOInit);  
  
    //RHICmdList.SetViewport(0, 0, 0.0f, DrawTargetResolution.X, DrawTargetResolution.Y, 1.0f);  
    PixelShader->SetParameters(RHICmdList, MyColor, MyTexture);  
  
    // Draw grid.  
    //uint32 PrimitiveCount = 2;  
    //RHICmdList.DrawPrimitive(PT_TriangleList, 0, PrimitiveCount, 1);  
    FMyTextureVertex Vertices[4];  
    Vertices[0].Position.Set(-1.0f, 1.0f, 0, 1.0f);  
    Vertices[1].Position.Set(1.0f, 1.0f, 0, 1.0f);  
    Vertices[2].Position.Set(-1.0f, -1.0f, 0, 1.0f);  
    Vertices[3].Position.Set(1.0f, -1.0f, 0, 1.0f);  
    Vertices[0].UV = FVector2D(0.0f, 1.0f);  
    Vertices[1].UV = FVector2D(1.0f, 1.0f);  
    Vertices[2].UV = FVector2D(0.0f, 0.0f);  
    Vertices[3].UV = FVector2D(1.0f, 0.0f);  
  
    static const uint16 Indices[6] =  
    {  
        0, 1, 2,  
        2, 1, 3  
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
  
void UTestShaderBlueprintLibrary::DrawTestShaderRenderTarget(  
    UTextureRenderTarget2D* OutputRenderTarget,   
    AActor* Ac,  
    FLinearColor MyColor,  
    UTexture* MyTexture  
)  
{  
    check(IsInGameThread());  
  
    if (!OutputRenderTarget)  
    {  
        return;  
    }  
      
    FTextureRenderTargetResource* TextureRenderTargetResource = OutputRenderTarget->GameThread_GetRenderTargetResource();  
    FTextureRHIParamRef MyTextureRHI = MyTexture->TextureReference.TextureReferenceRHI;  
    UWorld* World = Ac->GetWorld();  
    ERHIFeatureLevel::Type FeatureLevel = World->Scene->GetFeatureLevel();  
    FName TextureRenderTargetName = OutputRenderTarget->GetFName();  
    ENQUEUE_RENDER_COMMAND(CaptureCommand)(  
        [TextureRenderTargetResource, FeatureLevel, MyColor, TextureRenderTargetName, MyTextureRHI](FRHICommandListImmediate& RHICmdList)  
        {  
            DrawTestShaderRenderTarget_RenderThread(RHICmdList,TextureRenderTargetResource, FeatureLevel, TextureRenderTargetName, MyColor, MyTextureRHI);  
        }  
    );  
  
}  
  
#undef LOCTEXT_NAMESPACE  
```

至此我们完成了逻辑层到shader的数据传输
