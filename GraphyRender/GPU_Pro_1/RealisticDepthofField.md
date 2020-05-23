## 后期制作中的真实景深 | Realistic Depth of Field in Postproduction

景深（Depth of field，DOF）是一种典型的摄影效果，其结果是根据摄像机与摄像机的距离而产生不同的聚焦区域。

这章中，提出了一种交互式GPU加速的景深实现方案，其扩展了现有方法的能力，具有自动边缘改进和基于物理的参数。散焦效应通常由模糊半径控制，但也可以由物理特性驱动。此技术支持在图像和序列上使用灰度深度图图像和参数，如焦距，f-stop，subject  magnitude，相机距离，以及图像的实际深度。

另外，景深实现中额外的边缘质量改进会产生更逼真和可信的图像。而局部邻域混合算法的缺点是二次计算能力，但这其实可以通过GPU进行补偿。

[
![img](RealisticDepthofField.assets/262723e5a61ca21ab839fbdf6534329d.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/262723e5a61ca21ab839fbdf6534329d.jpg)

图 景深效果图

[
![img](RealisticDepthofField.assets/0b0a367098df217262a28c29e9502e28.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/0b0a367098df217262a28c29e9502e28.png)

图 模拟曝光的光圈孔径形状示例
