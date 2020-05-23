# 大气散射明暗器





本教程最后总结了我们模拟行星大气瑞利散射的过程。![img](https://www.alanzucconi.com/wp-content/uploads/2017/10/planets.gif)

下一个（也是最后一个）部分将展示如何更改着色器，使其也包括称为Mie Scattering的其他类型的散射。

您可以在这里找到本系列的所有文章：

- 第1部分。[体积大气散射](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7374&usg=ALkJrhjYMhWOeFn5j2IlPMWpMA64AiPlMg)
- 第2部分。[大气散射背后的理论](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7404&usg=ALkJrhhNvWi2Ma8gskQo9lVjBRr-spPMIg)
- 第3部分。 [瑞利散射的数学](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7472&usg=ALkJrhiArBwcvl4lZ1tg3w6zBYlp7hJKHg)
- 第4部分 [。穿越大气的旅程](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7557&usg=ALkJrhjMschsdC2q-wdtAHWdFW182MFNug)
- 第5部分。 [大气层着色器](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7665&usg=ALkJrhgTDkLQgvV6XWqIWD7d38K_d8Quxw)
- 第6部分。 [相交的气氛](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7781&usg=ALkJrhj54Ie8EPoQkg4AuMrWftgjjy1-aA)
- **第7部分。 [大气散射着色器](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7793&usg=ALkJrhiya4HGZA53eDuy9guoib53wbK9IQ)**
- 第8部分。 [三重理论概论](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7578&usg=ALkJrhiT9N0FnH53kCdo8wVccpn3C10IEA)

您可以参考“ [大气散射备忘单”](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7766&usg=ALkJrhjSEJtCcx3nq0bi_g1cPtOXSryBcg)  以获取所有所用方程式的完整参考。

您可以在页面底部**下载**本教程的**Unity软件包**。



#### 采样视线

让我们回想一下最近得出的大气散射方程：

 ![image-20200507201440144](AtmosphericScatteringShader.assets/image-20200507201440144.png)

我们接收到的光量等于从太阳发出的光量![I_S](AtmosphericScatteringShader.assets/quicklatex.com-8267520f1a54784637e791b96ef239b8_l3.svg)，乘以![P](AtmosphericScatteringShader.assets/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)该段中每个点的各个贡献之和![\ overline {AB}](AtmosphericScatteringShader.assets/quicklatex.com-01e3f48fa11a50273e3889539222abe7_l3.svg)。

我们可以直接在着色器中实现该功能。但是，几乎没有可以完成的优化。在以前的教程中曾暗示可以进一步简化该表达式。我们可以采取的第一步是将散射函数分解为两个基本组成部分：

![image-20200507201525739](AtmosphericScatteringShader.assets/image-20200507201525739.png)

由于角度和波长不取决于采样点，因此**相位函数** ![\ gamma \ left（\ theta \ right）](AtmosphericScatteringShader.assets/quicklatex.com-8fb8614c124bbd60135ff4d00fea2437_l3.svg)和**海平面上** 的**散射系数****相**![\ beta \ left（\ lambda \ right）](AtmosphericScatteringShader.assets/quicklatex.com-05448a0957014b2892578b9b570bc9e4_l3.svg)对于总和是恒定的。因此，可以将它们排除在外：![\ theta](AtmosphericScatteringShader.assets/quicklatex.com-7b2034939b850e3311120fca462ab64e_l3.svg)![\ lambda](AtmosphericScatteringShader.assets/quicklatex.com-8c37d2f1acb1d49f3e5e655797880475_l3.svg)

![image-20200507201537414](AtmosphericScatteringShader.assets/image-20200507201537414.png)

这个新表达式在数学上与上一个等效，但是由于某些最重的部分已从求和中删除，因此该表达式的计算效率更高。

我们还没有准备好开始实施它。![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)我们应该考虑到很多方面。的合理近似![一世](AtmosphericScatteringShader.assets/quicklatex.com-14b16a74c9ddcc6f9be3e94b9c8d8f08_l3.svg)是将![\ overline {AB}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-01e3f48fa11a50273e3889539222abe7_l3.svg)长度分成几个较小的部分![ds](AtmosphericScatteringShader.assets/quicklatex.com-0793eaa7d07ca060bd29efdb05f4ed82_l3.svg)，并累积每个单独部分的贡献。这样做时，我们假设每个段都足够小以具有恒定的密度。一般来说，情况并非如此，但是如果![ds](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0793eaa7d07ca060bd29efdb05f4ed82_l3.svg)a足够小，我们仍然可以达到一个合理的近似值。

![img](AtmosphericScatteringShader.assets/scattering_12.png)

由于所有段都位于视线上，因此其中的段数  ![\ overline {AB}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-01e3f48fa11a50273e3889539222abe7_l3.svg)称为**视图样本**。在着色器中，这将是_ViewSamples  属性。通过将其作为属性，可以从物料检查器访问它。这使我们可以降低着色器的精度，从而提高其性能。

以下代码允许循环遍历大气中的所有部分。

```glsl
// Numerical integration to calculate
// the light contribution of each point P in AB
float3 totalViewSamples = 0;
float time = tA;
float ds = (tB-tA) / (float)(_ViewSamples);
for (int i = 0; i < _ViewSamples; i ++)
{
	// Point position
	// (sampling in the middle of the view sample segment)
	float3 P = O + D * (time + ds * 0.5);

	// T(CP) * T(PA) * ρ(h) * ds
	totalViewSamples += viewSampling(P, ds);

	time += ds;
}

// I = I_S * β(λ) * γ(θ) * totalViewSamples
float3 I = _SunIntensity *  _ScatteringCoefficient * phase * totalViewSamples;
```

可变时间  用于跟踪我们距原点的距离，并 在每次迭代后增加ds。 ![Ø](AtmosphericScatteringShader.assets/quicklatex.com-5fd89de58d79b25e5ca6ae69a6ff464b_l3.svg)

#### 光学深度PA

沿视线的每个点都会对![\ overline {AB}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-01e3f48fa11a50273e3889539222abe7_l3.svg)我们绘制的像素的最终颜色产生自己的贡献。从数学上讲，该贡献是求和内的数量：

![image-20200507201626761](AtmosphericScatteringShader.assets/image-20200507201626761.png)

就像我们在上一段中所做的那样，让我们尝试简化它。通过替换![Ť](AtmosphericScatteringShader.assets/quicklatex.com-7e093fd43ad2c244140c11afe4d4bdff_l3.svg)其实际定义，我们可以进一步扩展该表达式：

![image-20200507201642058](AtmosphericScatteringShader.assets/image-20200507201642058.png)

透射过的产品![\ overline {CP}](AtmosphericScatteringShader.assets/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)和![\ overline {PA}](AtmosphericScatteringShader.assets/quicklatex.com-41400e1d57b339c76cdec946f670a6bb_l3.svg)变成：

![image-20200507201656696](AtmosphericScatteringShader.assets/image-20200507201656696.png)

将**合并的透射率**被建模为一个指数衰减与系数是的总和**光学深度**在由光（行进的路径![\ overline {CP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)和![\ overline {PA}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-41400e1d57b339c76cdec946f670a6bb_l3.svg)），乘以*在海平面散射系数*（![\ beta](AtmosphericScatteringShader.assets/quicklatex.com-0f39b655b53423e80558c68b8c2ae1c3_l3.svg)与![h = 0](AtmosphericScatteringShader.assets/quicklatex.com-fd16c23a91f843528cf3a40daf6ad564_l3.svg)）。

我们开始计算的第一个量是该片段的光学深度，该深度![\ overline {PA}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-41400e1d57b339c76cdec946f670a6bb_l3.svg)从进入点到大气，一直到我们当前在for循环中采样的点。让我们回想一下光学深度的定义：

![image-20200507201726205](AtmosphericScatteringShader.assets/image-20200507201726205.png)

如果必须天真的实现这一点，我们将创建一个名为OpticalDepth的函数，该函数对循环 之间和循环中的点进行采样。这是可能的，但是效率很低。实际上，我们已经在分析最外层的for循环的段的光学深度。如果我们计算当前segmenet居中的光学深度（opticalDepthSegment），并将其累积在for循环（opticalDepthPA）中，则可以节省很多计算。 ![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)![一个](AtmosphericScatteringShader.assets/quicklatex.com-816b613a4f79d4bf9cb51396a9654120_l3.svg)![D \ left（\ overline {PA} \ right）](AtmosphericScatteringShader.assets/quicklatex.com-e6dc267a1447cf77a665f03bc1ba86ba_l3.svg)![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)

```
// Accumulator for the optical depth
float opticalDepthPA = 0;

// Numerical integration to calculate
// the light contribution of each point P in AB
float time = tA;
float ds = (tB-tA) / (float)(_ViewSamples);
for (int i = 0; i < _ViewSamples; i ++)
{
	// Point position
	// (sampling in the middle of the view sample segment)
	float3 P = O + D * (time + viewSampleSize*0.5);

	// Optical depth of current segment
	// ρ(h) * ds
	float height = distance(C, P) - _PlanetRadius;
	float opticalDepthSegment = exp(-height / _ScaleHeight) * ds;

	// Accumulates the optical depths
	// D(PA)
	opticalDepthPA += opticalDepthSegment;

	...	

	time += ds;
}
```



#### 灯光采样

如果我们回顾一下的光贡献表达式![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)，我们会发现，唯一需要的数量就是线段的光学深度![\ overline {CP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)，

![image-20200507201806132](AtmosphericScatteringShader.assets/image-20200507201806132.png)

我们将把计算片段光学深度的代码![\ overline {CP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)移到一个名为lightSampling的函数中。该名称来自**光线**，**光线**是从此开始并指向太阳的部分。我们称其为离开大气的点是。 ![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)![C](AtmosphericScatteringShader.assets/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)

该 lightSampling  功能，但是，将不只是计算的光学厚度。到目前为止，我们只考虑了大气的贡献，却忽略了实际星球的作用。我们的方程式没有考虑从太阳光射向地球的可能性。如果发生这种情况，则必须舍弃到目前为止所做的所有计算，因为实际上没有光会到达相机。 ![\ overline {CP}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a38c3cc141c6a8e1d8097931aa5fa3c2_l3.svg)![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)

![img](AtmosphericScatteringShader.assets/scattering_17.png)

在上图中，很容易看出![P_0](AtmosphericScatteringShader.assets/quicklatex.com-5db3bdfeecf549515be6dbbbb959f2a3_l3.svg)应该忽略的光贡献，因为没有太阳光到达![P_0](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5db3bdfeecf549515be6dbbbb959f2a3_l3.svg)。在![P](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-fda1e51b12ba3624074fcbebad72b1fc_l3.svg)和之间循环移动时![C](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)， lightSampling  功能还将检查行星是否被撞到。这可以通过检查点的高度是否为负来完成。

```glsl
bool lightSampling
(	float3 P,	// Current point within the atmospheric sphere
	float3 S,	// Direction towards the sun
	out float opticalDepthCA
)
{
	float _; // don't care about this one
	float C;
	rayInstersect(P, S, _PlanetCentre, _AtmosphereRadius, _, C);

	// Samples on the segment PC
	float time = 0;
	float ds = distance(P, P + S * C) / (float)(_LightSamples);
	for (int i = 0; i < _LightSamples; i ++)
	{
		float3 Q = P + S * (time + lightSampleSize*0.5);
		float height = distance(_PlanetCentre, Q) - _PlanetRadius;
		// Inside the planet
		if (height < 0)
			return false;

		// Optical depth for the light ray
		opticalDepthCA += exp(-height / _RayScaleHeight) * ds;

		time += ds;
	}

	return true;
}
```



|      |      |
| ---- | ---- |
|      |      |

上面的函数首先![C](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)使用rayInstersect计算点。然后将其划分为 长度为ds的_LightSamples个分段。光学深度的计算与最外层回路中的计算相同。 ![\ overline {PA}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-41400e1d57b339c76cdec946f670a6bb_l3.svg)

如果行星已被撞击，该函数将返回false。我们可以使用它在最外层的循环中更新丢失的代码，代替 。。。。

```glsl
	// D(CP)
	float opticalDepthCP = 0;
	bool overground = lightSampling(P, S);

	if (overground)
	{
		// Combined transmittance
		// T(CP) * T(PA) = T(CPA) = exp{ -β(λ) [D(CP) + D(PA)]}
		float transmittance = exp
		(
			-_ScatteringCoefficient *
			(opticalDepthCP + opticalDepthPA)
		);

		// Light contribution
		// T(CPA) * ρ(h) * ds
		totalViewSamples += transmittance * opticalDepthSegment;
	}
```



|      |      |
| ---- | ---- |
|      |      |

现在我们已经考虑了所有元素，着色器就完成了。

#### 下一步…

这篇文章（最后！）完成了模拟空气散射的体积着色器。到目前为止，我们仅考虑了瑞利散射的贡献。有许多光学现象无法单独用瑞利散射来解释。下一篇文章将介绍第二种类型的散射，即米氏散射。

您可以在这里找到本系列的所有文章：

- 第1部分。[体积大气散射](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7374&usg=ALkJrhjYMhWOeFn5j2IlPMWpMA64AiPlMg)
- 第2部分。[大气散射背后的理论](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7404&usg=ALkJrhhNvWi2Ma8gskQo9lVjBRr-spPMIg)
- 第3部分。 [瑞利散射的数学](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7472&usg=ALkJrhiArBwcvl4lZ1tg3w6zBYlp7hJKHg)
- 第4部分 [。穿越大气的旅程](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7557&usg=ALkJrhjMschsdC2q-wdtAHWdFW182MFNug)
- 第5部分。 [大气层着色器](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7665&usg=ALkJrhgTDkLQgvV6XWqIWD7d38K_d8Quxw)
- 第6部分。 [相交的气氛](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7781&usg=ALkJrhj54Ie8EPoQkg4AuMrWftgjjy1-aA)
- **第7部分。 [大气散射着色器](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7793&usg=ALkJrhiya4HGZA53eDuy9guoib53wbK9IQ)**
- 第8部分。 [三重理论概论](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7578&usg=ALkJrhiT9N0FnH53kCdo8wVccpn3C10IEA)

您可以参考“ [大气散射备忘单”](https://translate.googleusercontent.com/translate_c?depth=1&pto=aue&rurl=translate.google.com.hk&sl=en&sp=nmt4&tl=zh-CN&u=https://www.alanzucconi.com/%3Fp%3D7766&usg=ALkJrhjSEJtCcx3nq0bi_g1cPtOXSryBcg)  以获取所有所用方程式的完整参考。