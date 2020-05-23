## 虚拟纹理映射简介 | Virtual Texture Mapping 101

在这篇文章主要探讨了如何实现一个功能完备的虚拟纹理映射（Virtual Texture Mapping，VTM）系统。

首先，虚拟纹理映射（VTM）是一种将纹理所需的图形内存量减少到仅取决于屏幕分辨率的技术：对于给定的视点，我们只将纹理的可见部分保留在图形存储器中适当的MIP映射级别上，如下图。

[
![img](VirtualTextureMapping.assets/beba6a37fa84e7ce99d9a614c3c67483.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/beba6a37fa84e7ce99d9a614c3c67483.jpg)

图 使用单个的虚拟纹理渲染出独特的纹理地形

早期的纹理管理方案是针对单个大纹理设计的[Tanner et al.  98],文章发表期间的VTM系统则更加灵活，模仿了操作系统的虚拟内存管理的思路：将纹理分成小的图块（tiles），或者页（pages）[Kraus  and Ertl 02, Lefebvre et  al.04]。这些会根据渲染当前视点的需要自动缓存并加载到GPU上。但是，有必要将对缺失数据的访问重定向（redirect）到后备纹理。这可以防止渲染中出现“空洞”（加载请求完成前的阻塞和等待的情况）。

文中的实现的灵感来源于GDC上Sean Barrett[Barret  08]的演讲。如下图所示，在每帧开始，先确定哪些图块（tiles）可见，接着识别出其中没有缓存且没有磁盘请求的图块。在图块上传到GPU上的图块缓存之后，更新一个间接纹理（indrection  texture,）或者页表（page table）。最终，渲染场景，对间接纹理执行初始查找，以确定在图块缓存中采样的位置。

[
![img](VirtualTextureMapping.assets/9197db42270ce9c5c4a422252d4a129d.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/9197db42270ce9c5c4a422252d4a129d.jpg)

图 渲染图块ID，然后识别并更新最近可见的图块到图块缓存中（图中的红色），并可能会覆盖不再可见的图块（图中的蓝色）。更新间接纹理并渲染纹理化表面（texturized surfaces）

间接纹理（indirection texture）是完整虚拟纹理的缩小版本，其中每个纹素都指向图块缓存（tile cache）中的图块。在文中的示例中，图块缓存只是GPU上的一个大纹理，包含小的，相同分辨率的正方形图块。

这意味着来自不同mip map级别的图块（tiles）会覆盖虚拟纹理的不同大小区域，但会大大简化图块缓存的管理。

## 

## 8.1 核心实现Shader代码

### 

### 8.1.1 MIP 贴图计算的Shader实现 | MIP Map Calculation

```
float ComputeMipMapLevel(float2 UV_pixels , float scale)
{
    float2 x_deriv = ddx (UV_pixels );
    float2 y_deriv = ddy (UV_pixels );
    float d = max (length (x_deriv ), length (y_deriv ));
    return max (log2(d) - log2(scale ), 0);
}
```

#### 

#### 8.1.2 图块ID 的Shader实现 | Tile ID Shader

```
float2 UV_pixels = In.UV * VTMResolution ,

float mipLevel = ComputeMipMapLevel(UV_pixels , subSampleFactor);
mipLevel = floor(min (mipLevel , MaxMipMapLevel));

float4 tileID ;
tileID .rg = floor (UV_pixels / (TileRes * exp2(mipLevel )));
tileID .b = mipLevel ;
tileID .a = TextureID ;

return tileID ;
```

#### 

#### 8.1.3 虚拟纹理查找的Shader实现 | Virtual Texture Lookup

```
float3 tileEntry = IndTex .Sample (PointSampler , In.UV);
float actualResolution = exp2(tileEntry .z);
float2 offset = frac(In.UV * actualResolution) * TileRes ;
float scale = actualResolution * TileRes ;
float2 ddx_correct = ddx (In.UV) * scale;
float2 ddy_correct = ddy (In.UV) * scale;
return TileCache .SampleGrad (TextureSampler ,
tileEntry .xy + offset ,
ddx_correct ,
ddy_correct );
```
