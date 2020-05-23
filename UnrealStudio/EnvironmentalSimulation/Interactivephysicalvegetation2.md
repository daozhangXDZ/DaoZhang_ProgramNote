# 虚幻4渲染编程（环境模拟篇）【第六卷：可交互物理植被模拟 - 下】



https://zhuanlan.zhihu.com/p/65895937

## 概述：

可交互物理植被在完成动力学模拟后，接下来就需要完成Shading部分了。因为我们是做游戏开发，我们需要考虑性能问题。所以我们不能使用高模把植被的每片叶子都做出来。我们的植被模型都是插片的（这好像是个做游戏的人都知道），但是我们不能知其然不知其所以然。我们需要用更科学的方法来思考这个问题。

传统的思考方式是：“因为我们需要效率，所以我们使用插片简模来制作植被模型从而达到提高效率的目的”。似乎说得过去但是思考深度太浅。

更科学的思考方式是：“我们需要效率，所以把高模的一部分信息烘焙到贴图里，然后把另一部分信息投射到低模上，最后再把这些烘焙下来的的静态信息在引擎里组合，还原高模信息”。使用这样的思考方式我们可以得到如下结论：

（1）我们的核心目的是还原高模信息。

（2）我们需要把高模信息烘焙下来储存在贴图和模型里，几何向量信息我们烘焙到法线贴图里，遮挡信息烘焙到AO里，高光几何信息烘焙到SpecularMap里，叶片厚度信息烘焙到厚度图里。高模形状信息制作到低模里，等等。至此我们知道我们到底要为一棵树做什么资源，而不是盲目做各种透贴各种trick。

有了这套理论支撑后，我们以后制作头发，制作草丛，制作树等就有一个大概的方向了“把高频信息烘焙下来，然后重新在游戏Runtime的时候使用还原这些高频信息”。



![img](https://pic2.zhimg.com/v2-e824b772b22177f64ad8fd26eae81b25_r.jpg)

这便是制作植被的基础理论了。制作头发这些效果的时候，这个理论同样适用。

## 【**对植被光照进行数学建模**】

（1）叶片级别精度的植被光照模型



![img](https://pic2.zhimg.com/v2-23aed1545f8a3d4206744ebfeed096dd_r.jpg)

直射光过来，光线就两个大的部分，反射和透射。我们使用标准PBR光照模型来描述这个情况的话，只需要在标准PBR光照模型的基础上考虑透射就可以了。透射会让物体的暗部提亮，并且随着摄像机移动到投射光线方向，物体的投射光线进入摄像机的比例会增加，反射光线进入摄像机的比例会减小。

![L = R + T](https://www.zhihu.com/equation?tex=L+%3D+R+%2B+T) 

![R = C_{diffuse} + C_{Specular} + C_{Abient}](https://www.zhihu.com/equation?tex=R+%3D+C_%7Bdiffuse%7D+%2B+C_%7BSpecular%7D+%2B+C_%7BAbient%7D) 



![C_{WrapNoL} = saturate((dot(n,l) + w)/((1+w)*(1+w)))](https://www.zhihu.com/equation?tex=C_%7BWrapNoL%7D+%3D+saturate%28%28dot%28n%2Cl%29+%2B+w%29%2F%28%281%2Bw%29%2A%281%2Bw%29%29%29) 

![w\subseteq[0,1]](https://www.zhihu.com/equation?tex=w%5Csubseteq%5B0%2C1%5D) 

![w=1](https://www.zhihu.com/equation?tex=w%3D1) 



![img](https://pic1.zhimg.com/80/v2-ede92c7355eb9aad2f5a2c768aeb2c44_hd.jpg)

![w=0.5](https://www.zhihu.com/equation?tex=w%3D0.5) 



![img](https://pic1.zhimg.com/v2-b5806164fc9acb26ce26934e91649ef0_r.jpg)

 对于透射光来说

![T= C_{Scatter} * C_{WrapNoL} * C_{SubsurfaceColor}](https://www.zhihu.com/equation?tex=T%3D+C_%7BScatter%7D+%2A+C_%7BWrapNoL%7D+%2A+C_%7BSubsurfaceColor%7D) 

![C_{Scatter} = GGX(x,saturate(-dot(v,l)))](https://www.zhihu.com/equation?tex=C_%7BScatter%7D+%3D+GGX%28x%2Csaturate%28-dot%28v%2Cl%29%29%29) 

![x\subseteq [0,1]](https://www.zhihu.com/equation?tex=x%5Csubseteq+%5B0%2C1%5D) 



![img](https://pic2.zhimg.com/v2-d7fb2f85372726aea1d78915a6370421_b.jpg)

于是就能得到这种简单的投射效果。这种透射模型还常常用于制作玉石等效果上。

这个Shading模型给叶片级别的模型时可以比较好的描述光线的传播。什么是叶片级别的模型呢：



![img](https://pic3.zhimg.com/80/v2-52090c844db4bda71ce95b0ed87527f6_hd.jpg)

就是模型精度描述到了叶片级别。但是如果模型精度描述到了树冠级，上面的光照模型就不适合了。



![img](https://pic3.zhimg.com/80/v2-471422dbab2dc2e40c680c52481a7856_hd.jpg)

因为计算的时候还是会基于这个低精度的模型来计算，也就是会出现奇怪的高光位置。



![img](https://pic4.zhimg.com/80/v2-035b83a5888396044f05b5a3dbe5d383_hd.jpg)

大概率高光会出现在面片中心，但实际上这种情况下高光还是应该出现在树叶上



![img](https://pic4.zhimg.com/v2-3172eb54be815717b2f86efa3c5e3b6b_r.jpg)

也就是说我们的高光散布信息丢失了。

（2）树冠级别的模型精度

在树冠级别的模型精度的情况下，树冠的几何信息已经被拍平了，我们这时候使用法线贴图也是无法还原树冠的高模信息的，法线只能基于这个低模面片扰动低模法线。几何遮挡信息，高光分布信息需要我们把它烘焙下来。

下面的图我只显示高光计算结果。没有烘焙高光分布信息下的高光结果，直接基于低模面片计算的结果：



![img](https://pic3.zhimg.com/v2-bf504f7dcdef63c7896ba6a93597beca_r.jpg)

烘焙高光分布信息，通过高光分布信息计算的高光结果：



![img](https://pic3.zhimg.com/v2-5ffc40145ab5743dc0877947a1be19fa_r.jpg)

来个真实照片的树，可以看到高光的分布和我们理论分析的是一致的。



![img](https://pic3.zhimg.com/v2-ece94ed071ddcc9f4408f6a471c761a6_r.jpg)

我的树叶没有加BaseColor等，我直接给个纯色上去，当然模型还需要做球形法线



![img](https://pic2.zhimg.com/80/v2-7f570ed11b092e57d154eff53619529d_hd.jpg)

在生成球形法线的时候不能一个球直接整个包裹过去，应该有个简单的包裹模型覆盖树的低模模型，这个简单的包裹模型最好是树的高模的封闭拓扑低模。然后再把这个封闭模型的法线映射到树的插片低模上即可。这一过程可使用houdini完成。

关于植被的烘焙问题，如果要使用Lightmap，植被的树叶部分其实不适合光子映射的烘焙方法，因为并没有考虑透射部分。

至此我们对植被制作有了一套完整的理论支撑。



![img](https://pic4.zhimg.com/v2-e90db86985fd5e274d58b270bd1ea43b_r.jpg)

enjoy it。
