# 虚幻4渲染编程（工具篇）【第一卷：开发我们的第一个引擎工具】

2018年12月26日 星期三

15:57

工具篇综述：

很多时候，我们需要一个工具来辅助我们完成一些功能，比如材质编辑器就是一个很好的例子，可以帮我们快速的预览到我们制作的材质，可以边做边看。很多时候技术美术最多写一些脚本插件，但是这些脚本插件功能其实还是很有限的。作为我大UE4教的技术美术，怎么能就此屈服呢，我们就是要写引擎级别的工具。

 

下面我们就先从简单的开始，开发一个能操纵整个关卡编辑器的工具：

先看下效果吧：



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image002.jpg)

我们自己做了一个引擎工具，这个工具有我们自己定义的logo。然后我们有一个界面，这个界面里面有一些按钮和命令，这个按钮可以操作关卡编辑器里的物体。

我这里先做了一个删除选中物体的操作，这只是一个演示。其实我们只要知道了方法，想做很多复杂操作都只是时间问题了，这里只是做个演示。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image004.jpg)

知道方法之后做其他功能就很简单了，比如吸地板



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image006.jpg)

然后点下保存就可以把这些数据保存在关卡里。

 

第一步：

先建立一个引擎用的窗口插件



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image007.jpg)

然后我们就可以在VS中得到如下目录



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image008.jpg)

我们可以得到如下几个文件



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image009.jpg)

 



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image010.jpg)

这个初始模板的代码结构分析在（大象无形-虚幻引擎程序设计浅析）的第210页有详细阐述，我这里就不赘述了。

第二步：

建立我们工具的内容

当完成第一步，我们点击插件只能显示一个空的窗口，我们需要创建我们的按钮。我们创建一个SEventTest.h文件和SEvent.cpp文件，下面是SEvent.h文件

\#include "SEditableTextBox.h"

\#pragma once

DECLARE_DELEGATE_TwoParams(FTestDelegate, FString, FString);

class SEventTest : public SCompoundWidget
 {
 public:

SLATE_BEGIN_ARGS(SEventTest) {}
         SLATE_EVENT(FTestDelegate, OnStartTest)
         SLATE_END_ARGS()

void Construct(const FArguments& InArgs);

private:

FReply OnTestButtonClicked();

FTestDelegate OnTestDelegate;
         TSharedPtr<SEditableTextBox>TestTextOnePtr;
         TSharedPtr<SEditableTextBox>TestTextTwoPtr;
         TSharedPtr<SButton>TestButtonPtr;

};

SEvent.cpp

\#include "SEventTest.h"
 \#include "STextBlock.h"

\#define LOCTEXT_NAMESPACE "SEventTest"

void SEventTest::Construct(const FArguments& InArgs)

{

        OnTestDelegate =
InArgs._OnStartTest;

        ChildSlot

        [

                SNew(SVerticalBox)

                //-----------------------------//

                +
SVerticalBox::Slot()

                [

                        SNew(SHorizontalBox)

                        +
SHorizontalBox::Slot()

                        [

                                SNew(SBox)

                                .HeightOverride(20.0f)

                                .WidthOverride(60.0f)

                                [

                                        SNew(STextBlock)

                                        .Text(LOCTEXT("TextDefaultValue0","SnapCamera
:"))

                                ]

                        ]

                        +
SHorizontalBox::Slot()

                        [

                                SNew(SBox)

                                .HeightOverride(20.0f)

                                .WidthOverride(150.0f)

                                [

                                        SAssignNew(TestButtonPtr,
SButton)

                                        .OnClicked(this,
&SEventTest::OnTestButtonClicked)

                                        .Text(LOCTEXT("Login",
"SnapCameraButton"))

                                ]

                        ]

                ]

                //-----------------------------//

                +
SVerticalBox::Slot()

                [

                        SNew(SHorizontalBox)

                        +
SHorizontalBox::Slot()

                        [

                                SNew(SBox)

                                .HeightOverride(20.0f)

                                .WidthOverride(150.0f)

                                [

                                        SNew(STextBlock)

                                        .Text(LOCTEXT("TextDefaultValue1",
"SecondTestLine"))

                                ]

                        ]

                ]

        ];

}

FReply SEventTest::OnTestButtonClicked()
 {
         //FString usn = TestTextOnePtr->GetText().ToString();
         //FString pwd = TestTextTwoPtr->GetText().ToString();

OnTestDelegate.ExecuteIfBound(TEXT("aa"), TEXT("bb"));
         return FReply::Handled();
 }

\#undef LOCTEXT_NAMESPACE

然后再创建WidgetDemo.h和WidgetDemo.cpp

\#pragma once

class SWidgetDemo : public SCompoundWidget
 {
 public:

SLATE_BEGIN_ARGS(SWidgetDemo){}
         SLATE_EVENT(FTestDelegate, OnStartTest)
         SLATE_END_ARGS()

void Construct(const FArguments& InArgs);

void OnMyTest(FString usn, FString pwd);

};

WidgetDemo.cpp

\#include "WidgetDemo.h"
 \#include "SEventTest.h"

\#include "LevelEditorActions.h"
 \#include "Engine/Selection.h"

\#define LOCTEXT_NAMESPACE "SWidgetdemo"

void SWidgetDemo::Construct(const FArguments& InArgs)
 {
                 ChildSlot
                 .HAlign(HAlign_Left)
                 [
                         SNew(SEventTest).OnStartTest(this, &SWidgetDemo::OnMyTest)
                 ];
 }

void SWidgetDemo::OnMyTest(FString usn, FString pwd)
 {
         FLevelEditorActionCallbacks::SnapObjectToView_Clicked();
         for (FSelectionIterator It(GEditor->GetSelectedActorIterator()); It; ++It)
         {
                 AActor* Actor = Cast<AActor>(*It);
                 Actor->Modify();
                 Actor->Destroy();
         }
 }

\#undef LOCTEXT_NAMESPACE

然后在PandaTools,cpp中对OnSpawnPluginTab做如下修改

再启动引擎能看到我们的工具了

最后再给以下我的工程完整目录



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image011.jpg)

 

下面对上述代码作解释：

SEvent.h



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image012.jpg)

这里声明了一个SEventTest类，派生自Slate的最基础的SCompoundWidget。这里我们声明了一个代理。关于代理如果不太理解了话，可以去看看我下面这篇博客：

[从仿函数到std::function再到虚幻4 Delegateblog.csdn.net](http://link.zhihu.com/?target=https%3A//blog.csdn.net/qq_16756235/article/details/79135798)

[![图标](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image014.jpg)](http://link.zhihu.com/?target=https%3A//blog.csdn.net/qq_16756235/article/details/79135798)

这里会保存外部传进来的方法



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image015.jpg)

构建函数里将按钮的OnClicked与OnTestButtonClicked函数绑定。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image016.jpg)

我曾在这里被绕晕了，再来捋一下这个调用吧。

在SWidgetDemo的construct函数中，我们在SEventTest构造的时候，把函数指针传进其构造函数

然后在SEventTest的构造函数中，OnTestDelegate与OnMyTest完成绑定



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image017.jpg)

然后再把俺就的OnClicked与OnTestButtonClicked绑定。当我们按动按键的时候，回去执行

OnTestButtonClicked。OnTestButtonClicked再去执行和它绑定的函数



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image018.jpg)

此时和OnTestDelegate绑定的是OnMyTest函数于是下面的逻辑就可以执行了



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image020.jpg)

在这个OnMyTest函数中，我们直接去调用GEditor的逻辑得到此时编辑器选中的物体，然后对它进行操作。

在FLevelEditorActionCallbacks中还有很多有趣的命令，我们可以用同样的方法写我们的工具逻辑



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image021.jpg)

于是乎以后我们想对我们开发的什么效果通过工具来调试就十分方便了。以前还碰到有一个怪物管理系统，比如在A据点的怪物战队的战力配置，在B据点怪物的战力和种类配置，也可以通过这个思路完成。还比如前段时间做的布料模拟效果，因为我的逻辑是在c++层的，我可以通过这种方式，直接在编辑器层设置数值然后把数值set给我的底层类，等等。

下面是吸地板的代码：



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image023.jpg)

bool SWidgetDemo::RayTracingHit(FVector RayOrigin, FVector RayDirection, float RayMarhingLength, FHitResult& OutHitResoult, AActor* OperatedActor)
 {
         const TArray<AActor*>IgActor;
         FVector startpos = RayOrigin;
         FVector endpos = RayOrigin + RayDirection * RayMarhingLength;
         return UKismetSystemLibrary::LineTraceSingle(
                 OperatedActor,
                 startpos,
                 endpos,
                 ETraceTypeQuery::TraceTypeQuery1,
                 false,
                 IgActor,
                 EDrawDebugTrace::Type::None,
                 OutHitResoult,
                 true,
                 FLinearColor::Blue,
                 FLinearColor::Red,
                 1.0f);
 }

void SWidgetDemo::OnMyTest(FString usn, FString pwd)
 {
         //FLevelEditorActionCallbacks::SnapObjectToView_Clicked();
         for (FSelectionIterator It(GEditor->GetSelectedActorIterator()); It; ++It)
         {
                 AActor* Actor = Cast<AActor>(*It);
                 Actor->Modify();
                 FHitResult OutHit;
                 RayTracingHit(Actor->GetActorLocation(), FVector(0,0,-1), 10000.0f, OutHit, Actor);
                 FVector HitPointLoc = OutHit.Location + OutHit.ImpactNormal * 0.1f;
                 Actor->SetActorLocation(HitPointLoc);
         }
 }

本篇只是做了个很简单的引擎自带的没有必要自己再做一遍的功能，旨在跑通整个工具开发流程。下一篇将开始搞一些实用的工具开发实例。

 

来自 <<https://zhuanlan.zhihu.com/p/41190957>> 
