# Basic Human Hair - 上



## **我都专栏目录：**

小IVan：专题概述及目录

zhuanlan.zhihu.com![图标](https://pic4.zhimg.com/v2-adfc32ab6d1929ce6ebb6863da9e0f0f_180x120.jpg)

## **简介：**

在游戏种制作种，人物的占比越来越大而且已经成为一个体系。渲染和优化的时候都会为角色量身定制一套方案。甚至为了角色表现，把展示选择大厅的角色还单独做一套效果和资源。角色身上的材质和制作都是游戏美术资源中最复杂的。人物篇将研究角色的各个部位的各种做法。

本篇将先从最难的头发开始。分别从制作大型和Shading几方面入手。目前业内经常使用Maya的XGEN作为主要制作工具。不过这一章我使用ZBrsuh+3DMax来制作头发。

------

## **【Hair Shading】**

本文使用Pekelis  et al. 2015, "A Data-Driven Light Scattering Model for  Hair"的Shading方案，这也是Unreal内置的HairShadingModel使用的方案。下面就来详细阐述其原理。


![img](https://pic2.zhimg.com/80/v2-6b229c0e8d1a328b8089a523ddcda535_hd.jpg)图片来自A Data-Driven Light Scattering Model for Hair

Kajiya  and Kay's  HairShadingModel只是大概描述了以下头发的光照模型，再七八年前效果还能满足需求，但是现在对渲染品质要求的提高，所以业界提出了新的光照模型。如果对怎么构建光照模型和Kajiya  and Kay's不熟的话，可以先去看我前面的两篇文章：

[KajiyaKay头发高光模型](https://zhuanlan.zhihu.com/p/38052151)

[构建光照模型的方法](https://zhuanlan.zhihu.com/p/46618943)


![img](https://pic4.zhimg.com/80/v2-be9876a139fe8daeefcc4bb90b87b347_hd.jpg)

将光路分为了三项

（1）R：由于头发纤维的倾斜，所以假设了一个偏差，将高光朝着发根的方向偏移，头发的各向异性高光。

（2）TT：头发的强烈散射部分，当光从头发背面打过来的时候，会产生强烈的透光散射就是这项计算的。

（3）TRT：在头发内部光线再次反射出来的光线，头发的次级高光点。

这个光照模型已经考虑得非常完善了，当然如果你还嫌不够的话还可以自己对光线进行建模，比如R摄入之后在头发介质中的传播还可以考虑多次散射。Data-Driven  Light Scattering Model for Hair对上述三项进行了改进，重要性采样等，效率更高效果更好。


![img](https://pic3.zhimg.com/80/v2-fb881f055141052c014771d057e0e93e_hd.jpg)

![S = C_{BaseColor} + S_{Specular}](Light Scattering from Human Hair Fibers.assets/equation-1559761944695.svg) ...........................................(1)

![S_{Specular} = R + TT + TRT](Light Scattering from Human Hair Fibers.assets/equation-1559761944652.svg) .......................................(2)



------

## **【Hair Assets Production】**

首先需要准备头发的模型。头发的做法根据建模的方式目前可以分为两种，一种是几何体形状的，一种是插片的。如果大量使用集合体状的来制作模型，一般是卡通项目。大量选用面片的话一般是写实类，但是写实类也会有使用几何模型来制作头发某些部分的情况。本篇是制作写实类的。下面是我在ZBrush中制作的头发基础模型。


![img](https://pic3.zhimg.com/v2-43bb53d1917b3f2f7c2bb631cf8b6ba6_b.jpg)

<svg x="16" y="18.5" class="GifPlayer-icon"></svg>

请无视GIF中因为压缩产生的残影

MeshFilter可以非常方便地制作头发的模型的大型，具体细节可以导回Max或者Maya中再做调整。不管用什么工具来制作，这个工具只要满足以下几个条件就可以使用这个工具来制作。

（1）方便制作大型，调整大型，各种发型，包括但不限于卷发，各种鞭子。

（2）能方便分UV，人工分这么复杂头发模型的UV实在不是个好注意。

（3）能够从高模烘焙出各种基础资源，如BaseColor，Tangent，Normal，ID，Depth等信息。

（4）头发面片穿插较少，层于层之间的间隔要固定，下图红圈部分的头发刚好侧面对着摄像机所以可以看到这一特性。


![img](https://pic4.zhimg.com/80/v2-e5dc8be3bbd679187eeb3b8353dea81b_hd.jpg)头发面片减少穿插

在导出模型之前，把FiterMesh使用FiterMeshUV。


![img](https://pic4.zhimg.com/80/v2-b6f0b7560f8f7b9f06ee86a3426b413f_hd.jpg)

因为我的模型已经Create过了所以这里是Disable的状态。导入到max可以看到如下效果：


![img](https://pic2.zhimg.com/80/v2-e0f015cda97f99809e3c0ec5ea249c59_hd.jpg)模型UV

UV被分得工工整整的，但是所有UV都是重叠的。


![img](https://pic3.zhimg.com/80/v2-95f2900fe6b7b19cdc2050b9a541347a_hd.jpg)

这正是我们想要的效果。准备好模型后就可以进入下一步了。我把头发分为长发部分，发梢部分，刘海部分，耳发部分，不同的模型会有不同的头发类型。下面就来制作头发的贴图。具体贴图怎么制作需要根据头发的Shader是如何写的来决定。

因为我们需要发丝的法线，Tangent，深度，Opacity等信息，所以我们需要制作头发的高模


![img](https://pic2.zhimg.com/80/v2-7951a1ca1c16f4e121cad9da6831ae9d_hd.jpg)头发高模制作

高模也可以用FiterMesh制作或者使用XGEN。然后架一个平面，把我们需要的信息从高模上烘焙到贴图上。

------

## 【Hair Shading in unreal engine 4】

把Opacity和Normal还有Base_Color导入引擎，设置好材质后可以看到如下效果：


![img](https://pic3.zhimg.com/80/v2-d06f835b61891379aa1c20a0b716ae0e_hd.jpg)无tangent切线

可以看到有很多问题。第一：因为目前所有头发使用了一个头发高模烘焙出来的发丝Opacity，所以变化比较单一，耳发。刘海都。第二：因为没有制作Tangent贴图所以各向异性高光计算错误。第三：没有深度偏移，所以头发没有层次感。下面就先从这三个问题切入。



**【1】**因为这是使用的面片，所以使用顶点自己本身的切线也可以大概描述发丝的走向，这样便可以计算R和TRT项了效果如下：


![img](https://pic2.zhimg.com/80/v2-51eb2a947b1f5fb526907a696e38fa35_hd.jpg)使用顶点切线

可是使用顶点的tangent并不精确，可以看到上图的高光是乱的。顶点Tangent如下图所示：


![img](https://pic2.zhimg.com/80/v2-a7196f6fd7f2bd707abc7d5f886624c1_hd.jpg)

如果头发模型的段数够高，或者角色是短发，可以跳过这个问题。如果不想使用头发自己的vertex tangent可以制作FlowMap，这道工序我会在后面提到。



**【2】**为了头发更自然，我多制作了几套头发片的高模。


![img](https://pic2.zhimg.com/80/v2-b99bff698b5873c3c2af031c3e1a2551_hd.jpg)增加高模种类

因为FiterMesh分出来的模型一开始UV都是重叠的，所以我们可以选中整片头发然后SplitUV然后慢慢调整。给头发的各个部分做区分后，可以得到如下效果：


![img](https://pic2.zhimg.com/80/v2-2a0a9f3e5e97c367bbc06cee9bb48a49_hd.jpg)增加高模烘焙后的效果

虽然头发变化增多了，但是头发整体还是感觉哪里很奇怪，这就要说到上一个话题，因为使用的是Vertex的Tangent，所以每个头发面片都是像鳞片一样镶嵌在头上的，不是一个整体。

下一步是把UV平展然后分出第二套UV


![img](https://pic4.zhimg.com/80/v2-ea4d770acc1b57ce92447881808d3233_hd.jpg)为FlowMap和Depthmap制作第二套UV

可以在二套UV上制作FlowMap和Depthmap。Depthmap用于做PixleOffset。下面我使用SubstancePainter制作FlowMap

在SP中制作flowmap第一步创建一张（128 0 255） 的FlowBaseMap

然后对笔刷做如下设置：


![img](https://pic4.zhimg.com/80/v2-25edc8fe1d098c761055476002bac82b_hd.jpg)

便可以绘制flowmap了


![img](https://pic2.zhimg.com/80/v2-ad2561dabb3a8ea85a317360bc3a7c9d_hd.jpg)


![img](https://pic3.zhimg.com/80/v2-aae12d9d44d57fd6a4f15b6c6ef3101a_hd.jpg)制作FlowMap

FlowMap可以讲头发面片整体化，可以看到不同面片的高光点位置连续了，如下图所示：


![img](https://pic2.zhimg.com/80/v2-4018de0105ccc4f21d57e28176ce3a95_hd.jpg)


![img](https://pic2.zhimg.com/80/v2-65e4f8e8bfd6929fd6c1a0ff3bb5db2d_hd.jpg)

和只使用顶点tangent的效果比起来，后脑勺部分的长头发高光效果改善显著。

【3】现在来解决第三个问题，层次感。发丝是有层次的，但是我们的模型是面片，也就是说面片模型会导致大片大片的发丝深度是一样的。


![img](https://pic1.zhimg.com/80/v2-c3c971479b6d209e86f0b262af88756c_hd.jpg)

模型发丝深度如左图所示，正确的发丝深度如右图所示。所以我们需要深度图。对于深度图其实还有很多作用，如果使用AlphaBlend来做头发的话深度还能防止透明乱序。

AlphaTest + TAA Dither Alpha 不需要考虑乱序的问题。

除了深度以外，还需要IDMap和RootMap。在开始制作深度图之前，需要先了解清楚DepthOffset的作用原理。把两个面片重叠在一起，可以看到如下效果：


![img](https://pic3.zhimg.com/80/v2-63b43590339abb09e138e1774f54528e_hd.jpg)

这就是常说的ZFighting，可以通过修改PixleDepth来对当前像素做深度偏移。


![img](https://pic2.zhimg.com/80/v2-73b450941e5419d7022e2d5200a026ad_hd.jpg)

用这种方法就可以对头发面片上的发丝做偏移了，这样可以制作出层次感和避免乱序。

如果不做偏移，同一个面片上的发丝始终是没有层次感的。


![img](https://pic3.zhimg.com/80/v2-91aedb631962d42332a8aa697bcb7d46_hd.jpg)

不过在烘焙深度和ID之前我们需要吧模型的Modeling做完。之前只是做了头发的基础，我们还需要完成头发的一些小的发丝。和制作头发基础模型一样，还是在zb中制作。发丝模型不必太多，只是零星点缀在头发模型表面。


![img](https://pic4.zhimg.com/80/v2-9ef66dc13701d5881a937d712465ce03_hd.jpg)

然后为其准备一个高模然后烘焙其Alpha


![img](https://pic4.zhimg.com/80/v2-c921a27e672317953e58f16206b9f1df_hd.jpg)

把它加到原来的模型上，效果如下：


![img](https://pic2.zhimg.com/80/v2-d6c22aff3b1f08750cc939f232d5522d_hd.jpg)

完成了最后的Modeling，那么就开始烘焙ID和深度来解决最后的头发面片本身无层次感的问题：


![img](https://pic3.zhimg.com/80/v2-65dff32f2860455c512642635bfdf30e_hd.jpg)

加入ID和深度后，头发的层次感增强。


![img](https://pic2.zhimg.com/80/v2-a2849be7a87e945478950434821959e5_hd.jpg)

------

## **Conclusion：**

头发制作之前需要根据具体的Shading方案来定制资源生产流程。就拿Data-Driven  Light Scattering Model for  Hair来说，主要需要提供IDTexture，AlphaMap，MetallicTexture，RouphnessTexture，DepthTexture，AOTexture，TangentTexture，BaseColorTexture

上面我使用的ZBrush+3DMax+SubstancePianter的制作流程的主要问题是制作头发高模的时候无法制作较好的BaseColorTexture和AphaTexture。DepthTexture效果也不令人满意。

下一节将完善这个流程。

Enjoy it ！

------

参考文献：

【1】[https://graphics.pixar.com/library/DataDrivenHairScattering/paper.pdf](https://link.zhihu.com/?target=https%3A//graphics.pixar.com/library/DataDrivenHairScattering/paper.pdf)

【2】[http://graphics.stanford.edu/papers/hair/hair-sg03final.pdf](https://link.zhihu.com/?target=http%3A//graphics.stanford.edu/papers/hair/hair-sg03final.pdf)
