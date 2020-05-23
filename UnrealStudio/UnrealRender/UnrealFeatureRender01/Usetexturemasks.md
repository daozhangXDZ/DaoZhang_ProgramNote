﻿**使用纹理遮罩**

2019年4月28日

1:41

 

创建 3D 资产时，您可能需要在同一材质中定义不同的表面类型。 实现此目标的一种简单而低成本的方法是使用 **纹理蒙版**，它可定义哪个表面应该受材质的哪个部分影响。 在以下操作指南中，我们将阐述如何在虚幻引擎 4 (UE4) 材质中使用纹理遮罩。

**纹理蒙板**

纹理蒙版是灰阶纹理，或者是纹理的单个通道（R、G、B 或 A），用于限制 **材质** 内受效果影响的区域。 蒙版通常包含在另一个纹理的单个通道内，例如漫射贴图或法线贴图的 **阿尔法通道**。 这是一种利用未使用的通道，将材质中取样的纹理数保持在最低限度的好办法。 在技术上，您可将任何纹理的任何通道视作并用作纹理蒙版。

以下是起步内容中 SM_Chair 静态网格的纹理蒙版的外观示例。

![TM_Chair_Mask_Texture.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image002.jpg)

**创建纹理蒙版**

创建纹理蒙版这一任务可以在任何 2D 图像处理程序中完成。 要完成此任务，您只需将需要遮罩的区域涂为白色，而保留所有其他区域为黑色。 在下图中，我们可以看到作用中的蒙版。

![TM_Mask_Break_Down.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image004.jpg)

在右侧，绿色外框内的内容就是蒙版纹理的外观。 请注意，只有几个区域涂为白色，而所有其他区域均涂为黑色。 这是因为，我们只希望影响白色区域。 在左侧，您可看到此蒙版纹理应用于椅子网格时，将会遮罩哪些区域。

创建纹理蒙版时，您应始终使用黑色或白色，切勿使用彩色信息。使用任何其他类型的颜色可能会导致在 UE4 中使用该蒙版时产生奇怪的伪影。

**导出纹理蒙版**

绘制蒙版纹理完成后，您可将其导出为单个图像，也可将多个蒙版一起打包到单个图像的 R、G、B 和 A 通道并导出该图像。 这通常称为“RGB 蒙版”打包，并且是创建蒙版纹理时的首选方法，因为这样可以提高性能并节省内存，而且需要完成的额外工作非常少。

如果您的确将一些内容打包到纹理的阿尔法通道中，请务必记得在您所使用的 2D 图像处理软件中启用阿尔法导出。 否则，就有导出纹理时不导出阿尔法通道的风险。

**使用纹理蒙版**

在 UE4 材质编辑器中，可以通过许多不同方式来使用蒙版纹理。 这包括定义自发光光源，也包括用作粗糙度纹理。 在下一节，我们将阐述一些在 UE4 中使用纹理遮罩的最常用方法。

**自发光蒙版**

使用蒙版纹理来完成的最常见任务之一是，使用它来控制材质的自发光部分。完成此任务时，通常先创建一个 使用白色来定义材质的哪些部分应该自发光的自发光蒙版纹理，然后在材质编辑器内将该蒙版纹理与某种颜色相乘。 这样，您就会对自发光效果的外观及强度拥有更大的控制权。 在以下示例中，我们可以看到作用中的自发光纹理遮罩。

![TM_Emissive_Mask_Materail.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image006.jpg)

在以上示例中，使用了蒙版纹理来帮助定义材质的哪些部分应该自发光。 用于自发光的颜色是将蒙版纹理与一个矢量 3 参数相乘计算而得。 自发光强度由一个标量值控制。 以此方式使用自发光遮罩的主要优点是，每当您需要更改与自发光外观相关的内容时，您只需 更改材质内的参数，而不必更新并重新导入纹理。

**材质遮罩**

使用蒙版纹理完成的另一项最常见任务是，将不同类型的纹理信息存储到个别的 R、G、B 和阿尔法通道中。 只要查看起步内容随附的 SM_Chair 静态网格，您就可找到这种技术的一个完美示例。

要找到 SM_Chair 及其随附的所有内容，请先在 **内容浏览器** 中选择 **起步内容（****Starter Content****）**文件夹，然后在搜索框中输入 “chair” 这将显示所有与这个椅子相关的内容。如果您看不到这个椅子，那么可能表示您未将起步内容包括在您的项目中。 要解决此问题，您需要创建新项目，或尝试使用 [迁移资产](http://api.unrealengine.com/CHN/Engine/Content/Browser/UserGuide/Migrate/index.html) 工具将椅子内容从另一个项目移至 此项目。

打开椅子材质 M_Chair，我们可以看到作用中的纹理贴图完美示例。

![TM_Chair_Material.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image008.jpg)

在此材质中，使用蒙版纹理 **T_Chair_M** 来控制椅子外观的每个方面。 从哪些部分应该是金属或非金属，到这些部分应该具有何种颜色，都可在蒙版纹理的帮助下定义。 在下图中，您可看到有关 SM_Chair 的蒙版纹理中每个通道的工作方式明细。 左侧是作为纹理的蒙版的样子。 右侧的小图像显示每个通道以及这些通道在椅子静态网格上影响的区域。

![TM_Mask_Example.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image010.jpg)

以下是椅子蒙版纹理的每个通道内存储的信息类型的明细。

·         **红色通道**：环境光遮蔽信息。在材质中，此信息用来帮助向底色添加一些表面变化。

![TM_Red_Channel.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image012.jpg)

·         **绿色通道**：金属色蒙版。在材质中，此信息用来定义哪些部分应该是金属。此信息也用来帮助定义金属应该具有的颜色。 

![TM_Green_Channel.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image014.jpg)

·         **蓝色通道**：非金属色蒙版。在材质中，此信息用来定义哪些部分不是金属。此蒙版还可帮助定义非金属部分的颜色。

![TM_Blue_Channel.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image016.jpg)

·         **阿尔法通道**：整体对象蒙版。此材质目前不使用这个蒙版。

将所有内容集合到一起之后，这个椅子在 UE4 图层中显示如下：

![TM_SM_Chair.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image018.jpg)

**遮罩提示与技巧**

纹理遮罩是一个功能非常强大的工具，与 UE4 中的其他工具结合使用时更是如此。在下一节中，我们将了解一些提示与技巧，以便 在您的工作中充分发挥纹理遮罩的强大功能。

**纹理遮罩与材质分隔**

将纹理遮罩与材质实例化配合使用是一种相当不错的方法，这可以向任何资产添加几乎无穷无尽的变化。 例如，您可使用纹理蒙版来定义哪些区域应具有特定属性（例如颜色），然后使用不同的材质实例来更改其中每个属性，从而产生几乎无穷无尽的选项变化。

![TM_TM_&_MI.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image020.jpg)

例如，根据 SM_Chair 材质建立材质实例后，我们可以调整颜色和其他值，从而提供几乎无穷无尽的不同外观的椅子，如上图所示。

**遮罩与通道失真**

由于 DirectX 的一个特点，纹理的绿色通道通常可以提供最佳的压缩率。如果您的任何蒙版存在严重的压缩失真问题，请先尝试将信息放入绿色通道，以确定是否有所裨益。如果这样做无法解决问题，请尝试使用阿尔法通道来存储信息。

当您尝试使用纹理的阿尔法通道来存储蒙版纹理时，务请谨慎。向纹理添加阿尔法通道会大大增加该纹理的内存用量， 达到一定程度时，可能会抵消通过将不同蒙版纹理打包到纹理的 RGB 通道而实现的所有裨益。

**sRGB** **与蒙版纹理**

将多个蒙版纹理打包到单个纹理时，应该禁用 sRGB，因为您的蒙版不应进行伽玛校正。

![TM_Disable_sRGB.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image022.jpg)

但是，您这样做时，需要确保调整“2D 纹理取样”（2D Texture Samplers）节点类型，因为它们期望输入的纹理启用 sRGB。 如果您未更改“取样类型”（Sampler Type），那么您的材质将无法通过编译，并且在“统计信息”（Stats）日志中将显示以下消息。

![TM_sRGB_Sampler_Node_Error.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image024.jpg)

要更正此错误，您只需将“取样类型”（Sampler Type）从默认值“颜色”（Color）更改为“线性颜色”（Linear Color），这个警告就会消失。 但是，为了保险起见，请重新编译材质，以确保更改生效。完成后，这个警告就会消失，材质现在已可供使用。

**总结**

纹理遮罩是功能非常强大的概念，您一旦掌握此概念，就可以使用非常少量的来源内容创建几乎无穷无尽的变化。 请记住，对于每个蒙版纹理，只有 4 个可以与其配合使用的通道，因此您应该明智地加以使用。 另外，请不要忘记对蒙版纹理禁用 sRGB，因为这对提高蒙版清晰度有很大帮助。

 

来自 <<http://api.unrealengine.com/CHN/Engine/Rendering/Materials/HowTo/Masking/index.html>> 

 