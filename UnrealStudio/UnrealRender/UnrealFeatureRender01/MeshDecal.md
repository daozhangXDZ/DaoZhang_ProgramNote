**使用模型贴花（****Mesh Decal****）**

2019年4月28日

1:42

 

在以下指南中，我们将为项目启用 Dbuffer 贴花，以便利用贴花材质的灯光特性；并且我们将创建一个可应用至静态网格体的基础延迟贴花材质。

**所需文件**

为重现此指南中的步骤，您需要下载、解压下列 FBX 和纹理文件，并将其导入 UE4。如您不熟悉操作方法，请查阅 [如何导入静态网格体指南](http://api.unrealengine.com/CHN/Engine/Content/ImportingContent/ImportingMeshes/index.html) 和 [如何导入纹理指南](http://api.unrealengine.com/CHN/Engine/Content/ImportingContent/ImportingTextures/index.html) ，了解如何进行操作。

[所需FBX及纹理下载](http://api.unrealengine.com/attachments/Engine/Rendering/Materials/HowTo/MeshDecals/MeshDecalAssets.zip)

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image001.jpg)](http://api.unrealengine.com/attachments/Engine/Rendering/Materials/HowTo/MeshDecals/MeshDecalAssets.zip)

 *（点击右键另存为**...**）*

**为项目启用** **Dbuffer** **贴花**

\1.     在 **Edit** 菜单中点击 **Project Settings** 查看虚幻编辑器选项。

![ProjectSettingsMenu.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image003.jpg)

\2.     在 **Engine** 标题下选择 **Rendering** 部分，找到包含诸多灯光选项的 **Lighting** 类目。

[![ProjectSettings.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image005.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/MeshDecals/ProjectSettings.png)

\3.     现在即可开启 **DBuffer Decals** 选项使用延迟贴花的灯光功能。

![EnableDBufferDecal.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image007.jpg)

\4.     使用此功能前需要先 **重启编辑器**。

![RestartTheEditor.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image009.jpg)

**创建基础延迟贴花**

\1.     在 **Content Browser** 中选择 **Add New** 按钮并选择选项 **Material** 创建新材质。为材质命名，便于之后寻找。为便于此指南的行文之便，此处将其命名为“M_MeshDecal”。

![AddNewMaterial.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image010.jpg)

\2.     选中 **材质**，双击将其打开。材质编辑器打开后，在 **Details** 面板对以下属性进行设置，使其可用作延迟贴花。

·         **Material Domain:**Deferred Decal

·         **Blend Mode:**Translucent

·         **Decal Blend Mode:**DBuffer Translucent Color, Normal, Roughness

·         接下来需要使用此页面 **所需文件** 中的纹理设置材质。该步骤中需要的 .zip 文件中有 3 张纹理：1 张弥散纹理、1 张遮罩纹理和 1 张法线纹理。导入这些材质后，在 **Content Browser** 中选中并将它们拖入材质编辑器图表。

![MaterialGraph1.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image012.jpg)

将 Texture Sample 节点的输出插入主材质节点上相应的输入。将遮罩纹理“T_MeshDecalDamage_M”插入 Opacity Mask 输入时必须使用 **Blue Channel** 输 出。这可确保纹理中蓝色的值用作显示内容的遮罩。

![MaterialGraph2.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image014.jpg)

\4.     在材质图表中点击右键，输入“Constant”，或按住“1”键并在图表中点击添加一个 **Constant** 值节点。将其插入 **Roughness** 输入并设置一个 **0.7** 的默认值。

![MaterialGraph3.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image016.jpg)

\5.     完成之前，我们需要一个方法来控制贴花几何体到基础几何体的偏移，以防止或减轻由于深度精确度引起的穿帮。将以下节点添加到材质图表并将 **Multiply** 节点的输出插入主材质节点的 **World Position Offset** 输入。

![MaterialGraph4.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image017.jpg)

操作完成后，材质图像应与下图相似：

[![FinalMaterialGraph.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image019.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/MeshDecals/FinalMaterialGraph.png)

\6.     延迟贴花材质完成后，将静态网格体“SM_MeshDecal”（包含在所需文件 .zip 包中）放置到关卡中，并将材质 **M_MeshDecal** 应用到静态网格体材质槽的 **Element 0**。可为基础网格体指定任意残值，甚至是 Element 1 的基础色彩，便于展示。最后生成的效果应与下图相似。

**最终结果**

![MeshDecal.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image021.jpg)

完成设置并了解如何自建结合模型贴花使用的材质后，即可放手在建模应用程序中创建资源，自建能充分利用灯光、结合应用的模型贴花使用的材质。

 

来自 <<http://api.unrealengine.com/CHN/Engine/Rendering/Materials/HowTo/MeshDecals/index.html>> 
