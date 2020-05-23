# S.T.A.L.K.E.R.中的延迟着色（Deferred Shading in S.T.A.L.K.E.R.）

## 

## 【章节概览】

本章是对《S.T.A.L.K.E.R.》中所用渲染器的几乎两年的研究和开发的事后剖析。该渲染器完全基于延迟着色（Derred Shading）和100%动态光照，目标是高端GPU，因为没有任何一个解决方案可以适合所有需求，所以这章并不是延迟着色的全面指南，但是可以作为一个很好的参考。

## 

## 【核心要点】

延迟着色（Deferred Shading），虽然并不适合每个游戏，但是确是《S.T.A.L.K.E.R》中的优秀渲染架构。它提供了一个渲染引擎，权衡了现代GPU，比传统的前向着色架构有更低的几何体处理需求，更低的像素处理需求及更低的CPU开销。场景管理器也更干净更简单。一旦避开了延迟着色固有的不足，如多材质系统的潜在限制和缺乏反失真功能，产生的架构既灵活又快速，允许区域很广的效果。

[
![img](DeferredShadinginS.T.A.L.K.E.R..assets/b2c19e6b54faf091f56980ed4c1091fe.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/b2c19e6b54faf091f56980ed4c1091fe.jpg)

图 基于延迟着色实现的渲染效果 @2005年

[
![img](DeferredShadinginS.T.A.L.K.E.R..assets/66a82c37040045d0c1c31ae82683e73a.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/66a82c37040045d0c1c31ae82683e73a.jpg)

图 基于延迟着色实现的渲染效果 @2005年

[
![img](DeferredShadinginS.T.A.L.K.E.R..assets/1322748b3b1719a88e7b97739a688cda.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUGems2%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/Part1/media/1322748b3b1719a88e7b97739a688cda.jpg)

图 基于延迟着色实现的渲染效果 @2005年

## 

## 【关键词】

延迟着色（Deferred Shading）

几何缓冲区（G-buffer）

反走样（Antialiasing）
