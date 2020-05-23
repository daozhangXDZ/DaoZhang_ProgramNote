# 虚幻4渲染编程（环境模拟篇）【第七卷：海洋模拟-上-海洋模拟理论推导】





## 简介：

海洋这个要素在游戏里占比越来越多，开放世界的游戏要求角色能上天入地下水。目前游戏里做海洋的方法就那几种。（1）预烘焙法（2）Gerstner  wave（3）FFT海洋。预烘焙法可以是实现烘焙好DisplacementMap或者是FFT的运算结果。Gerstner  wave可以在GPU或者CPU上算。FFT的话就是拿海洋频率模型算出Displacement。

------

## 【1】基础环境搭建

在开始研究之前我们需要先搭建起我们的环境。我选择在ComputeShader种完成各种计算，然后在顶点着色器种直接Sample前面的ComputeShader的波形计算结果。不要把波形的计算塞到VertexShader里。把波形计算独立出来还有个好处就是我能把波形的结果储存起来拿给其它效果使用，比如制作浮力部分的时候我们就需要知道海面波形的信息，如果塞VertexShader里就拿不到这些信息了。

搭建ComputeShader的方法前面我的文章有提到，这里我就直接贴代码了。使用的引擎版本是4.21.0，如果引擎更新了新版本可能代码有一点区别。FFT部分我会给出4.22的代码。

**如果不是在Unreal中实现或者不想做这么复杂，可以直接跳过这部分。**



![img](https://pic4.zhimg.com/80/v2-4ab738bee9f2f0f9000ffab4845f0bb3_hd.jpg)



![img](https://pic2.zhimg.com/80/v2-dc8f6793cb3b3573ec7cc7995691837d_hd.jpg)

SDHOcean.build.cs

```text
// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class SDHOcean : ModuleRules
{
	public SDHOcean(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
		
		PublicIncludePaths.AddRange(
			new string[] {
				// ... add public include paths required here ...
			}
			);
				
		
		PrivateIncludePaths.AddRange(
			new string[] {
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
                "UnrealEd",
                "Projects",
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

SDHOcean.h

```text
// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"
#include "Interfaces/IPluginManager.h"
#include "Misc/Paths.h"
#include "Modules/ModuleManager.h"

class FSDHOceanModule : public IModuleInterface
{
public:

	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
```

SDHOcean.cpp

```text
// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.

#include "SDHOcean.h"

#define LOCTEXT_NAMESPACE "FSDHOceanModule"

void FSDHOceanModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	FString PluginShaderDir = FPaths::Combine(IPluginManager::Get().FindPlugin(TEXT("SDHOcean"))->GetBaseDir(), TEXT("Shaders"));
	AddShaderSourceDirectoryMapping(TEXT("/Plugin/SDHOcean"), PluginShaderDir);
}

void FSDHOceanModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FSDHOceanModule, SDHOcean)
```

Ocean.h

```text
#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "Runtime/Engine/Classes/Components/ActorComponent.h"
#include "Engine/Classes/Engine/TextureRenderTarget2D.h"
#include "Ocean.generated.h"

typedef TRefCountPtr<class FRHITexture2D> FTexture2DRHIRef;
typedef TRefCountPtr<class FRHIUnorderedAccessView> FUnorderedAccessViewRHIRef;
typedef TRefCountPtr<class FRHIStructuredBuffer> FStructuredBufferRHIRef;
class FRHITexture;
class FRHIUnorderedAccessView;
class FRHICommandListImmediate;

USTRUCT(BlueprintType)
struct FOceanBasicStructData_GameThread
{
	GENERATED_USTRUCT_BODY()

	FOceanBasicStructData_GameThread(){}

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FVector4 OceanTime_GameThread;
};

UCLASS(hidecategories = (Object, LOD, Physics, Collision), editinlinenew, meta = (BlueprintSpawnableComponent), ClassGroup = Rendering, DisplayName = "OceanRenderComp")
class SDHOCEAN_API UOceanRenderComponent : public UActorComponent
{
	GENERATED_BODY()

public:

	UOceanRenderComponent(const FObjectInitializer& ObjectInitializer);
	//~ Begin UActorComponent Interface.
	virtual void OnRegister() override;
	virtual void TickComponent(float DeltaTime, enum ELevelTick TickType, FActorComponentTickFunction *ThisTickFunction) override;

	UPROPERTY(BlueprintReadWrite, EditAnywhere, Category = "OceanComponent")
	UTextureRenderTarget2D* OutputRenderTarget2D;

	//UniformData for Ocean render
	UPROPERTY(BlueprintReadWrite, EditAnywhere, Category = "OceanComponent")
	FOceanBasicStructData_GameThread OceanUniformDataBuffer;

	int32 TargetSize;
	ETextureRenderTargetFormat RenderTargetFormat;

private:

	//Render ocean render thread
	void OceanCalculating_GameThread();
	void OceanCalculating_RenderThread
	(
		FRHICommandListImmediate& RHICmdList,
		ERHIFeatureLevel::Type FeatureLevel,
		FRHITexture* OutputRenderTarget,
		int32 SurfaceSize,
		const FOceanBasicStructData_GameThread& OceanUniformData
	);
	
	FTexture2DRHIRef OutputTexture;
	FUnorderedAccessViewRHIRef OutputTextureUAV;
};
```

Ocean.cpp

```text
#include "SDHOcean/Public/Ocean.h"

#include "ShaderCore/Public/GlobalShader.h"

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
#include "RHI/Public/RHICommandList.h"
#include "RHI/Public/RHIResources.h"
#include "Engine/Classes/Kismet/KismetRenderingLibrary.h"
#include "Runtime/Engine/Classes/Kismet/GameplayStatics.h"

#define LOCTEXT_NAMESPACE "SDHOcean"

BEGIN_UNIFORM_BUFFER_STRUCT(FOceanBasicStructData, )
UNIFORM_MEMBER(FVector4, OceanTime)
END_UNIFORM_BUFFER_STRUCT(FOceanBasicStructData)

IMPLEMENT_UNIFORM_BUFFER_STRUCT(FOceanBasicStructData, TEXT("OceanBasicStructData"))

class FOceeanCSShader : public FGlobalShader
{

	DECLARE_SHADER_TYPE(FOceeanCSShader, Global)

public:

	FOceeanCSShader() {}
	FOceeanCSShader(const ShaderMetaType::CompiledShaderInitializerType& Initializer)
		: FGlobalShader(Initializer)
	{
		//TODO Bind pramerter here
		OutputBufferSurface.Bind(Initializer.ParameterMap, TEXT("OutputBufferSurface"));
		SurfaceClearColor.Bind(Initializer.ParameterMap, TEXT("SurfaceClearColor"));
	}
	//----------------------------------------------------//
	static bool ShouldCache(EShaderPlatform PlateForm)
	{
		return IsFeatureLevelSupported(PlateForm, ERHIFeatureLevel::SM5);
	}
	//----------------------------------------------------//
	static bool ShouldCompilePermutation(const FGlobalShaderPermutationParameters& Parameters)
	{
		return IsFeatureLevelSupported(Parameters.Platform, ERHIFeatureLevel::SM5);
	}
	//----------------------------------------------------//
	static void ModifyCompilationEnvironment(const FGlobalShaderPermutationParameters& Parameters, FShaderCompilerEnvironment& OutEnvironment)
	{
		FGlobalShader::ModifyCompilationEnvironment(Parameters, OutEnvironment);
		//Define micro here
		//OutEnvironment.SetDefine(TEXT("TEST_MICRO"), 1);
	}
	//----------------------------------------------------//

	void SetSurface(FRHICommandList& RHICmdList,
		FUnorderedAccessViewRHIRef& OutputUAV,
		const FLinearColor ClearColor
	)
	{
		//set the UAV
		FComputeShaderRHIParamRef ComputeShaderRHI = GetComputeShader();
		if (OutputBufferSurface.IsBound())
			RHICmdList.SetUAVParameter(ComputeShaderRHI, OutputBufferSurface.GetBaseIndex(), OutputUAV);
		if (SurfaceClearColor.IsBound())
			//RHICmdList.SetShaderParameter(GetComputeShader(), SurfaceClearColor.GetBufferIndex(), SurfaceClearColor.GetBaseIndex(), SurfaceClearColor.GetNumBytes(), ClearColor);
			SetShaderValue(RHICmdList, GetComputeShader(), SurfaceClearColor, ClearColor);
	}

	void SetOceanUniformBuffer(FRHICommandList& RHICmdList, const FOceanBasicStructData_GameThread& OceanStructData)
	{
		FOceanBasicStructData UniformData;
		UniformData.OceanTime = OceanStructData.OceanTime_GameThread;
		SetUniformBufferParameterImmediate(RHICmdList, GetComputeShader(), GetUniformBufferParameter<FOceanBasicStructData>(), UniformData);
	}

	void UnBindBuffers(FRHICommandList& RHICmdList)
	{
		FComputeShaderRHIParamRef ComputeShaderRHI = GetComputeShader();

		if (OutputBufferSurface.IsBound())
			RHICmdList.SetUAVParameter(ComputeShaderRHI, OutputBufferSurface.GetBaseIndex(), FUnorderedAccessViewRHIRef());
	}

	virtual bool Serialize(FArchive& Ar) override
	{
		bool bShaderHasOutdatedParameters = FGlobalShader::Serialize(Ar);
		//Serrilize something here
		Ar << OutputBufferSurface << SurfaceClearColor;
		return bShaderHasOutdatedParameters;
	}

private:

	FShaderResourceParameter OutputBufferSurface;
	FShaderParameter SurfaceClearColor;
};

IMPLEMENT_SHADER_TYPE(, FOceeanCSShader, TEXT("/Plugin/SDHOcean/Ocean.usf"), TEXT("OceanMainCS"), SF_Compute)

void UOceanRenderComponent::OceanCalculating_RenderThread
(
	FRHICommandListImmediate& RHICmdList,
	ERHIFeatureLevel::Type FeatureLevel,
	FRHITexture* OutputRenderTarget,
	int32 SurfaceSize,
	const FOceanBasicStructData_GameThread& OceanUniformData
)
{
	check(IsInRenderingThread());
	check(OutputRenderTarget);

	TShaderMapRef<FOceeanCSShader>OceanComputeShader(GetGlobalShaderMap(FeatureLevel));
	RHICmdList.SetComputeShader(OceanComputeShader->GetComputeShader());

	if (OutputTexture.IsValid() == false)
	{
		if (OutputTexture.IsValid())
			OutputTexture->Release();
		if (OutputTextureUAV.IsValid())
			OutputTextureUAV->Release();

		FRHIResourceCreateInfo CreateInfo;
		OutputTexture = RHICreateTexture2D(SurfaceSize, SurfaceSize, PF_FloatRGBA, 1, 1, TexCreate_ShaderResource | TexCreate_UAV, CreateInfo);
		OutputTextureUAV = RHICreateUnorderedAccessView(OutputTexture);

	}

	OceanComputeShader->SetSurface(RHICmdList, OutputTextureUAV, FLinearColor(1,1,1,1));
	OceanComputeShader->SetOceanUniformBuffer(RHICmdList ,OceanUniformData);

	DispatchComputeShader(RHICmdList, *OceanComputeShader, SurfaceSize / 32, SurfaceSize / 32, 1);
	OceanComputeShader->UnBindBuffers(RHICmdList);

	RHICmdList.CopyToResolveTarget(OutputTexture, OutputRenderTarget, FResolveParams());
	//FRHICopyTextureInfo copyinfo(SurfaceSize, SurfaceSize);
	//RHICmdList.CopyTexture(OutputTexture, OutputRenderTarget, copyinfo);
}

UOceanRenderComponent::UOceanRenderComponent(const FObjectInitializer& ObjectInitializer)
	:Super(ObjectInitializer)
{
	PrimaryComponentTick.bCanEverTick = true;
	bTickInEditor = true;
	bAutoActivate = true;

	RenderTargetFormat = RTF_RGBA32f;
}

void UOceanRenderComponent::OnRegister()
{
	Super::OnRegister();
}

void UOceanRenderComponent::TickComponent(float DeltaTime, enum ELevelTick TickType, FActorComponentTickFunction *ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	
	//Tick render the ocean
	OceanCalculating_GameThread();
}

void UOceanRenderComponent::OceanCalculating_GameThread()
{
	UWorld* world = GetWorld();
	ERHIFeatureLevel::Type FeatureLevel = world->Scene->GetFeatureLevel();
	checkf(FeatureLevel == ERHIFeatureLevel::SM5, TEXT("Only surpport SM5"));

	if (OutputRenderTarget2D == nullptr) return;

	//Using front RT to render,back buffer store last frame imformation
	UKismetRenderingLibrary::ClearRenderTarget2D(world, OutputRenderTarget2D);

	FTextureReferenceRHIRef OutputRenderTargetTextureRHI = OutputRenderTarget2D->TextureReference.TextureReferenceRHI;

	checkf(OutputRenderTargetTextureRHI != nullptr, TEXT("Can't get render target %d texture"));

	FRHITexture* RenderTargetTextureRef = OutputRenderTargetTextureRHI->GetTextureReference()->GetReferencedTexture();
	TargetSize = OutputRenderTarget2D->SizeX;

	//Update the uniform buffer
	OceanUniformDataBuffer.OceanTime_GameThread.X = UGameplayStatics::GetRealTimeSeconds(GetWorld());

	ENQUEUE_RENDER_COMMAND(OceanRenderCommand)
	(
		[FeatureLevel, RenderTargetTextureRef, this](FRHICommandListImmediate& RHICmdList)
		{
			OceanCalculating_RenderThread
			(
				RHICmdList,
				FeatureLevel,
				RenderTargetTextureRef,
				this->TargetSize,
				this->OceanUniformDataBuffer
			);
		}
	);
}

#undef LOCTEXT_NAMESPACE
```

Ocean.usf

```text
#include "/Engine/Private/Common.ush"

RWTexture2D<float4> OutputBufferSurface;
float4 SurfaceClearColor;

struct OceanUniform
{
    float Time;
};
void InitOceanUniform(out OceanUniform uniformval)
{
    uniformval.Time = OceanBasicStructData.OceanTime.x;
}

[numthreads(32, 32, 1)]
void OceanMainCS(uint3 ThreadId : SV_DispatchThreadID)
{
	//Set up some variables we are going to need
	//The size of outputsurface and input surface is same
    float sizeX, sizeY;
    OutputBufferSurface.GetDimensions(sizeX, sizeY);

    OceanUniform OceanUniformVal;
    InitOceanUniform(OceanUniformVal);

    float2 iResolution = float2(sizeX, sizeY);
    float2 UV = (ThreadId.xy / iResolution.xy) * 50.0f;

    float4 Output = float4(1.0f, 1.0f, 1.0f, 1.0f);

   Output.xyz = float3(sin(UV.x + OceanUniformVal.Time), 0, 0);

    OutputBufferSurface[ThreadId.xy] = Output;
}
```

我这里做了个UniformBuffer然后拿到系统的时间，把系统的时间变量塞到我的Compute shader中。



![img](https://pic3.zhimg.com/80/v2-88095020cb6b0dcb4dc54a777b64f4d6_hd.jpg)

直接把值采出来连到VertexPositionOffset上就可以把我们的ComputeShader的结果传到顶点着色器了。

------

## 【2】Gerstner Wave

在Gerstner Waves之前，先使用正玄波变形的方法模拟。对正玄波进行变形属于经验性的方法，把正弦波变形让它的形状更接近水浪。



![img](https://pic4.zhimg.com/80/v2-6bf09c6030306e6c2fe96cb6a6d8a05f_hd.jpg)

![F(x)=2(\frac{sin(x) + 1}{2})^{k}](https://www.zhihu.com/equation?tex=F%28x%29%3D2%28%5Cfrac%7Bsin%28x%29+%2B+1%7D%7B2%7D%29%5E%7Bk%7D) 

下面先来制作正玄波水面



![img](https://pic2.zhimg.com/80/v2-eab451ce66d2e7623ff74d70491b97f1_hd.jpg)

于是乎我们可以得到如下效果



![img](https://pic2.zhimg.com/v2-de748c163f619f706230575047d8bffd_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

有了基础的波形后，剩下就是让海面变化更丰富。想让海面变丰富那就是多叠几层波



![img](https://pic1.zhimg.com/v2-a64dcccdc118251d2c0f0494999dbe18_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

```text
    Output.z = 0.5 * pow((sin(WaveLength * Speed + dot(direction, UV * 0.8) * WaveLength) + 1) / 2, 2.5f);
    Output.z += 0.2 * pow((sin(WaveLength * Speed * 0.8f + dot(float2(0.8, 0.1), UV * 0.9) * WaveLength) + 1) / 2, 2.5f);
    Output.z += 0.15 * sin(WaveLength * Speed * 1.2f + dot(float2(-0.8, -0.1), UV) * WaveLength * 1.3f);
    Output.z += 0.1 * sin(WaveLength * Speed * 1.2f + dot(float2(0.6, -0.5), UV) * WaveLength * 1.5f);
    Output.z += 0.1 * sin(WaveLength * Speed * 0.5f + dot(float2(0.5, -0.1), UV) * WaveLength * 1.5f);

    Output.y = 0.5 * pow((cos(WaveLength * Speed + dot(direction, UV * 0.8) * WaveLength) + 1) / 2, 2.5f);
    Output.y += 0.2 * pow((cos(WaveLength * Speed * 0.8f + dot(float2(0.8, 0.1), UV * 0.9) * WaveLength) + 1) / 2, 2.5f);
    Output.y += 0.15 * cos(WaveLength * Speed * 1.2f + dot(float2(-0.8, -0.1), UV) * WaveLength * 1.3f);
    Output.y += 0.1 * cos(WaveLength * Speed * 1.2f + dot(float2(0.6, -0.5), UV) * WaveLength * 1.5f);
    Output.y += 0.1 * cos(WaveLength * Speed * 0.5f + dot(float2(0.5, -0.1), UV) * WaveLength * 1.5f);

    Output.z = 0.5 * pow((cos(WaveLength * Speed + dot(direction, UV * 0.8) * WaveLength) + 1) / 2, 2.5f);
    Output.z += 0.2 * pow((cos(WaveLength * Speed * 0.8f + dot(float2(0.8, 0.1), UV * 0.9) * WaveLength) + 1) / 2, 2.5f);
    Output.z += 0.15 * cos(WaveLength * Speed * 1.2f + dot(float2(-0.8, -0.1), UV) * WaveLength * 1.3f);
    Output.z += 0.1 * cos(WaveLength * Speed * 1.2f + dot(float2(0.6, -0.5), UV) * WaveLength * 1.5f);
    Output.z += 0.1 * cos(WaveLength * Speed * 0.5f + dot(float2(0.5, -0.1), UV) * WaveLength * 1.5f);

    OutputBufferSurface[ThreadId.xy] = Output;
```

可以看到正玄波水面波浪比较平，无法模拟出水波的波峰陡峭的特点。因此我们需要使用新的模拟模型：Gerstner Wave。



![img](https://pic2.zhimg.com/v2-2b7f8d03ba20f38a7e97f1cffee377d1_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

PositionOffset：



![img](https://pic3.zhimg.com/80/v2-411a49066c4f0a9ce6795db806513106_hd.jpg)

Normal：



![img](https://pic4.zhimg.com/80/v2-40f398d827736048f87be5ac4cc3e4db_hd.jpg)

Gerstner Wave是周期重力波欧拉方程的解, 其描述的是拥有无限深度且不可压缩的流体表面的波形 。



![img](https://pic1.zhimg.com/v2-dbb661495703ac0400f9ea6bdbee7bf4_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

代码如下：



![img](https://pic3.zhimg.com/80/v2-6c4496f082f6e44454acf849fc2dca4e_hd.jpg)

想要更好的效果可以优化下参数和多叠几层波，反正Computeshader里算这种东西很快的啦。

------

## 【3】FFT海面理论推导

FFT海面的核心思路是我们通过一系列测量得到真实海面的波的频率然后把这些频率通过FFT变换到时域然后计算出置换贴图。下面来公式推导

设波的高度为水平方向的位置和时间的关系 ![h(X,t)](https://www.zhihu.com/equation?tex=h%28X%2Ct%29) 。在水平方向上 ![X= （x,z）](https://www.zhihu.com/equation?tex=X%3D+%EF%BC%88x%2Cz%EF%BC%89) 根据Tessendorf J.2001的论文我们可以得到如下公式

![h(X,t）=\sum_{K}^{}{x}\tilde{h}(K,t)e^{iK\cdot X}](https://www.zhihu.com/equation?tex=h%28X%2Ct%EF%BC%89%3D%5Csum_%7BK%7D%5E%7B%7D%7Bx%7D%5Ctilde%7Bh%7D%28K%2Ct%29e%5E%7BiK%5Ccdot+X%7D) 

其中 ![K](https://www.zhihu.com/equation?tex=K) 代表波正在运动的二维水平方向， ![K = (k_{x}, K_{y})](https://www.zhihu.com/equation?tex=K+%3D+%28k_%7Bx%7D%2C+K_%7By%7D%29) 。

![k_{x} = 2\pi/L_{x}](https://www.zhihu.com/equation?tex=k_%7Bx%7D+%3D+2%5Cpi%2FL_%7Bx%7D) , ![k_{y} = 2\pi m/L_{y}](https://www.zhihu.com/equation?tex=k_%7By%7D+%3D+2%5Cpi+m%2FL_%7By%7D) 。

![n](https://www.zhihu.com/equation?tex=n) 是水平方向的Domain Resolution。 ![m](https://www.zhihu.com/equation?tex=m) 是竖直方向的Domain Resolution

 所以 ![K](https://www.zhihu.com/equation?tex=K) 的范围是：

![K=(2\pi/L_{x},2\pi m/L_{y})](https://www.zhihu.com/equation?tex=K%3D%282%5Cpi%2FL_%7Bx%7D%2C2%5Cpi+m%2FL_%7By%7D%29) 

The fft process generates the height field at discrete points

![X = (nL_{x}/N, mL_{z}/N)](https://www.zhihu.com/equation?tex=X+%3D+%28nL_%7Bx%7D%2FN%2C+mL_%7Bz%7D%2FN%29) 

![-N/2 \leq n, m < N/2](https://www.zhihu.com/equation?tex=-N%2F2+%5Cleq+n%2C+m+%3C+N%2F2) 

下面我做一系列化简

![0\leq n,m<N-1](https://www.zhihu.com/equation?tex=0%5Cleq+n%2Cm%3CN-1) 

![n = n - N/2](https://www.zhihu.com/equation?tex=n+%3D+n+-+N%2F2) 

![m = m - N/2](https://www.zhihu.com/equation?tex=m+%3D+m+-+N%2F2) 

m和n的可以在整形范围【16，2048】之间取值

![K = (\frac{2\pi n - \pi N}{L}, \frac{2\pi m - \pi N}{L})](https://www.zhihu.com/equation?tex=K+%3D+%28%5Cfrac%7B2%5Cpi+n+-+%5Cpi+N%7D%7BL%7D%2C+%5Cfrac%7B2%5Cpi+m+-+%5Cpi+N%7D%7BL%7D%29) 

![X=((n-\frac{N}{2})L/N,(m-\frac{N}{2})L/N)](https://www.zhihu.com/equation?tex=X%3D%28%28n-%5Cfrac%7BN%7D%7B2%7D%29L%2FN%2C%28m-%5Cfrac%7BN%7D%7B2%7D%29L%2FN%29) 

![-N/2 \leq k, l < N -1](https://www.zhihu.com/equation?tex=-N%2F2+%5Cleq+k%2C+l+%3C+N+-1) 

![X = (kL/N , lL/N)](https://www.zhihu.com/equation?tex=X+%3D+%28kL%2FN+%2C+lL%2FN%29) 

![\Rightarrow h(k,l,t) = \sum_{n=0}^{N-1}{\sum_{m=0}^{N-1}}\tilde{h}(n,m,t)e^{\frac{i(2\pi nk-\pi Nk)}{N}}e^{\frac{i(2\pi nl - \pi Nl)}{N}}](https://www.zhihu.com/equation?tex=%5CRightarrow+h%28k%2Cl%2Ct%29+%3D+%5Csum_%7Bn%3D0%7D%5E%7BN-1%7D%7B%5Csum_%7Bm%3D0%7D%5E%7BN-1%7D%7D%5Ctilde%7Bh%7D%28n%2Cm%2Ct%29e%5E%7B%5Cfrac%7Bi%282%5Cpi+nk-%5Cpi+Nk%29%7D%7BN%7D%7De%5E%7B%5Cfrac%7Bi%282%5Cpi+nl+-+%5Cpi+Nl%29%7D%7BN%7D%7D) 

![\Rightarrow h(k,l,t) = \sum_{n=0}^{N-1}{\sum_{m=0}^{N-1}}\tilde{h}(n,m,t)e^{\frac{i2\pi nk}{N}}e^{-i\pi k}e^{-i\pi l}](https://www.zhihu.com/equation?tex=%5CRightarrow+h%28k%2Cl%2Ct%29+%3D+%5Csum_%7Bn%3D0%7D%5E%7BN-1%7D%7B%5Csum_%7Bm%3D0%7D%5E%7BN-1%7D%7D%5Ctilde%7Bh%7D%28n%2Cm%2Ct%29e%5E%7B%5Cfrac%7Bi2%5Cpi+nk%7D%7BN%7D%7De%5E%7B-i%5Cpi+k%7De%5E%7B-i%5Cpi+l%7D) 

![e^{-i\pi} = 1](https://www.zhihu.com/equation?tex=e%5E%7B-i%5Cpi%7D+%3D+1) 

![\Rightarrow h(k,l,t) = \frac{1}{N \cdot N}\sum_{n=0}^{N-1}{[\sum_{m=0}^{N-1}}\tilde{h}(n,m,t)e^{\frac{i2\pi nk}{N}}]e^{\frac{i2\pi nk}{N}}](https://www.zhihu.com/equation?tex=%5CRightarrow+h%28k%2Cl%2Ct%29+%3D+%5Cfrac%7B1%7D%7BN+%5Ccdot+N%7D%5Csum_%7Bn%3D0%7D%5E%7BN-1%7D%7B%5B%5Csum_%7Bm%3D0%7D%5E%7BN-1%7D%7D%5Ctilde%7Bh%7D%28n%2Cm%2Ct%29e%5E%7B%5Cfrac%7Bi2%5Cpi+nk%7D%7BN%7D%7D%5De%5E%7B%5Cfrac%7Bi2%5Cpi+nk%7D%7BN%7D%7D) 

![h_{0}](https://www.zhihu.com/equation?tex=h_%7B0%7D) 需要使用一个海洋统计学计算模型Phillips spectrum，这个模型的原始数据是多年观测的来，它是一个经验公式。

![P_{h}(K)=a \frac{e^{-\frac{1}{(kL)^2}}}{k^4}\left| \tilde{K}\cdot \tilde{W} \right|^2](https://www.zhihu.com/equation?tex=P_%7Bh%7D%28K%29%3Da+%5Cfrac%7Be%5E%7B-%5Cfrac%7B1%7D%7B%28kL%29%5E2%7D%7D%7D%7Bk%5E4%7D%5Cleft%7C+%5Ctilde%7BK%7D%5Ccdot+%5Ctilde%7BW%7D+%5Cright%7C%5E2) 

![L = \frac{v^2}{g}](https://www.zhihu.com/equation?tex=L+%3D+%5Cfrac%7Bv%5E2%7D%7Bg%7D) 

![a](https://www.zhihu.com/equation?tex=a) : global wave amplitude

![\tilde{K}](https://www.zhihu.com/equation?tex=%5Ctilde%7BK%7D) : normalized wave direction vector

![k](https://www.zhihu.com/equation?tex=k) : the magnitude of 

![\tilde{W}](https://www.zhihu.com/equation?tex=%5Ctilde%7BW%7D) : normalized wind direction vector

![v](https://www.zhihu.com/equation?tex=v) : wind speed

![g](https://www.zhihu.com/equation?tex=g) : gravitational constant

为了具有随机性，我们使用高斯分布来获取随机波普，根据上面的公式

波高场的傅立叶振幅可以产生为：

![\tilde{h}_{0}(K)=\frac{1}{\sqrt{2}}(\xi _{r} + i\xi _{i})\sqrt{P_{h}(K)}](https://www.zhihu.com/equation?tex=%5Ctilde%7Bh%7D_%7B0%7D%28K%29%3D%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%28%5Cxi+_%7Br%7D+%2B+i%5Cxi+_%7Bi%7D%29%5Csqrt%7BP_%7Bh%7D%28K%29%7D) 

式中，ξr和ξi是高斯随机数发生器的普通独立绘图。

给定一个离散关系 ![w_{k}](https://www.zhihu.com/equation?tex=w_%7Bk%7D) ，则当时间为 ![t](https://www.zhihu.com/equation?tex=t) 时，波场的傅里叶振幅为：

![\tilde{h(k,t)} = \tilde{h_{0}}(k)exp\left\{ iω(k)t \right\} + \tilde{h_{0}^{*}}(−k)exp\left\{  -iω(k)t \right\} ](https://www.zhihu.com/equation?tex=%5Ctilde%7Bh%28k%2Ct%29%7D+%3D+%5Ctilde%7Bh_%7B0%7D%7D%28k%29exp%5Cleft%5C%7B+i%CF%89%28k%29t+%5Cright%5C%7D+%2B+%5Ctilde%7Bh_%7B0%7D%5E%7B%2A%7D%7D%28%E2%88%92k%29exp%5Cleft%5C%7B++-i%CF%89%28k%29t+%5Cright%5C%7D+) 

![ \tilde{h_{0}^{*}} = \tilde{h}(-k,t)](https://www.zhihu.com/equation?tex=+%5Ctilde%7Bh_%7B0%7D%5E%7B%2A%7D%7D+%3D+%5Ctilde%7Bh%7D%28-k%2Ct%29) 

式中 ![h_{0}](https://www.zhihu.com/equation?tex=h_%7B0%7D) 项为波普参数，使用这个式子可以执行FFT来计算结果。

------

## 【4】FFT海面实现步骤

（1）首先我们需要一个gauss分布



![img](https://pic3.zhimg.com/80/v2-285fa4882daaa08fedfb1aaf9df3fe5e_hd.png)



![img](https://pic4.zhimg.com/80/v2-4c86e21af99ce52b1d72a21f4715ad53_hd.jpg)

按照上面的公式可以渲染得到下面一张图：



![img](https://pic4.zhimg.com/80/v2-af31311d8161c849722fd2f163dc2eeb_hd.jpg)

（2）然后需要用高斯分布生成一个Phillips spectrum



![img](https://pic2.zhimg.com/80/v2-fd3284db8fb3bcc1ee55c958e35707b5_hd.jpg)



![img](https://pic3.zhimg.com/80/v2-396a7a0ffb2d0a0f5d7357a614e95a22_hd.jpg)

会得到如下效果



![img](https://pic2.zhimg.com/80/v2-afba77cea1beb7c45028aa6cda969655_hd.jpg)



把它和gauss分布结合后得到如下效果：



![img](https://pic4.zhimg.com/80/v2-de7986523352cdd9a3bea15e493c3b0b_hd.jpg)

然后现在我们有了海面的频谱图。下一步需要进行IFFT变换，但是在做变换前我们需要一个OmegaTexture做蝶形变换



![img](https://pic4.zhimg.com/80/v2-2f50dc53c4a1ff3d97d517db9133bcab_hd.jpg)



![img](https://pic1.zhimg.com/80/v2-a9407198f16802a5ff92dcd890503d78_hd.png)





（3）然后做IFFT变换生成Displacement，然后生成高度图和normal



![img](https://pic3.zhimg.com/80/v2-f1a1ec427b83e1c33c44ae0d4bc64c56_hd.jpg)

最后把这些生成的图弄到渲染管线种作为渲染资源渲染海面即可。下面就根据这上面的步骤来生成我们的海面。

下一卷我将给出具体FFT实现。

Enjoy it。

------

## Next：

YivanLee：虚幻4渲染编程（环境模拟篇）【第八卷：海洋模拟-中-在UE中实现FFT海洋】

zhuanlan.zhihu.com![图标](https://pic1.zhimg.com/v2-d37731435c7e3c4dd055d943130118fc_180x120.jpg)

------

【参考资料】

【1】[Ocean Shader with Gerstner Waves](https://link.zhihu.com/?target=https%3A//80.lv/articles/tutorial-ocean-shader-with-gerstner-waves/)

【2】[音速键盘猫：Shader相册第6期 --- 实时水面模拟与渲染(一)](https://zhuanlan.zhihu.com/p/31670275)

【3】[https://labs.karmaninteractive.com/ocean-simulation-pt-1-introduction-df134a47150](https://link.zhihu.com/?target=https%3A//labs.karmaninteractive.com/ocean-simulation-pt-1-introduction-df134a47150)

【4】[Ocean simulation part one: using the discrete Fourier transform](https://link.zhihu.com/?target=http%3A//www.keithlantz.net/2011/10/ocean-simulation-part-one-using-the-discrete-fourier-transform/)

【5】[Ocean simulation part two: using the fast Fourier transform](https://link.zhihu.com/?target=http%3A//www.keithlantz.net/2011/11/ocean-simulation-part-two-using-the-fast-fourier-transform/)

【6】[https://www.slideshare.net/Codemotion/an-introduction-to-realistic-ocean-rendering-through-fft-fabio-suriano-codemotion-rome-2017](https://link.zhihu.com/?target=https%3A//www.slideshare.net/Codemotion/an-introduction-to-realistic-ocean-rendering-through-fft-fabio-suriano-codemotion-rome-2017)

【7】[海洋模擬 FFT算法實現--基於GPU的基2快速傅里葉變換 2維FFT算法實現--基於GPU的基2快速二維傅里葉變換 【pbrt】使用openFrameworks調用pbrt](https://link.zhihu.com/?target=https%3A//www.twblogs.net/a/5b926b9f2b71772002d2d3e5)

【8】[白霂凡：一小时学会快速傅里叶变换（Fast Fourier Transform）](https://zhuanlan.zhihu.com/p/31584464)

【9】[海面模拟以及渲染（计算着色器、FFT、Reflection Matrix）](https://link.zhihu.com/?target=https%3A//blog.csdn.net/xiewenzhao123/article/details/79111004)

【10】[wubugui/Jerry-Tessendorf-2004](https://link.zhihu.com/?target=https%3A//github.com/wubugui/Jerry-Tessendorf-2004)

【11】[http://evasion.imag.fr/~Fabrice.Neyret/images/fluids-nuages/waves/Jonathan/articlesCG/waterslides2001.pdf](https://link.zhihu.com/?target=http%3A//evasion.imag.fr/~Fabrice.Neyret/images/fluids-nuages/waves/Jonathan/articlesCG/waterslides2001.pdf)

【12】[https://dsqiu.iteye.com/blog/1636299](https://link.zhihu.com/?target=https%3A//dsqiu.iteye.com/blog/1636299)

【13】[https://www.bilibili.com/video/av19141078?t=1053](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/av19141078%3Ft%3D1053)

傅里叶变换基础教程（如果对傅里叶变换完全不清楚的建议按顺序看完下面的链接）

【14】[Heinrich：傅里叶分析之掐死教程（完整版）更新于2014.06.06](https://zhuanlan.zhihu.com/p/19763358)

【15】[https://www.bilibili.com/video/av34364399/?spm_id_from=333.788.videocard.0](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/av34364399/%3Fspm_id_from%3D333.788.videocard.0)

【16】[https://www.bilibili.com/video/av34556069/?spm_id_from=333.788.videocard.0](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/av34556069/%3Fspm_id_from%3D333.788.videocard.0)

【17】[https://www.bilibili.com/video/av34845617/?spm_id_from=333.788.videocard.0](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/av34845617/%3Fspm_id_from%3D333.788.videocard.0)

【18】[https://www.bilibili.com/video/av35047004/?spm_id_from=333.788.videocard.0](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/av35047004/%3Fspm_id_from%3D333.788.videocard.0)

【19】[https://www.bilibili.com/video/av35810587/?spm_id_from=333.788.videocard.0](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/av35810587/%3Fspm_id_from%3D333.788.videocard.0)

【20】[https://www.bilibili.com/video/av36343956/?spm_id_from=333.788.videocard.0](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/av36343956/%3Fspm_id_from%3D333.788.videocard.0)
