# [UnityShader-菲涅尔反射（Fresnel Reflection）](https://www.cnblogs.com/lijiajia/p/8013168.html)

菲涅耳公式（或菲涅耳方程），由奥古斯丁·让·菲涅耳导出。用来描述光在不同折射率的介质之间的行为。由公式推导出的光的反射称之为“菲涅尔反射”。菲涅尔公式是光学中的重要公式，用它能解释反射光的强度、折射光的强度、相位与入射光的强度的关系
 ![奥古斯丁·让·菲涅耳](Untitled.assets/1208599-7dd85cd97f12b406.png)

## 在计算机图形学中的应用

一般运用于水面效果，试想一下你站在湖边，低头看向水里，你会发现近的地方非常清澈见底（反射较少），而看远的地方却倒映着天空（反射较多）。这就是菲尼尔效应

## 效果

![img](Untitled.assets/1208599-83212960c89a067e.png)
 这里直接让反射颜色为红色，可以看到远处的更红，而近处的为光照颜色白色
 ![fresnel效果的球体](https://upload-images.jianshu.io/upload_images/1208599-cb3cadec841d7ee9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/500)

![fresnel+cubemap效果](Untitled.assets/1208599-290956e8e56cd533.png)

## 简化后的公式

由于真实的菲尼尔公式计算量较多。在游戏里往往会用简化版的公式来提升效率达到近似的效果

```
fresnel = fresnel基础值 + fresnel缩放量*pow( 1 - dot( N, V ), 5 )
```

## Shader实现

```
Shader "lijia/fresnelTest"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _fresnelBase("fresnelBase", Range(0, 1)) = 1
        _fresnelScale("fresnelScale", Range(0, 1)) = 1
        _fresnelIndensity("fresnelIndensity", Range(0, 5)) = 5
        _fresnelCol("_fresnelCol", Color) = (1,1,1,1)
    }

    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            tags{"lightmode="="forward"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
                float3 normal : NORMAL;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 L : TEXCOORD1;
                float3 N : TEXCOORD2;
                float3 V : TEXCOORD3;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            float _fresnelBase;

            float _fresnelScale;

            float _fresnelIndensity;

            float4 _fresnelCol;

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                //将法线转到世界坐标
                o.N = mul(v.normal, (float3x3)unity_WorldToObject);
                //获取世界坐标的光向量
                o.L = WorldSpaceLightDir(v.vertex);
                //获取世界坐标的视角向量
                o.V = WorldSpaceViewDir(v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);

                float3 N = normalize(i.N);
                float3 L = normalize(i.L);
                float3 V = normalize(i.V);

                col.rgb *= saturate(dot(N, L)) * _LightColor0.rgb;
                //菲尼尔公式
                float fresnel = _fresnelBase + _fresnelScale*pow(1 - dot(N, V), _fresnelIndensity);

                col.rgb += lerp(col.rgb, _fresnelCol, fresnel) * _fresnelCol.a;

                return col;
            }

            ENDCG
        }
    }
}
```

转载请注明出处：  李嘉的博客 - <http://www.cnblogs.com/lijiajia>