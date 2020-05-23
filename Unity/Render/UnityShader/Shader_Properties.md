

# Properties

本文段落来自：[猫都能学会的Unity3D Shader入门指南](http://blog.csdn.net/zhuangyou123/article/details/26077783)。
 部分参考自：[【浅墨Unity3D Shader编程】](http://blog.csdn.net/poem_qianmo/article/details/40955607)
 请点击链接查看原文，尊重楼主版权。

\###**Property属性**

properties一般定义在着色器的起始部分，我们可以在Shader书写的时候定义多种多样的属性，而使用Shader的时候可以直接在材质检视面板(Material  Inspector)里编辑这些属性，取不同的值或者纹理。这可以说是Unity贴心&可见即所得的又一体现吧。
 以Unity自带的BasicVertex Lighting 基本顶点光照为例，一张很直观的图就是这样:



需要注意，Properties块内的语法都是单行的。每个属性都是由内部名称开始，后面括号中是显示在检视面板(Inspector)中的名字和该属性的类型。等号后边跟的是默认值。

在Properties{}中定义着色器属性，在这里定义的属性将被作为输入提供给所有的子着色器。每一条属性的定义的语法是这样的：

```
_Name("Display Name", type) = defaultValue[{options}]
1
```

- _Name - 属性的名字，简单说就是变量名，在之后整个Shader代码中将使用这个名字来获取该属性的内容
- Display Name - 这个字符串将显示在Unity的材质编辑器中作为Shader的使用者可读的内容
- type - 这个属性的类型，可能的type所表示的内容有以下几种：
- Color - 一种颜色，由RGBA（红绿蓝和透明度）四个量来定义；
- 2D - 一张2的阶数大小（256，512之类）的贴图。这张贴图将在采样后被转为对应基于模型UV的每个像素的颜色，最终被显示出来；
- Rect - 一个非2阶数大小的贴图；
- Cube - 即Cube map texture（立方体纹理），简单说就是6张有联系的2D贴图的组合，主要用来做反射效果（比如天空盒和动态反射），也会被转换为对应点的采样；
- Range(min, max) - 一个介于最小值和最大值之间的浮点数，一般用来当作调整Shader某些特性的参数（比如透明度渲染的截止值可以是从0至1的值等）；
- Float - 任意一个浮点数；
- Vector - 一个四维数；
- defaultValue 定义了这个属性的默认值，通过输入一个符合格式的默认值来指定对应属性的初始值（某些效果可能需要某些特定的参数值来达到需要的效果，虽然这些值可以在之后在进行调整，但是如果默认就指定为想要的值的话就省去了一个个调整的时间，方便很多）。
- Color - 以0～1定义的rgba颜色，比如(1,1,1,1)；
- 2D/Rect/Cube - 对于贴图来说，默认值可以为一个代表默认tint颜色的字符串，可以是空字符串或者"white",“black”,“gray”,"bump"中的一个
- Float，Range - 某个指定的浮点数
- Vector - 一个4维数，写为 (x,y,z,w)
- 另外还有一个{option}，它只对2D，Rect或者Cube贴图有关，在写输入时我们最少要在贴图之后写一对什么都不含的空白的{}，当我们需要打开特定选项时可以把其写在这对花括号内。如果需要同时打开多个选项，可以使用空白分隔。可能的选择有ObjectLinear,  EyeLinear, SphereMap, CubeReflect,  CubeNormal中的一个，这些都是OpenGL中TexGen的模式，具体的留到后面有机会再说。

所以，一组属性的申明看起来也许会是这个样子的：

```
//Define a color with a default value of semi-transparent blue
_MainColor ("Main Color", Color) = (0,0,1,0.5)  
//Define a texture with a default of white
_Texture ("Texture", 2D) = "white" {}  
1234
```

属性案例代码：

- **Properties { Property [Property …] }**
   定义属性块，其中可包含多个属性，其定义如下：
- **name (“display name”, Range (min, max)) =number**
   定义浮点数属性，在检视器中可通过一个标注最大最小值的滑条来修改。
- **name (“display name”, Color) =(number,number,number,number)**
   定义颜色属性
- **name (“display name”, 2D) = “name” {options }**
   定义2D纹理属性
- **name (“display name”, Rect) = “name”{ options }**
   定义长方形（非2次方）纹理属性
- **name (“display name”, Cube) = “name”{ options }**
   定义立方贴图纹理属性
- **name (“display name”, Float) = number**
   定义浮点数属性
- **name (“display name”, Vector) =(number,number,number,number)**
   定义一个四元素的容器(相当于Vector4)属性

#### 一些细节说明

- 包含在着色器中的每一个属性通过name索引（在Unity中, 通常使用下划线来开始一个着色器属性的名字）。属性会将display name显示在材质检视器中，还可以通过在等符号后为每个属性提供缺省值。
- 对于Range和Float类型的属性只能是单精度值。
- 对于Color和Vector类型的属性将包含4个由括号围住的数描述。
- 对于纹理(2D, Rect, Cube) 缺省值既可以是一个空字符串也可以是某个内置的缺省纹理：“white”, “black”, “gray” or"bump"
   随后在着色器中，属性值通过[name]来访问。