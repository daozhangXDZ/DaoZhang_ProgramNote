# (转)光线步进Ray Marching 与 体积绘

原文：https://blog.csdn.net/a003655/article/details/87797869

效果如下：

![img](Volume_Painting.assets/20190220153734643.gif)

第一步，定义视角相关的参数，观察点位置离观察目标点位置的距离，观察点视角度数，观察者头顶方向，得到摄像机矩阵

第二步，光线步进，每步进一次进行采样，定义最小步进深度，最大步进深度，如果光线和目标的距离小于0.01就算作捕捉到目标，返回光线的步进深度（长度）,如果N次光线步进没有捕获到目标或步进深度大于最大步进深度，就返回最大步进深度。

代码如下：

```
Shader "Unlit/howRayMarching"



{



	Properties



	{



		_MainTex ("Texture", 2D) = "white" {}



 



		//1.定义view matrix 的3参数



		_EyePosition("观察点位置",Vector) = (0,0,-2,0) 



		_EyeUp("观察点上方",Vector) = (1,0,0,0) 



		_EyeTarget("观察点目标",Vector) = (0,0,0,0)



		_FieldOfView("观察者视角角度",Float) = 60



 



		minDist ("光线步进的最小距离",Float) = 0.0



        maxDist ("光线步进的最大距离",Float) = 10.0



 		r("视角的旋转角度",Range(0,6.283))=0.0



	}



	SubShader



	{



		Tags { "RenderType"="Opaque" }



		LOD 100



 



		Pass



		{



			Blend SrcAlpha OneMinusSrcAlpha



			CGPROGRAM



			#pragma vertex vert



			#pragma fragment frag



			// make fog work



			#pragma multi_compile_fog



			



			#include "UnityCG.cginc"



 



			struct appdata



			{



				float4 vertex : POSITION;



				float2 uv : TEXCOORD0;



			};



 



			struct v2f



			{



				float2 uv : TEXCOORD0;



				UNITY_FOG_COORDS(1)



				float4 vertex : SV_POSITION;



			};



 



			sampler2D _MainTex;



			float4 _MainTex_ST;



 



			//2.在pass里重新写入一次



			float4 _EyePosition;



			float4 _EyeUp;



			float4 _EyeTarget;



			float _FieldOfView;



 



			float minDist;



            float maxDist;



            float r;



 



			v2f vert (appdata v)



			{



				v2f o;



				o.vertex = UnityObjectToClipPos(v.vertex);



				o.uv = TRANSFORM_TEX(v.uv, _MainTex);



				UNITY_TRANSFER_FOG(o,o.vertex);



				return o;



			}



 



			float4x4 GetWorldCameraMatrix(float3 eyePosition,float3 eyeUp,float3 eyeTarget)



			{



				eyeUp = normalize(eyeUp);



				float3 viewDirection = normalize( float3(eyeTarget - eyePosition));



				float3 eyeRight = cross(eyeUp,viewDirection);



 



				float4x4 worldCameraMatrix = float4x4(eyeRight,0,



											   eyeUp,0,



											   viewDirection,0,



											   0,0,0,1);



				return worldCameraMatrix;



			}



 



			//光线到四方体的距离检测



			float cubeSDF(float3 p) {



			    p = mul(float3x3(1.0,0.0,0.0,



        	    	  0.0,cos(r),sin(r),



            		  0.0,-sin(r),cos(r)),p);



    			float3 d = abs(p) - float3(1.0, 1.0, 0.001); //这里四面体的z轴长度设置为极小值，假设四面体为面片



    			float insideDistance = min(max(d.x, max(d.y, d.z)), 0.0);



    			float outsideDistance = length(max(d, 0.0));



    			float dis=insideDistance + outsideDistance;



    			return dis;



			}



 



 



			float overlay(float3 p)



			{



				return cubeSDF(p);



			}



 



			float getDist(float3 cameraOrign , float3 dir)



			{



				float depth = minDist;



				for(int i=0;i<500;i+=1){



					float3 rayPosition  = cameraOrign + depth*dir;



					float dist = overlay(rayPosition);



					if(dist<0.01){ //如果光线和目标的距离小于0.01，就返回光线的长度



						return depth;



					}



					depth += dist;



					if(depth>=maxDist){



						return maxDist;



					}



				}



				return maxDist;



			}



 



			fixed4 frag (v2f i) : SV_Target



			{



				float2 uv = i.uv;



			 	uv-=0.5;



			 	float2 size = float2(1.0,1.0);



			 	float z = size.y/tan(radians(_FieldOfView) / 2.0);



			 	float3 rayDir = normalize(float3(uv.xy,z));



 



				float4x4 worldCameraMatrix = GetWorldCameraMatrix(_EyePosition,_EyeUp,_EyeTarget);



 



				//3.将视线的世界坐标转化为视角坐标



				float3 ViewDirectionCamera = mul(worldCameraMatrix,float4(rayDir.xyz,0)).xyz;



 



				//4.光线步进进行采样



				float dist=getDist(_EyePosition,ViewDirectionCamera);  



 



				//5.光线步进深度超过最大步进深度就忽略当前像素



				if(dist>maxDist-0.001){



					return float4(0.0,0.0,0.0,1.0);



				}



 



				//其他：对一面进行绘制图片



    			float3 p =  _EyePosition + dist * ViewDirectionCamera;



 



    			p = mul( float3x3(1.0,0.0,0.0,



            	    	 0.0,cos(r),sin(r),



              			 0.0,-sin(r),cos(r)),p);



              		



    			float3 onRectUV = (p.xyz  +float3(1,1,0))*0.5;



    



    			float4 finalColor = float4(tex2D(_MainTex,onRectUV.xy));



    			finalColor.xyz*=finalColor.a;



    			if(finalColor.a<0.001){



    				return float4(0.0,0.0,0.0,1.0);



    			}



 



                return finalColor;



			}



			ENDCG



		}



	}



}
```