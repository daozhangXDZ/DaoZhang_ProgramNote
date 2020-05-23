# 二十六、OpenEXR图像文件格式（The OpenEXR Image File Format）

## 

## 【章节概览】

这章中，大名鼎鼎的工业光魔公司的Florian Kainz、Rod Bogart和Drwe Hess介绍了OpenEXR标准，这是一种当时新的高动态范围图像（HDRI）格式，在计算机成像的顶级电影中正在快速推广。对于基于图像照明的开发者而言，OpenEXR是关键的工具。

## 

## 【核心要点】

OpenEXR是由工业光魔（ Industrial Light & Magic ，ILM ）公司开发的高动态范围图像（ high-dynamic-range image ，HDRI）文件格式。OpenEXR网站是 [www.openexr.org](http://www.openexr.org) ，上面有关于此格式的全部细节。

下图是一个例子，说明了需要HDR存在的原因。

如下图是一张显示相当高的动态范围的场景，场景中左边的油灯的火焰比中间小盘子下的阴影大约亮100000倍。

[
![img](OpenEXRImageFileFormat.assets/38440d033d85c19ef77ba96890ad4d43.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/38440d033d85c19ef77ba96890ad4d43.png)

图 高动态范围场景

图像曝光的方式导致了一些区域的亮度超过了1.0，在计算机显示屏上，这些区域被裁剪（clipped）掉，并显示为白色或不自然的饱和桔色色调。

我们可以通过把图像变暗来校正白色和橘色区域，但是如果把原始图像存储在低动态范围文件格式中，如JPEG格式，把它变暗就会产生相当难看的图像。如下图。

[
![img](OpenEXRImageFileFormat.assets/3931c1f9af121e34b437f98117906fd6.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/3931c1f9af121e34b437f98117906fd6.png)

图 普通文件格式导致明亮的像素值被不可逆地裁剪，使得明亮的区域变灰，并且细节丢失，得到极不自然的效果

而如果原始图像存储在高动态范围文件格式中，如OpenEXR，保存明亮的像素值，而不是把他们裁剪到1.0，然后把图像变暗，就可以产生依旧自然的效果。如下图。

[
![img](OpenEXRImageFileFormat.assets/69c6d71d2ea14454a83640d331bec7b5.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/69c6d71d2ea14454a83640d331bec7b5.png)

图 上述变暗的图的高动态范围版本。在明亮的区域中显示出了其他细节，颜色看起来很自然

文章随后还讲到了OpenEXR的文件结构、数据压缩、使用、线性像素值、创建和使用HDR图像相关的内容。

## 

## 【本章配套源代码汇总表】

Example 26-1 读取OpenEXR图像文件（Reading an OpenEXR Image File）

Example 26-2 将图像绑定到纹理（Binding an Image to a Texture）

Example 26-3 合成两个图像并写入OpenEXR文件（Compositing Two Images and Writing an OpenEXR File）

Example 26-4 合成一个Pbuffer（Compositing into a Pbuffer）

Example 26-5 Cg Shader进行“Over”操作（Cg Shader for an "Over" Operation）

Example 26-6 Cg Shader进行“In”操作（Cg Shader for an "In" Operation）

Example 26-7 Cg Shader进行“Out”操作（Cg Shader for an "Out" Operation）

Example 26-8. 伽马校正一张图像并显示（Gamma-Correcting an Image for Display）

Example 26-9 调整调整图像的曝光（Adjusting an Image's Exposure）

Example 26-10 使用查找表来模拟摄影胶片的外观（Using a Lookup Table to Simulate the Look of Photographic Film）

## 

## 【关键词提炼】

高动态范围（High-Dynamic-Range , HDR）

高动态范围图像（High-Dynamic-Range Image，HDRI）

OpenEXR

# 

# Reference

[1] <https://cgcookie.deviantart.com/art/Subsurface-Scattering-Tutorial-658412208>

[2] <https://zhuanlan.zhihu.com/p/21247702?refer=graphics>

[3] <https://renderman.pixar.com/resources/RenderMan_20/subsurface.html>

[4] <https://www.davidmiranda.me/unity-skin/>

[5] <https://www.youtube.com/watch?v=OQ3D0Q5BlOs>

[6] <https://www.geforce.com/games-applications/pc-applications/a-new-dawn>

[7] <https://www.shroudoftheavatar.com/forum/index.php?threads/on-video-game-graphics.54435/>

[8] <https://support.solidangle.com/display/AFMUG/Guide+to+Rendering+Realistic+Skin>

[9] <http://forums.cgsociety.org/showthread.php?p=8310370>

[10] <https://www.dualshockers.com/uncharted-4-dev-explains-how-drakes-incredible-shaders-were-made-shows-direct-feed-wip-screenshots/>

[
![img](OpenEXRImageFileFormat.assets/be47b90b234000f802e16fa2ee4e509d.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/be47b90b234000f802e16fa2ee4e509d.jpg)

全文完。

With best wishes
