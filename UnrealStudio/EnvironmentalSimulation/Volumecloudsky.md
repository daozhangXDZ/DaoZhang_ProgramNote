# 虚幻4渲染编程（环境模拟篇）【第一卷：体积云天空模拟(1)---层云】



https://zhuanlan.zhihu.com/p/49489488

**开篇综述：**

场景制作已经越来越复杂，要求也越来越高，已经不是场景美术就能完成效果生产的了。比如大世界（面积几平方公里甚至几十平方公里），云海大气模拟，物理海洋模拟，沙漠戈壁，雨林等。而这些工作是技术美术和图形程序需要完成的。

环境模拟篇将专注于研究游戏中各种环境的模拟，天空大气，海洋，沙漠，草原，大世界地形开发等。环境模拟包括效果，优化，环境交互等内容。



------

这篇将研究体积云天空的内容。将由浅入深解决大气天空开发过程中的想法，理论知识，实际动手实现等。要想模拟天空效果主要模拟的有以下几部分。

## **（1）收集准备**

在环境模拟之前，必须要先找到目标参考。我选了下面这个比较有代表性的



![img](https://pic2.zhimg.com/80/v2-68309c5eda24181634c49e3397f9ec25_hd.jpg)

我把天空模拟分为以下几个部分：

【1】大规模云海，包括云海的运动，光照着色，光线散射

【2】天空的颜色变化，远景

【3】云层下的景物

首先来研究下最难的云层模拟。我把天空的云层分为四个部分

**高云族**

- [卷云](https://link.zhihu.com/?target=https%3A//zh.wikipedia.org/wiki/%25E5%258D%25B7%25E4%25BA%2591)（Ci, *Cirrus*）：常呈丝条状、羽毛或马尾状、钩状、片状、砧状等。
- [卷积云](https://link.zhihu.com/?target=https%3A//zh.wikipedia.org/wiki/%25E5%258D%25B7%25E7%25A7%25AF%25E4%25BA%2591)（Cc, *Cirrocumulus*）：似鳞片或球状细小云块。
- [卷层云](https://link.zhihu.com/?target=https%3A//zh.wikipedia.org/wiki/%25E5%258D%25B7%25E5%25B1%2582%25E4%25BA%2591)（Cs, *Cirrostratus*）：呈薄幕状。

**中云族**

**中云**于2500ｍ至6000m的高空形成。它们是由[过度冷冻](https://link.zhihu.com/?target=https%3A//zh.wikipedia.org/wiki/%25E9%2581%258E%25E5%2586%25B7)的小水点组成。



![img](https://pic2.zhimg.com/80/v2-705cb870483a111aab1258634da78fa5_hd.jpg)



**低云**是在2500ｍ以下的大气中形成。





![img](https://pic4.zhimg.com/80/v2-b641ebb4f126d394a627d97b0141fe9b_hd.jpg)

**直展云族**

- [积云](https://link.zhihu.com/?target=https%3A//zh.wikipedia.org/wiki/%25E7%25A7%25AF%25E4%25BA%2591)（Cu, *Cumulus*）：积云如同棉花团，云体垂直向上发展，常见于上午，午间发展最旺盛，并于午后开始逐渐消散。
- [积雨云](https://link.zhihu.com/?target=https%3A//zh.wikipedia.org/wiki/%25E7%25A7%25AF%25E9%259B%25A8%25E4%25BA%2591)（Cb, *Cumulonimbus*）：由积云发展而来，伴随雷暴与阵雨，云体高耸，顶部常呈花菜状或砧状，云底阴暗。

------

## **（2）云层模拟的方法**

现在业内模拟云层主要有两种方法

（1）模型法

（2）Raymarching

模型法一般适用于非常风格化的游戏。



![img](https://pic3.zhimg.com/80/v2-74936cbea4507b66970b1603a414e2ae_hd.jpg)

这种方法制作云好处是方便艺术家控制，坏处就是光影变化麻烦，需要制作一些非常trick的shading mode，而且面数要求极高，要是模拟大规模云海就十分吃力了。除此以外，云海的运动也没办法模拟，因为模型是定死的。



![img](https://pic1.zhimg.com/80/v2-2f3790991239c02f7ff4e8dc0f94614c_hd.jpg)



![img](https://pic1.zhimg.com/80/v2-73547fe1892376b6d6117f521fc270d8_hd.jpg)

下面是我的生成方式：

先生成一个简单的模型



![img](https://pic3.zhimg.com/80/v2-1f59350b901b1cdd8a18dc0c611ddb6a_hd.jpg)

由这个模型生成体积云



![img](https://pic1.zhimg.com/80/v2-5a449b809a0a5feeacdada443a8e3b5c_hd.jpg)

加上噪波



![img](https://pic1.zhimg.com/80/v2-64e9fc7c376bc87d5182bb64866e30dc_hd.jpg)

然后再把它转成模型



![img](https://pic2.zhimg.com/80/v2-1c907893b51b9b3298aaf875f2a684cd_hd.jpg)

我的节点如下



![img](https://pic4.zhimg.com/80/v2-305d7bee93cb83d327452249d0fa5c07_hd.jpg)

可以看到模型的面数巨高，综合考虑下来这种方法有很多局限的地方。所以现在的3A游戏都采用Ray Marching的方法。如果对RayMarching不熟悉可以看我之前的Ray Marching系列文章

[小IVan：Begin ray marching in unreal engine 4【第一卷：在材质编辑器中启程】](https://zhuanlan.zhihu.com/p/36759481)

[Begin ray marching in unreal engine 4【第二卷：开始加入光照】](https://zhuanlan.zhihu.com/p/36787006)

[Begin ray marching in unreal engine 4【第三卷：更多图形更复杂的光照】](https://zhuanlan.zhihu.com/p/36788227)

[Begin ray marching in unreal engine 4【第四卷：虚幻4中的MetaBall】](https://zhuanlan.zhihu.com/p/37055827)

[Begin ray marching in unreal engine 4【第五卷：3D体纹理云】](https://zhuanlan.zhihu.com/p/37308462)

RayMarching模拟云的话主要会使用两种办法，一种是程序化3D噪波生成体积场，一种是使用3D体纹理的方式生成体积场。3D体纹理可以在Houdini中方便创建，而且可以方便艺术家控制效果。3D噪波生成的体积场适合做大规模大范围层云。后面的文章就将围绕这两个方法来实现天空模拟。首先先来研究下程序化3D噪波模拟层云。

首先我们定义一个层云的高度场



![img](https://pic4.zhimg.com/80/v2-07f97d5d4a1259af8dc0085082aa1d33_hd.jpg)

然后在其表面铺上噪波扰动这个表面



![img](https://pic1.zhimg.com/80/v2-e66f6f76f24d5baffafe4753ed930700_hd.jpg)

然后从视角最远处反向向摄像机方向积分浓度



![img](https://pic4.zhimg.com/80/v2-d00f25d6f411f0dc1d07e963ac3f9557_hd.jpg)

下面是我做的几个效果：

（扭曲RayDirection的结果，可以做出暴风内部的效果）

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1045439999700439040?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



（正常情况）

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1045440043593920512?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



下面是我的代码：

```text
#define NUM_STEPS 200
#define NUM_NOISE_OCTAVES 4

#define HEIGHT_OFFSET 1.5

#define USE_TEXTURE false
#define WHITE_NOISE_GRID_SIZE 256.0

#define HASHSCALE1 443.8975
//  1 out, 2 in...
float hash12(float2 p)
{
	float3 p3  = frac(p.xyx * HASHSCALE1);
    p3 += dot(p3, p3.yzx + 19.19);
    return frac((p3.x + p3.y) * p3.z);
}

// NOTE: the bilinear interpolation is important! without it, the clouds look blocky.
// You can see this by returning noise00 or by having the texture use the "nearest" filter
float BilinearInterpolateWhiteNoise (float2 uv)
{
    uv = frac(uv);
    
    float2 uvPixels = uv * WHITE_NOISE_GRID_SIZE;
    
    float2 uvFrac = uvPixels - floor(uvPixels);
    
    float2 uvDiscreteFloor = floor(uvPixels) / WHITE_NOISE_GRID_SIZE;
    float2 uvDiscreteCeil = ceil(uvPixels) / WHITE_NOISE_GRID_SIZE;
    
    float noise00 = hash12(float2(uvDiscreteFloor.x, uvDiscreteFloor.y));
    float noise01 = hash12(float2(uvDiscreteFloor.x, uvDiscreteCeil.y ));
    float noise10 = hash12(float2(uvDiscreteCeil.x , uvDiscreteFloor.y));
    float noise11 = hash12(float2(uvDiscreteCeil.x , uvDiscreteCeil.y ));
    
    float noise0_ = lerp(noise00, noise01, uvFrac.y);
    float noise1_ = lerp(noise10, noise11, uvFrac.y);
    
    float noise = lerp(noise0_, noise1_, uvFrac.x);

    return noise;
}

float RandomNumber (in float3 position)
{
    // NOTE: the ceil here is important interestingly. it makes the clouds look round and puffy instead of whispy in a glitchy way
    float2 uv = (position.yz + ceil(position.x)) / float(NUM_STEPS);
    
    return BilinearInterpolateWhiteNoise(uv);
}

float4 mainImage(float2 fragCoord, float2 iResolution, float iTime, float3 rd, float3 ro, float3 wpos)
{
    float4 fragColor = float4(1,1,1,1);

    float3 direction = rd;
    //float3 direction = float3(0.8, fragCoord - 0.8);

    float3 skyColor = float3(0.6, 0.7, 0.8);
    float3 pixelColor = skyColor;

    for (int rayStep = 0; rayStep < NUM_STEPS; rayStep++)
    {
        float3 position = 0.05 * float(NUM_STEPS - rayStep) * direction + ro * 0.001;
        position.xy += iTime;
        float noiseScale = 0.5;
        float signedCloudDistance = position.z + HEIGHT_OFFSET;
        for (int octaveIndex = 0; octaveIndex < NUM_NOISE_OCTAVES; ++octaveIndex)
        {
            position *= 2.0;
            noiseScale *= 2.0;
            signedCloudDistance -= RandomNumber(position) / noiseScale;
        }
        if (signedCloudDistance < 0.0)
            pixelColor += (pixelColor - 1.0 - signedCloudDistance * skyColor.zyx) * signedCloudDistance * 0.4;
	}
    
    fragColor.rgb = pixelColor;
    fragColor.a = 1.0;
    return fragColor;
}
```

可以看到云大体上感觉出来了，不过有个明显的问题就是噪波不连续。

为了解决这个噪波不连续的问题，我们需要深入理解噪波的生成原理。下面是我之前做的噪波专题的文章

[小IVan：虚幻4渲染编程（程序化纹理篇）【第一卷：UnrealSubstance工具节点搭建---噪波】](https://zhuanlan.zhihu.com/p/47959352)

我重新使用Value Noise来生成云层的体积场。下面是使用新噪波后的效果

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1046002977344659456?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



（考虑到视频大小我压得有点狠，视频有点糊）

可以看到云层不再有不连续问题

代码如下：

```text
#define NUM_STEPS 200
#define NUM_NOISE_OCTAVES 4

#define HEIGHT_OFFSET 1.5

#define USE_TEXTURE false
#define WHITE_NOISE_GRID_SIZE 256.0

#define HASHSCALE1 443.8975

#if 0
//  1 out, 2 in...
float Noise(float3 p)
{
	float3 p3  = frac(p.xyz * HASHSCALE1);
    p3 += dot(p3, p3.yzx + 19.19);
    return frac((p3.x + p3.y) * p3.z);
}
#endif

float hash(float3 p)
{
    p = frac(p * 0.3183099 + 0.1);
    p *= 17.0;
    return frac(p.x * p.y * p.z * (p.x + p.y + p.z));
}

float Noise(in float3 x)
{
    float3 p = floor(x);
    float3 f = frac(x);
    f = f * f * (3.0 - 2.0 * f);

    return lerp(lerp(lerp( hash(p + float3(0,0,0)), 
                        hash(p + float3(1,0,0)),f.x),
                   lerp( hash(p + float3(0,1,0)), 
                        hash(p + float3(1,1,0)),f.x),f.y),
               lerp(lerp( hash(p + float3(0,0,1)), 
                        hash(p + float3(1,0,1)),f.x),
                   lerp( hash(p + float3(0,1,1)), 
                        hash(p + float3(1,1,1)),f.x),f.y),f.z);
}

// NOTE: the bilinear interpolation is important! without it, the clouds look blocky.
// You can see this by returning noise00 or by having the texture use the "nearest" filter
float BilinearInterpolateWhiteNoise (float3 uv)
{
    uv = frac(uv);
    
    float3 uvPixels = uv * WHITE_NOISE_GRID_SIZE;
    
    float3 uvFrac = uvPixels - floor(uvPixels);
    
    float3 uvDiscreteFloor = floor(uvPixels) / WHITE_NOISE_GRID_SIZE;
    float3 uvDiscreteCeil = ceil(uvPixels) / WHITE_NOISE_GRID_SIZE;
    
    float noise00 = Noise(float3(uvDiscreteFloor.x, uvDiscreteFloor.y, uvDiscreteFloor.z));
    float noise01 = Noise(float3(uvDiscreteFloor.x, uvDiscreteCeil.y ,uvDiscreteCeil.z));
    float noise10 = Noise(float3(uvDiscreteCeil.x , uvDiscreteFloor.y, uvDiscreteFloor.z));
    float noise11 = Noise(float3(uvDiscreteCeil.x , uvDiscreteCeil.y, uvDiscreteCeil.z));
    
    float noise0_ = lerp(noise00, noise01, uvFrac.y);
    float noise1_ = lerp(noise10, noise11, uvFrac.z);
    float noise2_ = lerp(noise10, noise11, uvFrac.x);
    
    float noise = lerp(lerp(noise0_, noise1_, uvFrac.x), noise2_, uvFrac.y);

    return noise;
}

float RandomNumber (in float3 position)
{
    // NOTE: the ceil here is important interestingly. it makes the clouds look round and puffy instead of whispy in a glitchy way
    float3 uv = (position.yzx + ceil(position.x)) / float(NUM_STEPS);
    
    //return BilinearInterpolateWhiteNoise(uv);
    return Noise(position);
}

float4 mainImage(float2 fragCoord, float2 iResolution, float iTime, float3 rd, float3 ro, float3 wpos)
{
    float4 fragColor = float4(1,1,1,1);

    float3 direction = rd;
    //float3 direction = float3(0.8, fragCoord - 0.8);

    float3 skyColor = float3(0.6, 0.7, 0.8);
    float3 pixelColor = skyColor;

    for (int rayStep = 0; rayStep < NUM_STEPS; rayStep++)
    {
        float3 position = 0.05 * float(NUM_STEPS - rayStep) * direction + ro * 0.001;
        position.xy += iTime;
        float noiseScale = 0.5;
        float signedCloudDistance = position.z + HEIGHT_OFFSET;
        for (int octaveIndex = 0; octaveIndex < NUM_NOISE_OCTAVES; ++octaveIndex)
        {
            position *= 2.0;
            noiseScale *= 1.6;
            signedCloudDistance -= RandomNumber(position) / noiseScale;
        }
        if (signedCloudDistance < 0.0)
            pixelColor += (pixelColor - 1.0 - signedCloudDistance * skyColor.zyx) * signedCloudDistance * 0.4;
	}
    
    fragColor.rgb = pixelColor;
    fragColor.a = 1.0;
    return fragColor;
}
```



至此我们完成了天空模拟的第一部分，后续文章将继续研究天空模拟的剩下部分。

Enjoy it.

------

## **Next：**

小IVan：虚幻4渲染编程（环境模拟篇）【第二卷：体积云天空模拟(2)---3D体纹理低云】

zhuanlan.zhihu.com![图标](https://pic1.zhimg.com/v2-d37731435c7e3c4dd055d943130118fc_180x120.jpg)

------

参考文章

【1】[高效真实的云渲染算法 - effulgent - 博客园](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/effulgent/archive/2008/10/06/real_time_cloud_rendering.html)

【2】[http://killzone.dl.playstation.net/killzone/horizonzerodawn/presentations/Siggraph15_Schneider_Real-Time_Volumetric_Cloudscapes_of_Horizon_Zero_Dawn.pdf](https://link.zhihu.com/?target=http%3A//killzone.dl.playstation.net/killzone/horizonzerodawn/presentations/Siggraph15_Schneider_Real-Time_Volumetric_Cloudscapes_of_Horizon_Zero_Dawn.pdf)

【3】[Lele Feng：游戏中的云海效果是怎样实现的？](https://www.zhihu.com/question/263532694/answer/272148547)
