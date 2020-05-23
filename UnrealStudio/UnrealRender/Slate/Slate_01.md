虚幻4渲染编程（UI篇）【第一卷：Slate框架综述】

2018年12月26日 星期三

15:55

 

Slate概述：

虚幻4有自己的UI框架Slate。引擎的编辑器也是用它写的。当然Slate也可以用来写游戏UI。作为美术我觉得有必要具备写UI的能力，这样就可以顺畅地开发工具和游戏UI效果了，比如要制作3D UI，UI上各种闪动的效果，都需要对UI有全面掌握。

 

首先先把目光投向下图四个模块



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image001.jpg)

这四个模块分别是Slate，SlateCore，SlateRHIRenderer，UMG。Slate和SlateCore共同构筑了逻辑层部分，SlateRHIRenderer则是渲染部分。UMG是在Slate和SlateCore上面的封装层，方便客户端调用，这也是为啥可以不费吹灰之力就能在unreal中用UserWidget开发一套UI的原因。在Unreal中UI就是铺在屏幕表面的面片，也是走顶点像素着色器，甚至还有后期，这和Unreal的SceneRendering的架构差不多。都是逻辑层负责组织资源，然后通知渲染层渲染。

下面就来捋一下整个Slate的渲染 , 我使用的引擎版本是4.20

首先EnginLoop会调用FSlateApplication的DrawWindows，开始了Slate的绘制，注意这里只是逻辑层



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image003.jpg)

然后在PrivateDrawWindows中会初始化一个DrawWindowArgs的东西，它由DrawBuffer和WidgetsToVisualizeUnderCursor等数据组成。在DrawBuffer中存了绘制所需的ElementList。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image005.jpg)

打开SlateDrawBuffer你将会看到：



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image007.jpg)

在开启绘制之前，需要把UI的图元全部压入这个DrawList才行。于是下面会执行DrawWindowAndChild



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image009.jpg)

这里会层层调用，最终会调用到具体一个UI控件的OnPaint函数，这里拿SImage做例子



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image011.jpg)

 



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image013.jpg)

最终会把图元的类型加到List里。具体的顶点和index会在后面的Batcher里真正添加



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image014.jpg)

 



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image016.jpg)

下面是Unreal在batcher中添加图元



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image018.jpg)

 



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image020.jpg)

于是这样就完成了UI数据的搜集。完成搜集之后就可以开始渲染啦，下图的标注2就是渲染部分的开始。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image022.jpg)

既然有要渲染肯定就需要渲染器啊，FSlateRenderer就是渲染Slate的基础渲染器。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image024.jpg)

FSlateRHIRenderer是FSlateRenderer的子类，DrawWindows是Slate渲染的入口



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image026.jpg)

在DrawWindow中会向渲染层发送绘制命令。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image028.jpg)

在DrawWindow_RenderThread中是使用之前准备好的DrawList来绘制。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image030.jpg)

在DrawWindow_RenderThread中完成最终的绘制



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image031.jpg)

在Slate流程清晰后，可以再来看看UMG，随便打开一个UMG的代码可以看到



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image033.jpg)

UMG就是对Slate的一个简单封装。

 

于是现在一切流程清晰后，可以得到如下结论：

【1】如果想新建一个自己的UI类型，直接派生一个SWidget子类然后重载OnPaint，然后再在UMG层建一个与之对应的简单封装即可。

【2】如果想要在UI上做一些花样，比如动态UI，3D UI可以在渲染层的vertexshader或者pixleshader上做文章，可以自己给UI写一些特殊shader。

【3】想要优化UI，也是在渲染层做优化，不过unreal的UI已经自带batch，剔除等优化操作了。

Enjoy it ！

 

来自 <[*https://zhuanlan.zhihu.com/p/45682313*](https://zhuanlan.zhihu.com/p/45682313)> 
