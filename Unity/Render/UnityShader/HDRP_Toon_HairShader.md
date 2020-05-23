![【HDRP Toon Shader】Unity实现崩坏3高质量卡通头发渲染](https://pic1.zhimg.com/v2-eb34032e6e9be20e0d2cd151373638a6_1200x500.jpg)

# 【HDRP Toon Shader】Unity实现崩坏3高质量卡通头发渲染

[![喵刀Hime](https://pic3.zhimg.com/v2-885af6453c9500081dddd3ec631e55fe_xs.jpg)](https://www.zhihu.com/people/blackcat1312)

[喵刀Hime](https://www.zhihu.com/people/blackcat1312)

不会写Shader的程序猿不是好MMDer

[MaxwellGeng](https://www.zhihu.com/people/maxwellgeng) 等 

本文将介绍如何在HDRP手写一个卡通头发Shader，想要熟悉HDRP或头发渲染的同学不要错过哦(。・∀・)ノ

效果（参数效果、视频版见[https://www.bilibili.com/video/av84593392/](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/av84593392/)）：

![img](https://pic4.zhimg.com/v2-e31db2a496f6c15b04a0849e1ab50437_b.jpg)



![img](https://pic1.zhimg.com/v2-f0dac9c0f7920489cd824100333e7834_b.jpg)



观察一下崩三的效果：

![img](https://pic1.zhimg.com/v2-a15de78d1e3ad2b8c9f1376858811a04_b.jpg)



- 高光

- - 低频固有高光+高频流动高光
  - 半角向量与法线夹角越小高光范围越大

- 阴影

- - 深色固有阴影+浅色动态阴影
  - 阴影形状近似球形

稍作分析可以发现都是比较简单的东西，标题的高质量完全靠美术来调整，稍后会提供用到的美术资源。

首先是球形的阴影，使用法线编辑工具修改法线以使阴影好看已经是卡通渲染必备的技术了。这里推荐2款插件：

[https://github.com/binarysudoku/NormalMagic](https://link.zhihu.com/?target=https%3A//github.com/binarysudoku/NormalMagic)[github.com](https://link.zhihu.com/?target=https%3A//github.com/binarysudoku/NormalMagic)[https://github.com/unity3d-jp/NormalPainter](https://link.zhihu.com/?target=https%3A//github.com/unity3d-jp/NormalPainter)[github.com](https://link.zhihu.com/?target=https%3A//github.com/unity3d-jp/NormalPainter)

上面的适用于max，有简单的功能，包括要用的替换法线的功能。下面的是Unity JP分享的非常强大的适用于unity的法线编辑工具，甚至能将法线存入顶点色，非常实用。

模型导入max，使用插件将球体的法线替换给头发：

![img](https://pic3.zhimg.com/80/v2-0b2dc361d5799a3a709fd77f32ca1742_hd.jpg)

导进Unity，由于HDRP的设置多而复杂，稍有错误效果则相差甚远，所以这里说一下需要注意的设置。

![img](https://pic2.zhimg.com/80/v2-9f76677a34baf80be14b91f01614125d_hd.jpg)后处理仅开启曝光

![img](https://pic4.zhimg.com/80/v2-4dd809f7f5c5fcf6e0291d18ce44dd2f_hd.jpg)平行光

![img](https://pic1.zhimg.com/80/v2-90df35f61801b3f3fb10c7a1351a84dc_hd.jpg)设置中的默认后处理都关掉

![img](https://pic3.zhimg.com/80/v2-c2c5668e659c46996fdaee9f8031245a_hd.jpg)颜色空间linear，颜色贴图勾上sRGB，非颜色无需

关于Gamma和linear还有些需要注意的，Unity处理贴图的RGB通道和A通道的方式不同，比如一张LightMap，不勾选sRGB，直接采样RGB的结果和PS中一致，而A却有偏差，需要经过1.48的gamma校正才能和PS中一致，以上是个人观察所得结果，如有大佬知晓原因欢迎留言。

下面开始写HDRP Shader。首先创建任意一个HDRP Shader，用Shader Graph创建以下属性和节点，并在Sample Texture2D节点上右键Show Generated Code：

![img](https://pic2.zhimg.com/80/v2-a9aefd43fb5836778b873b61bf962be1_hd.jpg)

生成的代码如下：

```csharp
Shader "Sample Texture 2D"
{
    Properties
    {
        [NoScaleOffset]_MainTex("Texture2D", 2D) = "white" {}
    }

    HLSLINCLUDE
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Packing.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/NormalSurfaceGradient.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/UnityInstancing.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/EntityLighting.hlsl"
    #include "Packages/com.unity.shadergraph/ShaderGraphLibrary/ShaderVariables.hlsl"
    #include "Packages/com.unity.shadergraph/ShaderGraphLibrary/ShaderVariablesFunctions.hlsl"
    #include "Packages/com.unity.shadergraph/ShaderGraphLibrary/Functions.hlsl"
    #define SHADERGRAPH_PREVIEW 1

    CBUFFER_START(UnityPerMaterial)
    CBUFFER_END
    TEXTURE2D(_MainTex); SAMPLER(sampler_MainTex); float4 _MainTex_TexelSize;
    SAMPLER(_SampleTexture2D_99F63624_Sampler_3_Linear_Repeat);

    struct SurfaceDescriptionInputs
    {
        half4 uv0;
    };


    struct SurfaceDescription
    {
        float4 RGBA_0;
    };

    SurfaceDescription PopulateSurfaceData(SurfaceDescriptionInputs IN)
    {
        SurfaceDescription surface = (SurfaceDescription)0;
        float4 _SampleTexture2D_99F63624_RGBA_0 = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, IN.uv0.xy);
        float _SampleTexture2D_99F63624_R_4 = _SampleTexture2D_99F63624_RGBA_0.r;
        float _SampleTexture2D_99F63624_G_5 = _SampleTexture2D_99F63624_RGBA_0.g;
        float _SampleTexture2D_99F63624_B_6 = _SampleTexture2D_99F63624_RGBA_0.b;
        float _SampleTexture2D_99F63624_A_7 = _SampleTexture2D_99F63624_RGBA_0.a;
        surface.RGBA_0 = float4 (0, 0, 0, 0);
        return surface;
    }

    struct GraphVertexInput
    {
        float4 vertex : POSITION;
        float4 texcoord0 : TEXCOORD0;
        UNITY_VERTEX_INPUT_INSTANCE_ID
    };

    GraphVertexInput PopulateVertexData(GraphVertexInput v)
    {
        return v;
    }

    ENDHLSL

    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            struct GraphVertexOutput
            {
                float4 position : POSITION;
                half4 uv0 : TEXCOORD;

            };

            GraphVertexOutput vert (GraphVertexInput v)
            {
                v = PopulateVertexData(v);

                GraphVertexOutput o;
                float3 positionWS = TransformObjectToWorld(v.vertex);
                o.position = TransformWorldToHClip(positionWS);
                float4 uv0 = v.texcoord0;
                o.uv0 = uv0;

                return o;
            }

            float4 frag (GraphVertexOutput IN ) : SV_Target
            {
                float4 uv0 = IN.uv0;

                SurfaceDescriptionInputs surfaceInput = (SurfaceDescriptionInputs)0;
                surfaceInput.uv0 = uv0;

                SurfaceDescription surf = PopulateSurfaceData(surfaceInput);
                return all(isfinite(surf.RGBA_0)) ? half4(surf.RGBA_0.x, surf.RGBA_0.y, surf.RGBA_0.z, 1.0) : float4(1.0f, 0.0f, 1.0f, 1.0f);

            }
            ENDHLSL
        }
    }
}
```

以此为基础进行修改，先复制出来保存为.shader，修改shader名称，删除一些不需要的部分，整理一下之后看起来和builtin除了texture的声明、函数不同之外基本没啥区别：

```csharp
Shader "Jason Ma/Hair"
{
    Properties
    {
        _MainTex ("Texture2D", 2D) = "white" { }
    }
    
    HLSLINCLUDE
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Packing.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/NormalSurfaceGradient.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/UnityInstancing.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/EntityLighting.hlsl"
    #include "Packages/com.unity.shadergraph/ShaderGraphLibrary/ShaderVariables.hlsl"
    #include "Packages/com.unity.shadergraph/ShaderGraphLibrary/ShaderVariablesFunctions.hlsl"
    #include "Packages/com.unity.shadergraph/ShaderGraphLibrary/Functions.hlsl"
    
    CBUFFER_START(UnityPerMaterial)
    
    CBUFFER_END
    
    TEXTURE2D(_MainTex); SAMPLER(sampler_MainTex);
    
    ENDHLSL
    
    SubShader
    {
        Tags { "RenderType" = "Opaque" "LightMode" = "ForwardOnly" }
        LOD 100
        
        Pass
        {
            HLSLPROGRAM
            
            #pragma vertex vert
            #pragma fragment frag
            
            struct GraphVertexInput
            {
                float4 vertex: POSITION;
                float4 texcoord0: TEXCOORD0;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };
            struct GraphVertexOutput
            {
                float4 position: POSITION;
                half4 uv0: TEXCOORD;
            };
            
            GraphVertexOutput vert(GraphVertexInput v)
            {
                GraphVertexOutput o;
                float3 positionWS = TransformObjectToWorld(v.vertex.xyz);
                o.position = TransformWorldToHClip(positionWS);
                o.uv0 = v.texcoord0;
                
                return o;
            }
            
            float4 frag(GraphVertexOutput IN): SV_Target
            {
                float4 uv0 = IN.uv0;
                
                float4 c = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv0.xy);
                
                return c;
            }
            ENDHLSL
            
        }
    }
}
```

![img](https://pic2.zhimg.com/80/v2-98e056ff8b6db13048a0a04726048271_hd.jpg)初始效果

然后收集我们需要的数据，为了获取这些数据要修改include，添加一些属性，修改结构体：

```csharp
    Properties
    {
        _MainTex ("Color Map", 2D) = "white" { }
        _LightMap ("Light Map", 2D) = "white" { }
        _Color ("Color", Color) = (1, 1, 1, 1)
        _ShadowColor ("Shadow Color", Color) = (0.6, 0.6, 0.6, 1)
        _DmcShadowIntensity ("Dynamic Shadow Intensity", Range(0, 1)) = 0.5
        _ShadowThreshold ("Shadow Threshold", Range(0, 1)) = 0.5
        [PowerSlider(6)]_ShadowFeather ("Shadow Feather", Range(0.0001, 1)) = 0.01
    }
    
    ...
    
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Packing.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/NormalSurfaceGradient.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/UnityInstancing.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/EntityLighting.hlsl"
    
    #include "Packages/com.unity.render-pipelines.high-definition/Runtime/ShaderLibrary/ShaderVariables.hlsl"
    #include "Packages/com.unity.render-pipelines.high-definition/Runtime/Lighting/Lighting.hlsl"
    
    CBUFFER_START(UnityPerMaterial)
    float4 _Color;
    float4 _ShadowColor;
    float _DmcShadowIntensity;
    float _ShadowThreshold;
    float _ShadowFeather;
    CBUFFER_END
    
    TEXTURE2D(_MainTex); SAMPLER(sampler_MainTex);
    TEXTURE2D(_LightMap); SAMPLER(sampler_LightMap);
    
    ...
   
            struct GraphVertexInput
            {
                float4 vertex: POSITION;
                float4 texcoord0: TEXCOORD0;
                float3 normal: NORMAL;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };
            struct GraphVertexOutput
            {
                float4 position: POSITION;
                half4 uv0: TEXCOORD0;
                float3 positionWS: TEXCOORD1;
                float3 normal: TEXCOORD2;
            };
            
            GraphVertexOutput vert(GraphVertexInput v)
            {
                GraphVertexOutput o;
                // 这里的World Space是相对于摄像机的
                //https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@7.1/manual/Camera-Relative-Rendering.html
                float3 positionWS = TransformObjectToWorld(v.vertex.xyz);
                o.position = TransformWorldToHClip(positionWS);
                o.positionWS = positionWS;
                o.normal = TransformObjectToWorldNormal(v.normal);
                o.uv0 = v.texcoord0;
                
                return o;
            }
            
            float4 frag(GraphVertexOutput i): SV_Target0
            {
                float4 uv0 = i.uv0;
                //Packages\com.unity.render-pipelines.high-definition@7.1.6\Runtime\Lighting\LightDefinition.cs
                DirectionalLightData light = _DirectionalLightDatas[0];
                float3 L = -light.forward.xyz;
                float3 V = GetWorldSpaceNormalizeViewDir(i.positionWS);
                float3 H = normalize(L + V);
                float3 N = normalize(i.normal);
                
                float4 c = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv0.xy);
                
                return c;
            }
```

![img](https://pic4.zhimg.com/80/v2-f23952b4951483da2c1f08863d457f3b_hd.jpg)

一些需要注意的地方代码中已经标了注释，HDRP中的光照存放在了数组中，一个pass即可遍历所有光照，这里只接收第一个平行光，DirectionalLightData结构体可在注释中的路径中找到。

下面写一个最简单的Toon光照模型，公式是从[UTS2](https://link.zhihu.com/?target=https%3A//github.com/unity3d-jp/UnityChanToonShaderVer2_Project/blob/master/Manual/UTS2_Manual_en.md)抄来的：

```csharp
            float4 frag(GraphVertexOutput i): SV_Target0
            {
                ...
                
                float halfLambert = dot(N, L) * 0.5 + 0.5;
                float shadowStep = saturate(1.0 - (halfLambert - (_ShadowThreshold - _ShadowFeather)) / _ShadowFeather);
                
                float4 baseColor = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv0.xy) * _Color;
                float4 shadowColor = baseColor * _ShadowColor;
                
                float4 finalColor = lerp(baseColor, shadowColor, shadowStep);
                
                return finalColor;
            }
```

![img](https://pic1.zhimg.com/80/v2-f1189e29c8279b21b794eac43cfa9bb0_hd.jpg)

然后加入2层阴影，稍微调整颜色：Color(D4CFC9)、Shadow Color(A8A8A8)：

```csharp
                float shadowStep = ...
                
                float4 lightMap = SAMPLE_TEXTURE2D(_LightMap, sampler_LightMap, uv0.xy);// 未使用A通道所以未校正Gamma
                shadowStep = max(shadowStep, lightMap.b);
                
                float4 baseColor = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv0.xy) * _Color;
                float4 dmcShadowColor = lerp((float4)1, _ShadowColor, _DmcShadowIntensity);
                float4 shadowColor = baseColor * lerp(dmcShadowColor, _ShadowColor, lightMap.b);
                
                float4 finalColor = ...
```

![img](https://pic2.zhimg.com/80/v2-53cb5544d3088fd28476eff8232b9b11_hd.jpg)

![img](https://pic1.zhimg.com/80/v2-3fc02b9700a2275531aefdc0f5b5f544_hd.jpg)RitaLightMap：R：高光强度 B：固有阴影强度 

![img](https://pic4.zhimg.com/80/v2-c400728e4adbaa93d1bcdb6d87f537cf_hd.jpg)

接下来就剩高光了，仔细观察LightMap，可以发现在绘制高光的时候，高光笔触在中间最亮，往上下逐渐变暗，在粗细发生变化时依旧适用，如此精细的绘制正是高质量高光的基础。

由于我们的高光只与左右旋转有关，与上下旋转无关，所以将H、N投影到观察空间XZ平面进行点乘：

```csharp
                float4 shadowColor = ...
                
                float3 NV = mul(UNITY_MATRIX_V, N);
                float3 HV = mul(UNITY_MATRIX_V, H);
                
                float NdotH = dot(normalize(NV.xz), normalize(HV.xz));// xz投影后NdotH
                
                
                float4 finalColor = lerp(baseColor, shadowColor, shadowStep) + pow(NdotH, 6);
```

![img](https://pic4.zhimg.com/v2-75f9a00fa250774c4228c7d84e339eeb_b.jpg)



接下来用一些函数和公式控制NdotH的范围，然后拿NdotH控制LightMap阈值进而控制高光的消失与出现。我希望NdotH越大时，阈值越低，高光范围越大，反之阈值越高，高光范围越小，lightStepMin大于lightMap.r时高光消失：

```csharp
        _LightColor_H ("Light Color H", Color) = (0.3, 0.3, 0.3, 1)
        _LightColor_L ("Light Color L", Color) = (0.05, 0.05, 0.05, 1)
        _LightWidth ("Light Width", Range(0, 1)) = 0.9
        _LightLength ("Light Length", Range(0.1, 1)) = 0.5
        _LightFeather ("Light Feather H", Range(0, 0.5)) = 0.2
        _LightThreshold ("Light Threshold L", Range(0.01, 0.9)) = 0.1
        _LightIntShadow ("Light Intensity In Shadow", Range(0, 1)) = 0.3
...
    float4 _LightColor_H;
    float4 _LightColor_L;
    float _LightWidth;
    float _LightLength;
    float _LightFeather;
    float _LightThreshold;
    float _LightIntShadow;

...
                float NdotH = ...
                NdotH = pow(NdotH, 6) * _LightWidth;//这里将6改为float或属性会遇到一些奇怪的bug，原因不明
                NdotH = pow(NdotH, 1 / _LightLength);//用gamma校正的公式简单控制长度
                
                float lightFeather = _LightFeather * NdotH;
                float lightStepMax = saturate(1 - NdotH + lightFeather);
                float lightStepMin = saturate(1 - NdotH - lightFeather);
                float3 lightColor_H = smoothstep(lightStepMin, lightStepMax, clamp(lightMap.r, 0, 0.99)) * _LightColor_H.rgb;
                
                float4 finalColor = lerp(baseColor, shadowColor, shadowStep);
                finalColor.rgb += lightColor_H;
                
                return finalColor;
```

![img](https://pic4.zhimg.com/v2-084a3d66978573480e113c83dd86e8ff_b.webp)



有内味儿了

其实到这里核心部分已经结束了，剩下的是一些小修小补。通过另一个阈值控制低频高光范围，调整动态阴影中的高光强度，以及固有阴影中不应有高光：

```csharp
                float3 lightColor_H = ...;
                float3 lightColor_L = smoothstep(_LightThreshold, 1, lightMap.r) * _LightColor_L.rgb;
                
                float4 finalColor = ...
                finalColor.rgb += (lightColor_H + lightColor_L) * (1 - lightMap.b) * lerp(1, _LightIntShadow, shadowStep);
                
                return finalColor;
```

完成！

![img](https://pic1.zhimg.com/v2-3f109b51646e8004d57ca9e3c58d1b14_b.jpg)



一些其他实用的效果比如硬标面描边、复杂光照等日后再做分享吧。

丽塔的头发模型和两张贴图已上传群文件（635385414），最后放上完整代码：

```csharp
// by 喵刀Hime  2020/1/22
Shader "Jason Ma/Hair"
{
    Properties
    {
        _MainTex ("Color Map", 2D) = "white" { }
        _LightMap ("Light Map", 2D) = "white" { }
        _Color ("Color", Color) = (1, 1, 1, 1)
        _ShadowColor ("Shadow Color", Color) = (0.6, 0.6, 0.6, 1)
        _DmcShadowIntensity ("Dynamic Shadow Intensity", Range(0, 1)) = 0.5
        _ShadowThreshold ("Shadow Threshold", Range(0, 1)) = 0.5
        [PowerSlider(6)]_ShadowFeather ("Shadow Feather", Range(0.0001, 1)) = 0.01
        
        _LightColor_H ("Light Color H", Color) = (0.3, 0.3, 0.3, 1)
        _LightColor_L ("Light Color L", Color) = (0.05, 0.05, 0.05, 1)
        _LightWidth ("Light Width", Range(0, 1)) = 0.9
        _LightLength ("Light Length", Range(0.1, 1)) = 0.5
        _LightFeather ("Light Feather H", Range(0, 0.5)) = 0.2
        _LightThreshold ("Light Threshold L", Range(0.01, 0.9)) = 0.1
        _LightIntShadow ("Light Intensity In Shadow", Range(0, 1)) = 0.3
    }
    
    HLSLINCLUDE
    
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Common.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Packing.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/NormalSurfaceGradient.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Color.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/UnityInstancing.hlsl"
    #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/EntityLighting.hlsl"
    
    #include "Packages/com.unity.render-pipelines.high-definition/Runtime/ShaderLibrary/ShaderVariables.hlsl"
    #include "Packages/com.unity.render-pipelines.high-definition/Runtime/Lighting/Lighting.hlsl"
    
    CBUFFER_START(UnityPerMaterial)
    float4 _Color;
    float4 _ShadowColor;
    float _DmcShadowIntensity;
    float _ShadowThreshold;
    float _ShadowFeather;
    
    float4 _LightColor_H;
    float4 _LightColor_L;
    float _LightWidth;
    float _LightLength;
    float _LightFeather;
    float _LightThreshold;
    float _LightIntShadow;
    CBUFFER_END
    
    TEXTURE2D(_MainTex); SAMPLER(sampler_MainTex);
    TEXTURE2D(_LightMap); SAMPLER(sampler_LightMap);
    
    ENDHLSL
    
    SubShader
    {
        Tags { "RenderType" = "Opaque" "LightMode" = "ForwardOnly" }
        LOD 100
        
        Pass
        {
            HLSLPROGRAM
            
            #pragma vertex vert
            #pragma fragment frag
            
            struct GraphVertexInput
            {
                float4 vertex: POSITION;
                float4 texcoord0: TEXCOORD0;
                float3 normal: NORMAL;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };
            struct GraphVertexOutput
            {
                float4 position: POSITION;
                half4 uv0: TEXCOORD0;
                float3 positionWS: TEXCOORD1;
                float3 normal: TEXCOORD2;
            };
            
            GraphVertexOutput vert(GraphVertexInput v)
            {
                GraphVertexOutput o;
                // 这里的World Space是相对于摄像机的
                //https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@7.1/manual/Camera-Relative-Rendering.html
                float3 positionWS = TransformObjectToWorld(v.vertex.xyz);
                o.position = TransformWorldToHClip(positionWS);
                o.positionWS = positionWS;
                o.normal = TransformObjectToWorldNormal(v.normal);
                o.uv0 = v.texcoord0;
                
                return o;
            }
            
            float4 frag(GraphVertexOutput i): SV_Target0
            {
                float4 uv0 = i.uv0;
                //Packages\com.unity.render-pipelines.high-definition@7.1.6\Runtime\Lighting\LightDefinition.cs
                DirectionalLightData light = _DirectionalLightDatas[0];
                float3 L = -light.forward.xyz;
                float3 V = GetWorldSpaceNormalizeViewDir(i.positionWS);
                float3 H = normalize(L + V);
                float3 N = normalize(i.normal);
                
                float halfLambert = dot(N, L) * 0.5 + 0.5;
                float shadowStep = saturate(1.0 - (halfLambert - (_ShadowThreshold - _ShadowFeather)) / _ShadowFeather);
                
                float4 lightMap = SAMPLE_TEXTURE2D(_LightMap, sampler_LightMap, uv0.xy);// 未使用A通道所以未校正Gamma
                shadowStep = max(shadowStep, lightMap.b);
                
                float4 baseColor = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv0.xy) * _Color;
                float4 dmcShadowColor = lerp((float4)1, _ShadowColor, _DmcShadowIntensity);
                float4 shadowColor = baseColor * lerp(dmcShadowColor, _ShadowColor, lightMap.b);
                
                float3 NV = mul(UNITY_MATRIX_V, N);
                float3 HV = mul(UNITY_MATRIX_V, H);
                
                float NdotH = dot(normalize(NV.xz), normalize(HV.xz));// xz投影后NdotH
                NdotH = pow(NdotH, 6) * _LightWidth;//这里将6改为float或属性会遇到一些奇怪的bug，原因不明
                NdotH = pow(NdotH, 1 / _LightLength);//用gamma校正的公式简单控制长度
                
                float lightFeather = _LightFeather * NdotH;
                float lightStepMax = saturate(1 - NdotH + lightFeather);
                float lightStepMin = saturate(1 - NdotH - lightFeather);
                float3 lightColor_H = smoothstep(lightStepMin, lightStepMax, clamp(lightMap.r, 0, 0.99)) * _LightColor_H.rgb;
                float3 lightColor_L = smoothstep(_LightThreshold, 1, lightMap.r) * _LightColor_L.rgb;
                
                float4 finalColor = lerp(baseColor, shadowColor, shadowStep);
                finalColor.rgb += (lightColor_H + lightColor_L) * (1 - lightMap.b) * lerp(1, _LightIntShadow, shadowStep);
                
                return finalColor;
            }
            ENDHLSL
            
        }
    }
}
```