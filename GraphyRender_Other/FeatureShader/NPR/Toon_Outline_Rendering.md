# 写在前面


 
 好久没写文章。最近在看[《Real Time Rendering, third edition》](http://www.amazon.com/Real-Time-Rendering-Third-Edition-Akenine-Moller/dp/1568814240)这本书，看到了NPR这一章就想顺便记录下一些常见的轮廓线渲染的方法。

在非真实感渲染中，对轮廓线的渲染是一个应用非常广泛的手法。根据《Real Time Rendering, third  edition》一书的总结，在这篇文章里介绍几种常见的渲染方法。当然，这里只是抛砖引玉，如果要用于实际项目中可能会根据需要进行完善。一些很好的效果可能需要去参考一些论文，这里不涉及那么深。    

测试场景如下： 
 

![这里写图片描述](Toon_Outline_Rendering.assets/20150508192011339)



其中，左右两边的模型是low polygon类型的模型，即表面比较平坦；中间膜型表面变化平缓。





# Surface Angle Silhouette



## 方法


 
 基本思想是，利用viewpoint的方向和surface normal的点乘结果得到轮廓线信息。这个值越接近0，说明离轮廓线越近。

在之前的[卡通风格的Shader（一）](http://blog.csdn.net/candycat1992/article/details/37882425#t3)中，描边技术就是使用了这种方法。

这个技术相当于使用一个Spherical environment map（EM）来对整个surface进行渲染。如下图所示（来源：《Real-time Rendering, third edition》）： 
 

![使用EM渲染轮廓线](Toon_Outline_Rendering.assets/20150508120020043)



在实际应用中，我们通常使用一张一维纹理来模拟，即使用视角方向和顶点法向的点乘对该纹理进行采样。 
 

## 实践


 
 下面代码使用了两种方法来实现这种技术。一种方式是和[卡通风格的Shader（一）](http://blog.csdn.net/candycat1992/article/details/37882425#t3)中的方法一样，即使用一个参数_Outline来控制轮廓线宽度；另一种方式是使用了一张一维纹理来控制。

```c++
Shader "Silhouette/Surface Angle Sihouetting" {
    Properties {
        _MainTex ("Base (RGB)", 2D) = "white" {}
        _Outline ("Outline", Range(0,1)) = 0.4
        _SilhouetteTex ("Silhouette Texture", 2D) = "white" {}
    }
    SubShader {
        Pass {
            Tags { "RenderType"="Opaque" }
            LOD 200

            CGPROGRAM
            #include "UnityCG.cginc"
            #include "Lighting.cginc"  
            #include "AutoLight.cginc" 

            #pragma vertex vert
            #pragma fragment frag

            sampler2D _MainTex;
            float _Outline; 
            sampler2D _SilhouetteTex;

            struct v2f {
                float4 pos : SV_POSITION;   
                float2 uv : TEXCOORD0;
                float3 worldNormal : TEXCOORD1;
                float3 worldLightDir: TEXCOORD2;
                float3 worldViewDir: TEXCOORD3;
            };

            v2f vert(appdata_full i) {
                v2f o;
                o.pos= mul(UNITY_MATRIX_MVP, i.vertex);
                o.uv = i.texcoord;
                o.worldNormal = mul(i.normal, (float3x3)_World2Object);
                o.worldLightDir = mul((float3x3)_Object2World, ObjSpaceLightDir(i.vertex));
                o.worldViewDir = mul((float3x3)_Object2World, ObjSpaceViewDir(i.vertex));

                TRANSFER_VERTEX_TO_FRAGMENT(o); 

                return o;
            }

            fixed3 GetSilhouetteUseConstant(fixed3 normal, fixed3 vierDir) {
                fixed edge = saturate(dot (normal, vierDir));   
                edge = edge < _Outline ? edge/4 : 1;

                return fixed3(edge, edge, edge);
            }

            fixed3 GetSilhouetteUseTexture(fixed3 normal, fixed3 vierDir) {
                fixed edge = dot(normal, vierDir);
                edge = edge * 0.5 + 0.5;
                return tex2D(_SilhouetteTex, fixed2(edge, edge)).rgb;
            }

            fixed4 frag(v2f i) : COLOR {
                fixed3 worldNormal = normalize(i.worldNormal);
                fixed3 worldLigthDir = normalize(i.worldLightDir);
                fixed3 worldViewDir = normalize(i.worldViewDir);

                fixed3 col = tex2D(_MainTex, i.uv).rgb; 

                // Use a constant to render silhouette  
//              fixed3 silhouetteColor = GetSilhouetteUseConstant(worldNormal, worldViewDir);
                // Or use a one dime silhouette texture
                fixed3 silhouetteColor = GetSilhouetteUseTexture(worldNormal, worldViewDir);

                fixed4 fragColor;
                fragColor.rgb = col * silhouetteColor;
                fragColor.a = 1.0;

                return fragColor;
            }

            ENDCG
        }
    } 
    FallBack "Diffuse"
}123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081
```

上面使用了纯色进行颜色渲染，没要考虑光照效果。 
 下图中仅显示使用一维纹理控制的效果： 
 

![纹理控制](Toon_Outline_Rendering.assets/20150508123749364)



使用的纹理如下：



![这里写图片描述](Toon_Outline_Rendering.assets/20150508131209535)



可以看出来对于左右模型这样的模型，这种方法的轮廓效果很难控制。有的地方轮廓很宽，有的地方却又捕捉不到 
 

这种方法的优点在于非常简单快速，我们可以在一个pass里就得到结果，而且还可以使用[texture filtering](http://en.wikipedia.org/wiki/Texture_filtering)对轮廓线进行抗锯齿。 
 

但是也有很多局限性，只适用于某些模型，而对于像cube这样的模型就会有问题。虽然我们可以使用一些变量来控制轮廓线的宽度（如果使用纹理的话就是纹理中黑色的宽度），但实际的效果是依赖于表面的曲率（curvature）的。对于像cube这样表面非常平坦的物体，它的轮廓线会发生突变，要么没有，要么就全黑。

游戏[《Cel Damage》](http://en.wikipedia.org/wiki/Cel_Damage)的作者Wu发现，在他们的游戏中，这种技术只适用于1/4的模型。可以看出，这种技术局限性还是很大的。 
 



# Procedural Geometry Silhouette



## 方法


 
 这种技术的核心是用两个pass渲染。第一个pass中正常渲染frontfaces，第二个pass中在渲染backfaces，并使用某些技术来让它的轮廓可见。

在[卡通风格的Shader（二）](http://blog.csdn.net/candycat1992/article/details/41120019)中，我们使用的就是这种思想。

当然，渲染背面的方法有很多，上面博文中只是使用了其中一种，即沿着顶点法线方向移动backfaces中的顶点，这种方法也被称为shell or halo method。

下面列举一些渲染背面的方法：

方法一：只渲染backfaces的edges（可以理解成把渲染模式设置为DRAW_EDGE），然后使用一些biasing等技术来保证这些线会在frontfaces的前面渲染。

方法二：    Z-bias方法。把backfaces渲染成黑色，然后在屏幕空间的z方向上向前移动它们，使其可见。移动的距离可以是一个固定值，或其他适应后的值。 
                 缺点：不能创建宽度相同的轮廓，因为frontface和backface的夹角不一样。可控性很弱。想象一个向里凹陷的物体，这种方法得到的背面将完全覆盖掉正面图形。

方法三：    Triangle Fattening。也就是说，把每个backface triangle的edges都“变胖”一定程度，使其在视角空间中看起来宽度是一致的。
 
                  缺点：对于一些瘦长的triangles来说，它的corner也会变得很细长。一种解决方法是可以把扩展后的edges链接在一起形成斜接在一起的corners。如下图（来源：《Real-time  Rendering, third edition》）： 
                 

![这里写图片描述](Toon_Outline_Rendering.assets/20150508142409837)

​                 而且，这种方法无法应用在GPU生成的一些curved surfaces上（因为没有edges）。



方法四：    Shell or halo method。把backface的顶点沿着顶点法向方向向外扩张。因为这种方法很像在模型外面又包裹了一层壳，所以叫做shell method。但是，正如在[卡通风格的Shader（二）](http://blog.csdn.net/candycat1992/article/details/41120019)中提到的一样，仅仅这样做会根据轮廓线宽度造成模型穿透问题。为了解决这个问题，我们可以把背面扁平化。
 
                 优点：很快速，可以在vertex shader中就完成，而且具有一定的健壮性。游戏[《Cel Damage》](http://en.wikipedia.org/wiki/Cel_Damage)就是使用了这种技术。
 
                 缺点：像cube这样的模型，它的同一个顶点在不同面上具有不同的顶点法向，所以向外扩张后会形成一个gaps。一种解决方法是，强迫同一个位置的顶点具有相同的法向。另一种方法是在这些轮廓处创建额外的网格结构。

上面所列出的所有方法都有一个共同的缺点，那就是对轮廓线的外观可控性很少，而且如果没有进行一些反锯齿操作，轮库线看起来锯齿比较严重。

但它们一个非常吸引人的优点就是，不需要任何关于相邻顶点/边等信息，所有的处理都是独立的，因此从速度上来说很快。



## 实践


 
 下面只给出了z-bias和vertex normal的方法。

关于vertex normal的实现，网上有一个主流版本就是[Unity Wiki的Silhouette-Outlined_Diffuse Shader](http://wiki.unity3d.com/index.php/Silhouette-Outlined_Diffuse)。原shader有两个地方需要注意，首先对顶点只在xy方向上扩张，这种操作在模型全是外凸的情况下基本没有什么问题，但是，如果一个有模型有内凹的部分就有可能会出现轮廓线挡住frontfaces的情况；另一点是，原shader在扩张顶点时考虑了顶点在投影矩阵中的深度值，这意味着模型轮廓线的宽度会随摄像机移动而改变。当然，不想这样的话可以去掉。

还有一些变种，例如如果我们想要实现宽度不一的轮廓线，可以利用顶点颜色作为一个参数来控制宽度。可以参见[这篇博客：在Unity中使用顶点颜色控制轮廓线厚度](http://yrkhnshk.hatenablog.com/entry/%E3%80%90Unity%E3%80%91%E9%A0%82%E7%82%B9%E3%82%AB%E3%83%A9%E3%83%BC%E3%81%A7%E8%BC%AA%E9%83%AD%E7%B7%9A%E3%81%AE%E5%A4%AA%E3%81%95%E3%82%92%E5%88%B6%E5%BE%A1%E3%81%99%E3%82%8B)。

```c++
Shader "Silhouette/Procedural Geometry Silhouette" {
    Properties {
        _MainTex ("Base (RGB)", 2D) = "white" {}
        _Outline ("Outline", Range(0,1)) = 0.1
    }
    SubShader {
        Tags { "RenderType"="Opaque" }
        LOD 200

        Pass {
            Tags { "LightMode"="ForwardBase" } 

            Cull Back   
            Lighting On  

            CGPROGRAM
            #include "UnityCG.cginc"
            #include "Lighting.cginc"  
            #include "AutoLight.cginc" 

            #pragma vertex vert
            #pragma fragment frag

            sampler2D _MainTex;

            struct v2f {
                float4 pos : SV_POSITION;   
                float2 uv : TEXCOORD0;
            };

            v2f vert(appdata_full i) {
                v2f o;
                o.pos= mul(UNITY_MATRIX_MVP, i.vertex);
                o.uv = i.texcoord;

                TRANSFER_VERTEX_TO_FRAGMENT(o); 

                return o;
            }

            fixed4 frag(v2f i) : COLOR {
                fixed3 col = tex2D(_MainTex, i.uv).rgb; 

                fixed4 fragColor;
                fragColor.rgb = col;
                fragColor.a = 1.0;

                return fragColor;
            }

            ENDCG
        }

        Pass {
            Tags { "LightMode"="ForwardBase" } 

            Cull Front   
            Lighting Off

            CGPROGRAM
            #include "UnityCG.cginc"
            #include "Lighting.cginc"  
            #include "AutoLight.cginc" 

            #pragma vertex vert
            #pragma fragment frag

            sampler2D _MainTex;
            float _Outline;

            struct v2f {
                float4 pos : SV_POSITION;   
                float2 uv : TEXCOORD0;
            };

            void ZBiasMethod(appdata_full i, inout v2f o) {
                float4 viewPos = mul(UNITY_MATRIX_MV, i.vertex);
                viewPos.z += _Outline;

                o.pos = mul(UNITY_MATRIX_P, viewPos);
            }

            void VertexNormalMethod0(appdata_full i, inout v2f o) {
                o.pos = mul(UNITY_MATRIX_MVP, i.vertex);

                float3 normal = mul ((float3x3)UNITY_MATRIX_IT_MV, i.normal);
                float2 offset = TransformViewToProjection(normal.xy);

                // Only modify the xy components
                // Multiply o.pos.z, as a result the width of your outline will depend on the distance from viewer
                o.pos.xy += offset * o.pos.z * _Outline;
            }

            void VertexNormalMethod1(appdata_full i, inout v2f o) {
                float4 viewPos = mul(UNITY_MATRIX_MV, i.vertex);

                float3 normal = mul( (float3x3)UNITY_MATRIX_IT_MV, i.normal);
                // This is a tricky operation
                // The value of z avoid the expended backfaces to intersect with frontfaces
                // When z = 0.0,  it is equal to VertexNormalMethod0
                normal.z = -1.0;  
                viewPos = viewPos + float4(normalize(normal),0) * _Outline;  

                o.pos = mul(UNITY_MATRIX_P, viewPos);
            }

            v2f vert(appdata_full i) {
                v2f o;

//              ZBiasMethod(i, o);
//              VertexNormalMethod0(i, o);
                VertexNormalMethod1(i, o);

                o.uv = i.texcoord;

                TRANSFER_VERTEX_TO_FRAGMENT(o); 

                return o;
            }

            fixed4 frag(v2f i) : COLOR {
                return fixed4(0, 0, 0, 1);  
            }

            ENDCG
        }
    }
    FallBack "Diffuse"
}123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129
```

下面是Z-bias的效果，可以看出很多地方不是很理想： 
 

![这里写图片描述](Toon_Outline_Rendering.assets/20150508143508143)



当然这里给出的是最简单的移动固定值的方法。有很多技术可以改善效果。

下面是vertex normal（VertexNormalMethod1）的效果： 
 

![这里写图片描述](Toon_Outline_Rendering.assets/20150508143534632)



注意其中左边模型的头顶和中间模型的脚部，由于它们在同一个顶点处没有使用相同的法线所以出现了gaps。

大家可以看下VertexNormalMethod0的效果，在中间模型的嘴部会出现明显的遮挡问题。还可以调整下VertexNormalMethod1中对normal.z的赋值，看看会发生什么变化（z越大，轮廓线越细，发生模型遮挡问题的可能越小）。 
 



# Silhouetting by Image Processing



## 方法


 
 这种技术利用了G-buffer，在每个buffer中使用了图像处理的技术来检测轮廓信息。

G-buffer的提出是用于延迟渲染（deferred shading）的，而近年来被一些学者扩充到NPR的领域。

基本思想是，利用图像处理中的一些算法，在Z-buffer中找到不连续地方，就可以找到大部分轮廓线了。还可以在surface normal中找到不连续点，来找到更完整的轮廓线。最后还可以在ambient colors中，进一步完备前两步找到的轮廓线信息。

因此，基本步骤是： 
 \1. 使用vertex shader把world space normals和z-depths渲染到纹理中。 
 \2. 使用一些滤波算法来找到边缘信息。一种常见的滤波算子是[Sobel边缘检测算子](http://en.wikipedia.org/wiki/Sobel_operator)。 
 \3. 找到边缘后，我们还可以使用一些图像处理操作，例如腐蚀和膨胀，来扩展或者缩小轮廓线宽度。

这种方法的优点在于： 
 \*  适用于任何种类的模型 
 \*  而且不需要CPU参与创建和传递一些边的信息。

但也有它的缺点： 
 \* 首先，这种对z-depth比较来检测边界的方法，会受z变化范围的影响，一些z变化很小的轮廓就无法检测出来。例如，桌子上的纸张。 
 \* 同样，纸张的normal map filter同样会不起作用，因为纸张表面的normal都是一样的。

对上述问题的改进，一种解决方法是在物体颜色上再添加一层滤波。但是，也不是万能解决方法。例如，如果一张纸自己折叠了一下，我们仍然无法检测出来这个折痕。 
 

## 实践


 
 在Unity中，官方提供了这种边缘检测的实现，[Edge Detect Effect Normals](http://docs.unity3d.com/Manual/script-EdgeDetectEffectNormals.html)。官方的实现里还提供了更多可调参数。

直接使用的效果： 
 

![这里写图片描述](Toon_Outline_Rendering.assets/20150508164142314)



注意其中锯齿还是比较严重。若想去除，可以考虑其他屏幕后处理效果中的反锯齿操作。 
 



# Silhouette Edge Detection



## 方法


 
 上面提到的各种方法，一个最大的问题是，无法控制轮廓线的风格渲染。对于一些情况，我们希望可以渲染出独特风格的轮廓线，例如水墨风格等等。

为此，我们希望可以检测出silhouette edges，然后直接渲染它们。检测一条edge是否是silhouette edge的公式很简单，只需要检查和一条edge相邻的两个三角形是否满足：

(*n*0⋅*v*>0)!=(*n*1⋅*v*>0)



其中*n*0

和

*n*1

表示三角面片的法向，

*v*

是从视角到该边上任意顶点的方向。即，检查它们是否一个朝正面，一个朝背面。

标准方法： 为了找到这些silhouette edges，标准方法是循环遍历模型所有的edges，然后进行上述检查。

优化：标准方法显然要求的工作量比较大，很多学者提出了优化的方法。 

* 一种优化是，在同一个平面上的edges可以直接跳过检查。也就是说，如果这两个三角面片的法向相同，那么就不需要检查这条edge了。


* 还有学者提出，可以避免重复的点乘操作。即重用每个面片上点乘的结果。


* 由于silhouette是闭合的，所以一旦找到一条silhouette edge，就检查它的临边是否也是。直到找到整个轮廓。


* 对于动画来说，如果每一帧都进行一次搜索是很费事的。因此有学者提出，可以通过上一帧的silhouette edges来找到下一帧的silhouette edges。虽然性能可以提升，但这种方法可能会miss掉新的silhouette。

总体而言，这种技术的优点在于，一旦找到了这些silhouette edges，我们使用一些风格化算法进行渲染了。当然，还需要一些biasing操作来让它们可见。

当然也有缺点： 
 \1. 这种方法得到的silhouette edge更加直线化，这是因为我们是以edge为单位渲染的。一些学者提出了方法可以绘制出曲线式的edges。
 
 \2. 在每一帧需要大量CPU计算。如果使用geometry shader来实现的话，可以优化这一点。
 
 \3. 会有Temporal Coherence的问题。解释一下就是说，由于是每一帧单独提取轮廓，所以在帧与帧之间会出现跳跃性。这也是图形学中的一个研究点。2014年SIGGRAPH有一篇论文（[Computing Smooth Surface Contours with Accurate Topology](http://www.labri.fr/perso/pbenard/publications/contours/)）就讲了相关工作。
 
 

## 实践


 
 由于Mac上的Unity不支持Geometry Shader，所有无法使用Geometry Shader实现。但有一篇很好的文章示范了如何使用OpenGL来实现这种方法。可以参见。[Silhouette Extraction](http://prideout.net/blog/?p=54)





# Hybrid Silhouette



## 方法


 
 在一些对美观度要求比较高的应用里，会混合使用上述各种方法。例如，首先找到silhouette  edges，然后对模型的三角面片和silhouette  edges指派不同的ID（这个ID只是为了区分它们，例如使用不同的颜色），并把它渲染到纹理。这个ID buffer可以使用Image  Processing的方法来识别出silhouette edges，并对它们进行风格化渲染。如下图所示（来源：《Real-time  Rendering, third edition》）： 
 

![这里写图片描述](Toon_Outline_Rendering.assets/20150508172712769)



# 写在最后


 
 上面列举了一些用于渲染轮廓线的常见方法。欢迎补充。

更多参考：

<http://wiki.unity3d.com/index.php/Silhouette-Outlined_Diffuse>

[在Unity中使用顶点颜色控制轮廓线厚度](http://yrkhnshk.hatenablog.com/entry/%E3%80%90Unity%E3%80%91%E9%A0%82%E7%82%B9%E3%82%AB%E3%83%A9%E3%83%BC%E3%81%A7%E8%BC%AA%E9%83%AD%E7%B7%9A%E3%81%AE%E5%A4%AA%E3%81%95%E3%82%92%E5%88%B6%E5%BE%A1%E3%81%99%E3%82%8B)

[Real Time Rendering, third edition](http://www.amazon.com/Real-Time-Rendering-Third-Edition-Akenine-Moller/dp/1568814240)