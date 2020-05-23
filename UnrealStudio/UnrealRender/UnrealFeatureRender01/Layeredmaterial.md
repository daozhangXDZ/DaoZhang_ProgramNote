**分层材质**

2019年4月28日

1:40

 

在这个简短教程中，我们将概述创建简单 **分层材质** 的过程，该材质包含两个材质层：铬合金和雪。最终的分层材质会自动将雪置于对象的顶部表面，从而在两种材质之间有效地进行切换。材质之间的混合将总是检查顶部表面，这意味着即使您旋转对象，雪也总是停留在顶部。

创建材质层时，通常将层创建为材质，然后将节点网络复制/粘贴到新函数中。但是，为了节省时间，我们先在函数内构建层。

**简单铬合金**

| **铬合金纹理**                                               |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [![T_ExampleLayers_Metal01_BC.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image002.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/T_ExampleLayers_Metal01_BC.png) | [![T_ExampleLayers_Metal01_N.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image004.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/T_ExampleLayers_Metal01_N.png) |
| **T_ExampleLayers_Metal_1_BC.png**                           | **T_ExampleLayers_Metal01_N.png**                            |
| **（右键单击并选择“另存为”）**                               | **（右键单击并选择“另存为”）**                               |

在第一个材质层中，我们将创建一个相当简单的铬合金，其表面有少许腐蚀或瑕疵。为了帮助说明一些可编辑性，我们还将创建一些输入来控制整体外观。

\1.     在 **内容浏览器** 中，单击 **新增（****Add New****）**按钮并选择 **材质与纹理（****Materials & Textures****）**> **材质函数（****Material Function****）**。

![NewFunction.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image005.jpg)

\2.     将新函数命名为 **Layer_Chrome**。

![Layer_Chrome.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image006.jpg)

**3.**    **双击** 该函数，以在材质编辑器中将其打开。

![EditLayerChrome.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image008.jpg)

\4.     在材质图区域中 **右键单击** 以打开快捷菜单，搜索 **Make** 并选择 **建立材质属性（****Make Material Attributes****）**。

![MakeMaterialAttributesContext.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image009.jpg)

\5.     将新的 *建立材质属性（**Make Material Attributes**）* 节点连接到 *输出结果（**Output Result**）*。

![ConnectedMMA.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image011.jpg)

**铬合金层网络**

此材质层的网络相当简单。为了加快构建速度，它已进行拆分。使用的两个纹理分别是 **T_ExampleLayers_Metal_1_BC.png**（用于底色及粗糙度）和 **T_ExampleLayers_Metal01_N.png**（用于法线贴图），这两个纹理均可从本页顶部下载。

**请单击以查看标准大小的图片，或者右键单击并选择****“****另存为****”****（****Save As****）**

[![ChromGraph.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image013.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/ChromGraph.png)

此材质层已拆分为注释块，说明如下：

**1.**    **底色（****Base Color****）**- 此部分的网络非常简单。我们已设置线性插值，该插值在铬合金底色与非常深的灰色之间进行混合。底色实际上是名为 *Tint* 的函数输入。这个输入设置为 Vector3，从而允许我们将颜色输入到函数中，并更改铬合金颜色。我们使用 *T_ExampleLayers_Metal_1_BC* 纹理的红色通道在这两者之间驱动插值。

**2.**    **金属色（****Metallic****）**- 因为我们要创建金属，所以将“金属色”（Metallic）设置为 1。

**3.**    **粗糙度（****Roughness****）**- 我们是在创建铬合金，因此粗糙度通常非常低。但是，我们要在较暗的区域稍稍加大粗糙度，以使材质整体看起来有一定的深度。实际上，除了仅仅在 0.2 与 0.4 之间插值之外，此网络与用于底色（Base Color）的网络相同。

**4.**    **可定制的法线（****Customizable Normal****）**- 此网络仅仅接收切线空间法线贴图，并分隔控制着大量贴图细节的绿色和红色通道。我们将每个通道乘以从另一个函数输入提供的值。此输入设置为标量类型，名为 *Normal Multiplier*，其默认值为 1.0。产生的结果将通过“附加矢量”（AppendVector）节点附加到一起，然后附加到法线贴图的蓝色通道。这样，用户就能够通过更改“法线乘数”（Normal Multiplier）值来调整法线的高度。

完成后，务请保存材质层函数。

**简单的雪**

| **雪纹理**                                                   |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [![T_Cave_Ice_Tiling_D.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image015.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/T_Cave_Ice_Tiling_D.png) | [![T_Cave_Ice_Noise_N.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image017.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/T_Cave_Ice_Noise_N.png) |
| **T_Cave_Ice_Tiling_D.png**                                  | **T_Cave_Ice_Noise_N.png**                                   |
| **（右键单击并选择“另存为”）**                               | **（右键单击并选择“另存为”）**                               |

现在，我们创建雪效果材质层：

\1.     在 **内容浏览器** 中，单击 **新增（****Add New****）**按钮并选择 **材质与纹理（****Materials & Textures****）****>** **材质函数（****Material Function****）**。

![NewFunction.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image005.jpg)

\2.     将新函数命名为 **Layer_Snow**。

![Layer_Snow.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image018.jpg)

**3.**    **双击** 该函数，以在材质编辑器中将其打开。

![EditLayerChrome.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image020.jpg)

\4.     在材质图区域中 **右键单击** 以打开快捷菜单，搜索 **Make** 并选择 **建立材质属性（****Make Material Attributes****）**。

![MakeMaterialAttributesContext.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image009.jpg)

\5.     将新的 *建立材质属性（**Make Material Attributes**）* 节点连接到 *输出结果（**Output Result**）*。

![ConnectedMMA.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image021.jpg)

**雪层网络**

下图是雪材质层的简单明细。这个层使用 **T_Cave_Ice_Tiling_D.png** 和 **T_Cave_Ice_Noise_N.png**，这两个纹理均可从本页顶部下载。

**请单击以使用完整大小，或者右键单击并选择****“****另存为****”****（****Save As****）**

[![SnowNetwork.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image023.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/SnowNetwork.png)

**1.**    **底色（****Base Color****）**- 这可能是此网络中唯一相对复杂的部分，这仅仅是因为使用了 *FuzzyShading* 材质函数。此函数的作用仅仅是避免材质在接收到光线时变得太暗。这有点像光线穿过纤维状表面。因此它是用于天鹅绒、苔藓或本例中的雪的完美选择。首先，我们处理底色（Base Color）纹理 (T_Cave_Ice_Tiling_D.png)，通过对它进行 0.3 幂运算来消除一定的对比度。
 接着，我们将结果插入 FuzzyShading 材质函数，该函数可从材质编辑器的“函数”（Functions）选项卡拉取。将 *核心暗度（**Core Darkness**）* 设置为 0，将 *幂（**Power**）* 设置为 1，并将 *边缘亮度（**EdgeBrightness**）* 设置为 0.5。最后，我们将整体结果乘以非常淡的蓝色 (R=0.8, G=0.9, B=0.95)，产生一种冰冷的颜色投射效果。

**2.**    **金属色（****Metallic****）**- 这是非金属表面，所以将“金属色”（Metallic）设置为 0。

**3.**    **粗糙度（****Roughness****）**- 我们希望雪在受到光线直射时发出一点光亮，因此使用 _Cave_Ice_Tiling_D.png 纹理的红色通道来驱动 0.6 与 0.3 之间的插值。

**4.**    **法线（****Normal****）**- 此设置也相当基本。我们希望降低切线空间法线贴图的效果，这可通过成倍增强蓝色通道来实现。加强蓝色会降低法线贴图高度的整体外观。

完成后，请保存结果！

**分层材质**

现在，我们可以使用目前为止生成的层来创建分层材质。我们将稍微增大空间以进行实例定制，使得雪总是出现在表面的顶部。

\1.     在 **内容浏览器** 中，单击 **新增（****Add New****）**按钮并从快捷菜单中选择“材质”（Material）。

![NewMaterialContextMenu.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image024.jpg)

\2.     将新函数命名为 **Mat_SnowyChrome**。

![Mat_SnowyChrome.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image025.jpg)

**3.**    **双击** 该材质，以在材质编辑器中将其打开。

![SnowyChromeMatEd.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image027.jpg)

\4.     从 **内容浏览器** 拖放上述步骤中创建的 **Layer_Chrome** 和 **Layer_Snow** 材质层。

[![cnd_Chrome_Snow.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image029.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/cnd_Chrome_Snow.png)

\5.     在 **细节（****Details****）**面板中，启用 **使用材质属性（****Use Material Attributes****）**。

![enableMatAttrib.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image030.jpg)

\6.     在“函数”（Functions）面板中，拖入 **MatLayerBlend_Simple** 函数和 **World_Aligned_Blend** 函数。我们将使用 MatLayerBlend_Simple 来处理从铬合金到雪的过渡，并使用 World_Aligned_Blend 根据表面的方向加强层混合效果。

**分层材质网络**

以下是 Mat_SnowyChrome 网络的明细以及每个注释区域的说明。

**请单击以查看标准大小的图片，或者右键单击并选择****“****另存为****”****（****Save As****）**

[![SnowCoveredChromeNetwork.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image032.jpg)](http://api.unrealengine.com/images/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/SnowCoveredChromeNetwork.png)

**1.**    **铬合金设置（****Chrome Setup****）**- 在此处，我们已引入铬合金材质层，并将 2 个材质参数与之相连。第一个是标量参数 *Chrome Normal*，用于驱动 *法线乘数（**Normal Multiplier**）* 输入。第二个是矢量参数 *Chrome Tint*，用于驱动 *色调（**Tint**）* 输入。这些参数可以用来改变法线贴图的强度，以及稍后进行实例化时更改铬合金颜色。

**2.**    **雪设置（****Snow Setup****）**- 这是最简单的操作：我们只需要雪材质层。

**3.**    **全局一致混合设置（****World Aligned Blend Setup****）**- 在这部分网络中，我们首先将 *混合清晰度（**Blend Sharpness**）* 设置为 10。然后，我们将标量参数 *雪偏差（**Snow Bias**）* 连接到 *混合偏差（**Blend Bias**）* 输入。这样，在将此材质实例化时，就可以编辑雪覆盖范围。

**4.**    **材质层混合（****MatLayerBlend****）**- 仅包含用于驱动混合的节点。基本材质为铬合金。顶部材质为雪。*World_Aligned_Blend* 负责处理过渡。

完成后，请记得保存材质！

**分层材质实例化**

我们已使用参数来设置此材质，这些参数进而驱动材质层的各个方面，现在，我们可以将此材质实例化并进行编辑。此过程在 UE4 中非常简单。

\1.     如果您创建项目时已包括“起步内容”，那么您有可应用新材质的一组椅子和桌子。否则，请随意添加您自己的资产或 BSP。

![DefaultLevel.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image034.jpg)

**2.**    **右键单击** Mat_SnowyChrome 材质，并选择 **创建材质实例（****Create Material Instance****）**。可以接受默认名称。

![CreateMaterialInstance_ContextMenu.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image035.jpg)

\3.     将新实例从 **内容浏览器** 拖放到场景中的某个对象上。

![DragDropMaterialSnowy.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image037.jpg)

**4.**    **双击** 该实例，并根据需要任意更改其属性。您可以更改铬合金的颜色、铬合金法线贴图的深度以及该实例顶部的积雪量。

![SnowChromeInstanceTesting.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image039.jpg)

 

来自 <<http://api.unrealengine.com/CHN/Engine/Rendering/Materials/HowTo/CreatingLayeredMaterials/index.html>> 

 
