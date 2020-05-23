# 用纹理贴图进行快速滤波宽度的计算（Fast Filter-Width Estimates with Texture Maps）

## 

## 【章节概览】

这章描述基于纹理映射在2D空间中进行快速过滤宽度计算（Fast Filter-Width Estimates）的方法。即使硬件profile对复杂函数的局部偏导函数不提供直接支持，基于本文提出的纹理操作技巧，也可以得到结果。

## 

## 【核心要点】

Cg标准库提供了ddx()和ddy()函数，计算任意量关于x和y像素的导数。换言之，调用ddx(v)，可以求出变量v在x方向的当前像素与下一个像素之间的变化量，调用ddy(v)同样也可以求出y方向的情况。

那么，下面贴出的这个filterwidth()函数，可以很容易地计算任何值在像素之间变化的速率，以及程序纹理说需要过滤的面积。

```
float filterwidth(float2 v)

{

  float2 fw = max(abs(ddx(v)), abs(ddy(v)));

  return max(fw.x, fw.y);

}
```

上述filterwidth()函数，仅在支持ddx()和ddy()函数的profile下工作，但可惜的是一些硬件profile不支持这两两个函数。而本文提出的这个trick，可以使用纹理映射硬件，进行与filterwidth()函数本质上相同的运算。

而这个技巧的关键在于，用函数tex2D()所做的纹理贴图查询，可以自动地对纹理查询进行反走样，而不考虑所代入的纹理坐标。也就是说，基于在相邻像素上所计算的纹理坐标，硬件可以为每个查询决定要过滤的纹理面积。

纹理映射的这个性质，可以用来替代滤波宽度函数filterwidth()，而无需调用ddx()和ddy()。我们以这样的一种方式执行纹理查询：通过它可以推测所过滤的纹理贴图面积，这里是推测需要过滤的程序化棋盘格纹理面积。这种解法分为两步：（1）为特定的纹理坐标选择mipmap级别；（2）利用上述技巧来决定过滤宽度。

最终，这个trick可以在很多情况下很好的计算滤波宽度，运行性能几乎与基于求导的计算滤波宽度函数filterwidth()相同。

## 

## 【本章配套源代码汇总表】

Example 25-1 抗锯齿棋盘函数（Antialiased Checkerboard Function）

Example 25-2使用估算滤波宽度的值来加载Mipmap级别的代码（Code to Load Mipmap Levels with Values Used for Estimating Filter Widths）

Example 25-3 使用示例25-2中的Mipmap来计算滤波器宽度的函数（Function to Compute Filter Widths Using Mipmaps from Listing 25-2）

Example 25-4 滤波器宽度函数不容易走样滤波器宽度（Filter-Width Function That Is Less Prone to Under-Aliasing Filter Widths）

## 

## 【关键词提炼】

快速滤波宽度估算（Fast Filter-Width Estimates）

在着色器中求导（Derivatives in Shaders）

用纹理计算过滤宽度（Computing Filter Width with Textures）
