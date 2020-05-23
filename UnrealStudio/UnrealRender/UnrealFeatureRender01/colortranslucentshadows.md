# **使用彩色半透明阴影**

2019年4月28日

1:39

 

在本操作指南中，我们将说明如何设置和使用 **半透明阴影颜色** 来创建可以投射彩色阴影的材质。 为场景注入一些颜色适合于许多应用，但最常用于彩绘玻璃窗等物品。

**示例：**

![translucent_T.JPG](./color translucent shadows.assets/clip_image002.jpg)

**半透明阴影颜色**

“半透明阴影颜色”术语用于说明阴影在穿过对象时如何拾取对象的颜色（也称为 **传播**）。 穿过材质的光线量由材质的不透明度值（介于 0 与 1 之间）及投射到材质的光线量确定。 例如，如果不透明度设置为 0，那么材质的彩色阴影不会有光线传播。如果不透明值设置为 1，那么它将是完全不透明物。

**材质设置**

·         在以下示例中，将使用“半透明度”作为选择的混合模式。

·         可以使用的“照亮”和“不照亮”混合模式是：半透明、递增法和调制

注

·         间接照明有时会削弱半透明阴影，使其饱和度低于半透明材质的自发光或漫射。

·         法线贴图强度可以通过增大 **半透明平行光强度** 进行人工调整

·         使用混合模式 **调制** 要求在“材质输入”（Material Inputs）面板中禁用“单独半透明”（Separate Translucency）。

**照亮材质**

**蒙版的阿尔法通道**

![TCS_Lit_Masked.PNG](./color translucent shadows.assets/clip_image004.jpg)

·         选中 **材质属性（****Material Attributes****）**节点，并在其 **细节（****Details****）**面板中更改下列各项：

·         混合模式（Blend Mode）：半透明（Translucent）

·         （可选）双面（Two Sided）：选中

·         半透明照明模型（Translucency Lighting Model）：表面半透明体积（Surface Translucency Volume）

·         将纹理样本（Texture Sample）的 **阿尔法** 通道连接到 **不透明（****Opacity****）**槽，以遮罩材质的某些部分。

**定制不透明度**

![TCS_Lit_CustomOpacity.PNG](./color translucent shadows.assets/clip_image006.jpg)

\1.     选中 **材质属性（****Material Attributes****）**，并在其 **细节（****Details****）**面板中更改下列各项：

·         混合模式（Blend Mode）：半透明（Translucent）

·         （可选）双面（Two Sided）：选中

·         半透明照明模型（Translucency Lighting Model）：TLM_Surface

\2.     创建 **乘法（****Multiply****）**节点，并将其连接到“材质属性”（Material Attriubutes）节点上的 **不透明（****Opacity****）**。

\3.     将“纹理样本”（Texture Sample）的 **阿尔法** 连接到引脚 **A**。

\4.     创建一个 **常量（****Constant****）**值，并将其设置为小于 1 的值。0 表示完全透明，而 1 表示完全不透明。

![TCS_LIT_CO_constantValue.PNG](./color translucent shadows.assets/clip_image008.jpg)

·         如果您计划让玩家同时看到具有该材质的网格的两面，那么最好使用 **双面（****Two Sided****）**。

·         如果 **不** 使用“双面”（Two Sided），那么光线必须投射到具有该材质的网格的可视面。

·         要遮罩部分图像，需要对纹理使用“阿尔法”通道。

**不照亮材质**

![TCS_Unlit_Mat.PNG](./color translucent shadows.assets/clip_image010.jpg)

·         选择 **材质属性（****Material Attributes****）**节点，并在其 **细节（****Details****）**面板中更改以下各项：

·         混合模式（Blend Mode）：半透明（Translucent）

·         明暗处理模型（Shading Model）不照亮（Unlit）

·         （可选）双面（Two Sided）：选中

·         半透明照明模型（Translucency Lighting Model）：TLM_Surface

·         将“纹理样本”（Texture Sample）连接到 **自发光（****Emissive****）**。

**使用中的彩色半透明阴影**

**蒙版的阿尔法通道**

·         混合模式（Blend Mode）：半透明（Translucent）

·         明暗处理模型（Shading Model）照亮或不照亮

![Logo_LIT_Masked.PNG](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image012.jpg)

**定制不透明度**

·         混合模式（Blend Mode）：半透明（Translucent）

·         阴影模型（Shading Model）照亮或不照亮

![TCS_Lit_CO_Result.PNG](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image014.jpg)

**阴影清晰度**

阴影清晰度可能受多个不同因素影响，其中包括接收到传播阴影颜色的网格的光照贴图分辨率、光线的来源角度以及纹理样本的质量。

**光照贴图分辨率**

![Lightmap Resolution 64](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image016.jpg)

**Lightmap Resolution 64**

![Lightmap Resolution 1024](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image018.jpg)

**Lightmap Resolution 1024**

**局限性**

·         只有 **静态光线** 才支持半透明阴影颜色

**结论**

有关彩色阴影需要牢记的最重要一点是，它 **仅** 支持 **静态光线**。 另外，您需要确保根据自己的设计需要，选择最佳的混合模式（半透明、递增法和调制）。 彩色阴影的应用十分广泛，并且，您可以根据项目的需要使用各种混合模式。

 

来自 <<http://api.unrealengine.com/CHN/Engine/Rendering/Materials/HowTo/ColoredTransluscentShadows/index.html>> 
