# Transllate_Unreal

[TOC]

在日常开发者接触过程中经常被问到透明物体相关问题，比如排序，品质，效率，表现等；另一方面透明材质也有些特有优势未被充分认识；希望能通过比较系统的介绍一下透明材质：从概念到特性，优势劣势，应用场景，并结合实践循序渐进展开。为更快速地定位解决相关问题，为拓展思路和应用想象空间抛砖引玉。

什么是透明材质：

UE4中透明材质主要是指Blend Mode是Translucent类型的材质。它的特征是可以有半透效果，能部分或者全部看到后面SceneColor(背景)，延迟渲染管线下还包括看到材质后的其他G-buffer的信息， 并且不写入深度（SceneDepth）；从广义上来讲能和材质后像素混合的材质都是透明材质，因此其他如Modulate, Additive, 以及AlphaComposition 等混合模式的材质都具有透明材质的特征。另外除了Surface类型材质，Deferred Decal, Volume目前只能使用透明Blend Mode。

透明材质的特性以及带来的相关优劣势：

1. 不写入场景深度（SceneDepth），但可以单独绘制深度到Custom Depth，及绘制Custom Stencil等buffer；
    因此深度相关的特性缺失。最常遇到的问题是基于像素的前后排序的问题。目前透明材质的前后排序仅能通过透明物体相对于摄像机距离远近来做前后排序，这个可以在物体的Translucent  sort里设置其优先级，优先级越高越靠前。另外粒子有其特定的信息来帮助排序，比如粒子诞生的时间，离摄像机的距离等，这些可以在粒子系统的相关参数中调整；另外多个透明物体由于随着摄像机移动产生绘制顺序的前后变化跳跃，我们也可以把这些透明物体作为一个Group通过使用一个Bounds来固定前后绘制顺序；但所有这些都基于物体而非像素，这是目前已有的局限；如果要基于像素的排序就需要有深度绘制，Epic一直使用的是通过非透明材质加Dither Opaque Mask的方式来模拟，效果效率有优劣，这里不再深入讨论。
    没有深度的另一个常见问题是透明物体景深效果（DOF）的问题。材质本身深度的缺失导致DOF散焦效果会基于透明物体背后的深度来计算，如果透明物体离背景较近，深度差别小，问题不严重；如果离背景远，比如非常近距离的透明物体背景是天空（无限远），整个透明物体就会被（DOF）模糊掉。目前解决方式是通过指定透明材质绘制到DOF效果之后而排除掉DOF对其的影响，然后再在材质里简易的模拟DOF效果（比如变大，变模糊），这里涉及到的材质节点是DepthOfFieldFunction，具体的实现可以参看ParticleDOF材质函数的实现，这里也不具体展开了
    没有深度也带来特殊的优势，我们可以通过忽略排序来让它绘制到最前面（材质中Disable Depth Test）。使用这种方式可以做一些局部区域类似后期的效果
    选择Real Time Ray Tracing渲染透明物体没有排序问题，这里也不展开
    
2. Unlit Translucency: 透明材质的最大特性是可以半透，同时看到前景和背景（背景的颜色，深度，法线，等等），或者说可以采样到背景作为前景；
    屏幕上透过透明材质看到的画面最终效果无非取决于三方面：前景，背景，以及两者的混合模式；
    前景指直接传入到Emissive Color中的信息；这个信息可以是贴图，数值，背景信息（背景颜色，深度，法线，位置等等），Custom通道信息
    背景指Opacity（0-1）为0时候看到的信息。我们对背景内容本身无法改变，能控制的是通过调整Opacity值决定看到的背景的多少，是线性控制；
    背景Opacity的控制也可以通过控制前景来模拟实现（通过Lerp  SceneColor）；比如以下的透明Logo效果可以用以下两种方式实现。他们在效果上没有区别，效率上在不同的情况下稍有差别（这里控制Opacity方式更快，但有时Lerp快）。这个需要注意下，根据实际情况选用合适的方式，尤其是OverDraw严重的时候会累计这种开销差别

![pic1.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic1-291x289-28fcd14b14eabb59467a28ede28c89e658fe94ac.png)
![pic2.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic2-441x512-021f8f974f932b0565d1bb50402c72f1315efa01.png)
![pic3.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic3-378x447-bb6259a9f90aac5f9f379101bf5d4609102b3200.png)

混合模式(Blend Mode)目前有Translucent\Modulate\Additive\AlphaComposition等；

![pic4.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic4-384x112-1bceb8eb69be9816ce51e07283c8a5f3c4ad451c.png)

混合方式(Blend Mode)的控制也可以通过控制前景模拟实现；以下是Modulate， Additive和AlphaComposition等Blend Mode通过Translucent Blend Mode来模拟。效果无差别，开销在不同情况差别不一。

比如Modulate混合模式是前景乘上背景的混合结果，一般来说会变得更暗。它也可以使用Translucent混合模式通过前景乘上SceneColor来实现（开销比较会根据实际情况变化）

![pic5.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic5-480x317-f16e82bea3f9ba18077fb01f3b0bb80f515a171e.png)

同样Additive混合模式是前景加上背景的混合结果，会变得更亮。可以使用Translucent 混合模式前景加上SceneColor实现

![pic6.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic6-483x330-008671a83e670f5e352858a3133d9179301ca778.png)

AlphaComposition混合模式是前景加上背景的结果和背景之间的线性混合，混合权重取决于Alpha；这种混合模式比较好的平衡了Additive和Translucent两者的优略，使得混合结果某些亮的区域在背景前不至于太爆，同时对于Alpha通道的品质要求也不高。适用于一些解决过曝粒子特效的问题。

![pic7.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic7-479x255-40995475f62b2a761d5bcdd4c079940604ded82c.png)

从AlphaComposition的模拟看出，其实它是Additive和Translucent两种混合模式在一个材质中的实现；我们看到控制前景模拟混合模式可见的好处是可以在一个材质里基于像素区分多种混合方式。以下例子就是把Modulate, Additive和AlphaComposition三种混合方式通过一张贴图的不同通道来做区分混合到了一个材质里。

![pic8.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic8-965x943-346d2ca2d5874d3ea6342a7dc405a3b7b3b4569c.png)

因此透明材质控制的三方面都可以归一化为前景控制。前景控制包括本身的值，和UV等；对于这些的控制可以实现不少效果，这里结合实践围绕这个特性循序渐进地展开一下

对Unlit Translucency材质半透特性的实践：

我们从一个不受光（Unlit）的透明材质开始，采样了背景颜色（SceneColor）并乘以一个自定义颜色；把它付给一个球体模型，并包裹目标；按预期的那样，我们通过采样背景作为前景（SceneColor*自定义颜色）的控制方式改变了特定区域的效果

![pic9.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic9-544x505-8f64461609dc7ae969134b1c4fec564383eb3697.png)
![pic10.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic10-544x304-c9bf6de6e8565e4c8ba8166ce7ed16cec8ff068d.png)

接下来我们把这个效果的特定区域进一步限定到仅影响目标物体；这可以通过打开目标的Custom Stencil来做Mask来实现

(项目设置中Custom Depth-Stencil Pass: Enabled with Stencil；对象Actor打开Render CustomDepth Pass并设置一个CustomDepth Stencil Value，这里为1)

![pic11.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic11-571x489-f66c0b1a28f0a3d7b37006f9d13d89c98d389260.png)
![pic12.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic12-629x554-0c8dbe9fbd62532762ef2515d5dcd7abe3d2a2a2.png)

这里我们并没有利用控制背景（Opacity）来限定区域，而全都通过控制前景Lerp SceneColor的方式实现了。

上面提到利用控制前景来模拟背景控制的方式执行效率上不同情况会变化，这里反而控制背景比控制前景实现方式增加几个指令（比较上下两图统计数字72vs70）

![pic13.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic13-512x537-3bde89193d61f238411791c926b0fbaf875b2a62.png)

除了SceneColor，延迟渲染下我们还可以拿到其他G-Buffer信息，所以可以修改这些信息，然后混合回SceneColor；

(PS: 这里用到“混合回”的描述是因为这是类似后期效果，可以理解为对已有背景信息的滤镜处理。并不能真正改变渲染在BasePass时的信息，如果需要更新Gbuffer本身可以通过之后提到的Deferred Decal材质来实现)

利用采样Ambient Occlusion加强或弱化对象的AO效果（通过对AO处理后叠回SceneColor）

![pic14.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic14-464x506-62d9c64d2618c164f993c799d2a9b20fcee5ed6e.png)
![pic15.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic15-483x548-5429c66adb4e6b6c2139e0412f732466b2720a73.png)
![pic16.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic16-877x477-ab26a122e4638a3d22cd5c0386d5504f44233c36.png)

利用SceneColor和BaseColor，对对象去色/或降低和提升饱和度

PS: 这里的透明模型为了减少OverDraw的开销，尽量减少透明的区域，因此使用了包裹对象更加紧凑的模型替代了球体。（这个模型可以利用引擎内生成的Simple Collision凸物体)

![pic17.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic17-534x541-0b280997050a4da61544f30c92b30ee09fecd401.png)
![pic18.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic18-1144x380-9b1157e00f64264eddcf34e79d358d7ecf4db97e.png)

利用Worldposition（世界空间像素位置）：不同于可以直接拿到背景的G-Buffer信息，透明材质无法直接在SceneTexture中选择拿到背景的WorldPosition，需要做一些计算。

我们叫它透明物体后场景的世界位置（Worldpostion Behind Translucency）：计算方式为从摄像机的位置为起点朝摄像机和材质像素连接方向延申到场景深度，然后把它作为一个材质函数复用之

![pic19.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic19-859x454-0b4ba490c0d0dc2529de39cf70719525f2f4b111.png)

利用它计算出和透明体Pivot的距离而生成一个从透明体中心到边缘的黑白球形遮罩；

![pic20.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic20-266x259-ed38cc1d2f948e3e056ec58a407d7e561814c00a.png)
![pic21_1.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic21_1-676x263-592fa9145880a7cb87c7ec61d9e36c509c670c69.png)

利用控制深度的容差产生沟边，相较于全屏后期处理，好处是基于Actor世界空间位置，区域可控

![pic22.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic22-306x275-0f66fca6299f0404f3db5cd779737f9935b69bfa.png)

结合可以做一些基于物体世界位置的后期效果；比如3D空间中选择目标区域的高亮绘制。

(PS: 以下的效果可以在角色身上利用Sphere Mask节点并结合Tick手部位置的传入信息来实现；但使用一个额外的透明球体实现自由高效的多)

![pic23.gif](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic23-b8574a8d76272f395e384914186d5ffcd4763580.gif)

如果把法线也考虑进来，得到屏蔽掉法线背向球心遮罩；两者结合改变背景颜色和亮度，模拟非投影点光效果

![pic24.gif](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic24-d5e36aaa2b0ffe5a9fa6ac6e7353ae5108f20790.gif)
![pic25.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic25-1600x701-6071758422e92c6b6ca8b635e8145c4ebb4db6aa.png)

通常透明材质贴图（前景贴图）UV来自于模型本身UV，因为透明材质可以取到背景信息的特性，可以利用背景的信息来改变其UV，比如利用上面提到的背景WorldPosition

利用它的X,Y作为前景贴图的UV，来实现模拟从上而下类似Decal的投影，比如可以用来模拟假阴影；也可以应用到特效中Mesh上产生投射效果（包括下面说到3轴的投射），作为目前特效无法生成Decal的备选方法

![pic26.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic26-700x594-889abb66bd1a112d0d67760fc7901e2113090e3c.png)
![pic27.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic27-1203x607-609490d43ee2118a8e81b35acd3829e036f8bccf.png)

利用它的 X,Y,Z作为前景贴图UV来实现类似BOX UVmapping的世界空间3轴投射，叠加到背景目标体上效果，改变目标体贴图

![pic28.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic28-701x446-72c9e1620c83df9cd96b091867191900fe4ac8f7.png)
![pic29.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic29-1180x636-4287614e736a7771ea7903e47e56174dcd339eea.png)

除了World Position作为背景UV，有时希望获取背景目标Tangent Space的UV坐标，作为前景贴图的UV，做一些特效，比如替换贴图。

![pic30.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic30-635x640-e7a871eb8c8123860a7e1d3a95e97b06993b621e.png)

综上实践可以应用到我们经常需要的角色材质技能特效的实现，避免把效果都写入角色材质中增加复杂度和维护成本，这些特效材质还可以被重复利用到不同角色身上

以下使用了Decal 透明材质结合角色Custom Depth作为蒙版为角色增加各种特效

![pic31.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic31-1600x266-daee4317d6d2cc977ab4dce8be952384bc190e70.png)

谈起叠加投射到背景上的效果自然想到Deferred Decal材质；它必须是透明的混合模式，它和普通的透明和非透明材质有什么区别呢？

- 普通透明材质仅能拿到Gbuffer信息，但无法写入；因此我们能做的是对这些信息做一些处理后画回SceneColor上。但Deferred Decal可以更新Gbuffer（无Depth）,这提供了计算灯光前让我们“改变材质属性”的机会。直观的应用是单独或者同时写入BaseColor，Normal, Roughness等等；
   Decal材质还能采样到部分buffer信息，比如  WorldNormal, AO, SceneDepth, CustomDepth,  CustomStencil，提供进一步应用想象空间。但它并没有像普通透明材质能看到的背景信息类型那么多（比如无法取到SceneColor）
   
- 非透明材质当然也直接了地写入Gbuffer（有Depth）；Deferred  Decal的透明材质没有Depth，这个特性决定了Decal是叠加绘制到背景上，非透明材质是直接绘制在当前几何体表面上。另外非透明材质无法单独写入个别材质属性到Gbuffer，而是全部。比如无法单独写入BaseColor而不画其Normal和Roughness。从这点上看如果希望使用Decal完全改变背景的所有材质属性，直接用非透明材质即可，效果类似并高效。
  
   概念的理解有利于增加应用想象空间的自由度：就如同上面角色的特效叠加，效果虽然也是可以直接写在角色本身材质里，但分开作为Mesh  Decal的好处除了上面提到的易于维护和减少复杂度外，分开的Mesh还可以有各种动画，变形等，有不少本身复杂材质很难实现的区域效果变化；比如角色的皱纹添加和变形（更新 normal+顶点动画）；熨斗烫平褶皱(更新  normal+MeshDecal平移动画)；一片有形状区域干湿的变化，这也许跨越了多个物体的多个材质，或者一个材质的部分区域（更新Roughness和BaseColor）
   ![wetness.gif](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_wetness-68948b8d1ec733ad124ffb447bc6f27ae7104949.gif)

继续往下实践其他背景信息：利用场景深度(SceneDepth)模拟区域雾效：比如我们大概来实现一下以下的需求

1. 雾的颜色需要远近可控；
2. 雾的浓度衰减方式需要随距离可控；
3. 雾的颜色和衰减在垂直距离上也需要同样的控制自由度；
4. 在不同朝向（逆光/顺光）需要有不同的颜色，并可控强度；
5. 可排除个别物体受雾影响

![pic32.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic32-830x349-ddcc00e66325f3fe13f7ebf3b3c4cf10b984d239.png)

Curve的RGB定义了远近颜色变化；A定义了远近浓度变化

![pic33.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic33-860x388-75ff9ad9d134ceb0ea44b7f7eb8b5ce06622ca50.png)

高度雾的控制需要考虑雾本身绘制到物体表面的高度以及摄像机高度对于雾可见度的影响

这里我们又用到了WorldPositionBehindTranslucency的材质函数

![pic34.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic34-909x573-d0f6b368edcdeff22f74df5bf1f67f0a2e8f0204.png)

这里我们还可以加太阳和天空对于雾的影响，甚至可以采样天空cube的低mip的贴图来增加色彩变化

![pic35.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic35-856x544-55df7a2d1740db006c774389ded5e7a6db07367d.png)

选择性排除不需要被雾影响的物件。需要接入Opacity通道

![pic36.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic36-846x532-925670c8593c8a6ec7e6cff86b281c6012f439a4.png)![pic37.gif](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic37-ffdbc6de1b455dc1723e813cd9e25ffc8d51a042.gif)

这个例子主要是想说明SceneDepth和WorldPosition在透明材质里被采样后的一种应用；当然这个作为全局雾效在后期材质里做可能更方便；但是透明物体具有区域可控的便利性；比如水体，洞穴等。

像洞穴这种类似Portal从一个空间到另一个空间的过度区域也是经常用到这种区域雾；相对于在雾中的效果，这提供了从外部看一个起雾区域的效果

深度的采样在表现水体真实性作用很大；比如随着深度增加水的颜色和透明变化，水底景物折射偏移程度，深度比较后（Pixel Depth和SceneDepth）产生交界处的渐变遮罩，这个遮罩可以用来做半透的融合，岸边的水泡区域。关于“体”的概念后文有更进一步的描述。

我们大概聊了不少应用Unlit Translucency 半透特性的实践，透明材质应用在模型表面可以有区域性后期效果，加上材质物件的顶点，骨骼动画，或作为粒子发射，或物理模拟等可以带来很多后期无法实现的动态效果及灵活自由度

1. Lit Translucency（受光透明材质）：光影及明暗和普通Surface材质很不一样；
    相对于CG中使用三角面Surface来表现实体不同，现实中透明物体可以看到物体内部，其实是一个“体”的概念。光影的变化是基于体积（或者厚度）的一个积累后的结果。比如透明度的变化，亮度，阴影的浓度，折射对光线的扭曲程度都直接和其“体”量有关。比如我们平时看到的水池就是个体，玻璃也是体，云雾也是体。
    需要注意的是，物理属性上讲利用透明材质表现头发，树叶这种镂空效果其实不属于透明材质本质特性的应用，而是为了减少顶点数利用了透明材质可部分透明的特性罢了，是很“游戏”的一种应用方式。
    对于Lit Translucency的材质的创建或模拟用“体”的思维方式我觉得更接近真实；这里我想分两部分来聊一下：

- UE4中Lit Translucency是如何处理光影
   谈这个的原因是这部分和Surface的处理很不同，为了平衡效率和效果，比较复杂多样，因此也引起不少疑惑以及问题。分光照和阴影两部分
   光照方面透明材质有几个特定的灯光模式可以选择。其中除了Surface ForwardShaing外，这些光照计算结果需要基于Volume Texture，在一个3D空间中积累明度；Volume Texture精度有限，受光和阴影品质也受到限制。

  ![pic38.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic38-327x111-f68ac93be71eb2dbd3b6e7b56b27a57b5f5b5a20.png)

  透明材质阴影比较多样，根据使用不同类型灯光，阴影投射对象的材质属性，阴影接受对象的材质属性，是否自阴影等因素，阴影的表现方式部分利用到上面提到的Volume Texture，部分使用了FOM（Fourier Opacity Map），部分是利用Shadow Depth  Map，部分就使用Lightmap；另外目前有些在实践中并不工作(bug)；因此难以定位问题或者利用好，这里总结了一个图表，描述了各种情况下阴影的方式，希望对更清晰地理解和定位问题有帮助
   从左到右：灯光类型-投射阴影物体类型-阴影方式-接受阴影物体类型；下载[Xmind](https://www.weiyun.com/disk/folder/cbfe2da8f822fe2abda6d17936e7e2f0)文件可查看细节

![pic39.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic39-1600x1041-0064ea6c528ad414ed8d16370412ead06617ef0e.png)

- 然后以玻璃为例谈下以“体”的思路模拟表现受光透明材质

![pic40_1.jpg](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic40_1-1375x453-f50a57ba01225f8730087ddeb3c05029bdb08306.jpg)

 

- 透明度随着厚度变化：厚度决定背景光线穿过材质到达摄像机的距离，距离决定被吸的光量，穿透光量决定透明度；因此越薄吸收越少就越透明，反之越不透明；
- 固有色随着厚度变化：我们看到的颜色更多的是光线穿越材质后被吸收掉某种波长的光谱而产生的颜色，材质在视野角度越厚，吸收越多，颜色越浓，也越暗；
- 折射随着厚度变化：现实中背景被折射偏移的程度除了材质本身折射率属性还取决于厚度，即光线在此材质中经过的距离，距离越大出材质后产生的偏移越大。由于玻璃球中间和边缘厚度变化，导致折射产生的光线偏移不均匀，景象产生弯曲；同样是透明球体肥皂泡几乎没有厚度所以基本无折射

实现上首先为了更好的表现高光和反射选择Surface Forward Shading的光照模式

- 玻璃透明度随着Opacity的减小，高光和反射同时也被消弱，接近0时，高光和反射基本消失，这并不是我们想要的。为了保持高光反射强度，我们通过文章最开始提到的通过控制前景来控制背景，即不连接Opacity，而采样SceneColor作为前景
- 玻璃颜色来自于光线某些波长的被吸收，因此并非BaseColor（Surface上的漫射颜色），所以通过设置BaseColor=0基本放弃了漫射，同时通过取 SceneColor乘上颜色连接到自发光通道的方式来染色，颜色需要根据厚度有变化。
- 玻璃折射，因为需要用到取背景SceneColor通过自发光来染色，因此这里放弃了材质本身的Refraction通道，而是通过偏移SceneColor的UV来模拟；同样折射的程度与厚度相关。下图A和B为不同厚度的同一材质光线出入其中后产生的偏差；可以看到介质越厚，光线被偏移的距离越大

![pic43.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic43-539x196-f2302d019a7370f941c7624eacc48c3132299d12.png)

因此要表现比较真实的折射效果我们需要在材质里定义对象的厚度，这个厚度为从摄像机角度看过去的厚度，因此非固定贴图可以表现；对于球形对象我们可以利用Fresnel节点，或者DOT模型法线和Camera Vector的结果作为灰度蒙版来变化折射率（这里是UV的偏移程度）

以下是没有定义厚度作为折射率蒙版（第一幅），以及不同灰度变化定义厚度作为折射率蒙版指定给一个球体模型后产生的结果；模拟现实中不同类型镜片

![pic44.png](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic44-1600x800-484ef68dcb646a3b41d43dcccdd337d572f8366b.png)

但对于非球体Fresnel的信息无法正确表达厚度，需要想办法来创造它。一个实体的厚度是光线进实体和出实体的距离，即前后表面的深度差，这可以利用当前表面的Pixel Depth和法线反转模型的CustomDepth求差得出

具体做法是把两个相同模型叠套在一起，一个法线正常用于绘制，一个法线反转用于产生深度。反转法线模型开启Custom Depth，赋予一透明材质，并打开Allow Custom Depth Writes, Opacity  0不被绘制，需要注意的是设置Opacity Mask Clip Value也为0，确保其透明度为0时也会绘制Custom depth。

法线正常的面是需要被绘制的玻璃，材质中需要采样到反转法线面的Custom depth信息，计算模拟模型在不同视角的厚度；此厚度作为Alpha权重使得不同厚度的地方有不同的固有色和折射

 

![pic45.gif](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic45-e3ed5c69aaea578b6182ecc77df5297924061fbd.gif)

应用到模型上最终效果可以看到颜色，透明度及折射（这里可能不是特别明显）随着厚度的变化；同时保持住了足够的高光和反射

（PS: 4.25版本中将增加专门的Thin Transparency Shading 模型来实现染色玻璃材质；基于PBR提供了很好的高光反射保持以及表现滤色的功能，但厚度仍需额外营造。）

![pic46.jpg](Transllate_Unreal.assets/Unreal Engine_EGC_Blog_transparent-material-in-UE4_pic46-1600x961-bfe97ed46c55483db2a78f9581808e5758532853.jpg)

总结：

- 透明材质没有深度，由此会产生问题，但也可巧妙利用
- 透明材质本质特性是可以半透明，镂空效果并不是透明材质本质特性的最好应用
- 透明材质最终效果取决于三方面：控制前景，控制背景可见性（Opacity），混合方式(Blend Mode)
- 采样SceneColor作为前景的方式提供了对Opacity，Blend Mode的模拟；自由度和效率在不同情况各有变化
- 我们可以通过采样背景的各种信息实现很多区域性的后期效果；并有着后期材质无法比拟的灵活性，应用想象空间丰富
- 透明材质的动态光影有局限性，需要精细应对。推荐最低限度地使用高级灯光模型和投射阴影
- 用“体”的思维去考虑创建受光的透明材质

 