## [*SSAO*](https://zhuanlan.zhihu.com/p/47117138)

一、

环境光被用来模拟散射。在现实中光线会以任意方向散射，所以它的强度受遮挡时是应该会有变化的。间接的光模拟叫做环境光遮蔽（Ambient Occlusion）。

基于ray-tracing的积分计算P点射线有多少被遮挡多少无遮挡。

![img](SSAO_PrintCiple_2.assets/v2-7e67405f89f64b3b8b2b8533fa8dc573_1440w.jpg)

二、SSAO方案:

1， 弄个半球区域，在半球内随机采样一系列点；再创建一个很小的随机噪声纹理平铺于屏幕上来对半球内的采样点做随机旋转。

![img](SSAO_PrintCiple_2.assets/v2-77435c94e7b1caa1aaad4d980186db1a_1440w.jpg)



通过随机采样点和对采样点的微旋转得到一个P点周边的随机点Q，比较P和点集Q的深度值来得到P点的遮蔽因子。

![img](SSAO_PrintCiple_2.assets/v2-25c13cc4dbcc24596cdab88aa37bc7ee_1440w.jpg)

上图FragColor是一个float，就是我要的遮蔽因子。使其直接乘以正常光照的环境光强度参数即可。

```text
    float AmbientOcclusion = texture(ssao, TexCoords).r;
    vec3 ambient = vec3(0.3 * Diffuse * AmbientOcclusion);
```



2，整体流程：

g_buffer获取位置、法线、颜色；

噪音纹理对随机采样点做随机旋转，配合g_buffer的位置、法线得到ssao纹理；

对ssao纹理做模糊处理，使阴影模糊。

再基于后置渲染加ssao纹理一起渲染到屏幕上。

![img](SSAO_PrintCiple_2.assets/v2-e724912f7bf442ae027d891d2d668597_1440w.jpg)

![img](SSAO_PrintCiple_2.assets/v2-5732cf08e7e01b092debc9f14e41c6de_1440w.jpg)

```cpp
TexParameteri position(GL_RGB16F, GL_RGB, GL_FLOAT, GL_NEAREST, GL_NEAREST, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE);
TexParameteri normal(GL_RGB16F, GL_RGB, GL_FLOAT, GL_NEAREST, GL_NEAREST, 0, 0);
TexParameteri albedos(GL_RGB16F, GL_RGB, GL_FLOAT, GL_NEAREST, GL_NEAREST, 0, 0);

TexParameteri ssao(GL_R16F, GL_RED, GL_FLOAT, GL_NEAREST , GL_NEAREST, 0, 0);
//TexParameteri 是我megranate_render里面一个便于glTexImage2D的类。
```

三、结果：

![img](SSAO_PrintCiple_2.assets/v2-751fb6f880fb5efa5f4495d47b480525_1440w.jpg)