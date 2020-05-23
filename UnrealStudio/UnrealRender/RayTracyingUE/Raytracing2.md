# 虚幻4渲染编程（光线追踪篇）【第二卷：一天入门光线追踪】



我的专栏目录：

小IVan：专题概述及目录

zhuanlan.zhihu.com![图标](Ray tracing 2.assets/v2-adfc32ab6d1929ce6ebb6863da9e0f0f_180x120.jpg)

光线追踪和光栅比起来有很多天生优势，实时光线追踪也是游戏未来发展的大方向。这一节将会实现“Ray  Tracing in a Weekend”的内容，不过与“Ray Tracing in a  Weekend”不同的是，我们将会在虚幻4中实现它，并且使用GPU来加速计算。

在开始本系列之前，如果没有光线追踪基础建议先阅读Ray Tracing in a weekend，Two Weekend 和last life

Ray Tracing in One Weekend (Ray Tracing Minibooks Book 1) eBook: Peter Shirley: Kindle Store

www.amazon.com![图标](https://pic2.zhimg.com/v2-543dc965cffa2a715cb9e0f0c39c7ec1_ipico.jpg)

这三本书。

------

## **【1】在Unreal中使用GPU做光线追踪的环境搭建**

我们还是使用插件的形式来搭建我们的代码，虚幻的插件和unity的有本质不同，虚幻的插件其实是一个新的模块。

我们新建一个名为RayTracing的插件，然后在插件里新建一个RayTracing.usf和一个RayRender.h，一个RayRender.cpp



![img](Raytracing2.assets/v2-fe279cfcab53f31a6300811d4d796092_hd.jpg)

对RayTracing.build.cs做如下修改



![img](Raytracing2.assets/v2-19d0cdd6a427f149da4863a86190a4e8_hd.jpg)

对RayTracing.uplugin做如下修改：



![img](Raytracing2.assets/v2-c730a3c5b417204672e7beebc589a2ba_hd.jpg)

然后在RayRender.h文件中，敲入如下代码



![img](Raytracing2.assets/v2-f2b20ff176cbc7347ceca21c3ff070e6_hd.jpg)

在RayRender.cpp中实现MainRayRender



![img](Raytracing2.assets/v2-a6950670302938813dba09698de5ea70_hd.jpg)

然后在RayTracing.usf中敲入如下代码



![img](Raytracing2.assets/v2-8b77885afc4919c03924136361cc8b8f_hd.jpg)

然后新建一个场景，做一个BP派生自RayRender



![img](Raytracing2.assets/v2-b830e7078303576bd19fc3d541610355_hd.jpg)

然后把它拖进去，在BP_RayRender中做如下设置



![img](Raytracing2.assets/v2-d804c1d4ed0650cd43fb2ae10b3a5a9f_hd.jpg)

OK现在完成了最基本的环境搭建。

------

## **【2】加入ComputeShader**

在RayRender.cpp中我们要建一个ComputeShader。这个CS将负责RayTracing的大部分计算。代码如下：



![img](Raytracing2.assets/v2-1f3d265e4c7d2557d6551f4e059a05b9_hd.jpg)

------

## **【3】使用ComputeShader来输出计算结果**

在MainRayRender函数前面我们增加一个函数



![img](Raytracing2.assets/v2-6a9754d72d064bbcafbaefb71b82514b_hd.jpg)

这个函数负责被逻辑线程的MainRayRender函数调用，然后它负责在渲染线程控制CS，在这个函数的末尾有个SaveArrayToTexture函数，我们需要在RayTracing_RenderThread前实现它。如下图所示：



![img](Raytracing2.assets/v2-11616f56ec29b0d0e4732523925f1f44_hd.jpg)

最后是我们的MainRayRender函数的实现。



![img](Raytracing2.assets/v2-d92c841803de479d78015a729e890616_hd.jpg)

然后在编辑器启动游戏点下R键之后，你将会在项目的Save目录下看到CS计算的结果



![img](Raytracing2.assets/v2-8133c20111138e3fd8e0bb5f0d84cf05_hd.jpg)

------

## **【4】在ComputeShader中加入RayTracing的逻辑完成天空的绘制**

使用CS的时候需要注意的是，uv的v方向是向下的



![img](Raytracing2.assets/v2-802743530f94688717cd7dea3e168e31_hd.jpg)

再改一下输出图片的分辨率（为了好看）

然后我们继续在RayTracing.usf敲入如下代码：



![img](Raytracing2.assets/v2-57857629fb5697eb5dd36e6535dce964_hd.jpg)

首先我们定义了一个光线的结构体，并且为这个结构体配套了一个point_at_paramerter的函数。然后定义了一个渲染场景的函数，最后在MainCS里定义了我们的摄像机。



![img](Raytracing2.assets/v2-d9c3a503a2ac8483af0183ae870f6368_hd.jpg)

在编辑器中运行点R键，你将会在项目的Save目录的ScreenShot里找到输出结果



![img](Raytracing2.assets/v2-39b3c6ea91e5a3a8229a882c1058e84a_hd.jpg)

------

## **【5】向RayTracing中加入一个球体**

我们先来使用数学方法建一个球体要判断光线是否与球相交，只需要判断射线方程和球面方程是否有交点即可



![img](Raytracing2.assets/v2-4bfa27c811c22bb78309a37ed7b154cb_hd.jpg)

（电脑上写的字巨丑，见谅）

所以我们定义一个hit_sphere函数如下



![img](Raytracing2.assets/v2-89cfa6ad3834600f6ca0bd93202f1f7b_hd.jpg)

我们的RenderSceneColor也要做相应变化，如果光线打到了球面上，则绘制红色。然后我们就可以得到如下的图：



![img](Raytracing2.assets/v2-509d39acdb7637bf9374bd33f480e414_hd.jpg)

------

## **【6】计算表面法线**

因为表面是球形的，所以法线就是球星到光线和表面的相交点方向的向量



![img](Raytracing2.assets/v2-a1d17db44287c877eb5e5f330d7a896b_hd.jpg)



![img](Raytracing2.assets/v2-81df3855cded00a2b8462abfcca2a75d_hd.jpg)



![img](Raytracing2.assets/v2-7e315a629c236f2d67e190933cb6bd68_hd.jpg)

------

## **【7】多物体计算**



![img](Raytracing2.assets/v2-697e36c2a251d88c26bf620630db8ad5_hd.jpg)

如果想得到一个场景肯定不可能只绘制一个东西，这时候我们需要绘制多个物体。这时候我们就需要在Shader里维护一个绘制列表。同时为了更方便绘制，我把摄像机的坐标系重新调整了一下。



![img](Raytracing2.assets/v2-418d37a7b213d74758b70f7c0692c72b_hd.jpg)

先定义一个结构体用来储存光追的结果



![img](Raytracing2.assets/v2-39fa95fff32072fd41d0554840c4b545_hd.jpg)

然后定义物体结构体和物体绘制列表结构

```abap
struct hitable_Sphere
{
    float3 center;
    float radius;
	void InitHitableObject(float3 centerlocation, float radiusvalue)
    {
        center = centerlocation;
        radius = radiusvalue;
    }
    bool hit(in Ray r, in float t_min, float t_max, out hit_record rec)
    {
        float3 oc = r.origin - center;
        float a = dot(r.direction, r.direction);
        float b = 2 * dot(oc, r.direction);
        float c = dot(oc, oc) - radius * radius;
        float discrimninant = b * b - 4 * a * c;
	
        if (discrimninant >= 0)
        {
            float temp = (-b - sqrt(discrimninant)) / (2.0f * a);
            if (temp < t_max && temp > t_min)
            {
                rec.t = temp;
                rec.p = r.point_at_paramerter(rec.t);
                rec.normal = (rec.p - center) / radius;
                return true;
            }
            temp = (-b + sqrt(discrimninant)) / (2.0f * a);
            if (temp < t_max && temp > t_min)
            {
                rec.t = temp;
                rec.p = r.point_at_paramerter(rec.t);
                rec.normal = (rec.p - center) / radius;
                return true;
            }
        }
        return false;
    }
};

struct hitablelist
{
    hitable_Sphere Sphere_001;
    hitable_Sphere Sphere_002;

    bool hit(in Ray rayline, in float t_min, in float t_max, out hit_record rec)
    {
        hit_record temp_rec;
        bool hit_anything = false;
        float closest_so_far = t_max;
		
        Sphere_001.InitHitableObject(float3(0, -1.0f, 0), 0.5f);
        if (Sphere_001.hit(rayline, t_min, closest_so_far, temp_rec))
        {
            hit_anything = true;
            closest_so_far = temp_rec.t;
            rec = temp_rec;
        }
		
        Sphere_002.InitHitableObject(float3(0, -1.0f, 20.5f), 20.0f);
        if (Sphere_002.hit(rayline, t_min, closest_so_far, temp_rec))
        {
            hit_anything = true;
            closest_so_far = temp_rec.t;
            rec = temp_rec;
        }

        return hit_anything;
    }
};
```

最后是我们的场景渲染函数和MainCS



![img](Raytracing2.assets/v2-3de051b70c43ca92b0f2b8ec0be5ffa6_hd.jpg)

------

## **【8】抗锯齿**

可以看到我们渲染出来的图锯齿还是很重的



![img](Raytracing2.assets/v2-9273a760cf3e0d52850eca176b2d3a44_hd.jpg)

我们可以对这个地方进行超采样来缓解。首先把Camera的逻辑封装一下



![img](Raytracing2.assets/v2-3025c260edcf5cc9f4c0cb21be9bb7da_hd.jpg)

主函数也需要做相应修改



![img](Raytracing2.assets/v2-86900c4d0aa499693126993500a47c0c_hd.jpg)

于是最后我们得到了平滑的图像



![img](Raytracing2.assets/v2-204c6242b8d5d33c1d479ecc64c4ed2b_hd.jpg)

这里我采样了2048次（其实不用这么多次），对于GPU来说小Case啦。我1060的垃圾卡都能瞬间做完运算并输出图片。

------

## **【9】DiffuseLighting**

我们有了法线就能做Lighting啦。

我们可以假设一种非常简单的光照模型，光打到一个物体上，一部分能量被吸收，一部分能量反弹，我们对每条光线做迭代即可



![img](Raytracing2.assets/v2-e722963655cbf4926155fee00d846f99_hd.jpg)



![img](Raytracing2.assets/v2-1f4db28496e4dc8c6badc92a2e01d51c_hd.jpg)

最后可以得到的输出结果



![img](Raytracing2.assets/v2-f76af13c5bf53b8af931122245c38fba_hd.jpg)

可以看到我们不需要可以渲染AO影子什么的，这些东西自己就有了。影子噪点非常多我们还需要对其进行降噪处理。

修改下Hit的最小距离，将其修改为0.001



![img](Raytracing2.assets/v2-6807f0e087996f94251c63a4d854d3f8_hd.jpg)

于是奇怪的bug纹就消失了



![img](Raytracing2.assets/v2-5dd35c71f6ff8d0fb2721a6488c6b62f_hd.jpg)



![img](Raytracing2.assets/v2-5686e8b717a9a4dde9d07be19f6104e6_hd.jpg)

------

先暂时写到这里吧，后面的全反射和折射，透射什么的有时间再写。

Enjoy it。
