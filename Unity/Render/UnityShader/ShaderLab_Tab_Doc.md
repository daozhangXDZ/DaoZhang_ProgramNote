# Unity ShaderLab的说明



## 一、Tags

表面着色器可以被若干的标签（tags）所修饰，而硬件将通过判定这些标签来决定什么时候调用该着色器。比如我们的例子中SubShader的第一句

```
Tags { "RenderType"="Opaque" }
```

告诉了系统应该在渲染非透明物体时调用我们。Unity定义了一些列这样的渲染过程，与RenderType是Opaque相对应的显而易见的是`"RenderType" = "Transparent"`，表示渲染含有透明效果的物体时调用。在这里Tags其实暗示了你的Shader输出的是什么，如果输出中都是非透明物体，那写在Opaque里；如果想渲染透明或者半透明的像素，那应该写在Transparent中。

另外比较有用的标签还有`"IgnoreProjector"="True"`（不被[Projectors](http://docs.unity3d.com/Documentation/Components/class-Projector.html)影响），`"ForceNoShadowCasting"="True"`（从不产生阴影）以及`"Queue"="xxx"`（指定渲染顺序队列）。这里想要着重说一下的是Queue这个标签，如果你使用Unity做过一些透明和不透明物体的混合的话，很可能已经遇到过不透明物体无法呈现在透明物体之后的情况。这种情况很可能是由于Shader的渲染顺序不正确导致的。Queue指定了物体的渲染顺序，预定义的Queue有：

| Background  | 最早被调用的渲染，用来渲染天空盒或者背景                     |
| ----------- | ------------------------------------------------------------ |
| Geometry    | 这是默认值，用来渲染非透明物体（普通情况下，场景中的绝大多数物体应该是非透明的） |
| AlphaTest   | 用来渲染经过[Alpha Test](http://docs.unity3d.com/Documentation/Components/SL-AlphaTest.html)的像素，单独为AlphaTest设定一个Queue是出于对效率的考虑 |
| Transparent | 以从后往前的顺序渲染透明物体                                 |
| Overlay     | 用来渲染叠加的效果，是渲染的最后阶段（比如镜头光晕等特效）   |

这些预定义的值本质上是一组定义整数，Background = 1000， Geometry = 2000, AlphaTest =  2450， Transparent = 3000，最后Overlay =  4000。在我们实际设置Queue值时，不仅能使用上面的几个预定义值，我们也可以指定自己的Queue值，写成类似这样：`"Queue"="Transparent+100"`，表示一个在Transparent之后100的Queue上进行调用。通过调整Queue值，我们可以确保某些物体一定在另一些物体之前或者之后渲染，这个技巧有时候很有用处。







## 二、RenderType

在Unity Shader中会经常在SubShader中使用Tags，其中就会涉及RenderType。

    SubShader{
        Tags{ "RenderType" = "Opaque" }
        ...
    }

内置的RenderType标签：

    http://www.ceeger.com/Components/SL-ShaderReplacement.html
    
    Opaque: most of the shaders (Normal, Self Illuminated, Reflective, terrain shaders).
    用于大多数着色器（法线着色器、自发光着色器、反射着色器以及地形的着色器）。
    Transparent: most semitransparent shaders (Transparent, Particle, Font, terrain additive pass shaders).
    用于半透明着色器（透明着色器、粒子着色器、字体着色器、地形额外通道的着色器）。
    TransparentCutout: masked transparency shaders (Transparent Cutout, two pass vegetation shaders).
    蒙皮透明着色器（Transparent Cutout，两个通道的植被着色器）。
    Background: Skybox shaders. 天空盒着色器。
    Overlay: GUITexture, Halo, Flare shaders. 光晕着色器、闪光着色器。
    TreeOpaque: terrain engine tree bark. 地形引擎中的树皮。
    TreeTransparentCutout: terrain engine tree leaves. 地形引擎中的树叶。
    TreeBillboard: terrain engine billboarded trees. 地形引擎中的广告牌树。
    Grass: terrain engine grass. 地形引擎中的草。
    GrassBillboard: terrain engine billboarded grass. 地形引擎何中的广告牌草。

功能说明

    http://www.ceeger.com/Components/SL-ShaderReplacement.html

Unity可以运行时替换符合特定RenderType的Shader。主要通过Camera.RenderWithShader或者Camera.SetReplacementShader这两个接口来实现。

    Camera.RenderWithShader
    
    public void RenderWithShader(Shader shader, string replacementTag);

    Camera.SetReplacementShader
    
    public void SetReplacementShader(Shader shader, string replacementTag);

两个接口的区别

RenderWithShader与SetReplacementShader的区别是RenderWithShader是 当前帧 用指定的Shader渲染，SetReplacementShader是替换后的 每一帧 用指定的Shader渲染。

当把代码SetReplacementShader换成RenderWithShader发现没什么效果，主要是因为RenderWithShader是当前帧用指定的Shader渲染，要与SetReplacementShader同样的效果，必须每帧都调用RenderWithShader。注意必须在OnGUI函数里调用。

功能验证

调用Camera.SetReplacementShader(Shader,"RenderType")时，相机会使用指定的Shader来替代场景中的其他Shader来对场景进行渲染。

比如现在有以下几个Shader:

    Shader "Shader1"{
        Properties(···)
        SubShader{
            Tags{ "RenderType"="Opaque" }
            Pass = {···}
        }
    
    ```
    SubShader{
        Tags{ "RenderType"="Transparent" }
        Pass = {···}
    }
    ```
    
    }

场景中一部分物体使用的是Shader2:

    Shader "Shader2"{
        Properties(···)
        SubShader{
            Tags{ "RenderType"="Opaque" }
            Pass = {···}
        }
    }

另一部分物体使用的是Shader3:

    Shader "Shader3"{
        Properties(···)
        SubShader{
            Tags{ "RenderType"="Transparent" }
            Pass = {···}
        }
    }

用法1

调用以下方法（参数2为""）：

    Camera.SetPlacementShader(Shader1, "");

执行代码之后，场景中的所有物体都使用Shader1进行渲染。

用法2

如果第二个参数不为空，如：

    Camera.SetPlacementShader(Shader1, "RenderType");

这种情况下,首先在场景中找到标签中包含该字符串（这里为“RenderType”）的Shader,再去看该字符串对应的数值是否与Shader1中该字符串的值一致，如果一致，则替代渲染，否则不渲染。

上面几个Shader的代码，由于Shader2中包含"RenderType"=“Opaque”，而且Shader1中的第一个SubShader中包含"RenderType"=“Opaque”，因此将Shader1中的第一个SubShader替换场景中的所有Shader2，同理，将Shader1中的第二个SubShader替换场景中的所有的Shader3。

用法3

另外，也可以自定义第二个参数，Shader代码如下:



    Shader "Shader1"{
        Properties(···)
        SubShader{
            Tags{ "RenderType"="Opaque" "CheckRenderTypeTag="On" }
            Pass = {···}
        }
    
    ```
    SubShader{
        Tags{ "RenderType"="Transparent" "CheckRenderTypeTag="Off" }
        Pass = {···}
    }
    ```
    }

    Shader "Shader2"{
        Properties(···)
        SubShader{
            Tags{ "RenderType"="Opaque" "CheckRenderTypeTag="On" }
            Pass = {···}
        }
    }

    Shader "Shader3"{
        Properties(···)
        SubShader{
            Tags{ "RenderType"="Transparent" "CheckRenderTypeTag="Off" }
            Pass = {···}
        }
    }

调用以下方法:

    Camera.SetReplacementShader(Shader1, "CheckRenderTypeTag");  

最后的结果是，Shader1的第一个SubShader将会替换Shader2和Shader3(因为“CheckRenderTypeTag”对应的数值匹配)。



## 三、LOD

它是Level of Detail的缩写。这个数值决定了我们能用什么样的Shader。在Unity的Quality  Settings中我们可以设定允许的最大LOD，当设定的LOD小于SubShader所指定的LOD时，这个SubShader将不可用。Unity内建Shader定义了一组LOD的数值，我们在实现自己的Shader的时候可以将其作为参考来设定自己的LOD数值，这样在之后调整根据设备图形性能来调整画质时可以进行比较精确的控制。

- VertexLit及其系列 = 100
- Decal, Reflective VertexLit = 150
- Diffuse = 200
- Diffuse Detail, Reflective Bumped Unlit, Reflective Bumped VertexLit = 250
- Bumped, Specular = 300
- Bumped Specular = 400
- Parallax = 500
- Parallax Specular = 600



## 四、IgnoreProjector

“IgnoreProjector”=“True”告诉Unity3D，我们不希望任何投影类型材质或者贴图，影响我们的物体或者着色器。这个特性往往那个用在GUI上。程序默认“IgnoreProjector”=“Flase”。