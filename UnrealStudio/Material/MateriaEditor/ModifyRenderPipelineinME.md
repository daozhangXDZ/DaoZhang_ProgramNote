# 虚幻4渲染编程(材质编辑器篇)【第七卷：Modify RenderPipeline in ME】



## **My blog directory**

小IVan：专题概述及目录

zhuanlan.zhihu.com![图标](Modify RenderPipeline in ME.assets/v2-adfc32ab6d1929ce6ebb6863da9e0f0f_180x120.jpg)

## **Introduce：**

As  we all know, we can't modify the main render pipeline of unreal engine  4。We can only edit our shader in the material editor. If we want to do  something special which material editor can't meet our needs, Using c++  to modify the engine is currently the only viable method. My previous  article has detailed implementation steps for this method.

[小IVan：虚幻4渲染编程(材质编辑器篇)【第二卷：自定义光照模型】](https://zhuanlan.zhihu.com/p/36840778)

However,  Using c++ to modify the engine is not a good way. Because This method  is very inconvenient. Below I will introduce a way to modify the  rendering pipeline directly in the material editor.

------

Let's see the results first.



![img](ModifyRenderPipelineinME.assets/v2-8ad070d8aeb7ff0693cf469a3f3f87ab_hd.jpg)



![img](ModifyRenderPipelineinME.assets/v2-921e1006ee368b2ecb98517abc3cc6b2_hd.jpg)

The  code shown above is relatively simple, but the goal of modifying the  rendering pipeline directly in the material editor has been achieved.

First we need to modify the source code of CustomNode。



![img](ModifyRenderPipelineinME.assets/v2-bc2cba798f82beec59095031b48044af_hd.jpg)



![img](ModifyRenderPipelineinME.assets/v2-53ba1cf41d8dac3c3f883fd4e35e52fc_hd.jpg)

Compile the engine, then open the material editor to add a CustomNode and you will see the following result.



![img](ModifyRenderPipelineinME.assets/v2-6be58a948a17cd882ae3cc55f17a3cde_hd.jpg)

If you write a macro to def, the macro will be pushed into the shader, and the rendering pipeline will get the macros.



![img](ModifyRenderPipelineinME.assets/v2-6805e6df9c555cd8cd80d2ca13dbf9a7_hd.jpg)

Then we can write our code into the  engine shader, which can be easily enabled using the material editor.



![img](ModifyRenderPipelineinME.assets/v2-4e6e10bfbd5213a21bb3fd728cbe9498_hd.jpg)

Enjoy it ！
