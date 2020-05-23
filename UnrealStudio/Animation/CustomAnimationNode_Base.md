(原)Unreal源码搬山-动画篇  自定义动画节点

2018年11月21日 星期三

18:27

@author:黑袍小道

 

# 前言：

​        本文是接着上文 Unreal搬山之动画模块_Unreal动画流程和框架，进行简单入门如何自定义动画图标的AnimNode。

 

# 正文：

## 一、AnimNode

Unreal 4的AnimNode负责的骨骼动画的单项计算，最后汇总到AnimGraph有，然后交付给AnimInstance统一收集和处理。

下图未AnimNode相关的结构



![img](./CustomAnimationNode.assets/clip_image002.jpg)

 

 

 

## 二、CustomAnimNode

该例子实现修改指定的一系列骨骼，并再AnimGraphy预览和编辑



![img](./CustomAnimationNode.assets/clip_image004.jpg)

 



![img](./CustomAnimationNode.assets/clip_image006.jpg)

 



![img](./CustomAnimationNode.assets/clip_image008.jpg)

 

## 三、Unreal4 AnimNode的结构和使用套路（流程）

###  

###  

## 四、案例源码

### DZAnimStudio.uplugin

**------------------------------------------------------------------------------------------------------------------------------------------------------**

{

"FileVersion": 3,

"Version": 1,

"VersionName": "1.0",

"FriendlyName": "DZAnimStudio",

"Description": "This is Anim Studio",

"Category": "Other",

"CreatedBy": "BaiPao_XD",

"CreatedByURL": "<https://www.cnblogs.com/BaiPao-XD/>",

"DocsURL": "",

"MarketplaceURL": "",

"SupportURL": "",

"CanContainContent": true,

"IsBetaVersion": false,

"Installed": false,

"Modules": [

{

"Name": "DZAnimStudio",

"Type": "Runtime",

"LoadingPhase": "PreDefault",

"WhitelistPlatforms": [

"Android",

"Mac",

"Win32",

"Win64",

"PS4",

"XboxOne"

]

},

{

"Name": "DZAnimStudioEditor",

"Type": "Editor",//这里最好选着Developer这样在stand模式下启动也会加载

"LoadingPhase": "Default",

"WhitelistPlatforms": [

"Win32",

"Win64",

"Mac"

]

}

]

}

 

###  

### DZAnimStudioEditor.h

**------------------------------------------------------------------------------------------------------------------------------------------------------**

\#pragma once

\#include "ModuleManager.h"

class FDZAnimStudioEditorModule : public IModuleInterface

{

public:

virtual void StartupModule() override;

virtual void ShutdownModule() override;

};

 

### DZAnimStudioEditor.cpp

**------------------------------------------------------------------------------------------------------------------------------------------------------**

\#include "DZAnimStudioEditor.h"

\#include "DZAnimStudio.h"

\#include "DZAnimStudioEditorPrivatePCH.h"

\#include "EditMode/DZAnimNode_ScaleBoneEditMode.h"

\#define LOCTEXT_NAMESPACE "FAnimGraphIKModule"

 

void FDZAnimStudioEditorModule::StartupModule()

{

FEditorModeRegistry::Get().RegisterMode<FDZAnimNode_ScaleBoneEditMode>(DZAnimNodeEditModes::ScaleBone, LOCTEXT("DZAnimNode_ScaleBoneEditMode", "DZAnimNode_ScaleBone"), FSlateIcon(), false);

}

 

void FDZAnimStudioEditorModule::ShutdownModule()

{

 

FEditorModeRegistry::Get().UnregisterMode(DZAnimNodeEditModes::ScaleBone);

}

 

\#undef LOCTEXT_NAMESPACE

 

IMPLEMENT_MODULE(FDZAnimStudioEditorModule, DZAnimStudioEditor)

 

 

### DZAnimStudioEditor.Build.cs

\---------------------------------------------------------------------------------------------------------------------------------------------------

// Copyright 2018 azhecheng, Inc. All Rights Reserved.

 

using UnrealBuildTool;

using System.IO;

public class AnimGraphIK : ModuleRules

{

\#if WITH_FORWARDED_MODULE_RULES_CTOR

​    public AnimGraphIK(ReadOnlyTargetRules Target) : base(Target)

\#else

​    public AnimGraphIK(TargetInfo Target)

\#endif

 

​    {

​        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

​        PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "Public"));

​        PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "../AnimIK/Public"));

​        PublicIncludePaths.Add(ModuleDirectory);

​        PublicIncludePaths.AddRange(

new string[] {

​                "Editor/AnimGraph/Public",

​                "Editor/AdvancedPreviewScene/Public"

//                 "Editor/AnimGraph/Classes",

// ... add public include paths required here ...

}

​            );

 

 

PrivateIncludePaths.AddRange(

new string[] {

"AnimGraphIK/Private",

​                 "AnimIK/Private"

// ... add other private include paths required here ...

}

);

 

 

PublicDependencyModuleNames.AddRange(

new string[]

{

"Core",

​                "CoreUObject",

​                "Engine",

​                "Slate",

​                "AnimGraphRuntime",

​                "BlueprintGraph",

​                "AnimIK",

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

​                "InputCore",

​                "UnrealEd",

​                "GraphEditor",

​                "PropertyEditor",

​                "EditorStyle",

​                "AnimGraph",

// ... add private dependencies that you statically link with here ...        

}

);

​        PrivateIncludePathModuleNames.AddRange(

​            new string[] {

​                "Persona",

​                "SkeletonEditor",

\#if WITH_FORWARDED_MODULE_RULES_CTOR

​                "AdvancedPreviewScene",

\#endif

​            }

​        );

​        DynamicallyLoadedModuleNames.AddRange(

new string[]

{

// ... add any modules that your module loads dynamically here ...

}

);

}

}

 

### DZAnimStudioEditor.Build.cs

\---------------------------------------------------------------------------------------------------------------------------------------------------

// Copyright 2018 azhecheng, Inc. All Rights Reserved.

\#pragma once

\#include "AnimGraphNode_SkeletalControlBase.h"

\#include "DZAnimNode_ScaleBone.h"

\#include "EdGraph/EdGraphNodeUtils.h" 

\#include "DZAnimNode_ScaleBoneEdit.generated.h"

 

UCLASS(MinimalAPI)

class UDZAnimNode_ScaleBoneEdit : public UAnimGraphNode_SkeletalControlBase

{

GENERATED_UCLASS_BODY()

 

UPROPERTY(EditAnywhere, Category = Settings)

FDZAnimNode_ScaleBone Node;

 

public:

 

virtual FText GetTooltipText() const override;

 

virtual void CopyNodeDataToPreviewNode(FAnimNode_Base* AnimNode) override;

 

 

virtual FText GetNodeTitle(ENodeTitleType::Type TitleType) const override;

 

virtual FEditorModeID GetEditorMode() const override;

virtual void Draw(FPrimitiveDrawInterface* PDI, USkeletalMeshComponent * PreviewSkelMeshComp) const override;

 

void SetDefaultValue(const FString& InDefaultValueName, const FTransform& InValue);

protected:

 

virtual FText GetControllerDescription() const override;

virtual const FAnimNode_SkeletalControlBase* GetNode() const override { return &Node; }

 

 

};

 

### DZAnimNode_ScaleBoneEdit.cpp

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#include "DZAnimNode_ScaleBoneEdit.h"

\#include "DZAnimStudioEditorPrivatePCH.h"

\#include "EditMode/DZAnimNode_ScaleBoneEditMode.h"

 

\#define LOCTEXT_NAMESPACE "DZAnimBaseNodeEditMode"

UDZAnimNode_ScaleBoneEdit::UDZAnimNode_ScaleBoneEdit(const FObjectInitializer& ObjectInitializer)

: Super(ObjectInitializer)

{

 

}

 

 

FText UDZAnimNode_ScaleBoneEdit::GetTooltipText() const

{

return LOCTEXT("AnimGraphNode_DZAnNo_ScaleBodyBone_Tooltip", "The DZAnNode ScaleBodyBone");

}

 

void UDZAnimNode_ScaleBoneEdit::CopyNodeDataToPreviewNode(FAnimNode_Base* AnimNode)

{

 

}

 

 

FText UDZAnimNode_ScaleBoneEdit::GetNodeTitle(ENodeTitleType::Type TitleType) const

{

return GetControllerDescription();

}

 

FEditorModeID UDZAnimNode_ScaleBoneEdit::GetEditorMode() const

{

return DZAnimNodeEditModes::ScaleBone;

}

 

void UDZAnimNode_ScaleBoneEdit::Draw(FPrimitiveDrawInterface* PDI, USkeletalMeshComponent * PreviewSkelMeshComp) const

{

 

}

 

void UDZAnimNode_ScaleBoneEdit::SetDefaultValue(const FString& InDefaultValueName, const FTransform& InValue)

{

 

}

FText UDZAnimNode_ScaleBoneEdit::GetControllerDescription() const

{

return LOCTEXT("DZAnimNode_ScaleBodyBone", "DZAnimNode ScaleBodyBone");

}

 

 

### DZAnimNode_ScaleBoneEditMode.h

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#pragma once

\#include "CoreMinimal.h"

\#include "UnrealWidget.h"

\#include "AnimNodeEditMode.h"

\#include "DZAnimNode_ScaleBoneEdit.h"

\#include "DZAimBaseNodeEditMode.h"

class FEditorViewportClient;

class FPrimitiveDrawInterface;

class USkeletalMeshComponent;

struct FViewportClick;

 

class FDZAnimNode_ScaleBoneEditMode : public FDZAnimBaseNodeEditMode

{

public:

FDZAnimNode_ScaleBoneEditMode();

};

 

 

### *DZAnimNode_ScaleBoneEditMode.cpp*

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#include "DZAnimNode_ScaleBoneEditMode.h"

\#include "DZAnimStudioEditorPrivatePCH.h"

\#include "SceneManagement.h"

\#include "EngineUtils.h"

\#include "IPersonaPreviewScene.h"

\#include "Animation/DebugSkelMeshComponent.h"

 

FDZAnimNode_ScaleBoneEditMode::FDZAnimNode_ScaleBoneEditMode()

{

 

}

 

### *DZAimBaseNodeEditMode.h*

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#pragma once

\#include "CoreMinimal.h"

\#include "InputCoreTypes.h"

\#include "UnrealWidget.h"

\#include "IAnimNodeEditMode.h"

\#include "BonePose.h"

\#include "Animation/AnimNodeBase.h"

 

class FCanvas;

class FEditorViewportClient;

class FPrimitiveDrawInterface;

class USkeletalMeshComponent;

struct FViewportClick;

 

struct DZANIMSTUDIO_API DZAnimNodeEditModes

{

const static FEditorModeID ScaleBone;

};

class FDZAnimBaseNodeEditMode : public IAnimNodeEditMode

{

public:

FDZAnimBaseNodeEditMode();

 

/** IAnimNodeEditMode interface */

virtual ECoordSystem GetWidgetCoordinateSystem() const override;

virtual FWidget::EWidgetMode GetWidgetMode() const override;

virtual FWidget::EWidgetMode ChangeToNextWidgetMode(FWidget::EWidgetMode CurWidgetMode) override;

virtual bool SetWidgetMode(FWidget::EWidgetMode InWidgetMode) override;

virtual FName GetSelectedBone() const override;

virtual void DoTranslation(FVector& InTranslation) override;

virtual void DoRotation(FRotator& InRotation) override;

virtual void DoScale(FVector& InScale) override;

virtual void EnterMode(class UAnimGraphNode_Base* InEditorNode, struct FAnimNode_Base* InRuntimeNode) override;

virtual void ExitMode() override;

 

/** IPersonaEditMode interface */

virtual bool GetCameraTarget(FSphere& OutTarget) const override;

virtual class IPersonaPreviewScene& GetAnimPreviewScene() const override;

virtual void GetOnScreenDebugInfo(TArray<FText>& OutDebugInfo) const override;

 

/** FEdMode interface */

virtual void Render(const FSceneView* View, FViewport* Viewport, FPrimitiveDrawInterface* PDI) override;

virtual void DrawHUD(FEditorViewportClient* ViewportClient, FViewport* Viewport, const FSceneView* View, FCanvas* Canvas) override;

virtual bool HandleClick(FEditorViewportClient* InViewportClient, HHitProxy* HitProxy, const FViewportClick& Click) override;

virtual FVector GetWidgetLocation() const override;

virtual bool StartTracking(FEditorViewportClient* InViewportClient, FViewport* InViewport) override;

virtual bool EndTracking(FEditorViewportClient* InViewportClient, FViewport* InViewport) override;

virtual bool InputKey(FEditorViewportClient* InViewportClient, FViewport* InViewport, FKey InKey, EInputEvent InEvent) override;

virtual bool InputDelta(FEditorViewportClient* InViewportClient, FViewport* InViewport, FVector& InDrag, FRotator& InRot, FVector& InScale) override;

virtual bool GetCustomDrawingCoordinateSystem(FMatrix& InMatrix, void* InData) override;

virtual bool GetCustomInputCoordinateSystem(FMatrix& InMatrix, void* InData) override;

virtual bool ShouldDrawWidget() const override;

virtual void Tick(FEditorViewportClient* ViewportClient, float DeltaTime) override;

};

 

### DZAimBaseNodeEditMode.cpp

\---------------------------------------------------------------------------------------------------------------------------------------------------

// Copyright 2018 azhecheng, Inc. All Rights Reserved.

\#include "DZAimBaseNodeEditMode.h"

\#include "DZAnimStudioEditorPrivatePCH.h"

\#include "EditorViewportClient.h"

\#include "IPersonaPreviewScene.h"

\#include "Animation/DebugSkelMeshComponent.h"

\#include "BoneControllers/AnimNode_SkeletalControlBase.h"

\#include "EngineUtils.h"

\#include "AnimGraphNode_SkeletalControlBase.h"

\#include "AssetEditorModeManager.h"

 

const FEditorModeID DZAnimNodeEditModes::ScaleBone("AnimGraph.SkeletalControl.ScaleBone");

\#define LOCTEXT_NAMESPACE "DZAnimBaseNodeEditMode"

 

FDZAnimBaseNodeEditMode::FAnimIKNodeEditMode()

{

 

}

 

bool FDZAnimBaseNodeEditMode::GetCameraTarget(FSphere& OutTarget) const

{

 

return true;

}

 

IPersonaPreviewScene& FDZAnimBaseNodeEditMode::GetAnimPreviewScene() const

{

return *static_cast<IPersonaPreviewScene*>(static_cast<FAssetEditorModeManager*>(Owner)->GetPreviewScene());

}

 

void FDZAnimBaseNodeEditMode::GetOnScreenDebugInfo(TArray<FText>& OutDebugInfo) const

{

 

}

 

ECoordSystem FDZAnimBaseNodeEditMode::GetWidgetCoordinateSystem() const

{

return ECoordSystem::COORD_None;

}

 

FWidget::EWidgetMode FDZAnimBaseNodeEditMode::GetWidgetMode() const

{

return FWidget::EWidgetMode::WM_None;

}

 

FWidget::EWidgetMode FDZAnimBaseNodeEditMode::ChangeToNextWidgetMode(FWidget::EWidgetMode CurWidgetMode)

{

return FWidget::EWidgetMode::WM_None;

}

 

bool FDZAnimBaseNodeEditMode::SetWidgetMode(FWidget::EWidgetMode InWidgetMode)

{

return false;

}

 

FName FDZAnimBaseNodeEditMode::GetSelectedBone() const

{

return NAME_None;

}

 

void FDZAnimBaseNodeEditMode::EnterMode(UAnimGraphNode_Base* InEditorNode, FAnimNode_Base* InRuntimeNode)

{

 

}

 

void FDZAnimBaseNodeEditMode::ExitMode()

{

 

}

 

void FDZAnimBaseNodeEditMode::Render(const FSceneView* View, FViewport* Viewport, FPrimitiveDrawInterface* PDI)

{

 

}

 

void FDZAnimBaseNodeEditMode::DrawHUD(FEditorViewportClient* ViewportClient, FViewport* Viewport, const FSceneView* View, FCanvas* Canvas)

{

 

}

 

bool FDZAnimBaseNodeEditMode::HandleClick(FEditorViewportClient* InViewportClient, HHitProxy* HitProxy, const FViewportClick& Click)

{

 

}

 

FVector FDZAnimBaseNodeEditMode::GetWidgetLocation() const

{

return FVector::ZeroVector;

}

 

bool FDZAnimBaseNodeEditMode::StartTracking(FEditorViewportClient* InViewportClient, FViewport* InViewport)

{

return true;

}

 

bool FDZAnimBaseNodeEditMode::EndTracking(FEditorViewportClient* InViewportClient, FViewport* InViewport)

{

return true;

}

 

bool FDZAnimBaseNodeEditMode::InputKey(FEditorViewportClient* InViewportClient, FViewport* InViewport, FKey InKey, EInputEvent InEvent)

{

bool bHandled = false;

 

return bHandled;

}

 

bool FDZAnimBaseNodeEditMode::InputDelta(FEditorViewportClient* InViewportClient, FViewport* InViewport, FVector& InDrag, FRotator& InRot, FVector& InScale)

{

 

bool bHandled = false;

 

 

 

return bHandled;

}

 

bool FDZAnimBaseNodeEditMode::GetCustomDrawingCoordinateSystem(FMatrix& InMatrix, void* InData)

{

 

return false;

}

 

bool FDZAnimBaseNodeEditMode::GetCustomInputCoordinateSystem(FMatrix& InMatrix, void* InData)

{

return GetCustomDrawingCoordinateSystem(InMatrix, InData);

}

 

bool FDZAnimBaseNodeEditMode::ShouldDrawWidget() const

{

return true;

}

 

void FDZAnimBaseNodeEditMode::DoTranslation(FVector& InTranslation)

{

 

}

 

void FDZAnimBaseNodeEditMode::DoRotation(FRotator& InRotation)

{

 

}

 

void FDZAnimBaseNodeEditMode::DoScale(FVector& InScale)

{

 

}

 

void FDZAnimBaseNodeEditMode::Tick(FEditorViewportClient* ViewportClient, float DeltaTime)

{

 

}

 

void FDZAnimBaseNodeEditMode::ConvertToComponentSpaceTransform(const USkeletalMeshComponent* SkelComp, const FTransform & InTransform, FTransform & OutCSTransform, int32 BoneIndex, EBoneControlSpace Space)

{

 

}

 

 

void FDZAnimBaseNodeEditMode::ConvertToBoneSpaceTransform(const USkeletalMeshComponent* SkelComp, const FTransform & InCSTransform, FTransform & OutBSTransform, int32 BoneIndex, EBoneControlSpace Space)

{

 

}

 

FVector FDZAnimBaseNodeEditMode::ConvertCSVectorToBoneSpace(const USkeletalMeshComponent* SkelComp, FVector& InCSVector, FCSPose<FCompactHeapPose>& MeshBases, const FName& BoneName, const EBoneControlSpace Space)

{

FVector OutVector = InCSVector;

 

 

return OutVector;

}

 

FQuat FDZAnimBaseNodeEditMode::ConvertCSRotationToBoneSpace(const USkeletalMeshComponent* SkelComp, FRotator& InCSRotator, FCSPose<FCompactHeapPose>& MeshBases, const FName& BoneName, const EBoneControlSpace Space)

{

FQuat OutQuat = FQuat::Identity;

 

 

return OutQuat;

}

 

FVector FDZAnimBaseNodeEditMode::ConvertWidgetLocation(const USkeletalMeshComponent* SkelComp, FCSPose<FCompactHeapPose>& MeshBases, const FName& BoneName, const FVector& Location, const EBoneControlSpace Space)

{

FVector WidgetLoc = FVector::ZeroVector;

return WidgetLoc;

}

 

\#undef LOCTEXT_NAMESPACE

 

### DZAnimStudioPrivatePCH.h

\---------------------------------------------------------------------------------------------------------------------------------------------------

// Copyright 2018 azhecheng, Inc. All Rights Reserved.

\#ifndef __DZAnimStudioPrivatePCH_h__

\#define __DZAnimStudioPrivatePCH_h__

\#include "Engine.h"

\#include "Runtime/Launch/Resources/Version.h"

\#include "DZAnimStudio.h"

\#endif

 

 

### DZAnimStudio.Build.cs

\---------------------------------------------------------------------------------------------------------------------------------------------------

// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.

 

using UnrealBuildTool;

using System.IO;

public class DZAnimStudio : ModuleRules

{

\#if WITH_FORWARDED_MODULE_RULES_CTOR

​    public DZAnimStudio(ReadOnlyTargetRules Target) : base(Target)

\#else

public DZAnimStudio(TargetInfo Target)

\#endif

{

PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "Public"));

PublicIncludePaths.Add(ModuleDirectory);

PublicIncludePaths.AddRange(

new string[] {

"Runtime/Core/Public/Modules",

"Runtime/AnimGraphRuntime/Public/BoneControllers",

// ... add other public include paths required here ...

}

);

 

 

PrivateIncludePaths.AddRange(

new string[] {

"DZAnimStudio/Private",

// ... add other private include paths required here ...

}

);

 

 

PublicDependencyModuleNames.AddRange(

new string[]

{

"Core",

"CoreUObject",

"Engine",

"Slate",

"AnimGraphRuntime",

// ... add other public dependencies that you statically link with here ...

}

);

}

}

 

 

###  

### DZ_AnimNode_SnapIK.h

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#include "Misc/CoreMisc.h"

\#include "Stats/Stats.h"

\#include "Engine/EngineTypes.h"

\#include "EngineDefines.h"

\#include "AnimNode_SkeletalControlBase.h"

\#include "DZ_AnimNode_SnapIK.generated.h"

 

 

USTRUCT(BlueprintInternalUseOnly)

struct DZANIMSTUDIO_API FDZ_AnimNode_SnapIK : public FAnimNode_SkeletalControlBase

{

GENERATED_USTRUCT_BODY()

 

// Called to gather on-screen debug data. This is called on the game thread.

virtual void GatherDebugData(FNodeDebugData& DebugData) override;

 

// Evaluate the new component-space transforms for the affected bones.

virtual void EvaluateSkeletalControl_AnyThread(FComponentSpacePoseContext& Output, TArray<FBoneTransform>& OutBoneTransforms) override;

 

// Return true if it is valid to Evaluate

virtual bool IsValidToEvaluate(const USkeleton* Skeleton, const FBoneContainer& RequiredBones) override;

 

private:

// Initialize any bone references you have

virtual void InitializeBoneReferences(const FBoneContainer& RequiredBones) override;

 

};

 

 

 

### DZAnimNode_ScaleBone.h

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#include "DZAnimStudioCore.h"

\#include "AnimNode_SkeletalControlBase.h"

\#include "DZAnimNode_ScaleBone.generated.h"

 

 

 

USTRUCT()

struct DZANIMSTUDIO_API FDZAnimNode_ScaleBone : public FAnimNode_SkeletalControlBase

{

GENERATED_USTRUCT_BODY()

 

public:

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = BodyBone)

TArray<FDZScaleBoneData> mEdBoneList;

 

// FAnimNode_Base interface

virtual void GatherDebugData(FNodeDebugData& DebugData) override;

// End of FAnimNode_Base interface

\#if ENGINE_MINOR_VERSION >= 16

virtual void EvaluateSkeletalControl_AnyThread(FComponentSpacePoseContext& Output, TArray<FBoneTransform>& OutBoneTransforms) override;

\#else

virtual void EvaluateBoneTransforms(USkeletalMeshComponent* SkelComp, FCSPose<FCompactPose>& MeshBases, TArray<FBoneTransform>& OutBoneTransforms) override;

\#endif

virtual bool IsValidToEvaluate(const USkeleton* Skeleton, const FBoneContainer& RequiredBones) override;

private:

// FAnimNode_SkeletalControlBase interface

virtual void InitializeBoneReferences(const FBoneContainer& RequiredBones) override;

};

 

 

 

### DZAnimStudio.h

\---------------------------------------------------------------------------------------------------------------------------------------------------

// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.

 

\#pragma once

 

\#include "CoreMinimal.h"

\#include "Modules/ModuleManager.h"

 

class FDZAnimStudioModule : public IModuleInterface

{

public:

 

/** IModuleInterface implementation */

virtual void StartupModule() override;

virtual void ShutdownModule() override;

};

 

 

 

### DZAnimStudio_Check_BluprintFunction.h

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#pragma once

//#include "CoreMinimal.h"

//#include "Kismet/BlueprintFunctionLibrary.h"

//#include "DZAnimStudio_Check_BluprintFunction.generated.h"

//

//

//class DZANIMSTUDIO_API UDZAnimStudio_CheckAnim_BluprintFuntion :public UBlueprintFunctionLibrary

//{

//        GENERATED_BODY();

//public:

//

//        UFUNCTION(BlueprintCallable, Category = "DZAnimStudio|PlayAnimBluprintFuntion", meta = (WorldContext = "WorldContextObject"))

//        static void DZ_PlayAnimtionMontage();

//};

 

 

 

### DZAnimStudioCore.h

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#pragma once

\#include "Misc/CoreMisc.h"

\#include "Stats/Stats.h"

\#include "Engine/EngineTypes.h"

\#include "EngineDefines.h"

\#include "AnimNode_SkeletalControlBase.h"

\#include "Runtime/Launch/Resources/Version.h"

\#include "DZAnimStudioCore.generated.h"

 

UENUM()

enum EDZBoneModificationMode

{

/** The modifier ignores this channel (keeps the existing bone translation, rotation, or scale). */

DZBMM_Ignore UMETA(DisplayName = "Ignore"),

 

/** The modifier replaces the existing translation, rotation, or scale. */

DZBMM_Replace UMETA(DisplayName = "Replace Existing"),

 

/** The modifier adds to the existing translation, rotation, or scale. */

DZBMM_Additive UMETA(DisplayName = "Add to Existing")

};

 

/************************************************************************/

/*    *Editer Bone Item Config Data

*@Author: BaiPaoXD                                                     * /

/************************************************************************/

USTRUCT(BlueprintType)

struct FDZScaleBoneData

{

GENERATED_USTRUCT_BODY()

public:

UPROPERTY(EditAnywhere, Category = EDITBOBE)

FBoneReference mEd_Bone;

UPROPERTY(EditAnywhere, Category = EDITBOBE)

TEnumAsByte<EDZBoneModificationMode> ScaleMode;

UPROPERTY(EditAnywhere, Category = EDITBOBE)

TEnumAsByte<enum EBoneControlSpace> ScaleSpace;

/** New Scale of bone to apply. This is only worldspace. */

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = EDITBOBE, meta = (PinShownByDefault))

FVector Scale;

};

 

USTRUCT()

struct FDZAnimStudioBoneTransform

{

GENERATED_USTRUCT_BODY()

 

UPROPERTY()

int32 BoneIndex;

 

UPROPERTY()

FTransform Transform;

};

 

struct DZANIMSTUDIO_API FDZAnimStudioCore

{

static FVector GetCurrentLocation(FCSPose<FCompactPose>& MeshBases, const FCompactPoseBoneIndex& BoneIndex);

};

 

 

### *DZ_AnimNode_SnapIK.cpp*

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#include "DZ_AnimNode_SnapIK.h"

\#include "AnimationRuntime.h"

\#include "Animation/AnimInstanceProxy.h"

 

void FDZ_AnimNode_SnapIK::GatherDebugData(FNodeDebugData& DebugData)

{

 

}

 

void FDZ_AnimNode_SnapIK::EvaluateSkeletalControl_AnyThread(FComponentSpacePoseContext& Output, TArray<FBoneTransform>& OutBoneTransforms)

{

 

}

 

bool FDZ_AnimNode_SnapIK::IsValidToEvaluate(const USkeleton* Skeleton, const FBoneContainer& RequiredBones)

{

return false;

}

 

void FDZ_AnimNode_SnapIK::InitializeBoneReferences(const FBoneContainer& RequiredBones)

{

 

}

 

 

 

### *DZAnimNode_ScaleBone.cpp*

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#include "DZAnimNode_ScaleBone.h"

\#include "DZAnimStudioPrivatePCH.h"

\#include "AnimationRuntime.h"

\#include "Animation/AnimInstanceProxy.h"

 

//FDZAnimNode_ScaleBone::FDZAnimNode_ScaleBone()

//{

//

//}

 

void FDZAnimNode_ScaleBone::GatherDebugData(FNodeDebugData& DebugData)

{

 

}

/************************************************************************/

/* 白袍小道 骨骼节点缩放                                                */

/************************************************************************/

\#if ENGINE_MINOR_VERSION >= 16

void FDZAnimNode_ScaleBone::EvaluateSkeletalControl_AnyThread(FComponentSpacePoseContext & Output, TArray<FBoneTransform>& OutBoneTransforms)

{

const FBoneContainer& BoneContainer = Output.Pose.GetPose().GetBoneContainer();

\#else

void FDZAnimNode_ScaleBone::EvaluateBoneTransforms(USkeletalMeshComponent * SkelComp, FCSPose<FCompactPose>& MeshBases, TArray<FBoneTransform>& OutBoneTransforms)

{

const FBoneContainer& BoneContainer = MeshBases.GetPose().GetBoneContainer();

\#endif

for (int i = 0; i < this->mEdBoneList.Num(); i++)

{

FCompactPoseBoneIndex CompactPoseBoneToModify = this->mEdBoneList[i].mEd_Bone.GetCompactPoseIndex(BoneContainer);

FTransform NewBoneTM = Output.Pose.GetComponentSpaceTransform(CompactPoseBoneToModify);

FTransform ComponentTransform = Output.AnimInstanceProxy->GetComponentTransform();

if (this->mEdBoneList[i].ScaleMode != DZBMM_Ignore)

{

// Convert to Bone Space.

FAnimationRuntime::ConvertCSTransformToBoneSpace(ComponentTransform, Output.Pose, NewBoneTM, CompactPoseBoneToModify, this->mEdBoneList[i].ScaleSpace);

 

if (this->mEdBoneList[i].ScaleMode == DZBMM_Additive)

{

NewBoneTM.SetScale3D(NewBoneTM.GetScale3D() * this->mEdBoneList[i].Scale);

}

else

{

NewBoneTM.SetScale3D(this->mEdBoneList[i].Scale);

}

// Convert back to Component Space.

FAnimationRuntime::ConvertBoneSpaceTransformToCS(ComponentTransform, Output.Pose, NewBoneTM, CompactPoseBoneToModify, this->mEdBoneList[i].ScaleSpace);

}

 

OutBoneTransforms.Add(FBoneTransform(this->mEdBoneList[i].mEd_Bone.GetCompactPoseIndex(BoneContainer), NewBoneTM));

}

}

 

bool FDZAnimNode_ScaleBone::IsValidToEvaluate(const USkeleton* Skeleton, const FBoneContainer& RequiredBones)

{

for (int i = 0; i < this->mEdBoneList.Num(); i++)

{

if (!this->mEdBoneList[i].mEd_Bone.IsValidToEvaluate(RequiredBones)) {

return false;

}

}

// if both bones are valid

return true;

}

 

void FDZAnimNode_ScaleBone::InitializeBoneReferences(const FBoneContainer& RequiredBones)

{

for (int i = 0; i < this->mEdBoneList.Num(); i++)

{

this->mEdBoneList[i].mEd_Bone.Initialize(RequiredBones);

}

 

}

 

 

 

### *DZAnimStudio.cpp*

\---------------------------------------------------------------------------------------------------------------------------------------------------

// Copyright 1998-2018 Epic Games, Inc. All Rights Reserved.

 

\#include "DZAnimStudio.h"

 

\#define LOCTEXT_NAMESPACE "FDZAnimStudioModule"

 

void FDZAnimStudioModule::StartupModule()

{

// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module

}

 

void FDZAnimStudioModule::ShutdownModule()

{

// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,

// we call this function before unloading the module.

}

 

\#undef LOCTEXT_NAMESPACE

 

IMPLEMENT_MODULE(FDZAnimStudioModule, DZAnimStudio)

 

 

###  

### *DZAnimStudio_Check_BluprintFunction.cpp*

\---------------------------------------------------------------------------------------------------------------------------------------------------

//#include "DZAnimStudio_Check_BluprintFunction.h"

//

//void UDZAnimStudio_CheckAnim_BluprintFuntion::DZ_PlayAnimtionMontage()

//{

//

//}

###  

### *DZAnimStudioCore.cpp*

\---------------------------------------------------------------------------------------------------------------------------------------------------

\#include "DZAnimStudioCore.h"

\#include "DZAnimStudioPrivatePCH.h"

\#include "AnimationRuntime.h"

\#include "Animation/AnimCompress.h"

\#include "Components/SkeletalMeshComponent.h"

\#include "Animation/AnimNotifies/AnimNotify.h"

FVector FDZAnimStudioCore::GetCurrentLocation(FCSPose<FCompactPose>& MeshBases, const FCompactPoseBoneIndex& BoneIndex)

{

return MeshBases.GetComponentSpaceTransform(BoneIndex).GetLocation();

}

 

 
