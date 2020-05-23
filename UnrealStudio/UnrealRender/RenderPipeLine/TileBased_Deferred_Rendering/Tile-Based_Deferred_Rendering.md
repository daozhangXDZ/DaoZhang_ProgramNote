#  [Tile-Based Deferred Rendering(TBDR)](http://link.zhihu.com/?target=http%3A//blog.imgtec.com/powervr/a-look-at-the-powervr-graphics-architecture-tile-based-rendering) 

目前所有的移动设备都使用的是 [Tile-Based Deferred Rendering(TBDR)](http://link.zhihu.com/?target=http%3A//blog.imgtec.com/powervr/a-look-at-the-powervr-graphics-architecture-tile-based-rendering) 的渲染架构。TBDR  的基本流程是这样的，当提交渲染命令的时候，GPU 不会立刻进行渲染，而是一帧内所有的渲染命令积攒起来，最后统一渲染。在渲染到  FrameBuffer 的时候，也不是依次执行所有的命令将 Fragment 结果填充到 FrameBuffer 中。而是在 GPU  内部有着叫做 Tile 的高速渲染器，这些 Tiles 虚拟的将 FrameBuffer 分割成小块（光栅化后得到很多  Fragment，很容易就能决定 Fragment 所在的 Tile），每次执行一小块中的所有渲染命令，完成后将结果写回  FrameBuffer。这些 Tile 一般会在 32x32 像素的大小，当然根据设计的不同而各部相同。Tile 的数量一般不足以完全平铺整个  FrameBuffer，一次只能覆盖一部分 FrameBuffer 的区域，所以每帧内同一个 Tile 会执行多次渲染操作。 

TBDR  的渲染架构带来了一个非常大的好处，就是 Hidden Surface Removal。当 vertex shader  执行完成后，通过插值得到很多 fragment，这个之后每个 fargment  的深度值就已经知道了，那么就可以利用这个深度值将最终不会渲染到屏幕（被其它 fragment 遮挡）的 fragment 剔除，减少了很多  fragment shader 计算量，提高了填充率。注意，这个只对非透明的物体有效，如果是 AlphaTest（shader 中表面为使用了  clip 或者 discard） 或者 Transparent（Alpha 不是 1），是没有 Hidden Surface Removal  效果的。因为很简单，透明的 fragment 无法遮挡住后面 fragment。也就是说并不是 AlphaTest 和 Blend  本身是大消耗操作，而是因为破坏了 Hidden Surface Removal。 

在  TBDR 的渲染架构下还有很重要的一点需要注意。立即渲染模式下，有一个技巧是，当每一帧都不去清屏的时候是可以提高效率的，因为 clear  操作需要将值写入 FramBuffer 中的每一个像素中，这是需要花费一定时间的。而这个技巧在 TBDR  中是行不通的，反而会起到反效果。这是因为，如果你没有调用 clear 操作，表示你认为上一帧的内容是不能丢弃的，所以在渲染 tile  的时候，硬件会将 FrameBuffer 中数据先写入  Tile，然后再执行渲染，这个写入操作无形中增加了很多的负担，有可能就会严重影响到程序的执行效率。 

下面是几个很好的参考资料： 

[OpenGLInsights-TileBasedArchitectures.pdf](http://link.zhihu.com/?target=http%3A//www.seas.upenn.edu/~pcozzi/OpenGLInsights/OpenGLInsights-TileBasedArchitectures.pdf) 

[Tuning Your OpenGL ES App](http://link.zhihu.com/?target=https%3A//developer.apple.com/library/tvos/documentation/3DDrawing/Conceptual/OpenGLES_ProgrammingGuide/Performance/Performance.html) 

 

来自 <https://zhuanlan.zhihu.com/p/26279464>  

 