# 相交大气

#### 相交大气

如前所述，我们计算穿过大气层的**光学深度**的唯一方法是通过**数值积分**。这意味着将间隔分成较小的长度段![ds](IntersectingTheAtmosphere.assets/quicklatex.com-0793eaa7d07ca060bd29efdb05f4ed82_l3.svg)，并在假定其密度恒定的情况下计算每个光学深度。

![img](IntersectingTheAtmosphere.assets/scattering_12.png)

在上图中，![\ overline {AB}](IntersectingTheAtmosphere.assets/quicklatex.com-01e3f48fa11a50273e3889539222abe7_l3.svg)使用4个样本计算的光学深度，每个样本仅考虑片段本身中心的密度。

显然，第一步是找到要点![一个](IntersectingTheAtmosphere.assets/quicklatex.com-816b613a4f79d4bf9cb51396a9654120_l3.svg)和![乙](IntersectingTheAtmosphere.assets/quicklatex.com-c74288aabc0e2ca280d25d92bf1a1ec2_l3.svg)。如果我们假设我们正在渲染球体，则Unity将尝试渲染其表面。屏幕上的每个像素对应于球体上的一个点。在下图中，该点被称为![Ø](IntersectingTheAtmosphere.assets/quicklatex.com-5fd89de58d79b25e5ca6ae69a6ff464b_l3.svg)为*原点*。在表面着色器中，![Ø](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5fd89de58d79b25e5ca6ae69a6ff464b_l3.svg)对应于Input  结构 内的worldPos变量。这就是着色器的作用范围。我们唯一可获得的信息是，指示**光线**方向的方向和以半径为中心的大气层。挑战在于计算和  ![Ø](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5fd89de58d79b25e5ca6ae69a6ff464b_l3.svg)![d](IntersectingTheAtmosphere.assets/quicklatex.com-c10ec9debc8ec5dce4c3c5887557202d_l3.svg)![C](IntersectingTheAtmosphere.assets/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)![[R](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d6abdd487c56e5efbb2c9522ed4b9360_l3.svg)![一个](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-816b613a4f79d4bf9cb51396a9654120_l3.svg)![乙](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c74288aabc0e2ca280d25d92bf1a1ec2_l3.svg)。最快的方法是使用几何方法，从而减少了查找大**气球**与摄像机的**视线**之间的交点的问题。
 ![img](IntersectingTheAtmosphere.assets/scattering_15.png)

首先，我们应该注意到![Ø](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5fd89de58d79b25e5ca6ae69a6ff464b_l3.svg)，![一个](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-816b613a4f79d4bf9cb51396a9654120_l3.svg)并且![乙](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c74288aabc0e2ca280d25d92bf1a1ec2_l3.svg)都位于视线中。这意味着我们可以将其位置称为3D空间中的点，而不是视线到原点的距离。虽然![一个](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-816b613a4f79d4bf9cb51396a9654120_l3.svg)是实际点（在着色器中表示为 float3），但将是其与原点的距离（表示为float）。这两个和两个同等有效的方式来表示同一个点，它认为： ![AO](IntersectingTheAtmosphere.assets/quicklatex.com-6c53a9f288e66a1dd82bc34cbde9c38e_l3.svg)![Ø](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5fd89de58d79b25e5ca6ae69a6ff464b_l3.svg) ![一个](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-816b613a4f79d4bf9cb51396a9654120_l3.svg)![AO](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6c53a9f288e66a1dd82bc34cbde9c38e_l3.svg)

![image-20200507201025219](IntersectingTheAtmosphere.assets/image-20200507201025219.png)

上划线表示![\ overline {XY}](IntersectingTheAtmosphere.assets/quicklatex.com-7e3596ba14d772d2d8d76479f854b8ee_l3.svg)任意点![X](IntersectingTheAtmosphere.assets/quicklatex.com-996ff7036e644e89f8ac379fa58d0cf7_l3.svg)和之间的线段长度![ÿ](IntersectingTheAtmosphere.assets/quicklatex.com-42ae22abcaa05c2d6c2fdc3746446019_l3.svg)。

出于效率方面的考虑，在着色器代码中，我们将使用![AO](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6c53a9f288e66a1dd82bc34cbde9c38e_l3.svg)和![BO](IntersectingTheAtmosphere.assets/quicklatex.com-f44e6bf8caf4c3f74a0145bb11195611_l3.svg)，并从中进行计算![OT](IntersectingTheAtmosphere.assets/quicklatex.com-355ec54b7fe63a1ae4b0759b341e6879_l3.svg)：

 ![image-20200507201046664](IntersectingTheAtmosphere.assets/image-20200507201046664.png)

我们还应该注意，段![\ overline {AT}](IntersectingTheAtmosphere.assets/quicklatex.com-2206db03f7bc481ef23dcae4299fed19_l3.svg)和  ![\ overline {BT}](IntersectingTheAtmosphere.assets/quicklatex.com-f9ff5d6d894fdbda6482363caba5d795_l3.svg)具有相同的长度。现在我们需要找到交点的是计算![\ overline {AO}](IntersectingTheAtmosphere.assets/quicklatex.com-009503ca3d80b89dd044c14f54dabae5_l3.svg)和![\ overline {AT}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-2206db03f7bc481ef23dcae4299fed19_l3.svg)。

![\ overline {OT}](IntersectingTheAtmosphere.assets/quicklatex.com-86d3b1a18628bd2c5e202d5e8ffb49d0_l3.svg)最容易计算的细分。如果我们看一下上面的图，我们可以看到这![\ overline {OT}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-86d3b1a18628bd2c5e202d5e8ffb49d0_l3.svg)是向量![一氧化碳](IntersectingTheAtmosphere.assets/quicklatex.com-98746627ddda8d9313ad9e1a6642876f_l3.svg)在视线上的投影。从数学上讲，这种投影可以用**点积完成**。如果您熟悉着色器，您可能会知道点积可以衡量两个方向的“对齐”程度。当将其应用于两个向量并且第二个向量具有单位长度时，它将成为投影运算符：

![image-20200507201101216](IntersectingTheAtmosphere.assets/image-20200507201101216.png)

应该注意的![\ left（CO \ right）](IntersectingTheAtmosphere.assets/quicklatex.com-33abb6901962b8a67ac1bfff745c58ee_l3.svg)是3D向量，而不是![C](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ed12970f60569db1dfd9f13289854a0d_l3.svg)和之间的线段长度![Ø](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5fd89de58d79b25e5ca6ae69a6ff464b_l3.svg)。

接下来我们需要计算的是片段的长度![\ overline {AT}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-2206db03f7bc481ef23dcae4299fed19_l3.svg)。这可以使用三角上的**毕达哥拉斯定理**来计算![\ overset {\ triangle} {ACT}](IntersectingTheAtmosphere.assets/quicklatex.com-8d05bb8359ae0b269d1a59544333b549_l3.svg)。实际上，它认为：

![image-20200507201120763](IntersectingTheAtmosphere.assets/image-20200507201120763.png)

意思就是：

![image-20200507201134187](IntersectingTheAtmosphere.assets/image-20200507201134187.png)

的长度![\ overline {CT}](IntersectingTheAtmosphere.assets/quicklatex.com-0f8173f999d7ce788f4087eee30c14d4_l3.svg)仍然未知。但是，可以通过在三角形上再次应用毕达哥拉斯定理来计算![\ overset {\ triangle} {OCT}](IntersectingTheAtmosphere.assets/quicklatex.com-80703ccdc1875dea37522755f4020761_l3.svg)：

![image-20200507201150582](IntersectingTheAtmosphere.assets/image-20200507201150582.png)

我们知道我们需要的所有数量。把它们加起来：

 ![image-20200507201208028](IntersectingTheAtmosphere.assets/image-20200507201208028.png)

该组方程包含平方根。它们仅在非负数上定义。如果为![R ^ 2> \ overline {CT} ^ 2](IntersectingTheAtmosphere.assets/quicklatex.com-ae6d050cbe187c02f9ec702a7526fd39_l3.svg)，则没有解决方案，这意味着视线不与球体相交。

我们可以将其转换为以下Cg函数：

```
bool rayIntersect
(
	// Ray
	float3 O, // Origin
	float3 D, // Direction

	// Sphere
	float3 C, // Centre
	float R,	// Radius
	out float AO, // First intersection time
	out float BO  // Second intersection time
)
{
	float3 L = C - O;
	float DT = dot (L, D);
	float R2 = R * R;

	float CT2 = dot(L,L) - DT*DT;
	
	// Intersection point outside the circle
	if (CT2 > R2)
		return false;

	float AT = sqrt(R2 - CT2);
	float BT = AT;

	AO = DT - AT;
	BO = DT + BT;
	return true;
}
```

没有一个值，但有三个要返回的值：![\ overline {AO}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-009503ca3d80b89dd044c14f54dabae5_l3.svg)，![\ overline {BO}](IntersectingTheAtmosphere.assets/quicklatex.com-4978f0678237b06334d66272dfbdd7a5_l3.svg)以及是否存在交集。这两个段的长度使用out  关键字返回，这使函数在终止后对这些参数所做的任何更改都保持不变。

#### 与地球相撞

我们还必须考虑其他问题。某些视线照射到行星上，因此它们穿过大气层的旅程会提前终止。一种方法可能是修改上面介绍的推导。

一种简单但效率较低的方法是运行rayIntersect  两次，然后在需要时调整终点。

![img](IntersectingTheAtmosphere.assets/scattering_16.png)

这将转换为以下代码：

```
// Intersections with the atmospheric sphere
float tA;	// Atmosphere entry point (worldPos + V * tA)
float tB;	// Atmosphere exit point  (worldPos + V * tB)
if (!rayIntersect(O, D, _PlanetCentre, _AtmosphereRadius, tA, tB))
	return fixed4(0,0,0,0); // The view rays is looking into deep space

// Is the ray passing through the planet core?
float pA, pB;
if (rayIntersect(O, D, _PlanetCentre, _PlanetRadius, pA, pB))
	tB = pA;
```



#### 下一步…

这篇文章展示了如何找到球和射线之间的交点。在下一篇文章中，我们将使用它来计算大气层中视线的入射点和出射点。