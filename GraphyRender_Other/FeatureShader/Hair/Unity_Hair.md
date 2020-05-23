# 真实角色渲染---头发

Unity的Default PBR很多效果都很难支持，需要对其进行扩展。本篇先以写实游戏中的角色头发作为入口点，简单谈谈对于真实头发的渲染理论以及代码实现。

头发在光照渲染中表现出很明显的各向异性(Anisotropic，在不同方向表现出的光照效果会产生差异，拉丝金属，光碟也有同样的表现)。这种反射效果通常由物体表面的微表面特效所导致：物体表面主要由大量的方向一致的细长划痕或纤维表面组成，对于头发表面则是由大量的头发丝组成。如果这个采用普通的PBR高光模型渲染的话，很难达到不同方向上的差异性效果。渲染中主要技术点：1，AlphaTest  + AlphaBlend配合，以解决头发边缘硬边的问题 2，双层高光Kaijaya-Kay模型。核心代码u如下：

![img](Unity_Hair.assets/v2-9fe815bad7b8292f1bf02a76bd9c91d2_hd.jpg)第一次AlphaTest

![img](Unity_Hair.assets/v2-c81d085c828be0994cf17407386a8c7f_hd.jpg)第二次AlphaBlending

![img](Unity_Hair.assets/v2-38ab9f81f131c4c3e94f2ce5b3969fba_hd.jpg)双层高光

![img](Unity_Hair.assets/v2-8c39b3962ccbfe747a56d6ca59c77f16_hd.jpg)Rim效果

![img](Unity_Hair.assets/v2-ed39257b126db31fc016f84f59a20351_hd.jpg)参考UE4间接高光部分

再加上漫反射部分的代码，基本效果就出来了。考虑到手机上的性能，在计算直接高光部分的时候并没有常规的D和F项，F，D两项采用了代价较为低廉的公式。

下面放上效果图仅供参考。

![img](Unity_Hair.assets/v2-a1e5d9062de380c1884b6a3f0b4c15f8_hd.jpg)

![img](Unity_Hair.assets/v2-90bc4cfc6972fb88915022e56205ee3d_hd.jpg)

最近修改了一些参数，做了一版女性写实角色头发，效果图如下：

![img](Unity_Hair.assets/v2-a41faf64004aabc2089be66a1fc27266_hd.jpg)

![img](Unity_Hair.assets/v2-7241942869b9112f8add1a0b0f7e17a9_hd.jpg)

![img](Unity_Hair.assets/v2-f3fb29e34d28f3772670f3cfac8b7e03_hd.jpg)



编辑于 2019-08-03