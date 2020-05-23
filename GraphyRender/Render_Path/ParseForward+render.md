# Forward框架的逆袭：解析Forward+渲染

​                                                   2015年10月20日 09:35:29           [pizi0475](https://me.csdn.net/pizi0475)           阅读数：2148                   

​                   

转载请注明出处为[KlayGE游戏引擎](http://www.klayge.org/)，本文地址为[http://www.klayge.org/2012/04/21/forward%e6%a1%86%e6%9e%b6%e7%9a%84%e9%80%86%e8%a2%ad%ef%bc%9a%e8%a7%a3%e6%9e%90forward%e6%b8%b2%e6%9f%93/](http://www.klayge.org/2012/04/21/forward%E6%A1%86%E6%9E%B6%E7%9A%84%E9%80%86%E8%A2%AD%EF%BC%9A%E8%A7%A3%E6%9E%90forward%E6%B8%B2%E6%9F%93/) 

AMD在7900系列显卡发布的时候同时推出了[Leo demo](http://developer.amd.com/samples/demos/pages/AMDRadeonHD7900SeriesGraphicsReal-TimeDemos.aspx)， 并说明它不是用近年流行的Deferred框架渲染完成，而是用到了一种叫Forward+的框架。这个框架不需要Deferred的大带宽要求，却仍能 实时渲染上千光源。EG2012上有篇新paper叫做Forward+:  Bringing Deferred Lighting to the Next Level，讲述的就是这个方法。但目前作者还没有放出该论文的全文，这里我只能通过只言片语和AMD的文档来解析这个神奇的Forward+。

## Tiled-based Deferred Shading

在进入正题之前，我们先回顾一下Intel在SIGGRAPH Courses 2010里提到的[Tiled-based Deferred Shading](http://visual-computing.intel-research.net/art/publications/deferred_rendering/)。它的算法框架是：

1. 生成G-Buffer，这一步和传统deferred shading一样。
2. 把G-Buffer划分成许多16×16的tile，每个tile根据depth得到bounding box。
3. 对于每个tile，把它的bounding box和light求交，得到对这个tile有贡献的light序列。
4. 对于G-Buffer的每个pixel，用它所在tile的light序列累加计算shading。

在原先的deferred框架下，每个light需要画一个light volume，以决定它会影响到哪些pixel（也就是light culling）。而用tiled based的方法，只需要一个pass就可以对所有的光源进行求交。如果用了AMD在[Mecha  demo](http://developer.amd.com/samples/demos/pages/ATIRadeonHD5800SeriesRealTimeDemos.aspx)中用到的OIT方法，还可以做一个per-tile linked list，直接把light序列存在链表里。

## Forward+ Rendering

有了Tiled-based Deferred Shading的基础，理解Forward+就变得简单多了。Forward+  Rendering和Tiled-based Deferred Shading的关系就好比原先的Forward Shading和Deferred  Shading，所以我们可以照猫画虎一次：

1. Z-prepass，很多forward shading都会用这个作为优化，而在forward+中，这个变成了必然步骤。
2. 把Z-Buffer划分成许多16×16的tile，每个tile根据depth得到bounding box。
3. 对于每个tile，把它的bounding box和light求交，得到对这个tile有贡献的light序列。
4. 对于每个物体，在PS中用该pixel所在tile的light序列累加计算shading。

从这里可以看出，前两步与Tiled-based deferred shading大同小异，但只需要Z-Buffer，而不需要很消耗带宽的G-Buffer（[G-Buffer最小也要32bit  color + 32bit depth](http://www.klayge.org/2011/11/28/klayge-4-0%E4%B8%ADdeferred-rendering%E7%9A%84%E6%94%B9%E8%BF%9B%EF%BC%88%E4%BA%8C%EF%BC%89%EF%BC%9A%E6%8B%A5%E6%8C%A4%E7%9A%84g-buffer/)）。第三步是完全一样的。第四部由于用了forward，可以有forward的各种好处：

- 复杂材质
- 支持硬件AA（虽然我一直认为硬件AA多算了很多东西，是一种巨大的浪费）
- 带宽利用率高
- 支持透明物体

由于light已经在步骤3中cache了，所以也可以不像传统的forward那样，把材质和光源搅在一起。加上shader中动态分支的能力，   不难实现类似deferred那样的巨量光源支持。由于带宽省了很多，Forward+的速度能比Deferred快。在原paper里的性能比较足以说  明这个问题。

[![Forward+  VS Deferred](Parse Forward+ render.assets/Forward+VSDeferred.png)](http://www.klayge.org/wp/wp-content/uploads/2012/04/Forward+VSDeferred.png)

另一个有趣的地方是透明物体的渲染。虽然我在KlayGE中用Deep G-Buffer的方法解决了[纯Deferred下透明物体的渲染](http://www.klayge.org/2011/11/29/klayge-4-0%E4%B8%ADdeferred-rendering%E7%9A%84%E6%94%B9%E8%BF%9B%EF%BC%88%E4%B8%89%EF%BC%89%EF%BC%9A%E9%80%8F%E6%98%8E%E7%9A%84%E7%83%A6%E6%81%BC/)。  正如很多读者指出的，这么做所带来的带宽翻倍在很大程度上拖慢了整个系统。在Forward+中，第一步生成Z-prepass的时候，可以采用双Z-  Buffer的办法，一个放不透明物体的Z，另一个放透明物体的Z。在第二步计算tile bounding  box的时候，不管透不透明都放在一起计算一个总的bounding box。后面步骤不变，就能原生支持透明物体。

由于有了Z-Buffer，其他原先对Deferred有利的效果，比如GI、SSR，都可以直接应用。SSAO、SSVO之类的方法，如果需要考虑pixel normal，就需要适当的修改才能应用上。

在AMD的demo中，步骤2和3是用compute shader实现的。而在[Tiled-based Forward Rendering](http://www.pjblewis.com/articles/tile-based-forward-rendering/)这篇blog中，他完全用PS实现了per-tile linked list，但仍然需要D3D11的UAV特性。所以Forward+还没法再D3D11之前的硬件上实现。

## 总结

所谓三十年河东三十年河西，作为Forward框架的新发展，Forward+给我们提供了一个新思路。这样的竞争性发展总比所有资源都投到一方、忽视另一方要好。

从贡献程度来看，最有突破性的其实不是Forward部分，其实是Tiled-based。Forward+只能算作Tiled-based Deferred 
