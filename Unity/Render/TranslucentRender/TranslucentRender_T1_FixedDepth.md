# unity 半透明渲染技巧(1)：固定深度法

半透明渲染排序问题 长期在各种3d引擎存在，这里将一些针对性技巧。因为通用的解决方案 已经有各种OIT专业方案，比如 gpu 链表 和 depth peeling。但还是那个普遍规律越通用的性能就越不够理想 因为他们不知道你资源的特殊性 可以做哪些极端的简化。所以这里只分享些个人针对一些具体开发积累的小小技巧(持续补充中...)。

对于 为什么会出现这个问题本质原因还不清楚的 可以看这篇基础说明

[小袋子：Shader 学习笔记：透明渲染zhuanlan.zhihu.com

![图标](TranslucentRender_T1_FixedDepth.assets/zhihu-card-default.svg)]

(https://zhuanlan.zhihu.com/p/81883537)

理解这个基础原因很有好处，否则一堆美术问你为什么max maya 没问题 unity ue有问题的时候 你不知道怎么回答。更直接的说是2个原因

1 半透明混合的算法 是 srcAlpha oneMinusSrcAlpha 这个公式是 前后不对称的 所以严重依赖渲染顺序（这也是特效的翅膀半透明模型为什么没深度问题 特效大量用 one one混合 这是前后色对称的 无关顺序的）

2 引擎的半透明排序是逐对象的，离线渲染工具是逐像素的所以没问题

所以接下来针对这2个修改 实现些高性能方案

------

## **深度写入的alphaBlend(固定深度法)**

案例：这是针对头发这种需求，大量中心部分不透明，边缘透明。

原理： 先在不透明区域绘制一遍不写颜色的深度，来强制实行这些像素半透明材质的染顺序正确（因为本被遮挡 有可能渲染到前面的半透明 因为这层深度写入 会绝对剔除 不可能再有机会渲染到前面 产生乱序），因为这部分是模型的绝大部分区域 所以可以确保绝大部分区域的效果正确。但是半透明边缘遮挡半透明边缘的时候 就无法确保正确了 因为 上面这套深度图 不包含这些区域，好在这些区域很小所以可接受 实际效果图如下（为了简化主题 剥离了头发专有的高光计算）。

![img](TranslucentRender_T1_FixedDepth.assets/v2-be3c445e4823384c0505a3e67fdf96b3_1440w.jpg)

全部alphatest效果 边缘不柔和

![img](TranslucentRender_T1_FixedDepth.assets/v2-1ebe05b583c55469a374bde7673695fa_1440w.jpg)

全部 alpahblend效果 边缘柔和但深度错误

![img](TranslucentRender_T1_FixedDepth.assets/v2-726eae13c4b70ea998b6857d100843a9_1440w.jpg)

该方案效果 深度大部分正确+边缘柔和

```glsl
Shader "Hidden/Advanced Hair Shader Pack/Aniso_Opaque" {
	Properties{
	_MainTex("Diffuse (RGB) Alpha (A)", 2D) = "white" {}
	_Color("Main Color", Color) = (1,1,1,1)
    _Cutoff("Alpha Cut-Off Threshold", float) = 0.95
 
	}
	SubShader{
 		Tags{ "Queue" = "AlphaTest"  "RenderType" = "TransparentCutout" }
	 	Blend Off
	 
		Cull off
		ZWrite on
	    colormask 0
  

		Pass
		{
		Name "OPAQUE"
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
		 
 
			#include "UnityCG.cginc"

			struct appdata
			{
				float4 vertex : POSITION;
				float2 uv : TEXCOORD0;
			};

			struct v2f
			{
				float2 uv : TEXCOORD0;
 				float4 vertex : SV_POSITION;
			};

			sampler2D _MainTex;
			float4 _MainTex_ST;
			half4 _Color;
			half _Cutoff;
			v2f vert(appdata v)
			{
				v2f o;
				o.vertex = UnityObjectToClipPos(v.vertex);
				o.uv = TRANSFORM_TEX(v.uv, _MainTex);
 				return o;
			}

				fixed4 frag(v2f i) : SV_Target
				{
				// sample the texture
				fixed a = tex2D(_MainTex, i.uv).a*_Color.a;
				clip(a - _Cutoff);
 				return 0;
			}
		ENDCG
		}
	 }
  
 
}
Shader "Advanced Hair Shader Pack/Aniso_Transparent" {
	Properties{
	_MainTex("Diffuse (RGB) Alpha (A)", 2D) = "white" {}
	_Color("Main Color", Color) = (1,1,1,1)
        _Cutoff("Alpha Cut-Off Threshold", float) = 0.95

	}
		SubShader{
		  UsePass "Hidden/Advanced Hair Shader Pack/Aniso_Opaque/OPAQUE"

		Cull off
		ZWrite off

		 Tags{ "Queue" = "Transparent" "IgnoreProjector" = "True" "RenderType" = "Transparent" "ForceNoShadowCasting" = "True" }

		CGPROGRAM

                 #include "Lighting.cginc"
                 #pragma surface surf Lambert  alpha:auto 
                #pragma target 3.0

         struct Input
	{
	 float2 uv_MainTex;
         float3 viewDir;
	};
       sampler2D _MainTex;
	float _Cutoff;
	fixed4  _Color;
        void surf(Input IN, inout SurfaceOutput o)
	{
		fixed4 albedo = tex2D(_MainTex, IN.uv_MainTex);
		o.Albedo = albedo.rgb*_Color.rgb;
		o.Alpha = saturate(albedo.a / (_Cutoff + 0.0001));
		clip(albedo.a - 0.0001);
	}

	ENDCG

	}


}
```

------