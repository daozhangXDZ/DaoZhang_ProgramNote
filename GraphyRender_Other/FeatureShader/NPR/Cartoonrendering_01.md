# 非真实渲染技术（NPR）-1.卡通渲染

非真实感绘制(Non-photorealistic rendering)

(NPR)是计算机图形学的一类，主要模拟艺术式的绘制风格，也用于发展新绘制风格。和传统的追求真实感的计算机图形学不同，NPR受到油画，素描，技术图纸，和动画卡通的影响。NPR已经以"卡通造影"的形式出现在电影和电子游戏中，它也已出现在设计图纸和试验动画中

（一）卡通渲染

卡通渲染是一种特殊的非真实感绘制技术，它要求帖图由不明显的渐变色块夹杂一些不复杂的纹理组成。它强调粗细线条和简单色块，忽略细节。利用这些很简单很纯粹的线条和色块，就能渲染出设计师所要求的质感很强的卡通效果，从而营造出互动的二维动画世界。

 

采用该技术的游戏：《网络急速赛车》

 

 

 

 

卡通绘画中，包含：勾边、卡通光影、边缘光晕、头发高光等技术，如下：

 

 

 

我们下面对 勾边 和 卡通着色（cartoon shading）进行讲解；

Silhouette（轮廓勾边）：

勾边方式有 像素勾边和顶点勾边，我们采用了sobel边缘检测算法，其理论基础请参考：

http://blog.csdn.net/tianhai110/archive/2010/06/11/5663756.aspx

 

实现原理：

1.      把模型渲染到一张纹理图上；

2.      对这张图进行sobel边缘检测，找出边界并把渲染到屏幕空间中。

 

所以我们需要通过两个Pass渲染， 第一个pass把模型渲染到一张纹理中，第二个pass进行边缘检测并输出渲染效果。

第二个pass的vs,ps如下：

VS_OUTPUT vs_main( VS_INPUT In )

{

   VS_OUTPUT Out;

 

// 保证物体的坐标在[-1,1]之间

   In.Pos.xy = sign(In.Pos.xy);

 

// 让物体以屏幕坐标系统渲染；

   Out.Pos       = float4(In.Pos.xy, 0.0, 1.0);

  

//对齐纹理坐标

   Out.TexCoord.x = 0.5 * (1 + In.Pos.x);

   Out.TexCoord.y = 0.5 * (1 - In.Pos.y);

 

   return Out;

}

 

Pixel Shader 为：

sampler2D rttMap;

const float off = 1.0/512.0;

 

float4 ps_main( float2 tex:TEXCOORD0) : COLOR0

{

   float p00 = tex2D( rttMap, tex + float2(-off, -off)).r;

   float p01 = tex2D( rttMap, tex + float2( 0, -off)).r;

   float p02 = tex2D( rttMap, tex + float2( off, -off)).r;

  

   float p10 = tex2D( rttMap, tex + float2(-off, 0)).r;

   float p12 = tex2D( rttMap, tex + float2( off, 0)).r;

  

   float p20 = tex2D( rttMap, tex + float2(-off, off)).r;

   float p21 = tex2D( rttMap, tex + float2( 0, off)).r;

   float p22 = tex2D( rttMap, tex + float2( 1, off)).r;

  

// sobel算子的横纵灰度值

   float gx = (p00 + 2*p10 + p20) - (p02 + 2*p12 + p22);

   float gy = (p00 + 2*p01 + p02) - (p20 + 2*p21 + p22);

  

   float edgeSqr = gx*gx + gy*gy;

  

// 阀值0.07

   return 1 - ( edgeSqr > 0.07*0.07);

}

 

这个实例中，渲染状态要改 D3DRS_CULLMODE 为 D3DCULL_NONE; 不然不显示

 

编程中const float off = 1.0/512.0 写成了 const float off = 1/512;

结果半天都显示不出来， 注意1/512 为0；   而1.0/512.0 为0.001953125;

 

 

 

卡通着色（Cel-Shading）

为了实现卡通着色， 我们需要创建一个带强度级别的灰度纹理， 来达到卡通绘画中的阴影过度效果。

 

然后在顶点着色器中，我们执行基本的散射运算，通过 光向量L与法向量N的点积，以确定顶点接受到了多少光线：

S= L.N

如果s<0;表明光线和顶点法线间的夹角大于90度，顶点接受不到任何光线，所以如果s<0,则让s=0;  以便让s位于[0,1]之间，方便在纹理坐标空间取值。

像素处理器中，我们从亮度纹理中取值， 由于亮度纹理只有3中颜色，所以着色的结果是一种颜色到另一种颜色的生硬过度，这正是我们所期望的。

 

VS代码片段：

VS_OUTPUT vs_main( VS_INPUT Input )

{

   VS_OUTPUT Output;

 

   Output.Position = mul( Input.Position, matViewProjection );

  

   float3 posW    = mul( matView, Input.Position );

   float3 normalW = mul( Input.Normal, matView);

  

   float diffuse = max(0, dot(vecLightDir, normalW));

   Output.Texcoord.x = diffuse;

   Output.Texcoord.y = 0.0f;

  

   return( Output );

  

}

PS代码：

sampler cartoonMap;

 

float4 ps_main( float2 tex:TEXCOORD0) : COLOR0

{  

   return tex2D( cartoonMap, tex);  

}

 

结果如下：

 

 

 

带轮廓的卡通渲染：

综合以上两种技术，要实现带轮廓的卡通图， 需要3个pass来渲染：

1.      把模型的卡通渲染图 渲染到一张纹理上(RTT),  alpha设置为1，以便轮廓的查找；

2.      第二个pass，对刚才得到的纹理的alpha通道，进行边缘检测（绘制过的地方为1，没绘制的地方为0），并将结果也绘制到一张纹理中。

3.      合并上面得到的2张图，如果边缘图上有边缘，就绘制边缘图上的颜色，否则绘制第一个pass上的颜色。

结果如下：

---------------------
作者：挨踢大侠 
来源：CSDN 
原文：https://blog.csdn.net/tianhai110/article/details/5666190 
版权声明：本文为博主原创文章，转载请附上博文链接！
