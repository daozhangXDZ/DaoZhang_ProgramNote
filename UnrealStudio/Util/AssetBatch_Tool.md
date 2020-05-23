虚幻4渲染编程（工具篇）【第三卷：自定义资源及批处理工具】

2018年12月26日 星期三

15:59

 

在各个引擎里其实都会有对资源进行批处理的需求，假设有一千张贴图的设置需要修改，不可能一张一张点开设置吧，效率太低了。我使用过的其它各大引擎都有资源批操作的方式，但是虚幻目前鲜有耳闻，4.20倒是推出了这一特性，但是能力感觉还是很有限。下面就来一起自定义一个我们自己的资源，然后再对它用我们自己写的批处理工具来操作它们吧。

 

首先建一个我们自己的类，UMyCustomAsset



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image001.jpg)

然后再建一个UMyAssetsFactory

h文件



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image002.jpg)

cpp文件



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image004.jpg)

这样我们就能在contentbrower里创建一个我们的MyCustomAsset的资源文件了。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image005.jpg)

 



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image006.jpg)

双击我们自己创建的资源将可以看到



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image007.jpg)

接下来再我们一节的工具的基础上做一下改动，把Buttom点击的回调函数改一下



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image009.jpg)

我们先在contentbrower中选中我们自己创建的资源然后点击按钮，我们这里就可以拿到我们选中的那个资源。通过GetAsset就可以拿到那个选中资源对应的DCO

然后就可以操作资源文件中的数据啦。



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image011.jpg)

然而现在我们改的仅仅是内存中的数据，我们需要把这个数据保存到磁盘的Uasset文件中



![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image013.jpg)

这样我们重启编辑器后，数据就依然是我们修改的值了。

Enjoy it

 

来自 <<https://zhuanlan.zhihu.com/p/44471473>> 
