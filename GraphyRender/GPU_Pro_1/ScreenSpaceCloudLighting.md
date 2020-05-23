## 实时屏幕空间的云层光照 | Real-Time Screen Space Cloud Lighting

在创造逼真的虚拟环境时，云是一个重要的视觉元素。实时渲染美丽的云可能非常具有挑战性，因为云在保持交互式帧率的同时会呈现出难以计算的多重散射（multiple scattering）。

目前的问题是，大多数游戏都无法承担精确计算物理上正确的云层光照的计算成本。

本章介绍了一种可以实时渲染真实感的云层的非常简单的屏幕空间技术。这种技术已经在PS3上实现，并用于游戏《大航海时代Online》（Uncharted  Waters  Online）中。这项技术并不关注严格的物理准确性，而是依靠重新创建云层的经验外观。另外需要注意的是，此技术适用于地面场景，玩家可以在地面上观看，并且只能从远处观看云层。

光照是创造美丽和真实感云彩最重要的方面之一。当太阳光穿过云层时，被云层中的粒子吸收，散射和反射。下图展示了一个典型的户外场景。

[
![img](ScreenSpaceCloudLighting.assets/9f705cf6b5a91b5fae1b81c1c61603bd.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/9f705cf6b5a91b5fae1b81c1c61603bd.png)

图 一个典型的户外场景。 最靠近太阳的云显示出最大的散射并且看起来最亮

如图所示，从图中所示的视图看云层时，最靠近太阳的云显得最亮。这种现象是由于太阳的光线到达云层的后方，然后通过多次散射，在云的前部（最靠近观察者）重新出现。这一观察结果是这章所介绍技术的关键部分。为了再现这种视觉提示，屏幕空间中的简单点模糊或方向模糊足以模仿通过云层的光散射。

### 

### 17.1 实现方案

这章的云层渲染技术可以分为三个pass执行：

- 首先，渲染云密度（cloud density）为离屏渲染目标（RT），且云密度是可以由艺术家绘制的标量值。
- 其次，对密度贴图（density map）进行模糊处理。
- 最终，使用模糊的密度贴图来渲染具有散射外观的云层。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/7b87efd297e401d47bf14224f0fa0227.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/7b87efd297e401d47bf14224f0fa0227.png)

图 基于这章技术实现的demo截图

在demo中，云层被渲染为一个统一的网格。 云层纹理在每个通道中包含四个密度纹理。每个通道代表不同的云层，根据第一个通道中的天气在像素着色器中混合。并且也通过滚动纹理坐标UV来实现动画。

总之，这章提出了一种实时渲染的真实感天空的技术。由于云的形状与光源分离，程序化云的生成和程序化动画都可以支持。

需要注意的是，此方法忽略了大气的某些物理特性，以创建更高效的技术。例如，不考虑大气的密度，但这个属性对于创造逼真的日落和日出是必要的。也忽略了进入云层的光的颜色。在日落或日出的场景中，只有靠近太阳的区域应该明亮而鲜艳地点亮。有必要采取更基于物理的方法来模拟太阳和云之间的散射，以获得更自然的结果。

### 

### 17.2 核心实现Shader代码

以下为云层光照像素着色器核心代码;注意，常数为大写。此着色器可以通过适当设置SCALE和OFFSET常量来提供平行线或点的模糊：

```
// Pixel shader input
struct SPSInput 
{
    float2 vUV : TEXCOORD0 ;
    float3 vWorldDir : TEXCOORD1 ;
    float2 vScreenPos : VPOS;
};

// Pixel shader
float4 main( SPSInput Input ) 
{
    // compute direction of blur.
    float2 vUVMove = Input .vScreenPos * SCALE + OFFSET ;

    // Scale blur vector considering distance from camera .
    float3 vcDir = normalize ( Input .vWorldDir );
    float fDistance = GetDistanceFromDir( vcDir );
    vUVMove *= UV_SCALE / fDistance ;

    // Limit blur vector length .
    float2 fRatio = abs ( vUVMove / MAX_LENGTH );
    float fMaxLen = max ( fRatio .x, fRatio .y );
    vUVMove *= fMaxLen > 1.0 f ? 1.0 f / fMaxLen : 1.0 f;

    // Compute offset for weight .
    // FALLOFF must be negative so that far pixels affect less.
    float fExpScale = dot ( vUVMove , vUVMove ) * FALLOFF ;

    // Blur density toward the light.
    float fShadow = tex2D ( sDensity , Input.vUV ).a;
    float fWeightSum = 1.0 f;
    for ( int i = 1; i < FILTER_RADIUS; ++i ) {
    float fWeight = exp ( fExpScale * i );
    fShadow +=
    fWeight * tex2D(sDensity , Input .vUV +vUVMove *i).a;
    fWeightSum += fWeight ;
    }
    fShadow /= fWeightSum ;

    // 0 means no shadow and 1 means all shadowed pixel .
    return fShadow ;
}
```
