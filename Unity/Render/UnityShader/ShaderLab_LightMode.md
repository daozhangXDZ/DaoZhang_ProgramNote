

# LightMode multi_compile_fwdbase



# ForwardBase

```
Tags { "LightMode" = "ForwardBase" }
```

 告诉渲染管线，这个pass作为ForwardBase处理，缺少它将画不出任何东西。

```
#pragma multi_compile_fwdbase
```

 unity官方文档，只有multi_compile的说明，对于multi_compile_fwdbase可谓只字未提，网上[唯一能搜到的一篇](http://joeyfladderak.com/let-there-be-shadow/)也是一语带过（虽然不甚详细，但是非常感谢作者分享）。后来打开unity shader面板的Variants里看到：

```
DIRECTIONAL LIGHTMAP_OFF DIRLIGHTMAP_OFF SHADOWS_OFF
DIRECTIONAL LIGHTMAP_ON DIRLIGHTMAP_OFF SHADOWS_OFF
DIRECTIONAL LIGHTMAP_ON DIRLIGHTMAP_ON SHADOWS_OFF
DIRECTIONAL LIGHTMAP_OFF DIRLIGHTMAP_OFF SHADOWS_SCREEN
DIRECTIONAL LIGHTMAP_ON DIRLIGHTMAP_OFF SHADOWS_SCREEN
DIRECTIONAL LIGHTMAP_ON DIRLIGHTMAP_ON SHADOWS_SCREEN
DIRECTIONAL LIGHTMAP_OFF DIRLIGHTMAP_OFF SHADOWS_OFF VERTEXLIGHT_ON
DIRECTIONAL LIGHTMAP_OFF DIRLIGHTMAP_OFF SHADOWS_SCREEN VERTEXLIGHT_ON
DIRECTIONAL LIGHTMAP_OFF DIRLIGHTMAP_OFF SHADOWS_SCREEN SHADOWS_NATIVE
DIRECTIONAL LIGHTMAP_ON DIRLIGHTMAP_OFF SHADOWS_SCREEN SHADOWS_NATIVE
DIRECTIONAL LIGHTMAP_ON DIRLIGHTMAP_ON SHADOWS_SCREEN SHADOWS_NATIVE
DIRECTIONAL LIGHTMAP_OFF DIRLIGHTMAP_OFF SHADOWS_SCREEN SHADOWS_NATIVE VERTEXLIGHT_ON
```



很多看过unity生成的vertex/fragment代码的同学，会感到很困惑，代码里充斥着各种条件编译代码，然而unity也没有给出文档，到底有哪些keyword？各自的作用是什么？ 
看到这个就非常清楚了，unity为forwardbase pass定义的keyword都在这里，而multi_compile_fwdbase就是unity专门为forwardbase预定义的multi_compile。 
如果再打开unity最终编译成的glsl代码的话，可以看到，unity为每一组keywards都生成了单独的代码。 
如果缺少这行代码的话，那么unity默认会编译

```
DIRECTIONAL LIGHTMAP_ON DIRLIGHTMAP_ON SHADOWS_OFF
```

这一组条件，碰到其他的情况，那么渲染就会出错。 
我们看到，上述每一组条件，都是DIRECTIONAL，那么如果场景中没有平行光呢？点光源或者聚光灯还会起作用么？ 
答案是不会。forwardbase pass只能以逐像素的方式处理平行光，点光源和聚光灯都会被忽略掉，对应的_LightColor0都将是黑色。注意上面黑体的逐像素，因为可能有人会说，我场景里只有一个点光源，可以把场景照亮。是的，但它是以逐顶点的方式照亮的，后面将会细说。

```
// vertex-to-fragment interpolation data



#ifdef LIGHTMAP_OFF



struct v2f_surf {



  float4 pos : SV_POSITION;



  float2 pack0 : TEXCOORD0;



  fixed3 normal : TEXCOORD1;
  fixed3 vlight : TEXCOORD2;
  LIGHTING_COORDS(3,4)
};
#endif
#ifndef LIGHTMAP_OFF
struct v2f_surf 
{
  float4 pos : SV_POSITION;
  float2 pack0 : TEXCOORD0;
  float2 lmap : TEXCOORD1;
  LIGHTING_COORDS(2,3)
};
```