# PCF算法消除阴影(ShadowMap)的锯齿

 

在看这节教程前你得先学会的技术：一，如何用D3D11实现模糊算法  D3D11教程二十六之Blur(模糊处理)

                                                                二，如何用D3D11和ShadowMap实现物体的阴影  D3D11教程三十一之ShadowMap(阴影贴图)
一，SoftShadow(柔软阴影)

在之前我分享一篇大牛写的有关"ShadowMap"介绍的技术博客  Shadow Maping。

我在  D3D11教程三十一之ShadowMap(阴影贴图) 结尾的时候说过，阴影锯齿的诞生是因为ShadowMap的一个像素对应于3D场景的一片区域或者说是ShadowMap的一个像素对应于3D场景的多个像素。

 

看上节的教程我把镜头拉近看，看到的阴影锯齿非常明显，如下图:

 

 

 

首先得说一下，阴影算法有三大类：1，基于ray tracing       2，基于shadow volume   3，  基于shadowmap（Z buffer）

这里我们针对的是ShadowMap成阴影的，大概说一下基于shadowmap有几种算法能削弱阴影的锯齿


(1),Percentage-Closer Filtering(PCF)

(2) Perspective Shadow Maps(PSM)
(3)Light Space Perspective Shadow Maps(LSPSM)
(4)Parallel-Split Shadow Maps for Large-scale Virtual Environments
(5),Variance Shadow Maps.(VSM)

 

我们这个教程消除阴影锯齿的算法的主要是来源于PCF算法的，即“”百分比更近过滤“”。

 

说说算法的步骤：

 

第一步，想正常一样渲染整个场景得到ShadowMap

第二步，渲染阴影所在的地面，阴影的部分为黑色，非阴影部分为白色，这样就形成一张2D仅仅有黑色和白色的纹理图，如图所示：

 

 

第三，对第二步得到的那张黑白色的2D纹理进行模糊算法处理，模糊阴影的锯齿，得到如下面图：

 

 

 

 

第四，对底面进行正常的渲染，用模糊后的黑白色纹理图对地面进行阴影处理，这样地面阴影的锯齿就显得模糊了。

 

 

 

这里请注意的两点是 ：       

          一，这里用到RTT技术，有两个RTT类，一个是RenderModelToDepthTexure类，用于获取ShadowMap(深度图)，一个是RenderModelToBackTexure类用于获取黑白两色的2D纹理图以及进行模糊处理的2D纹理图。
    
          二 ， 通过Usage = D3D11_USAGE_DEFAULT来创建的常量缓存在更新值时又很小的几率会遇上BUG，那个BUG就是你的值无法正确写入到Shader里，非常奇怪。所以更新缓存我还是推荐动态更新缓存，用Map和Unmap来更新，详情可看D3D11之缓存更新(update buffer)       

  


​        

下面放出代码:

 

 

绘制黑白色2D纹理的Shader:  DrawBlackWhiteShadowShader.fx

 

    Texture2D ShadowMap:register(t0);  //阴影纹理
    SamplerState ClampSampleType:register(s0);   //采样方式
    //VertexShader
    cbuffer CBMatrix:register(b0)
    {
    	matrix World;
    	matrix View;
    	matrix Proj;
    	matrix WorldInvTranspose;
    	matrix ProjectorView;
    	matrix ProjectorProj;
    };
     
    cbuffer CBLight:register(b1)
    {
    	float3 PointLightPos;
    	float pad; //填充系数
    };
     
    struct VertexIn
    {
    	float3 Pos:POSITION;
    	float2 Tex:TEXCOORD0;  //多重纹理可以用其它数字
    	float3 Normal:NORMAL;
    };


​     
    struct VertexOut
    {
    	float4 Pos:SV_POSITION;
    	float4 ProjPos:POSITION; //基于点光源投影在齐次裁剪空间的坐标
    	float2 Tex:TEXCOORD0;
    	float3 W_Normal:NORMAL;  //世界空间的法线
    	float3 Pos_W:NORMAL1; //物体在世界空间的顶点坐标
     
    };


​     
    VertexOut VS(VertexIn ina)
    {
    	VertexOut outa;
     
    	//将坐标变换到观察相机下的齐次裁剪空间
    	outa.Pos = mul(float4(ina.Pos,1.0f), World);
    	outa.Pos = mul(outa.Pos, View);
    	outa.Pos = mul(outa.Pos, Proj);
     
    	//将顶点法向量由局部坐标变换到世界坐标
    	outa.W_Normal = mul(ina.Normal, (float3x3)WorldInvTranspose);  //此事世界逆转置矩阵的第四行本来就没啥用
     
    	//对世界空间的顶点法向量进行规格化
    	outa.W_Normal = normalize(outa.W_Normal);
     
    	//获取纹理坐标
    	outa.Tex= ina.Tex;
     
    	//将坐标变换到投影相机下的齐次裁剪空间
    	outa.ProjPos= mul(float4(ina.Pos, 1.0f), World);
    	outa.ProjPos = mul(outa.ProjPos, ProjectorView);
    	outa.ProjPos = mul(outa.ProjPos, ProjectorProj);
     
    	//获取物体在世界空间下的坐标
    	outa.Pos_W= (float3)mul(float4(ina.Pos, 1.0f), World);
    	return outa;
    }


​     
    float4 PS(VertexOut outa) : SV_Target
    {
        float ShadowMapDepth; //r值存储的都是深度
    	float DiffuseFactor;
        float2 ShadowTex;   //阴影纹理坐标
    	float4 color;
    	float bias;
    	float Depth;


​     
    	//设置偏斜量
    	bias = 0.001f;
     
    	//第一,默认下为黑色
    	color = float4(0.0f,0.0f,0.0f,1.0f) ; 
    	
    	//第二,求出相应顶点坐标对应在ShdowMap上的深度值
    	//获取投影相机下的投影纹理空间的坐标值[0.0,1.0]  u=0.5*x+0.5;   v=-0.5*y+0.5;   -w<=x<=w  -w<=y<=w  
    	ShadowTex.x = (outa.ProjPos.x / outa.ProjPos.w)*0.5f + 0.5f;
    	ShadowTex.y = (outa.ProjPos.y / outa.ProjPos.w)*(-0.5f) + 0.5f;


​     
    	//第三,由于3D模型可能超出投影相机下的视截体，其投影纹理可能不在[0.0,1.0],所以得进行判定这个3D物体投影的部分是否在视截体内(没SV_POSITION签名 显卡不会进行裁剪)
    	if (saturate(ShadowTex.x) == ShadowTex.x&&saturate(ShadowTex.y) == ShadowTex.y)
    	{
    		//求出顶点纹理坐标对应的深度值
    		ShadowMapDepth = ShadowMap.Sample(ClampSampleType, ShadowTex).r;
     
    		//求出顶点坐标相应的深度值(点光源到渲染点的深度值)
    		Depth = outa.ProjPos.z / outa.ProjPos.w;


​     
    		//阴影偏斜量
    		ShadowMapDepth = ShadowMapDepth + bias;
     
    		//如果不被遮挡,则物体具备漫反射光
    		if (ShadowMapDepth >= Depth)
    		{
    			//求出漫反射光的的方向
    			float3 DiffuseDir = outa.Pos_W - PointLightPos;


​     
    			//求漫反射光的反光向
    			float3 InvseDiffuseDir = -DiffuseDir;
     
    			//求出漫反射因子[0.0,1.0]
    			DiffuseFactor = saturate(dot(InvseDiffuseDir, outa.W_Normal));
    		
    			//如果漫反射因子大于0，则为白色
    			if (DiffuseFactor>0)
    			{
    				color = float4(1.0f, 1.0f, 1.0f, 1.0f);
    			}
    		}
    	}
    	
    	return color;
    }

 








绘制地面阴影的Shader:   SoftShadowShader.fx

 

    Texture2D BaseTexture:register(t0);  //基础纹理
    Texture2D BlackWhiteShadowMap:register(t1);  //投影纹理
    SamplerState WrapSampleType:register(s0);   //采样方式
    SamplerState ClampSampleType:register(s1);   //采样方式
    //VertexShader
    cbuffer CBMatrix:register(b0)
    {
    	matrix World;
    	matrix View;
    	matrix Proj;
    	matrix WorldInvTranspose;
    };
     
    cbuffer CBLight:register(b1)
    {
    	float4 DiffuseColor;
    	float4 AmbientColor;
    	float3 PointLightPos;
    	float pad; //填充系数
    }
     
    struct VertexIn
    {
    	float3 Pos:POSITION;
    	float2 Tex:TEXCOORD0;  //多重纹理可以用其它数字
    	float3 Normal:NORMAL;
    };


​     
    struct VertexOut
    {
    	float4 Pos:SV_POSITION;
    	float4 ProjPos:POSITION; //基于观察相机的投影在齐次裁剪空间的坐标
    	float2 Tex:TEXCOORD0;
    	float3 W_Normal:NORMAL;  //世界空间的法线
    	float3 Pos_W:NORMAL1; //物体在世界空间的顶点坐标
     
    };


​     
    VertexOut VS(VertexIn ina)
    {
    	VertexOut outa;
     
    	//将坐标变换到观察相机下的齐次裁剪空间
    	outa.Pos = mul(float4(ina.Pos,1.0f), World);
    	outa.Pos = mul(outa.Pos, View);
    	outa.Pos = mul(outa.Pos, Proj);
     
    	//将顶点法向量由局部坐标变换到世界坐标
    	outa.W_Normal = mul(ina.Normal, (float3x3)WorldInvTranspose);  //此事世界逆转置矩阵的第四行本来就没啥用
     
    	//对世界空间的顶点法向量进行规格化
    	outa.W_Normal = normalize(outa.W_Normal);
     
    	//获取纹理坐标
    	outa.Tex= ina.Tex;
     
    	//将坐标变换到投影相机下的齐次裁剪空间
    	outa.ProjPos= mul(float4(ina.Pos, 1.0f), World);
    	outa.ProjPos = mul(outa.ProjPos, View);
    	outa.ProjPos = mul(outa.ProjPos, Proj);
     
    	//获取物体在世界空间下的坐标
    	outa.Pos_W= (float3)mul(float4(ina.Pos, 1.0f), World);
    	return outa;
    }


​     
    float4 PS(VertexOut outa) : SV_Target
    {
    	float4 TexColor; //采集基础纹理颜色
        float4 ShadowColor;//阴影贴图采集的颜色
    	float DiffuseFactor;
    	float4 DiffuseLight;
        float2 ShadowTex;   //阴影纹理坐标
    	float4 color = {0.0f,0.0f,0.0f,0.0f}; //最终输出的颜色


​     
    	//获取基础纹理的采样颜色
        TexColor = BaseTexture.Sample(WrapSampleType, outa.Tex);
     
    	//求出漫反射光的的方向
    	float3 DiffuseDir = outa.Pos_W - PointLightPos;
     
    	//求出点光源到像素的距离
    	float distance = length(DiffuseDir);
     
    	//求出衰减因子
    	float atten1 = 0.5f;
    	float atten2 = 0.1f;
    	float atten3 = 0.0f;
    	float LightIntensity = 1.0f / (atten1 + atten2*distance + atten3*distance*distance);
     
    	//求漫反射光的反光向
    	float3 InvseDiffuseDir = -DiffuseDir;


​     
    	//求出漫反射因子[0.0,1.0]
    	DiffuseFactor = saturate(dot(InvseDiffuseDir, outa.W_Normal));
     
    	//求出漫射光
    	DiffuseLight = DiffuseFactor*DiffuseColor*LightIntensity;
     
    	//颜色加上漫反射光
    	color += DiffuseLight;
    	color = saturate(color);
    	
    	//第三,求出相应顶点坐标对应在ShdowMap上的深度值
    	//获取投影相机下的投影纹理空间的坐标值[0.0,1.0]  u=0.5*x+0.5;   v=-0.5*y+0.5;   -w<=x<=w  -w<=y<=w  
    	ShadowTex.x = (outa.ProjPos.x / outa.ProjPos.w)*0.5f + 0.5f;
    	ShadowTex.y = (outa.ProjPos.y / outa.ProjPos.w)*(-0.5f) + 0.5f;
    	
    	//第四，求出黑白ShadowMap采集的颜色
    	ShadowColor= BlackWhiteShadowMap.Sample(ClampSampleType, ShadowTex);


​    	
    	//用黑白ShadowMap的颜色调节像素
    	color = color*ShadowColor;
     
    	//不管有没有遮挡，都应该具备环境光,注意环境光不生成阴影,这里仅仅是漫反射光生成阴影
    	color += AmbientColor;
     
    	//用基础纹理颜色进行调节
    	color = color*TexColor;
     
    	return color;
    }

 










最后放出程序运行图：

 

 

阴影锯齿果然模糊了很多，以后有时间我回来实现以下其它的SoftShadow算法。

 

集成了CSM算法的3D渲染引擎源码：

  https://github.com/2047241149/SDEngine

源代码链接如下:

http://download.csdn.net/detail/qq_29523119/9673916

 

另外一种方法实现(不借用黑白纹理)的PCF的源码链接:

http://download.csdn.net/detail/qq_29523119/9864010
--------------------- 
作者：小毛狗 
来源：CSDN 
原文：https://blog.csdn.net/qq_29523119/article/details/53038901 
版权声明：本文为博主原创文章，转载请附上博文链接！
