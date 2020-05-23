# 虚幻4渲染编程（环境模拟篇）【第四卷：体积云天空模拟(4) - 基于Texture的体积云】



## **简介：**

前面三节分别介绍了高度场体积云，3D纹理体积云，大面积程序化生成的体积云天空，某种程度上说前面的三节是非常初级的实现方案，因为它存在太多问题。最突出的一个问题就是可控性极差，因为可控性差也就导致了美术表现无法控制等一系列问题。如果想要进一步提高效果，就需要加入更多计算，性能下降显著，几乎是指数下降。所以我考虑使用预烘焙的方式，将大量的计算烘焙到贴图里。

------

## **[1]Modeling**

渲染体积云的一个主要思路是先建立体积场把云朵“建模”出来，然后考虑光照，然后考虑变化。不同于前面几篇文章的实现方法，这篇使用预计算的方式。所以我们首先需要准备一张名为Weather-map的贴图来存放我们的数据。

**（1）Weather-map and Cloud Noise Texture 3D**

在创建细节丰富的体积云朵之前需要先为其创建一个低频的空间范围，然后再往这个空间上叠各种细节信息。weather map将负责完成这个信息的储存。



![img](https://pic1.zhimg.com/80/v2-4963925c73512347604e5086949b1dd8_hd.jpg)

R通道储存云朵会出现的位置，G通道用来存储高频一点的云朵位置信息,B通道储存云朵的云峰的高度，A通道储存云朵在世界空间种的高度。



![img](https://pic3.zhimg.com/80/v2-9e92f8a53ef998bec1b04146c554a6be_hd.jpg)

在开始Marching前我们需要确定的一点是，我们是在贴图空间种做Marching的，所以我们需要把世界空间转换到UV空间。

![RayPos = (WorldPos - ActorPos) / (MarchingBoxScale * 100) + 0.5](https://www.zhihu.com/equation?tex=RayPos+%3D+%28WorldPos+-+ActorPos%29+%2F+%28MarchingBoxScale+%2A+100%29+%2B+0.5) 

![Coverage = WeatherMap.r](https://www.zhihu.com/equation?tex=Coverage+%3D+WeatherMap.r) 

![HeghtScale = WeatherMap.a](https://www.zhihu.com/equation?tex=HeghtScale+%3D+WeatherMap.a) 

**（1）基于求交检测后重定位Marching原点的方法：**



![img](https://pic2.zhimg.com/80/v2-f7999860d3ac0f52ac5d3b9a38ec58d1_hd.jpg)

这种方法的优势是能Marching整个天空，缺点是没法穿到云里。必须要使用两个SphereHit或者两个PannerHit求到Marching的高度范围，如果只有一个平面的话云会有畸变，远处的云会被压扁。



![img](https://pic1.zhimg.com/80/v2-90fce56ae8700aecf278a30cd2a0c910_hd.jpg)

Weather-map的R通道用于控制云朵的位置，下面可以做个简单试验，绘制几个简单的方块：



![img](https://pic3.zhimg.com/80/v2-cb24e77877aacc86b22052a03fcd0196_hd.jpg)

代码如下：



![img](https://pic4.zhimg.com/80/v2-acb1846b8234369cfd8e58bd7133b2ab_hd.jpg)



![img](https://pic4.zhimg.com/80/v2-c156909ab54e3cc0ba4baaa78e2c088f_hd.jpg)

你将会看到如下效果：



![img](https://pic2.zhimg.com/v2-4915e626c709ae088dc601eb35a9dac9_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

如果我们正常绘制简单的云朵的形状：



![img](https://pic2.zhimg.com/80/v2-f91e18243be99d441d0d59d3bc4b4f65_hd.jpg)

那么将会看到我们已经为体积云初步勾勒出了一个立体的空间范围：



![img](https://pic1.zhimg.com/80/v2-715739eb1a0dc4b154ec633eeaba2b60_hd.jpg)



![img](https://pic3.zhimg.com/80/v2-63b126d8cccc06540d9c9c9d6367fc46_hd.jpg)



![img](https://pic1.zhimg.com/80/v2-61fa296fd26e15197e405da26a0b5be8_hd.jpg)

（2）基于非等距步长Marching方法从摄像机原点开始Marching的方法

但是使用HeitSphere或者HitPane这种定位Marching起始点的方式是无法穿梭导云层里的，所以我们需要准备一个inversebox然后使用第三节里面的非等距距离追踪方法，从视口开始marching这样就可以穿梭到云层里了。然后使用WeatherMap的A通道来限制空间中云层的Z方向高度即可。



![img](https://pic4.zhimg.com/80/v2-6ad854980a69f12b5e67481e073f3eeb_hd.jpg)



![img](https://pic2.zhimg.com/80/v2-4f5f49eb61611005a8ab67b8e219f971_hd.jpg)

```text
float HeightScale = WeatherTex.SampleLevel(WeatherTexsampler2D, raypos.zz, 0).a;
```



**（2）Add detail for cloud**

分别准备一张WeatherNoiseTextureLow和WeatherNoiseTextureHeigh的3DNoiseTexture，分别在RGBA四个通道里叠加各种频率的噪声。



![img](https://pic1.zhimg.com/80/v2-413b55557322a4d9e7fe383bd8c41f00_hd.jpg)

R通道存放低频的Perlin-Worley，G通道存放中等频率的Worley-noise，B通道存放高频率的Worley-noise，A通道存放更高频率的Worley-noise

用这种方式可以方便地将一个FBM4存储在一张贴图里，并且一次Sample就把它采出来。

将WeatherNoise和WeatherNoiseTextureLow和WeatherNoiseTextureHeigh分别叠加后就可以得到我们的最基础的云朵形状了。



![img](https://pic3.zhimg.com/80/v2-218480ce528d4e552a2c8c410620c17e_hd.jpg)

代码如下：



![img](https://pic3.zhimg.com/80/v2-220b11cc87e5f15a69646f7d0ec80ec6_hd.jpg)

------

## **[2]Lighting**

还是使用上一节说过的HenyeyGreenstein光照模型



![img](https://pic1.zhimg.com/80/v2-c006f7021ebec0724762bd70cf9fd258_hd.jpg)

在浓度积分的同时在做一次沿着太阳方向的积分即可。

```text
        if(density > 0.001f)
        {
            float3 sundenspos = raypos;
            for (int j = 0; j < 6; j++)
            {
                sundensity += GetDensity(sundenspos, actorpos, weathertex, weathertexSampler, weathernoisetex, weathernoisetexSampler, weathercloudtex, weathercloudtexSampler);

                sundenspos += SunDir * Marching_Size;
            }
        }
```



至此完了了天空渲染大方面的探索，剩下的是对上述四个方案的完善提高，比如Noise的叠加方式及优化。我还是觉得把它集成到引擎渲染管线里比较省，现在我把所有计算全部堆在PixleShader里的确不是一个好的选择。

下面是我的完整代码：

```text
#define Marching_Steps 136
#define Marching_Size 20000.0f
#define Marching_Box_Scale 200000.0f
#define MarchingSizeReScale 1.2f
#define GlobalCoverage 0.9f
#define M_PI 3.141592f;

#define SunDir float3(1, 1, 1)
#define BeerTerm 0.5f
#define InScatter 0.6f
#define OutScatter 0.7f
#define ExtraEdgeInt 0.5f
#define ExtraEdgeExp 1.2f
#define MixScatter 0.5f

float remap(float V, float L0, float H0, float Ln, float Hn)
{
    return Ln + (V - L0) * (Hn - Ln) / (H0 - L0);
}

float3 ScaleWorldSpaceToTextureSpace(float3 WorldSapcePosition, float3 actorpos)
{
    return ((WorldSapcePosition - actorpos) / (Marching_Box_Scale * 100) * MarchingSizeReScale) + 0.5f;
}

float HenyeyGreenstein(float cos_angle, float g)
{
    float g2 = g * g;
    return ((1.0f - g2) / pow((1.0f + g2 - 2.0f * g * cos_angle), 1.5f)) / 4 * M_PI;
}

float GetDensity(float3 raypos, float3 actorpos, Texture2D WeatherTex, SamplerState WeatherTexsampler2D,
Texture3D weathernoisetex, SamplerState weathernoisetexSampler, Texture3D weathercloudtex, SamplerState weathercloudtexSampler)
{
	//Marching in tangent space
    raypos = ScaleWorldSpaceToTextureSpace(raypos, actorpos);
	//The density of cloud
    float density = 0;

    float3 WeatherData = WeatherTex.SampleLevel(WeatherTexsampler2D, raypos.xy, 0).rgb;
    float HeightScale = WeatherTex.SampleLevel(WeatherTexsampler2D, raypos.zz, 0).a;
    HeightScale = saturate(remap(HeightScale, 0, 0.07, 0, 1));
    float cloudcover = WeatherData.r;

    float4 LowFrecNoise = weathernoisetex.SampleLevel(weathercloudtexSampler, frac(raypos * 10), 0);
    float lowfreqFBM = LowFrecNoise.g * 0.625f + LowFrecNoise.b * 0.25f + LowFrecNoise.a * 0.125f;
    float cloudbase = saturate(remap(LowFrecNoise.r, -(1 - lowfreqFBM), 1, 0, 1));

    cloudcover = pow(cloudcover, saturate(remap(0.5, 0.65, 0.95, 1, GlobalCoverage)));
    float basecloudcolver = saturate(remap(cloudbase, 1 - cloudcover, 1, 0, 1));

    float3 highFreqNoise = weathercloudtex.SampleLevel(weathernoisetexSampler, frac(raypos * 20), 0);
    float highFreqFBM = (highFreqNoise.r * 0.625f) + (highFreqNoise.g * 0.25f) + (highFreqNoise.b * 0.125f);
    float highFreqNoiseModifier = saturate(remap(highFreqNoise.r, highFreqFBM, 1 - highFreqFBM, 0, 1));
    highFreqNoiseModifier *= 0.35 * exp(-GlobalCoverage * 0.75);

    density = saturate(remap(basecloudcolver, highFreqFBM, 1, 0, 1)) * HeightScale;
    //density = cloudcover * HeightScale;

    return density;
}

float4 mainImage(float2 viewsize, float time, float3 ro, float3 actorpos, float3 wpos, Texture2D weathertex, SamplerState weathertexSampler, Texture3D weathernoisetex, SamplerState weathernoisetexSampler, Texture3D weathercloudtex, SamplerState weathercloudtexSampler, float4 DebugData)
{
    float4 finalcol = float4(0, 0, 0, 0);
    float3 rd = normalize(wpos - ro);
    float3 raypos = ro;

    float cos_angle = dot(SunDir, rd);

    float density = 0.0f;
    float sundensity = 0.0f;
    for (int i = 0; i < Marching_Steps; i++)
    {
        density += GetDensity(raypos, actorpos, weathertex, weathertexSampler, weathernoisetex, weathernoisetexSampler, weathercloudtex, weathercloudtexSampler);

		if(density > 0.001f)
        {
            float3 sundenspos = raypos;
            for (int j = 0; j < 6; j++)
            {
                sundensity += GetDensity(sundenspos, actorpos, weathertex, weathertexSampler, weathernoisetex, weathernoisetexSampler, weathercloudtex, weathercloudtexSampler);

                sundenspos += SunDir * Marching_Size;
            }
        }

        raypos += rd * Marching_Size * exp(0.015 * i);
    }

    float edgeLEx = ExtraEdgeInt * pow(saturate(cos_angle), ExtraEdgeExp);
    float scatter = lerp(max(HenyeyGreenstein(cos_angle, InScatter), edgeLEx), HenyeyGreenstein(cos_angle, -OutScatter), MixScatter);

    float AttenPrim = exp(-BeerTerm * sundensity);

    finalcol.r = density;
    finalcol.g = sundensity * AttenPrim;

    return finalcol;
}

//return  mainImage(viewsize, time, ro, actorpos, wpos, weathertex, weathertexSampler, weathernoisetex, weathernoisetexSampler, weathercloudtex, weathercloudtexSampler,  DebugData);
```

Enjoy it ！
