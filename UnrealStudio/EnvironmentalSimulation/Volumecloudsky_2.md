# 虚幻4渲染编程（环境模拟篇）【第二卷：体积云天空模拟(2)---3D体纹理低云】





在第一卷，先搭建了层云的模拟方法，光的衰减，云的影子，光线散射这些效果还没有往上做，先把整个天空系统搭建完成之后，再统一加这些比较好。

第一卷层云模拟链接：

[小IVan：虚幻4渲染编程（环境模拟篇）【第一卷：体积云天空模拟(1)---层云】](https://zhuanlan.zhihu.com/p/49489488)

现在来模拟下面这张参考图中的2，3部分的中低云的效果。



![img](https://pic1.zhimg.com/80/v2-84a72365f74bbd22c22654fb8a24c7a4_hd.jpg)

这种云使用程序化噪波的方式生成已经不太适用了，因为它的变化非常丰富，体积感很强而且这部分云在整个空中起到了遮挡，层次感的作用，所以某种程度上还需要我们可以控制它，最好艺术家设计师能使用软件或者什么调整它，所以3D体纹理成为了很好的选择，我们需要使用到houdini生产我们的素材。

**先搭建个能work的环境。**

我们拿一个甜甜圈做个快速测试。下面这个快速测试的原理可以去看我之前的博客，或者去看epic技术美术Ryan的ShaderBits博客（链接见参考文档部分）

[小IVan：Begin ray marching in unreal engine 4【第五卷：3D体纹理云】](https://zhuanlan.zhihu.com/p/37308462)

下面是在Houdini中的效果。



![img](https://pic1.zhimg.com/80/v2-b14c5d2d4430db36ee85d12c9ab3ae1c_hd.jpg)

Houdini的设置如下



![img](https://pic2.zhimg.com/80/v2-cd8dee278de76a235cde0a549a814e01_hd.jpg)

我们制作好的体纹理效果如下：



![img](https://pic4.zhimg.com/80/v2-5a81535aacaa430a32145c9cb8d117a3_hd.jpg)

制作好体纹理后，我们需要制作一个inverse normal的正方体盒子



![img](https://pic2.zhimg.com/80/v2-1982634df219c0b8f1dd0cd6d7b90b19_hd.jpg)



![img](https://pic3.zhimg.com/80/v2-232b98e171469f4e83359ee11a56ab06_hd.jpg)

然后我们做一个RayMarching的材质



![img](https://pic1.zhimg.com/80/v2-b2e9db3f22b2f4e079ae87b50e44cf1c_hd.jpg)

代码如下：

```text
float numFrames = XYFrames * XYFrames;
float accumdist = 0;

float stepsize = 1 / maxsteps;

for(int i = 0; i < maxsteps; i++)
{
    float cursample = 1 - PseudoVolumeTexture(Tex, TexSampler, saturate(Curpos), XYFrames, numFrames).r;
    accumdist += cursample * stepsize;
    Curpos += CameraVec * stepsize;
}

return accumdist;
```

效果如下：

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1046097033055866880?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



后面建云的流程也是这样，只不过形状更复杂罢了。现在我们有了一条可以work的管线之后，接下来当然就是去做天空中的“低云”咯。

------

使用houdini制作一块云(我这里搭建得比较简单)



![img](https://pic3.zhimg.com/80/v2-1fdcdec0bdd71d0efd6061f6c0bc897e_hd.jpg)



![img](https://pic3.zhimg.com/80/v2-6834fe98c5829a2a0752e18248b968f6_hd.jpg)

我选择模型生成的方式制作，这样方便控制。



![img](https://pic4.zhimg.com/80/v2-1c86cd42a460fa0c2ef3620bb9808c87_hd.jpg)

在引擎里的效果如下（还未计算光照，只对浓度进行了积分）

<iframe allowfullscreen="" src="https://www.zhihu.com/video/1046400779128258560?autoplay=false&amp;useMSE=" frameborder="0"></iframe>



目前有几个问题需要解决。第一就是云朵精度损失严重，很多细节都丢失了，这些细节如果想保留下来，就需要增大切片图的尺寸，而现在的切片图的尺寸已经很大了。



![img](https://pic4.zhimg.com/80/v2-b7b4a566df05fd609f091d2fe1b810d3_hd.jpg)

第二个问题就是我们使用ray  marching来制作云的初衷是为了弥补模型云的缺陷，但是现在看来，Volume  Texture也是事先烘焙的，无法使其变化。第三个问题和第一个问题有一定联系性，我们现在的诉求是做一片云海，然而现在一朵云都已经这样了，如果在尽量想为以后留优化空间的情况下，已经没有办法通过增加资源的精度来解决上述问题了。在下一节再完成对上述问题的解决。

Enjoy it！

------

## **Next：**

小IVan：虚幻4渲染编程（环境模拟篇）【第三卷：体积云天空模拟(3)---高层云】

zhuanlan.zhihu.com![图标](https://pic1.zhimg.com/v2-d37731435c7e3c4dd055d943130118fc_180x120.jpg)

------

参考文章

【1】 [Epic TA Ryan Shader Bits](https://link.zhihu.com/?target=https%3A//shaderbits.com/blog/)
