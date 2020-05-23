# 分段缓冲（Segment Buffering）

## 

## 【章节概览】

本章介绍了一项可以明显减少一个显示帧中渲染的批次数目的技术——分段缓冲（segment buffering），以及其改进。

## 

## 【核心要点】

分段缓冲（segment buffering）技术汇集了在场景中彼此靠近的多个实例，把它们合并到“超级实例（über-instances）”中，这样减少了批次的数目，而且提供了解决批次瓶颈问题的一个简单优化的方案。

分段缓冲（segment buffering）技术自动合并相似的实例，同时保持呈现单独实例的大部分优势。分段缓冲的主要好处在于非重复的外观，以及无需重新绘制原始的实例，就像这部分实例从可见集合中被删除了一样，所以可以明显减少一个显示帧中渲染的批次的数目。而其具体步骤分为三步，原书中有进一步地说明。

而关于分段缓冲（Segment Buffering）的改进，文章提出了结合自动纹理图集生成（automatic texture-atlas generation [NVIDIA 2004]）的相关思路。

[
![img](SegmentBuffering.assets/4333a11bdd0cd59f176689ac47e84716.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/4333a11bdd0cd59f176689ac47e84716.jpg)

图 包含同一个物体的多个实例的场景

## 

## 【关键词】

实例化（instance）

批次（batch）

分段缓冲（segment buffering）

超级实例（über-instances）

自动纹理图集生成（automatic texture-atlas generation）
