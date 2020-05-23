## 基于间接光照的快速，基于模板的多分辨率泼溅 Fast, Stencil-Based Multiresolution Splatting for Indirect Illumination

本章介绍了交互式即时辐射度（radiosity）解决方案的改进，该解决方案通过使用多分辨率泼溅（multiresolution  splats）技术，显着降低了填充率（fill rate），并展示了其使用模板缓冲（stencil  buﬀer）的一种高效实现。与最原始的多分辨率泼溅[Nichols and Wyman  09]不同的是，此实现不通过几何着色器执行放大，因此能保持在GPU快速路径（GPU fast  path）上。相反，这章利用了GPU的分层模板剔除（hierarchical stencil culling）和Z剔除（z  culling）功能，以在合适的分辨率下高效地进行光照的渲染。

其核心实现算法如下：

```
pixels ←FullScreenQuad();
vpls ← SampledVirtualPointLights();
for all ( v ∈ vpls ) do
    for all ( p ∈ pixels ) do
        if ( FailsEarlyStencilTest( p ) ) then
            continue; // Not part of multiresolution splat
        end if
        IlluminatePatchFromPointLight( p, v );
    end for
end for
```

[
![img](ultiresolutionSplattingforIndirectIllumination.assets/2c9b16a1c95fb8284a498967e6e5e19b.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/2c9b16a1c95fb8284a498967e6e5e19b.png)

图  多分辨率光照泼溅开始于直接光照的渲染（左图）。每个VPL产生一个全屏幕的图示，允许每个VPL为每个像素提供光线。每个VPL产生一个全屏的泼溅，允许每个VPL为每个像素提供光线。但根据本地照明变化的速度，这些图层会以多种分辨率呈现。伪彩色全屏泼溅（中图）显示了不同分辨率的区域，这些区域被渲染为不同的buffer（右图）

[
![img](ultiresolutionSplattingforIndirectIllumination.assets/d334dde4b4259dddeb29cad0a92eb953.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/d334dde4b4259dddeb29cad0a92eb953.png)

图 多分辨率片的迭代求精从统一的粗图像采样开始（例如，162个采样）。处理粗粒度片元，识别需要进一步求精的片元并创建四个更精细的分辨率片元。进一步的操作会进一步细化片元直到达到某个阈值，例如最大精度级别或超过指定的片元数量。

[
![img](ultiresolutionSplattingforIndirectIllumination.assets/cf2ff293b62b459a26b503c79036a663.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/cf2ff293b62b459a26b503c79036a663.png)

图 前一幅图中的，多分辨率泼溅可以进行并行计算而不是迭代计算（左图）。右图中的多分辨率buffer中的片元，都为并行处理。

### 

### 9.1 实现思路小结

#### 

#### 9.1.1 多分辨率泼溅的实现思路 | Multiresolution Splatting Implement

以下是多分辨率泼溅实现思路，其中VPL的全称是虚拟点光源（virtual point light）：

```
1.	Render a shadow map augmented by position, normal, and color.
2.	Select VPLs from this shadow map.
3.	Render from the eye using only direct light.
4.	For each VPL:
    (a)	Draw a full-screen “splat.”
    (b)	Each splat fragment illuminates one texel (in one of the multiresolu- tion buﬀers in Figure 1.4) from a single VPL, though this texel may ultimately aﬀect multiple pixels.
    (c)	Blend each fragment into the appropriate multiresolution buﬀer.
5.	Combine, upsample and interpolate the multiresolution buﬀers.
6.	Combine the interpolated illumination with the direct light.
```

#### 

#### 9.1.2 设置可接受模糊 | Setting acceptable blur

```
patches ← CoarseImageSampling();
    for (i=1 to numRefinementPasses) do
        for all (p ∈ patches) do
        if ( NoDiscontinuity( p ) ) then
            continue;
        end if
        patches ← (patches − {p});
        patches ← (patches ∪ SubdivideIntoFour( p ) );
    end for
end for
```

#### 

#### 9.1.3 从虚拟点光源收集光照进行泼溅 | Gathering illumination from VPLs for splatting

```
patches ← IterativelyRefinedPatches();
vpls ← SampledVirtualPointLights();
for all ( v ∈ vpls ) do
    for all ( p ∈ patches ) do
        TransformToFragmentInMultiresBuffer( p ); // In vertex shader
        IlluminateFragmentFromPointLight( p, v ); // In fragment shader
        BlendFragmentIntoMultiresBufferIllumination( p );
    end for
end for
```

#### 

#### 9.1.4 降采样多分辨率照明缓存 | Unsampling the multiresolution illumination buffer.

```
coarserImage ← CoarseBlackImage();
for all ( buffer resolutions j from coarse to fine ) do
    finerImage ← MultresBuffer( level j );
    for all ( pixels p ∈ finerImage ) do
        if ( InvalidTexel( p, coarserImage ) ) then
            continue; // Nothing to blend from lower resolution!
        end if
        p1, p2, p3, p4 ← FourNearestCoarseTexels( p, coarserImage );
        ω1, ω2, ω3, ω4 ← BilinearInterpolationWeights( p, p1, p2, p3, p4);
        for all ( i ∈ [1..4] ) do
            ωi = InvalidTexel( pi, coarserImage ) ) ? 0 : ωi;
        end for
        finerImage[p] += (ω1p1 + ω2p2 + ω3p3 + ω4p4)/(ω1 + ω2 + ω3 + ω4)
    end for
    coarserImage ← finerImage;
end for
```

#### 

#### 9.1.5 并行泼溅求精 | Parallel splat refinement

```
for all (fragments f ∈ image) do
    if ( _ j such that f ∈ MipmapLevel( j ) ) then
        continue; // Fragment not actually in multires buffer
    end if
    j ← GetMipmapLevel( f );
    if ( IsDiscontinuity( f, j ) ) then
        continue; // Fragment needs further subdivision
    end if
    if ( NoDiscontinuity( f, j + 1 ) ) then
        continue; // Coarser fragment did not need subdivision
    end if
    SetStencil( f );
end for
```

#### 

#### 9.1.6 最终基于模板的多分辨率泼溅算法

```
pixels ←FullScreenQuad();
vpls ← SampledVirtualPointLights();
for all ( v ∈ vpls ) do
    for all ( p ∈ pixels ) do
        if ( FailsEarlyStencilTest( p ) ) then
            continue; // Not part of multiresolution splat
        end if
        IlluminatePatchFromPointLight( p, v );
    end for
end for
```
