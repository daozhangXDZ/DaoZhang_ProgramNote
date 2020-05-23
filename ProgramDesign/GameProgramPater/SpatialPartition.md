## 空间分区模式Spatial Partition

将对象存储在基于位置组织的数据结构中，来有效的定位对象。

### 

### 要点

- 对于一系列对象，每个对象都有空间上的位置。将它们存储在根据位置组织对象的空间数据结构中，让我们有效查询在某处或者附近的对象。当对象的位置改变时，更新空间数据结构，这样它可以继续找到对象。
- 最简单的空间分区：固定网格。想象某即时战略类游戏，一改在单独的数组中存储我们的游戏对象的常规思维，我们将它们存到网格的格子中。每个格子存储一组单位，它们的位置在格子的边界内部。当我们处理战斗时，一般只需考虑在同一格子或相邻格子中的单位，而不是将每个游戏中的单位与其他所有单位比较，这样就大大节约了计算量。

### 

### 使用场合

- 空间分区模式在需要大量存储活跃、移动的游戏物体，和静态的美术模型的游戏中比较常用。因为复杂的游戏中不同的内容有不同的空间划分。
- 这个模式的基本适用场景是你有一系列有位置的对象，当做了大量通过位置寻找对象的查询而导致性能下降的时候。
- 空间分区的存在是为了将O(n)或者O(n²) 的操作降到更加可控的数量级。你拥有的对象越多，此模式就越好用。相反的，如果n足够小，也许就不需要使用此模式。

### 

### 引申与参考

- 了解了空间分区模式，下一步应该是学习一下常见的结构。常见的有：
  - [Grid](http://en.wikipedia.org/wiki/Grid_(spatial_index))
  - [Quadtree](http://en.wikipedia.org/wiki/Quad_tree)
  - [BSP](http://en.wikipedia.org/wiki/Binary_space_partitioning)
  - [k-d tree](http://en.wikipedia.org/wiki/Kd-tree)
  - [Bounding volume hierarchy](http://en.wikipedia.org/wiki/Bounding_volume_hierarchy)
- 每种空间划分数据结构基本上都是将一维数据结构扩展成更高维度的数据结构。知道它的直系子孙有助于分辨它是否适合解决当前的问题：
  - 网格其实是持续的[桶排序](http://en.wikipedia.org/wiki/Bucket_sort)。
  - BSP，k-d tree，和层次包围盒是[线性搜索树](http://en.wikipedia.org/wiki/Binary_search_tree)。
  - 四叉树和八叉树是[多叉树](http://en.wikipedia.org/wiki/Trie)。
- 本节内容相关的英文原文：<http://gameprogrammingpatterns.com/spatial-partition.html>
- 本节内容相关的中文翻译： <http://gpp.tkchu.me/spatial-partition.html>
