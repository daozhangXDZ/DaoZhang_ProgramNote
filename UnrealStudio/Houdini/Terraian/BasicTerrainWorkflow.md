# Houdini Terrian & UE4 （一）基础的地形工作流

[![键盘侠·伍德](https://pic2.zhimg.com/c9f2a1ea500343fc04a3aeaf2e3dbe18_xs.jpg)](https://www.zhihu.com/people/kbmwooder)

[键盘侠·伍德](https://www.zhihu.com/people/kbmwooder)

不会写策划案的美术不是好程序



**导言**

houdini本身是很优秀的地形编辑工具，houdini engine让我们可以在UE4中使用houdini生成的HDA文件快速的构建地形地貌，并且支持协同工作。

![img](https://pic1.zhimg.com/80/v2-3db1e0b4ad2dcfb19c073be8e77d0110_hd.jpg)UE4 &amp; Houdini Pipeline

这里要了解到的一个概念是：我们在houdini中制作好了hda文件之后，在ue4中就可以反复的使用这个文件来做修改了，并不是传统的互相修改同一份文件来实现的，这使得ue4中可以进行闭环的操作，而不需要每一个使用到这部分功能的制作人员都掌握houdini使用方法

（注：未安装houdiniFX的电脑上，要想使用hda，一种选择是装sidefx提供的houdini engine版本，还有一种选择是在一台共用机上安装一个houdini engine，所有人在插件设置里使用tcp连接到共用机）。

这篇教程主要是为了带着大家走一遍houdini&ue4的基础，从houdini制作基础的高度图开始，导入ue4，在ue4中做一些调整，然后再使用hda文件cook一次，这就是最基础的一套操作环节啦！

关于一些houdini中基础的地形节点，请参照这篇文章呢！

键盘侠·伍德：Houdini Terrian & UE4 （〇）Terrian基础

zhuanlan.zhihu.com![图标](https://pic4.zhimg.com/v2-78688b3257f69ec05838d759607873e3_180x120.jpg)

**1、houdini中制作height field**

首先我们在obj目录里创建一个Geometry节点。

![img](https://pic1.zhimg.com/80/v2-2770e06043a1174ac848bd89016748f0_hd.jpg)



然后我们创建一个新的assert

![img](https://pic4.zhimg.com/80/v2-da44002201346f05fd44cae5badc64fb_hd.jpg)

![img](https://pic4.zhimg.com/80/v2-90696669108cf2def2e93cc1e626e667_hd.jpg)

这里我们把输入设置到0，因为初始化地形的节点并不需要输入

![img](https://pic1.zhimg.com/80/v2-b7fc615d6e3e37d599451f69d276b03c_hd.jpg)

然后我们在之前创建的Geometry节点里面，创建这个assert。

![img](https://pic1.zhimg.com/80/v2-90198db213d70fe6ce849bfc42e290ec_hd.jpg)

这里我们要打开编辑功能才能进去编辑LandScapeInit节点

![img](https://pic3.zhimg.com/80/v2-427e10d25eb5ddc9330c447b4ee887e2_hd.jpg)

这里我们就之做一个最基本的地形生成，怎么做的好看就自己研究啦~

![img](https://pic3.zhimg.com/80/v2-cc40810045ff10996ba6f71985d18efe_hd.jpg)

对于最基础的节点，我们按照ue4的标准来设置地形信息，否则导入ue4后地形边缘一圈会出现拉伸。

![img](https://pic2.zhimg.com/80/v2-f59ab897e30c509f1be047b98462215d_hd.jpg)

![img](https://pic3.zhimg.com/80/v2-f0ba4e3320aeb0489c4fb770b9bad596_hd.jpg)

这里插一个步骤，我们在ue4中先创建一个地形材质，这里我们简单的用颜色来表达。

![img](https://pic3.zhimg.com/80/v2-49d9ae0786e8a35ca0225a89f129074e_hd.jpg)

然后复制这个材质的引用

![img](https://pic1.zhimg.com/80/v2-b2eee14104bd64385abba3564f32ba58_hd.jpg)

用上面的引用在create attribute节点里面设置给unreal_material属性，记得要去头去尾哦。

这里的属性name是约定的。具体其他的属性可以参见官方文档或者看源码。

[https://www.sidefx.com/docs/unreal/_attributes.html](https://link.zhihu.com/?target=https%3A//www.sidefx.com/docs/unreal/_attributes.html)

这里我们设置好以后，地形被导入UE4时就会自动被赋予指定的材质

![img](https://pic2.zhimg.com/80/v2-1f5f8c8562b4361f0913de29095bfd99_hd.jpg)

然后我们选中最后一个节点并保存这个hda

![img](https://pic1.zhimg.com/80/v2-a2f89adbe26ca3973c898bb197220574_hd.jpg)

**2、导入ue4**

刚刚我们创建好的hda文件，我们把它拖入UE4，这时候就能看到一个houdini图标的uassert了。

![img](https://pic4.zhimg.com/80/v2-40199ec8f192d83f86b0ad4074f28bfb_hd.jpg)

然后拖入到场景当中，hda会自动把我们上面创建的地形cook出来。

![img](https://pic3.zhimg.com/80/v2-6a51ea38f1a56fe1184a3503e32cb212_hd.jpg)

这里我们看到的地形因为没有layer的信息，所以是全黑的。

![img](https://pic3.zhimg.com/80/v2-4e394833db41148ab0d30f2b7861c266_hd.jpg)

点击LandScapeInit里面detail面板上的bake按钮，把地形脱离开来，这时候LandScapeInit文件就可以从场景中删除了。

![img](https://pic1.zhimg.com/80/v2-cf99ef7bb63d1bec17c8839f8799e848_hd.jpg)

到这里，地形的高度信息就已经导入成功了，下面我们要给地形生成一些mask。后续可以用作山顶、斜坡贴图等。

**3、创建一个制作mask信息的hda文件**

和上面一样。我们创建一个新的assert叫LandScapeMask，但是这里我们希望它有一个输入参数，来接收一个heightfield。

![img](https://pic2.zhimg.com/80/v2-dbfff979c1536b054d4eb2548d8c8471_hd.jpg)

![img](https://pic4.zhimg.com/80/v2-eaf7a0c29758904c2129c39ce5cc0677_hd.jpg)

我们把这个节点创建到之前的LandScapeInit之后

打开允许编辑，我们来制作这个hda文件。

同样，这里也是做一个简单的mask创建。我们在这里用mask by feature对斜率信息做一个mask，然后把mask赋值到Slope。

后面反转slope层作为Base mask。

![img](https://pic1.zhimg.com/80/v2-b9869ad8765708be3c53486c92afcac4_hd.jpg)

选择最后一个节点，保存

![img](https://pic4.zhimg.com/80/v2-a72ff32697efbda6b6f813e6dc08e78f_hd.jpg)

**4、回到UE4**

我们把新的hda文件拖入UE4。

![img](https://pic4.zhimg.com/80/v2-ee748509190bbdba494ed6f581860473_hd.jpg)

然后我们就能看到刚刚我们定义的Input出现在了Detail面板里。

![img](https://pic1.zhimg.com/80/v2-815228a80bf25acb5d3febcb1666bde4_hd.jpg)

这里我们选择Update Input Landscape Data(更新输入的地形数据，不勾选的话会创建一个新的)，然后点击列表中的Landscape，hda就会自动把地形送到houdini library处理了。

![img](https://pic3.zhimg.com/80/v2-7a3b6252efdd0c4333721e60043463b6_hd.jpg)

处理完之后我们就能看到我们的地形上的斜坡被着色了。

![img](https://pic3.zhimg.com/80/v2-694e68ae04fab6e9dd676763e172a0f6_hd.jpg)

我们将这个处理之后的地形bake出来以后，可以做一些修改。这里我们在UE4中拉了一下地形。

![img](https://pic3.zhimg.com/80/v2-305c71fdc1d601f90cdf020b73dc08da_hd.jpg)

拖入LandScapeMask再次提交地形就可以看到，被提交的地形重新计算了slope layer的信息。

![img](https://pic2.zhimg.com/80/v2-a4db52c52cabf388bca5824c5aae9ec9_hd.jpg)

**5.将houdini的调整参数带入UE4**

打开houdini，进入LandScapeMask节点

![img](https://pic3.zhimg.com/80/v2-8f561119dd9574cb565f53b9b8a05032_hd.jpg)

这里就是可以放入参数并带入UE4的地方啦。

![img](https://pic3.zhimg.com/80/v2-d2fa10328f8261a31b7cc55571420b9a_hd.jpg)

我们选中mask by feature节点，直接将参数拽入parameters面板中，应用并保存hda文件。

![img](https://pic3.zhimg.com/80/v2-8b471ab87e6f49ca55558b593940de46_hd.jpg)

并且在UE4的内容浏览器里右键LandScapeMask选择Reimport，把修改的hda更新到uassert中。

![img](https://pic3.zhimg.com/80/v2-d22ba555679ff8ba8fcba28d24dd3cf6_hd.jpg)

拖入场景，就能看到Detail面板里这些信息了。

![img](https://pic3.zhimg.com/80/v2-ced0635a09e57c64578679a7d9d4e0c2_hd.jpg)

如果地形没有被bake出来的话，在这里调整参数会直接应用到地形上。

**6.注意点**

- 可以注意到我们这里用了两个hda节点来制作，其实也是个人自己觉得比较方便的方式。毕竟除了初始化地形的操作以外，很多操作如果没有输入是无法直接在houdini中预览效果的。通过这样的制作和连接方式，我们可以在制作mask活着后面撒点的时候都可以有个预览。



- parameter和input都可以把参数抛进UE4中，但是input更常用一点，毕竟在houdini中input可以直接作为输入口来预览。



- 每次用hda文件cook出结果后，最好都把结果bake出来，然后删除hda节点，下次要使用的时候再把hda拖进场景。当然，在确保没问题的情况下，把修改的地形放在hda下面能够得到更加及时的更新。 



- 每次hda操作之前和之后最好都保存并重新打开场景。

- - 如果操作前不保存，可能出现输入houdini engine的数据并不是当前最新的情况。
  - 如果操作后不保存重启，地形上的mask信息可能是错乱的，而且会发现调整地形或者画layer的时候笔刷在地形上很卡的情况。保存重开保存重开！真的很重要！

**后记**

到这里为止，我们在没有修改houdini engine插件的情况下完成了一次地形的基础工作流。在一些更加深入的工作流程探究时，我们还是会发现有很多不如人意的地方，这里暂不一一举例。

使用houdini&UE4做开发，除了houdini本身的使用外，还有很大一部分就是houdini engine根据项目的需求进行定制化，后面的分享也会围绕houdini engine定制来写。

还望多点赞，多指正，感谢感谢！