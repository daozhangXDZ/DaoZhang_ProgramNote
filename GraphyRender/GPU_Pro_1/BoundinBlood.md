## 《狂野西部：生死同盟》中的渲染技术 | Rendering Techniques in Call of Juarez: Bound in Blood

《狂野西部：生死同盟》（Call of Juarez: Bound in Blood）是由Techland公司开发，育碧发行，并于2009年夏季在PS3，Xbox360和PC上发布的游戏。

[
![img](BoundinBlood.assets/8c1f5c8e294d71153c1d505cc6e3e4c6.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/8c1f5c8e294d71153c1d505cc6e3e4c6.jpg)

图《狂野西部：生死同盟》封面

[
![img](BoundinBlood.assets/5dbe0eb8c0cb6c2f658f874a56f05889.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/5dbe0eb8c0cb6c2f658f874a56f05889.jpg)

图《GPU Pro 1》的封面，即是采用的《狂野西部：生死同盟》的图片

[
![img](BoundinBlood.assets/728c736d64bbd6d8d1a5b4245ada9324.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/728c736d64bbd6d8d1a5b4245ada9324.jpg)

图 《狂野西部：生死同盟》游戏截图

《狂野西部：生死同盟》基于ChromeEngine 4，游戏中大量用到了延迟着色（deferred shading）技术。

众所周知，延迟着色 [Hargreaves 04]是一种在屏幕空间使用存储了诸如漫反射颜色，法向量或深度值等像素信息的中间缓冲区（G-buffer）的技术。

G-buffer是一组屏幕大小的渲染目标（MRT），可以使用现代图形硬件在单个pass中生成，可以显着降低渲染负载。然后使用G-buffer作为着色算法的输入（例如光照方程），而无需浏览原始几何体（此阶段计算所需的所有信息，如三维世界空间中的像素的位置，可以从G-buffer中提取）。以这种方式，算法仅对可见像素进行操作，这极大地降低了照明计算的复杂性。

[
![img](BoundinBlood.assets/045f3d4f1d5db9bc2d624b24cd5dbf78.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/045f3d4f1d5db9bc2d624b24cd5dbf78.png)

表 《狂野西部：生死同盟》中的MRT配置

延迟着色方法的主要优点是对渲染管线的简化，节省复杂着色器资源和计算的开销，以及能对复杂光照（如动态光源）进行简约而健壮的管理。

延迟着色技术在与后处理渲染效果的结合方面可以获得不错的化学反应。在《狂野西部：生死同盟》中，延迟渲染与诸如屏幕空间环境光遮蔽（SSAO），运动模糊（motion-blur），色调映射（tone  mapping）以及用于改善最终图像质量的边缘抗锯齿（edge anti-aliasing）等后处理效果都可以很好的结合使用。

[
![img](BoundinBlood.assets/5805c19c529c4437067ceeb9420b79ee.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/5805c19c529c4437067ceeb9420b79ee.jpg)

图 拥有动态光源和环境光遮蔽的室内场景

这章中还展示了不少《狂野西部：生死同盟》中自然现象效果的渲染方法，如雨滴，体积地面雾，light shafts，真实感天空和云彩，水面渲染，降雨效果，以及体积光的渲染技巧。以及色调映射相关的技术。

[
![img](BoundinBlood.assets/6bb9df54b962f3cd39d0672319db0ffc.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/6bb9df54b962f3cd39d0672319db0ffc.jpg)

图 场景色调映射，在阴影区域和光照区域之间转换
