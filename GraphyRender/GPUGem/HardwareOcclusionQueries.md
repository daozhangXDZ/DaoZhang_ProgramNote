# 让硬件遮挡查询发挥作用（Hardware Occlusion Queries Made Useful）

## 

## 【章节概览】

这章探究了如何最好地应用硬件遮挡查询（Hardware Occlusion Queries）的思路，介绍了一个简单但强大的算法，其最小化了调用查询的次数，而且减少了由查询结果延迟造成的停滞影响。

## 

## 【核心要点】

遮挡查询作为一个GPU特性，反馈的延迟很高，可以确定一个物体在被渲染之后是否看得见，不像早期的遮挡查询裁剪技术，Michael等人的算法是像素完美的，即此算法没有引入渲染走样，并产生一组最合适的可见物体来渲染，没有把不必要的负载放到GPU上，而且CPU的开销最小。

文中介绍的算法可以解决这些问题。 该算法用前一帧的遮挡查询结果来初始化和调度当前帧的查询，利用了可见性的空间和时间相关性。这通过把场景存储在一个层的数据结构来完成（比如k-d树或八叉树），以从前到后的顺序处理层的节点，渲染某些先前可见的节点来交叉地遮挡查询。

也就是说，该算法几乎可以节省任何在CPU和GPU上等待遮挡查询结果的时间。这是利用时间一致性（temporal coherence）来实现的，假设正在先前帧可见的物体在当前帧仍保持可见。算法使用层结构来在单次测试中裁剪掉大块被遮挡的区域，减少了遮挡查询的数量，同事也避免了大部分其他内节点的遮挡测试。

[
![img](HardwareOcclusionQueries.assets/1b35dc4e59118fbd172135badb4dfd4e.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/1b35dc4e59118fbd172135badb4dfd4e.jpg)

图 两个连续帧中层次结构节点的可见性

## 

## 【关键词】

硬件遮挡查询（Hardware Occlusion Queries）

时间一致性（temporal coherence）

一致性层裁剪（Coherent Hierarchical Culling）
