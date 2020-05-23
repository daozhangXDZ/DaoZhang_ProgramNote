## 、快速传统阴影滤波 | Fast Conventional Shadow Filtering

这章介绍了如何减少常规阴影贴图过滤的硬件加速百分比邻近过滤（percentage closer  filtering，PCF）纹理操作次数。现在只需要16次PCF操作就可以执行通常使用49次PCF纹理操作进行的均匀8×8过滤器。由于纹理操作的数量通常是传统阴影滤波的限制因素，因此实现的加速效果比较显著。PS:文中附带了大量的shader实现源码。

[
![img](ConventionalShadowFiltering.assets/64b005316a6260bb9fa241d2072b75a1.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/64b005316a6260bb9fa241d2072b75a1.jpg) 图 效果截图

## 

## 二十、混合最小/最大基于平面的阴影贴图 | Hybrid Min/Max Plane-Based Shadow Maps

这章介绍了如何从常规的深度阴影贴图（depth-only shadow  map）导出二次贴图。这种二次纹理可以用来大大加快昂贵的阴影滤波与过大的过滤器性能占用。它以原始阴影图中二维像素块的平面方程或最小/最大深度的形式存储混合数据。,被称为混合最小/最大平面阴影贴图（hybrid  min/max plane shadow  map，HPSM）。该技术特别适用于在大型过滤区域和前向渲染的情况下加速阴影过滤，例如，当阴影过滤成本随着场景的深度复杂度而增加时。

[
![img](ConventionalShadowFiltering.assets/47c584f6c0b089d7c64be5ce26f2fa93.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/47c584f6c0b089d7c64be5ce26f2fa93.jpg)

图 一个最小/最大阴影贴图像素（即有噪声的四边形）可以映射到许多屏幕上的像素。
