# 动态环境光遮蔽与间接光照（Dynamic Ambient Occlusion and Indirect Lighting）

## 

## 【章节概览】

这章在讲大家很熟知的环境光遮蔽（Ambient Occlusion , AO）。

文中的描述是，介绍了一种用于计算散射光传递的新技术，并演示如何用它来计算运动场景中的全局光照。主要是一种用GPU加速环境光遮蔽计算的技术，并将此算法变成了实时的解决方案。

## 

## 【核心要点】

这章介绍的这项技术效率很高，可以实现在渲染每帧时即时计算环境光遮蔽和间接光照数据。其并没有预计算辐射传递（Precomputed Radiance Transfer ，PRT）或预计算环境光遮蔽技术存在的限制。

[
![img](DynamicAmbientOcclusion.assets/0c3a47c39852e77246b1f98c9fa341d7.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/0c3a47c39852e77246b1f98c9fa341d7.jpg)

图 通过环境光遮蔽和间接光照增加真实感

图注：左边的场景只用环境光，看起来很平面化。中间的场景用环境光遮蔽加模糊阴影，右边的场景增加的间接光照，感觉格外真实。

这章的技术通过把多边形网格看做一些可以发出、传播或反射光的元素，并且可以互相产生阴影的表面元素集合来工作。此方法效率很高，因为它不需要计算一个元素到另一个元素的可见性，而是用一种更简单而且更快的技术——基于近似投影的方法——来处理遮挡的几何体。

## 

## 【关键词】

环境光遮蔽（Ambient Occlusion, AO）

间接光照（Indirect Lighting）
