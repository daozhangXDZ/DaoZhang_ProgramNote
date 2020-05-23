## 屏幕空间软阴影 | Screen Space Soft Shadows

这章中提出了一种基于阴影映射的半影（penumbrae）实时阴影渲染的新技术。该方法使用了包含阴影与其潜在遮挡物之间距离的屏幕对齐纹理，其用于设置在屏幕空间中应用的各向异性高斯滤波器内核的大小，从而平滑标准阴影创建半影（penumbra）。考虑到高斯滤波器是可分离的，创建半影的样本数量会远低于其他软阴影方法。因此，该方法获得了更高的性能，同时也能得到外观正确的半影。

[
![img](https://github.com/QianMo/Game-Programmer-Study-Notes/raw/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/e60c1736e7712e99c5bc75c52c3f2848.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/e60c1736e7712e99c5bc75c52c3f2848.jpg)

图 不同光源尺寸和不同光源颜色的半影的示例
