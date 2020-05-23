# 荒野大镖客2云层阴影UE4复现

首先，荒野大镖客2对云层使用的是Exponential Shadow Map技术做的阴影

![img](Cloud%20shadow.assets/v2-f498a23b0763394e232304cf82008c3b_720w.jpg)

Exponential SM是各种制作阴影的技术中的一种，和Convolution SM以及Varaince SM属于一类的shadowmap，统称prefilter shadow  map。这种SM的特点是可以通过对生成的ShadowMap做预处理再应用到画面上从而得到软阴影，但是三种阴影都有漏光的缺点。PCF在十年前因为没有硬件支持，效率低。但是现在不一样了，PCF的过程很适合被做成硬件电路批量执行，现在的效率反而不是问题了，再加上对于PCSS的支持，现在大多数引擎实现的阴影都用普通的级联阴影加PCF滤波了。

ESM具体原理参考：

[Convolution&Exponential shadow map](https://link.zhihu.com/?target=https%3A//blog.csdn.net/toughbro/article/details/6091152)[blog.csdn.net![图标](Cloud%20shadow.assets/v2-6efec82663afd676a552cc0fb46abad3_180x120.jpg)](https://link.zhihu.com/?target=https%3A//blog.csdn.net/toughbro/article/details/6091152)

具体步骤就是得到深度然后用exp(Expceoff * depthZ)存储到ShadowMap中，然后对ShadowMap做一次降采样的高斯模糊，半分辨率存储到ShadowMap的mip1中。

对于云层阴影，ESM的漏光反而不是缺点而是个优点了，因为云层阴影并不是那么实在，特别是云层的自阴影是个很柔和的从淡到浓的过渡：

而且物体穿梭于云层阴影中的时候，如果距离云层很近，那么我们还需要注意阴影并不是特别的实，这个时候注意ESM和普通阴影对于判别阴影强度的曲线:

我们用demos加几个参数看看，目标是让ESM在阴影中靠近阴影图深度的很大的范围都能够受半阴影的影响并且阴影强度是平滑的随距离差的增大而增大，这个时候我们需要把曲线斜率降低:

然后在UE4渲染ScreenSpaceShadowMask的时候利用场景深度转成世界坐标，再把世界坐标转换到太阳视口，得到太阳视口下的线性深度，然后采样ShadowMap的Mip1，将值用ESM的阴影概率公式计算出明度，将值存储到ScreenSpaceShadowMask的蓝通道里面，后续对阴影的实际渲染就让UE4自己来做了。

当然云层本身也会受到云层阴影影响，分离地形和云层ESM的阴影比较系数可以做到云层阴影过渡通透自然，地形阴影边缘柔和中央实在。

云层使用ESM阴影的最大好处是可以模拟渐变的透光效果，而且很容易增加参数让阴影过渡变得柔和自然，原始的ESM是：

ESM阴影图中内容esmDepth = exp(k * depth)

长相是这样的（32000米总深度，k = 0.00007，下图为了看到更多云，将图片的0-5范围映射到0-1显示了）：

![img](Cloud%20shadow.assets/v2-cb5e0fd76d70d16a2f2ef584f28457e1_720w.jpg)

渲染阴影到画面中的时候是正常使用这样的值：

esmDepth = ESM.SampleLevel(ESMSampler,UVZInShadow.xy,0).x

ShadowAtten = saturate(esmDepth/exp(k * UVZInShadow.z))

我们看看k对于ShadowAtten的影响：

![img](Cloud%20shadow.assets/v2-5652d928160202469858880eecc0023f_b.jpg)



上图绿线就是阴影depth = 10000时，画面中各个位置在阴影中的深度所得到的ShadowAtten，可以看到k值越大，半影区域越小，不过k再怎么大ShadowAtten始终是平滑截止到0的。

如果depth= 10000 k = 0.00007 ，查看数值曲线：

![img](Cloud%20shadow.assets/v2-34aa5376a1a9287e393c338e71e8a819_720w.jpg)

可以看到这根曲线会拖很长，从10000米深度到40000都会感觉像半影，这个时候我们可以增加一些参数修整输出：

ShadowAtten = saturate(saturate(esmDepth/exp(k * UVZInShadow.z)) * (1+c) - c)

现在我们调整c = 1.5看看：

![img](Cloud%20shadow.assets/v2-660f5938445df7abcaaf89f44ec731bc_720w.jpg)

相比于绿色的拖尾，红色线条给的半影区域明显缩小了很多10000到16000这段范围是半影区域，继续加大c可以让半影区域继续缩减，直到得到需要的范围。

![img](Cloud%20shadow.assets/v2-717eeb95e92e6edb4826d2b6601e3813_b.jpg)



可以看到c的变化可以缩放半影区域大小并且能够使ShadowAtten和0点并不是平滑过渡过去的。

利用k和c我们就可以实现舒适的云层阴影：

c = 1.5 k = 0.0007时：

![img](Cloud%20shadow.assets/v2-0d55645e798e8cd34af10537417102ff_720w.jpg)

c = 1.5 k = 0.00007时：

![img](Cloud%20shadow.assets/v2-1bedb84268cca52e0bba5d0c85c30ddf_720w.jpg)

k从0.0007到0.00007可以看到的是云朵阴影柔和了

下面考察c，当然编辑器界面里面的值是ShadowParam.w的值，地形受云层阴影的c值我使用的是ShadowParam.w，云朵自阴影我使用的是ShadowParam.x

c = 3.0 k = 0.00007:

![img](Cloud%20shadow.assets/v2-c22ba7512124931d0d0df33590cefc26_720w.jpg)

云层对地面的阴影明显浓郁了。

c = 300 k = 0.00007:

![img](Cloud%20shadow.assets/v2-169973752cd573699cdccc670a6d156f_720w.jpg)

半影都被搞成了实体阴影了。

其他阴影就没有ESM对于渲染云层阴影这么好用了。

下面讲讲怎么在UE4里面渲染云层阴影：

首先我们要渲染太阳的阴影，必须先在太阳方向上定义一个正交投影，目的是从太阳位置开始Raymarch云层，累积Transmission，当Transmission小于0.01时存储这个位置的深度乘以k的exp值。

构建视口到世界坐标的矩阵：

```cpp
FMatrix SunViewRotationMatrix = FInverseRotationMatrix(SunCameraForward.Rotation()) * FMatrix(
	FPlane(0, 0, 1, 0),
	FPlane(1, 0, 0, 0),
	FPlane(0, 1, 0, 0),
	FPlane(0, 0, 0, 1));

FMatrix SunViewMatrix = FTranslationMatrix(-SunCameraPos) * SunViewRotationMatrix;
FMatrix InvSunViewMatrix = SunViewRotationMatrix.GetTransposed() * FTranslationMatrix(SunCameraPos);

FMatrix SunProjectMatrix = CalculateOrthographicProjectionMatrix(cp->SizeScaler * 200.0f, 1.0f, 0.0f, cp->SunToActorDistance * 200.0f);
FMatrix InvSunProjectMatrix = InvertProjectionMatrix(SunProjectMatrix);
SunScreenToWorldMatrixValue = FMatrix(
	FPlane(1, 0, 0, 0),
	FPlane(0, 1, 0, 0),
	FPlane(0, 0, SunProjectMatrix.M[2][2], 1),
	FPlane(0, 0, SunProjectMatrix.M[3][2], 0))
	* InvSunProjectMatrix * InvSunViewMatrix;
```

构建世界坐标到贴图空间的矩阵：

```cpp
SunWorldToUVMatrixValue = SunViewMatrix * SunProjectMatrix * FMatrix(
	FPlane(.5f, 0, 0, 0),
	FPlane(0, .5f, 0, 0),
	FPlane(0, 0, 1.0f, 0),
	FPlane(.5f, .5f, 0, 1));
```

视口到世界坐标的矩阵用在从太阳位置开始Raymarch出云层不透明位置的过程中，我是用的贴图尺寸为768x768分辨率，分16帧Raymarch，因为是平行投影并且太阳位置相对移动缓慢，所以可以简单的按顺序分帧渲染4x4的区块。

渲染完了阴影，我们再进行一次降采样加高斯模糊，当然正常是横向模糊一次再纵向模糊一次，模糊好的图放到阴影图的mip1里面去，云层阴影采样用的就是mip1。有需要可以继续降采样形成完整的mip链，后续可以根据距离做更舒服的柔边阴影。

当渲染完云层阴影后就可以把云层阴影应用到画面中了，方法是利用ScreenSpaceShadowMask来绘制阴影。ScreenSpaceShadowMask来自于：ShadowRendering.cpp里面：

![img](Cloud%20shadow.assets/v2-3450345eb20554c42c9c01f1b5de7d81_720w.jpg)

需要的小伙伴可以自行查找。

渲染的Shader如下：

```c
float GetObjectShadowAtten(float3 pos)
{
    float4 uvInSunView = mul(float4(pos, 1.0f),SunWorldToUVMatrix);
    uvInSunView.z *= SunViewFarClip;
    float attenOfCloudRate;
    float2 sunViewPortPos = abs((uvInSunView.xy * 2.0f) - 1.0f.xx);
    float ShadowParamW = lerp(ShadowParam.w,ShadowParam.w*2.5f,saturate(dot(-Light0Dir,float3(0,0,1.0f))));
    if (any(bool2(sunViewPortPos.x > 1.0f, sunViewPortPos.y > 1.0f)))
    {
        attenOfCloudRate = ShadowViewParam.w;
    }
    else
    {
        float ShadowEsm = CloudShadowMap.SampleLevel(CloudShadowMapSampler, uvInSunView.xy , 1.0f).x;
        float rate = saturate((max(sunViewPortPos.x, sunViewPortPos.y) - 0.9f) * 10.0f);
        float A = saturate(saturate((saturate(ShadowEsm / exp(Exponential_K * uvInSunView.z)) * (1.0f + ShadowParamW)) - ShadowParamW));
        float B = ShadowViewParam.w;
        attenOfCloudRate = lerp(A,B,rate);
    }
    return attenOfCloudRate * attenOfCloudRate;
}

void DrawCloudDirectShadow(float2 TexCoord : TEXCOORD0,
    float3 ScreenVector : TEXCOORD1,
    float4 SVPos : SV_POSITION,
    out float4 OutColor : SV_Target0)
{
    float2 screenPos = ViewportUVToScreenPos(BufferUVToViewportUV(TexCoord));
    float sceneDepth = CalcSceneDepth(TexCoord);
    float4 HomogeneousWorldPosition = mul(float4(screenPos * sceneDepth, sceneDepth, 1.0f), View.ScreenToWorld);
    float3 wpos = HomogeneousWorldPosition.xyz / HomogeneousWorldPosition.w;
    float shadow = GetObjectShadowAtten(wpos);
    OutColor = float4(0.0f,0.0f,shadow,0.0f);
}
```

UE4里面自定义渲染过程这些东西我就不讲了，教程很多，自己动手找找就是一大把。

伸手党还是给你们推荐一个教程：

[YivanLee：虚幻4渲染编程（Shader篇）【第二卷：不用虚幻4Shader管线使用自己的shader】](https://zhuanlan.zhihu.com/p/36635394)

[zhuanlan.zhihu.com![图标](Cloud%20shadow.assets/v2-332dc53560fb3fc09bb82caf8bd29a8f_180x120.jpg)](https://zhuanlan.zhihu.com/p/36635394)

最后放上一张图：

![img](Cloud%20shadow.assets/v2-6b11cfa325c3ac4340a05a1972755ff7_720w.jpg)



编辑于 2020-04-22