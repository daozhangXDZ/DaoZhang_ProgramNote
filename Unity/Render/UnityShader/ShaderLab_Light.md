# Unity3D -- shader光照常用函数和变量

1、内置的光照变量

```
_LightColor0    		float4  	//该Pass处理的逐像素光源的颜色
_WorldSpaceLightPos0    float4  	//_WorldSpaceLightPos0.xyz是该Pass处理的逐像素光源的位置。如果该光源是平行光，那么_WorldSpaceLightPos0.w是0，其他光源类型是1
_LightMatrix0   		float4x4	//从世界空间到光源空间的变换矩阵，可以用于采样cookie和光强衰减纹理
unity_4LightPosX0,
unity_4LightPosY0,
unity_4LightPosZ0   	float4  	//仅用于Base Pass,前4个非重要的点光源在世界空间中的位置
unity_4LightAtten() 	float4  	//仅用于Base Pass， 存储了前4个非重要的点光源的衰减因子
unity_LightColor    	half4[4]    //仅用于Base Pass，存储了前4个非重要的点光源的颜色
```

 

2 、LightMode标签支持的渲染路径设置选项

```
Always  		//不管使用哪种渲染路径，该Pass总会被渲染，但是不会计算任何光照
ForwardBase 	//用于前向渲染，该Pass会计算环境光，最重要的的平行光，逐顶点/SH光源和Lightmaps
ForwardAdd  	//用于前向渲染，该Pass会计算额外的逐像素光源，每个Pass对应一个光源
Deferred    	//用于延迟渲染，该Pass会渲染G缓冲（G_buffer）
ShadowCaster    //把物体的深度信息渲染到阴影映射纹理或一张深度纹理中
PrepassBase 	//用于遗留延迟渲染，该Pass会渲染法线和高光反射的指数部分
PrepassFinal    //用于遗留延迟渲染，该Pass通过合并纹理、光照、自发光来渲染得到的最后的颜色
Vertex,VertexLMRGBM和VertexLM    //用于遗留的顶点照明渲染
```

 

3、顶点照明渲染路径中可以使用的内置变量

```
unity_LightColor    half4[8]    //光源颜色
unity_LightPosition float4[8]   //xyz分量是视角空间中的光源位置，如果光源是平行光，那么z分量值为0，其他光源类型z分量值为1
unity_LightAtten    half4[8]    //光源衰减因子，如果光源是聚光灯，x分量是cos(spotAngle/2),y分量是1/cos(spotAngle/4);如果是其他光源，x分量是-1，y分量是1，z分量是衰减的平分，w分量是光源范围开根号的结果
unity_SpotDirection float4[8]   //如果光源是聚光灯的话，值为视角空间的聚光灯的位置，如果是其他类型的光源，值为（0,0,1,0）
```

 

4、顶点照明渲染路径中可以使用的内置函数

```
float3 ShadeVertexLights(float4 vertex,float normal)     
//输入模型空间中的顶点位置和法线，计算四个顶点光源的光照以及环境光

float3 ShadeVertexLightsFull(float4 vertex, float3 normal, int lightCount, bool spotLig
```