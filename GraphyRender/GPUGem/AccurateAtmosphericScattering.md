# 精确的大气散射（Accurate Atmospheric Scattering）

## 

## 【章节概览】

生成真实大气散射的效果一直是计算机图形学领域的难题。描述大气的散射方程式非常复杂，以至于可以用整本书去解决这个课题。计算机图形模型通常使用简化的方程，这些模型中只有少数可以以交互速率运行。

这章介绍如何实现一个完全运行在GPU上的大气散射实时算法（原始算法由Nishita等人在1993年提出），并提供了实现此算法的全部CG和GLSL源代码。

## 

## 【核心要点】

这章解释了如何在GPU着色器中实现Nishita等人在1993年提出的散射方程，并以可交互的速率运行。这些方程能更加精确地对大气建模，保证当高度降低的同时密度也呈指数级降低。且可以在不需要牺牲图像质量同时省略查找表，着色器代码足够小而快，可以在一个GPU着色器中实现整个算法。

一个重要的细节是怎样模拟大气中一个点的散射（Scattering）。最常见的两种大气散射形式是瑞利散射（Rayleigh Scattering）和米氏散射（Mie Scattering）。

瑞利散射（Rayleigh Scattering）是由空气中的小分子引起的，而且它对波长端的光散射更强（最先是蓝色，然后是绿色和红色）。

米氏散射（Mie Scattering）由空气中更大一些的粒子引起，这些粒子被称为浮尘（aerosols），如灰尘（dust）或污染物（pollution）。

章节构成方面，这章一开始用一定的篇幅进行了散射方程的求解和简化，最终得到的实现在原本的大气散射模型上进行了不少简化，以至于最终的实现可以在对硬件要求不高的前提下，达到交互的速率进行渲染。并且采用了高范围动态（HDR）渲染，得到了更好的大气散射效果。

[
![img](AccurateAtmosphericScattering.assets/d398916378dc464ce8113f698a8f9f66.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/d398916378dc464ce8113f698a8f9f66.jpg)

图 散射Demo的截图

## 

## 【关键词】

大气散射（Atmospheric Scattering）

瑞利散射（Rayleigh Scattering）

米氏散射（Mie Scattering）

高范围动态渲染（High-Dynamic-Range Rendering）
