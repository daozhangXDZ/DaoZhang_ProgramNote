# 虚幻4渲染编程（程序化纹理篇）【第一卷：UnrealSubstance工具节点搭建---噪波】



## **本篇概述：**

​         程序化纹理有着很多好处，第一可以方便修改，当我们的生成逻辑写好后，想要调整的话就是调调参数的事情。第二就是思路清晰，这张图是怎么来的，逻辑非常清晰，而不是传统的图像绘制，画到哪儿想到哪儿，思维是游走的，离散的。第三我们可以实时生成，可以让纹理和玩家产生互动等等。

​          现在主流的是用Substance来生成，但是其实引擎也能做，引擎本来就是用来操作这些素材的地方。想看引擎和Substance的对接的话可能你要失望了，对于目前的Substance而言，我个人极力反对目前版本的Substance和引擎直接结合。本章将在引擎里实现各种程序化纹理，不管是离线烘焙也好，还是实时生成也罢。

**程序化纹理篇的大概规划是，先把程序化生成需要的节点我们自己全部开发一次，然后把这些工具节点撸好以后在开始用这些工具做纯程序化的纹理（在引擎中）。我们的核心目的是把材质编辑器拓展成引擎内置的“Substance”，像Substance一样能有几何生成，图像转换等功能。**当然拓展材质编辑器有很多种办法，不止改引擎一个。

​        在开始本篇之前最好能熟练使用Substance软件。欢迎各路大神斧正错误。

------

​        Substance有很多噪波生成器，下面将从最基础的噪波开始，把Substance有的或者没有的噪波生成节点全部在Unreal种实现。使用噪波的组合，我们能做出很多效果。

​        要生成一个噪声，我们一般需要三步，第一步是构造随机发生器，第二步是插值，第三步是叠加。

噪声从生成方式上可以分为几种：

（1）white noise

（2）perlin noise

（3）value noise

（4）worley noise

## **【1】Fast Noise（White Noise）**

效果：



![img](https://pic1.zhimg.com/80/v2-51e046a6b761b3b20b8b58ce28ca3ff0_hd.jpg)

公式代码：

```text
float RandFast( uint2 PixelPos, float Magic = 3571.0 )
{
	float2 Random2 = ( 1.0 / 4320.0 ) * PixelPos + float2( 0.25, 0.0 );
	float Random = frac( dot( Random2 * Random2, Magic ) );
	Random = frac( Random * Random * (2 * Magic) );
	return Random;
}
```

材质：



![img](https://pic3.zhimg.com/80/v2-fbe7579ecc83e5fcec6af23bc6c3f052_hd.jpg)

其实为啥这个算法是这样呢，并没有为啥，就是拟合得好所以就这样了。我把这些常用的函数封装到材质函数节点里，以后做程序化纹理的时候就能直接用了。



![img](https://pic4.zhimg.com/80/v2-3cf7e9e4b4faa839dc2c09e9069a2067_hd.jpg)



![img](https://pic3.zhimg.com/80/v2-3ee20596f1daa66279fc48d53daf110a_hd.jpg)

后面的很多介绍里的很多这种公用逻辑都会这样做，做完这些只会我们就能建立一个自己的工具库，就像Substance那样。这时有人就要说了，我们不是有noise节点么，为啥还要自己写呢？其实我们应该更多靠自己，我们需要知道原理之后才能根据需求来改进它和精进它，而不是一直拿来主义。

这一步就是只做了构造随机发生器这一步。

------

## **【2】Random With Scale（White Noise）**

这种是对上面的改进，加入缩放因素，可以让我们做出棋盘格之类的纹理

效果：



![img](https://pic3.zhimg.com/80/v2-51e20fa1b1647d4e5d509cca96d772ca_hd.jpg)

代码：

```text
float2 Random(float2 uv)
{
    float2 Random2 = ( 1.0 / 4320.0 ) * PixelPos + float2( 0.25, 0.0 );
	float Random = frac( dot( Random2 * Random2, Magic ) );
	Random = frac( Random * Random * (2 * Magic) );
	return Random;
}
```

材质：





------

## **【3】Perlin Noise**

想要生成柏林噪声，需要做以下几步：

（1）定义晶格,每个晶格的顶点有一个“伪随机”的梯度向量（其实就是个向量啦）。对于二维的Perlin噪声来说，晶格结构就是一个平面网格，三维的就是一个立方体网格。

（2）输入一个点（二维的话就是二维坐标，三维就是三维坐标，n维的就是n个坐标），我们找到和它相邻的那些晶格顶点（二维下有4个，三维下有8个，n维下有 ![2^{n}](https://www.zhihu.com/equation?tex=2%5E%7Bn%7D) 个），计算该点到各个晶格顶点的距离向量，再分别与顶点上的梯度向量做点乘，得到 ![2^{n}](https://www.zhihu.com/equation?tex=2%5E%7Bn%7D) 个点乘结果。

（3）使用缓和曲线来计算它们的权重和。

以二维为例主要代码如下（解释看注释）

```text
//随机数
float2 hash22(float2 p)
{
    p = float2( dot(p,float2(127.1,311.7)),
              dot(p,float2(269.5,183.3)));

    return -1.0 + 2.0 * frac(sin(p) * 43758.5453123);
}

//构造perlin noise，输入一个点
float perlin_noise(float 2p)
{
    //生成第二步：构建晶格
    float2 pi = floor(p);
    float2 pf = p - pi;
    float2 w = pf * pf * (3.0 - 2.0 * pf);

    //生成第三步：使用缓和曲线
    return lerp(lerp(dot(hash22(pi + float2(0.0, 0.0)), pf - float2(0.0, 0.0)), 
                   dot(hash22(pi + float2(1.0, 0.0)), pf - float2(1.0, 0.0)), w.x), 
               lerp(dot(hash22(pi + float2(0.0, 1.0)), pf - float2(0.0, 1.0)), 
                   dot(hash22(pi + float2(1.0, 1.0)), pf - float2(1.0, 1.0)), w.x),
               w.y);
}
```

把单一的perlin noise进行叠加即可出现很多有趣的效果。下面几个是多层叠加的柏林噪波

效果：

Noise itself



Noise_Sum



noise_sum_abs



![img](https://pic4.zhimg.com/80/v2-127feda02c4fffe96a56b68b1d98617f_hd.jpg)

noise_sum_abs_sin



![img](https://pic3.zhimg.com/80/v2-dc92312648b486acceba72ccd11285ce_hd.jpg)

代码：

```text
//#define Use_Perlin
//#define Use_Value
#define Use_Simplex

// ========= Hash ===========

float3 hashOld33(float3 p)
{   
	p = float3( dot(p,float3(127.1,311.7, 74.7)),
			  dot(p,float3(269.5,183.3,246.1)),
			  dot(p,float3(113.5,271.9,124.6)));
    
    return -1.0 + 2.0 * frac(sin(p)*43758.5453123);
}

float hashOld31(float3 p)
{
    float h = dot(p,float3(127.1,311.7, 74.7));
    
    return -1.0 + 2.0 * frac(sin(h)*43758.5453123);
}

// Grab from https://www.shadertoy.com/view/4djSRW
#define MOD3 float3(0.1031, 0.11369, 0.13787)
//#define MOD3 float3(443.8975,397.2973, 491.1871)
float hash31(float3 p3)
{
	p3  = frac(p3 * MOD3);
    p3 += dot(p3, p3.yzx + 19.19);
    return -1.0 + 2.0 * frac((p3.x + p3.y) * p3.z);
}

float3 hash33(float3 p3)
{
	p3 = frac(p3 * MOD3);
    p3 += dot(p3, p3.yxz+19.19);
    return -1.0 + 2.0 * frac(float3((p3.x + p3.y)*p3.z, (p3.x+p3.z)*p3.y, (p3.y+p3.z)*p3.x));
}

// ========= Noise ===========

float value_noise(float3 p)
{
    float3 pi = floor(p);
    float3 pf = p - pi;
    
    float3 w = pf * pf * (3.0 - 2.0 * pf);
    
    return 	lerp(
        		lerp(
        			lerp(hash31(pi + float3(0, 0, 0)), hash31(pi + float3(1, 0, 0)), w.x),
        			lerp(hash31(pi + float3(0, 0, 1)), hash31(pi + float3(1, 0, 1)), w.x), 
                    w.z),
        		lerp(
                    lerp(hash31(pi + float3(0, 1, 0)), hash31(pi + float3(1, 1, 0)), w.x),
        			lerp(hash31(pi + float3(0, 1, 1)), hash31(pi + float3(1, 1, 1)), w.x), 
                    w.z),
        		w.y);
}

float perlin_noise(float3 p)
{
    float3 pi = floor(p);
    float3 pf = p - pi;
    
    float3 w = pf * pf * (3.0 - 2.0 * pf);
    
    return 	lerp(
        		lerp(
                	lerp(dot(pf - float3(0, 0, 0), hash33(pi + float3(0, 0, 0))), 
                        dot(pf - float3(1, 0, 0), hash33(pi + float3(1, 0, 0))),
                       	w.x),
                	lerp(dot(pf - float3(0, 0, 1), hash33(pi + float3(0, 0, 1))), 
                        dot(pf - float3(1, 0, 1), hash33(pi + float3(1, 0, 1))),
                       	w.x),
                	w.z),
        		lerp(
                    lerp(dot(pf - float3(0, 1, 0), hash33(pi + float3(0, 1, 0))), 
                        dot(pf - float3(1, 1, 0), hash33(pi + float3(1, 1, 0))),
                       	w.x),
                   	lerp(dot(pf - float3(0, 1, 1), hash33(pi + float3(0, 1, 1))), 
                        dot(pf - float3(1, 1, 1), hash33(pi + float3(1, 1, 1))),
                       	w.x),
                	w.z),
    			w.y);
}

float simplex_noise(float3 p)
{
    const float K1 = 0.333333333;
    const float K2 = 0.166666667;
    
    float3 i = floor(p + (p.x + p.y + p.z) * K1);
    float3 d0 = p - (i - (i.x + i.y + i.z) * K2);
    
    // thx nikita: https://www.shadertoy.com/view/XsX3zB
    float3 e = step(float3(0, 0, 0), d0 - d0.yzx);
	float3 i1 = e * (1.0 - e.zxy);
	float3 i2 = 1.0 - e.zxy * (1.0 - e);
    
    float3 d1 = d0 - (i1 - 1.0 * K2);
    float3 d2 = d0 - (i2 - 2.0 * K2);
    float3 d3 = d0 - (1.0 - 3.0 * K2);
    
    float4 h = max(0.6 - float4(dot(d0, d0), dot(d1, d1), dot(d2, d2), dot(d3, d3)), 0.0);
    float4 n = h * h * h * h * float4(dot(d0, hash33(i)), dot(d1, hash33(i + i1)), dot(d2, hash33(i + i2)), dot(d3, hash33(i + 1.0)));
    
    return dot(float4(31.316, 31.316, 31.316, 31.316), n);
}

float noise(float3 p) 
{
#ifdef Use_Perlin
    return perlin_noise(p * 2.0);
#elif defined Use_Value
    return value_noise(p * 2.0);
#elif defined Use_Simplex
    return simplex_noise(p);
#endif
    
    return 0.0;
}

// ========== Different function ==========

float noise_itself(float3 p)
{
    return noise(p * 8.0);
}

float noise_sum(float3 p)
{
    float f = 0.0;
    p = p * 4.0;
    f += 1.0000 * noise(p); p = 2.0 * p;
    f += 0.5000 * noise(p); p = 2.0 * p;
	f += 0.2500 * noise(p); p = 2.0 * p;
	f += 0.1250 * noise(p); p = 2.0 * p;
	f += 0.0625 * noise(p); p = 2.0 * p;
    
    return f;
}

float noise_sum_abs(float3 p)
{
    float f = 0.0;
    p = p * 3.0;
    f += 1.0000 * abs(noise(p)); p = 2.0 * p;
    f += 0.5000 * abs(noise(p)); p = 2.0 * p;
	f += 0.2500 * abs(noise(p)); p = 2.0 * p;
	f += 0.1250 * abs(noise(p)); p = 2.0 * p;
	f += 0.0625 * abs(noise(p)); p = 2.0 * p;
    
    return f;
}

float noise_sum_abs_sin(float3 p)
{
    float f = noise_sum_abs(p);
    f = sin(f * 2.5 + p.x * 5.0 - 1.5);
    
    return f ;
}
```

材质：



这个节点相对上一个节点，噪声构造步骤就算走全了，有噪声发生器的构造，插值，叠加这三步。叠加是在fbm（分形布朗运动）函数中完成。

通过对柏林噪声修改我们可以得到很多效果，把这些效果进行组合又是很多种变化。对每种噪声的参数进行修改又是很多变化。

------

## **【4】turbulence noise**

Perlin noise_sum_abs和这个很像

效果：



代码：

```text
// Some useful functions
float3 mod289(float3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float2 mod289(float2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float3 permute(float3 x) { return mod289(((x*34.0)+1.0)*x); }

float snoise(float2 v) {

    // Precompute values for skewed triangular grid
    const float4 C = float4(0.211324865405187,
                        // (3.0-sqrt(3.0))/6.0
                        0.366025403784439,
                        // 0.5*(sqrt(3.0)-1.0)
                        -0.577350269189626,
                        // -1.0 + 2.0 * C.x
                        0.024390243902439);
                        // 1.0 / 41.0

    // First corner (x0)
    float2 i  = floor(v + dot(v, C.yy));
    float2 x0 = v - i + dot(i, C.xx);

    // Other two corners (x1, x2)
    float2 i1 = float2(0.0, 0.0);
    i1 = (x0.x > x0.y)? float2(1.0, 0.0):float2(0.0, 1.0);
    float2 x1 = x0.xy + C.xx - i1;
    float2 x2 = x0.xy + C.zz;

    // Do some permutations to avoid
    // truncation effects in permutation
    i = mod289(i);
    float3 p = permute(
            permute( i.y + float3(0.0, i1.y, 1.0))
                + i.x + float3(0.0, i1.x, 1.0 ));

    float3 m = max(float3(0.5,0.5,0.5) - float3(dot(x0,x0),dot(x1,x1),dot(x2,x2)), 0.0);

    m = m*m ;
    m = m*m ;

    // Gradients:
    //  41 pts uniformly over a line, mapped onto a diamond
    //  The ring size 17*17 = 289 is close to a multiple
    //      of 41 (41*7 = 287)

    float3 x = 2.0 * frac(p * C.www) - 1.0;
    float3 h = abs(x) - 0.5;
    float3 ox = floor(x + 0.5);
    float3 a0 = x - ox;

    // Normalise gradients implicitly by scaling m
    // Approximation of: m *= inversesqrt(a0*a0 + h*h);
    m *= 1.79284291400159 - 0.85373472095314 * (a0* a0 + h * h);

    // Compute final noise value at P
    float3 g = float3(0.0, 0.0, 0.0);
    g.x  = a0.x  * x0.x  + h.x  * x0.y;
    g.yz = a0.yz * float2(x1.x, x2.x) + h.yz * float2(x1.y, x2.y);
    return 130.0 * dot(m, g);
}

#define OCTAVES 3
float fbm (in float2 st) 
{
    // Initial values
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 0.0;
    //
    // Loop of octaves
    for (int i = 0; i < OCTAVES; i++) 
    {
        value += amplitude * abs(snoise(st));
        st *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}
```

材质：



![img](https://pic1.zhimg.com/80/v2-a62340db1f5a88186a592163ec09e62c_hd.jpg)

其实后面那个参数可以暴露出来可调。

------

## **【5】ridge noise**

做道路，线，布料，青苔根须，能量等效果都非常合适

效果：



![img](https://pic1.zhimg.com/80/v2-0719d93fb825d1515e1f4b0cc7afaa04_hd.jpg)

代码：

```text
// Some useful functions
float3 mod289(float3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float2 mod289(float2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
float3 permute(float3 x) { return mod289(((x*34.0)+1.0)*x); }

//
// Description : GLSL 2D simplex noise function
//      Author : Ian McEwan, Ashima Arts
//  Maintainer : ijm
//     Lastmod : 20110822 (ijm)
//     License :
//  Copyright (C) 2011 Ashima Arts. All rights reserved.
//  Distributed under the MIT License. See LICENSE file.
//  https://github.com/ashima/webgl-noise
//
float snoise(float2 v) {

    // Precompute values for skewed triangular grid
    const float4 C = float4(0.211324865405187,
                        // (3.0-sqrt(3.0))/6.0
                        0.366025403784439,
                        // 0.5*(sqrt(3.0)-1.0)
                        -0.577350269189626,
                        // -1.0 + 2.0 * C.x
                        0.024390243902439);
                        // 1.0 / 41.0

    // First corner (x0)
    float2 i  = floor(v + dot(v, C.yy));
    float2 x0 = v - i + dot(i, C.xx);

    // Other two corners (x1, x2)
    float2 i1 = float2(0.0, 0.0);
    i1 = (x0.x > x0.y)? float2(1.0, 0.0):float2(0.0, 1.0);
    float2 x1 = x0.xy + C.xx - i1;
    float2 x2 = x0.xy + C.zz;

    // Do some permutations to avoid
    // truncation effects in permutation
    i = mod289(i);
    float3 p = permute(
            permute( i.y + float3(0.0, i1.y, 1.0))
                + i.x + float3(0.0, i1.x, 1.0 ));

    float3 m = max(0.5 - float3(
                        dot(x0,x0),
                        dot(x1,x1),
                        dot(x2,x2)
                        ), 0.0);

    m = m*m ;
    m = m*m ;

    // Gradients:
    //  41 pts uniformly over a line, mapped onto a diamond
    //  The ring size 17*17 = 289 is close to a multiple
    //      of 41 (41*7 = 287)

    float3 x = 2.0 * frac(p * C.www) - float3(1.0, 1.0, 1.0);
    float3 h = abs(x) - 0.5;
    float3 ox = floor(x + 0.5);
    float3 a0 = x - ox;

    // Normalise gradients implicitly by scaling m
    // Approximation of: m *= inversesqrt(a0*a0 + h*h);
    m *= 1.79284291400159 - 0.85373472095314 * (a0*a0+h*h);

    // Compute final noise value at P
    float3 g = float3(0.0, 0.0, 0.0);
    g.x  = a0.x  * x0.x  + h.x  * x0.y;
    g.yz = a0.yz * float2(x1.x, x2.x) + h.yz * float2(x1.y, x2.y);
    return 130.0 * dot(m, g);
}

#define OCTAVES 4

// Ridged multifractal
// See "Texturing & Modeling, A Procedural Approach", Chapter 12
float ridge(float h, float offset) 
{
    h = abs(h);     // create creases
    h = offset - h; // invert so creases are at top
    h = h * h;      // sharpen creases
    return h;
}

float fbm(float2 p) 
{
    float lacunarity = 2.0;
    float gain = 0.5;
    float offset = 0.9;

    float sum = 0.0;
    float freq = 1.0, amp = 0.5;
    float prev = 1.0;
    for(int i=0; i < OCTAVES; i++) 
    {
        float n = ridge(snoise(p*freq), offset);
        sum += n*amp;
        sum += n*amp*prev;  // scale by previous octave
        prev = n;
        freq *= lacunarity;
        amp *= gain;
    }
    return sum;
}
```

材质：



![img](https://pic4.zhimg.com/80/v2-20c53e4d62c6be8c4cb49e9a2a2f3b9f_hd.jpg)

------

## **【6】Domain Warping**

它用来做水，云雾，地形等效果都挺不错。

效果：



![img](https://pic2.zhimg.com/80/v2-e7211149ba0d495a32e8103bb4489e11_hd.jpg)

代码：

```text
float random (in float2 _st) {
    return frac(sin(dot(_st.xy,
                         float2(12.9898,78.233)))*
        43758.5453123);
}

// Based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
float noise (in float2 _st) {
    float2 i = floor(_st);
    float2 f = frac(_st);

    // Four corners in 2D of a tile
    float a = random(i);
    float b = random(i + float2(1.0, 0.0));
    float c = random(i + float2(0.0, 1.0));
    float d = random(i + float2(1.0, 1.0));

    float2 u = f * f * (float2(3.0, 3.0) - 2.0 * f);

    return lerp(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

#define NUM_OCTAVES 5

float fbm ( in float2 _st) {
    float v = 0.0;
    float a = 0.5;
    float2 shift = float2(100.0, 100.0);
    // Rotate to reduce axial bias
    float2x2 rot = float2x2(cos(0.5), sin(0.5),
                    -sin(0.5), cos(0.50));
    for (int i = 0; i < NUM_OCTAVES; ++i) 
    {
        v += a * noise(_st);
        _st = mul(rot , _st) * 2.0 + shift;
        a *= 0.5;
    }
    return v;
}
```

材质：



![img](https://pic2.zhimg.com/80/v2-d1b4ce51bb192ead6519d6d8703d01fd_hd.jpg)

------

## **【7】Voronoi Nose**

Voronoi Nose的思路就是把UV空间分成若干个格子，然后在格子里撒点，算点到像素的最短距离。维诺噪声因为比较像水的caustic，所以也常常拿来做水下Caustic效果。

效果：



![img](https://pic1.zhimg.com/80/v2-5ff8f5911bb8715121a3621cc977c630_hd.jpg)



![img](https://pic2.zhimg.com/v2-401f5dd8aaa25ee7a15d64124eac1f2d_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

代码：

```text
#define HASHSCALE3 float3(0.1031, 0.1030, 0.0973)

float2 hash22(float2 p)
{
    float3 p3 = frac(p.xyx * HASHSCALE3);
    float tem =  dot(p3, p3.yzx + float3(19.19, 19.19, 19.19));
    p3 = p3 + float3(tem, tem, tem);
    return frac((p3.xx + p3.yz) * p3.zy);
}

float wnoise(float2 p, float time) 
{
    float2 n = floor(p);
    float2 f = frac(p);
    float md = 5.0;
    float2 m = float2(0.0 ,0.0);
    for (int i = -1; i <= 1; i++) 
    {
        for (int j = -1; j <= 1; j++) 
        {
            float2 g = float2(i, j);
            float2 o = hash22(n + g);
            o = float2(0.5, 0.5) + 0.5* sin(float2(time, time) + 6.28 * o);
            float2 r = g + o - f;
            float d = dot(r, r);
            if (d < md) 
            {
                md = d;
                m = n + g + o;
            }
        }
    }
    return md;
}
```

材质



![img](https://pic1.zhimg.com/80/v2-8350c8db72abb836b24eb7e14fc86a44_hd.jpg)

------

## **【8】Curl Noise**

这种Noise十分适合拿来做流体。做岩石，河床等被流体冲刷过的效果也挺不错的。

效果：



![img](https://pic2.zhimg.com/80/v2-1cb50773e23fafe1a97247c6c890ae49_hd.jpg)

代码：

```text
#define noiseSwirlSteps 2
#define noiseSwirlValue 1.0
#define noiseSwirlStepValue noiseSwirlValue / noiseSwirlSteps

#define noiseScale 2.0
#define noiseTimeScale 0.1


float3 mod289(float3 x) 
{
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

float4 mod289(float4 x) 
{
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

float4 permute(float4 x) 
{
     return mod289(((x * 34.0) + float4(1, 1, 1, 1)) * x);
}

float4 taylorInvSqrt(float4 r)
{
    return 1.79284291400159 - 0.85373472095314 * r;
}

float simplex(float3 v)
{
    const float2  C = float2(1.0/6.0, 1.0/3.0);
    const float4  D = float4(0.0, 0.5, 1.0, 2.0);

    // First corner
    float3 i = floor(v + dot(v, C.yyy));
    float3 x0 = v - i + dot(i, C.xxx);

    // Other corners
    float3 g = step(x0.yzx, x0.xyz);
    float3 l = float3(1.0, 1.0, 1.0) - g;
    float3 i1 = min( g.xyz, l.zxy );
    float3 i2 = max( g.xyz, l.zxy );

    //   x0 = x0 - 0.0 + 0.0 * C.xxx;
    //   x1 = x0 - i1  + 1.0 * C.xxx;
    //   x2 = x0 - i2  + 2.0 * C.xxx;
    //   x3 = x0 - 1.0 + 3.0 * C.xxx;
    float3 x1 = x0 - i1 + C.xxx;
    float3 x2 = x0 - i2 + C.yyy; // 2.0*C.x = 1/3 = C.y
    float3 x3 = x0 - D.yyy;      // -1.0+3.0*C.x = -0.5 = -D.y

    // Permutations
    i = mod289(i);
    float4 p = permute(permute(permute(i.z + float4(0.0, i1.z, i2.z, 1.0)) + i.y + float4(0.0, i1.y, i2.y, 1.0)) + i.x + float4(0.0, i1.x, i2.x, 1.0));

    // Gradients: 7x7 points over a square, mapped onto an octahedron.
    // The ring size 17*17 = 289 is close to a multiple of 49 (49*6 = 294)
    float n_ = 0.142857142857; // 1.0/7.0
    float3 ns = n_ * D.wyz - D.xzx;

    float4 j = p - 49.0 * floor(p * ns.z * ns.z); //  mod(p,7*7)

    float4 x_ = floor(j * ns.z);
    float4 y_ = floor(j - 7.0 * x_); // mod(j,N)

    float4 x = x_ *ns.x + ns.yyyy;
    float4 y = y_ *ns.x + ns.yyyy;
    float4 h = 1.0 - abs(x) - abs(y);

    float4 b0 = float4( x.xy, y.xy );
    float4 b1 = float4( x.zw, y.zw );

    //float4 s0 = float4(lessThan(b0,0.0))*2.0 - 1.0;
    //float4 s1 = float4(lessThan(b1,0.0))*2.0 - 1.0;
    float4 s0 = floor(b0) * 2.0 + 1.0;
    float4 s1 = floor(b1) * 2.0 + 1.0;
    float4 sh = -step(h, float4(0, 0, 0, 0));

    float4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
    float4 a1 = b1.xzyw + s1.xzyw * sh.zzww;

    float3 p0 = float3(a0.xy, h.x);
    float3 p1 = float3(a0.zw, h.y);
    float3 p2 = float3(a1.xy, h.z);
    float3 p3 = float3(a1.zw, h.w);

    //Normalise gradients
    float4 norm = taylorInvSqrt(float4(dot(p0, p0), dot(p1, p1), dot(p2, p2), dot(p3, p3)));
    p0 *= norm.x;
    p1 *= norm.y;
    p2 *= norm.z;
    p3 *= norm.w;

    // Mix final noise value
    float4 m = max(0.6 - float4(dot(x0, x0), dot(x1, x1), dot(x2, x2), dot(x3, x3)), 0.0);
    m = m * m;
    return 42.0 * dot( m * m, float4(dot(p0, x0), dot(p1, x1), dot(p2, x2), dot(p3, x3)));
}

float fbm3(float3 v) 
{
    float result = simplex(v);
    result += simplex(v * 2.0) / 2.0;
    result += simplex(v * 4.0) / 4.0;
    result /= (1.0 + 1.0 / 2.0 + 1.0 / 4.0);
    return result;
}

float fbm5(float3 v) 
{
    float result = simplex(v);
    result += simplex(v * 2.0) / 2.0;
    result += simplex(v * 4.0) / 4.0;
    result += simplex(v * 8.0) / 8.0;
    result += simplex(v * 16.0) / 16.0;
    result = result / (1.0 + 1.0 / 2.0 + 1.0 / 4.0 + 1.0 / 8.0 + 1.0 / 16.0);
    return result;
}

float getNoise(float3 v) 
{
    //  make it curl
    for (int i = 0; i < noiseSwirlSteps; i++) 
    {
    	v.xy += float2(fbm3(v), fbm3(float3(v.xy, v.z + 1000.0))) * noiseSwirlStepValue;
    }
    //  normalize
    return fbm5(v) / 2.0 + 0.5;
    //return v.z;
}
```

材质：



![img](https://pic3.zhimg.com/80/v2-06593dd5746e2a9883266a7a459ae0fa_hd.jpg)



![img](https://pic3.zhimg.com/80/v2-dd50eb0cac2ce68347e1060ffc179dc2_hd.jpg)

主函数调getNoise即可。

------

## **【9】其它叠加**

效果：



![img](https://pic1.zhimg.com/80/v2-897bac7ba4a0002892e3f5ed31402a98_hd.jpg)

代码

```text
    const int MAX_ITER = 5;
    float2 p = fmod(uv * 3.14, 3.14) - 250.0;

    float2 i = float2(p);
    float c = 1.0;
    float inten = 0.005;

    for (int n = 0; n < MAX_ITER; n++) 
    {
        float t = Time * (1.0 - (3.5 / float(n + 1)));
        i = p + float2(cos(t - i.x) + sin(t + i.y), sin(t - i.y) + cos(t + i.x)); 
        c += 1.0 / length(float2(p.x / (sin(i.x + t) / inten), p.y / (cos(i.y + t) / inten))); 
    }

    c /= float(MAX_ITER);
    c = 1.17 - pow(c, 1.4);
    float val = pow(abs(c), 8.0);
```

这个我是用Computeshader算出来放到RT上的



![img](https://pic3.zhimg.com/80/v2-2e249dcccab4cbe932be20510b2f5442_hd.jpg)

------

至此我们的UnrealSubstance噪波生成工具节点算是初步开发完成了，后面如果有新的需求再加。我们暂时把这些逻辑放在材质函数里，以后再把它们开发成C++节点，后期如果虚幻材质编辑器扛不住巨大的计算压力，甚至可以加入CS为节点加速。



![img](https://pic4.zhimg.com/80/v2-6dc93ba5e32070189906a48c017f73bb_hd.jpg)

Enjoy It！

------

参考资料

【1】[http://webstaff.itn.liu.se/~stegu/jgt2012/article.pdf](https://link.zhihu.com/?target=http%3A//webstaff.itn.liu.se/~stegu/jgt2012/article.pdf)

【2】[https://thebookofshaders.com/11/](https://link.zhihu.com/?target=https%3A//thebookofshaders.com/11/)

【3】[Shadertoy](https://link.zhihu.com/?target=https%3A//www.shadertoy.com/view/4dS3Wd)

【4】[http://www.iquilezles.org/www/articles/morenoise/morenoise.htm](https://link.zhihu.com/?target=http%3A//www.iquilezles.org/www/articles/morenoise/morenoise.htm)

【5】[[数学\][转载][柏林噪声] - Memo - 博客园](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/Memo/archive/2008/09/08/1286963.html)

【6】[Shadertoy](https://link.zhihu.com/?target=https%3A//www.shadertoy.com/view/4sc3z2)

【7】[中级Shader教程23 voronoi算法](https://link.zhihu.com/?target=https%3A//blog.csdn.net/tjw02241035621611/article/details/80137615)

【8】[https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph2007-curlnoise.pdf](https://link.zhihu.com/?target=https%3A//www.cs.ubc.ca/~rbridson/docs/bridson-siggraph2007-curlnoise.pdf)

【10】[Shadertoy](https://link.zhihu.com/?target=https%3A//www.shadertoy.com/view/MsdGWn)

【10】[Shadertoy](https://link.zhihu.com/?target=https%3A//www.shadertoy.com/view/MsdGWn)

【11】[【图形学】谈谈噪声 - candycat - CSDN博客](https://link.zhihu.com/?target=https%3A//blog.csdn.net/candycat1992/article/details/50346469)（强烈推荐这篇博客）
