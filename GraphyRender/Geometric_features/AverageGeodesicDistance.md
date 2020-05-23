# 几何特征系列：Average Geodesic Distance（平均测地距离）



2016-07-09



LEEMANCHIU



[0 Comment](http://lemonc.me/average-geodesic-distance.html#respond)



[理工男](http://lemonc.me/category/science-engineering)

这篇文章将介绍  Average Geodesic Distance，中文名译作「平均测地距离」。Geodesic  Distance（测地距离）从字面上推测，就是地表两点之间的最短路径的距离。而在数学或几何领域，通常出现在图网络以及网格表面的距离计算之中。当 Average  Geodesic Distance 作为一种三维几何特征时，可以用来度量三维模型点与模型中心的偏离程度。

## Average Geodesic Distance 的介绍

在介绍 Average Geodesic Distance 之前，首先介绍一下 Geodesic Distance。

"geodesic"（测地线）一词来源于  geodesy（测地学），是一门测量地球大小和形状的学科。就从 geodesic 的本意来说，就是地球表面两点之间的最短路径，因此  Geodesic Distance  最初是指地球表面两点之间的最短距离，但随后这一概念便被推广到了数学空间的测量之中。例如在图论中，Geodesic Distance  就是图中两节点的最短路径的距离。这与我们平时在几何空间通常用到的 Euclidean  Distance（欧氏距离），即两点之间的最短距离，有所区别。在下图中，两个黑点的 Euclidean Distance  应是用虚线所表示的线段的长度 *d*15，而 Geodesic Distance 作为实际路径的最短距离，其距离应为沿途实线段距离之和的最小值，即 *d*12+*d*23+*d*34+*d*45。

![distance-compare](Average Geodesic Distance.assets/distance-compare.jpg)

在三维网格中，Geodesic Distance 就是两顶点沿网格表面最短路径的距离。如下图所示，标注出的绿色线段长度就是顶点 *v**s* 到顶点 *v**t* 的 Geodesic Distance。

![shorteset-path-on-mesh](Average Geodesic Distance.assets/shorteset-path-on-mesh.jpg)

另外，对于计算三维点云中两点的 Geodesic Distance，首先要利用点云中所有点构建出一个类似于网格的表面结构的图，随后通过找到两点在图中的最短路径，再去计算 Geodesic Distance。

在了解了  Geodesic Distance 后，就可以很容易理解 Average Geodesic Distance  的概念。其概念就是给定一个点，计算该点到剩余所有点的 Geodesic Distance 的平均值。用这个 Average Geodesic  Distance  作为一个三维点的几何特征时，越靠近中心部位的点的值会越低，而边缘末端的点的值会相对更高，所以很容易通过此特征捕获到这两种类型的区域。

## Average Geodesic Distance 的原理

其实  Average Geodesic Distance 的原理并不复杂，需要先得到每对点的 Geodesic Distance，而为了得到这个  Geodesic Distance，关键是获得两点之间的最短路径。目前已经存在很多关于寻找最短路径的算法，但其中最经典、最为人所熟知的算法便是 [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)。现有的很多算法书上已经有详尽的解释和成熟的实现，这里便不再赘述了。随后，便可对每一个三维点，计算其与剩余点的 Geodesic Distance，并求出它们的平均，作为该点的几何特征值。

需要注意的是，这看似简单的算法原理在实际的计算中还是相当耗时的，会随着三维点数的增加，耗时呈指数级的增长。但由于实际中往往并不需要用到非常精确的  Geodesic Distance，因此，目前有很多加速计算过程和近似结果的工作，在文章的末尾会列出一些相关参考文献。

## Average Geodesic Distance 的实现

根据上述的原理，计算每个三维点 Average Geodesic Distance 几何特征的参考伪代码如下：

For each point {     double totalDistance = 0;     int totalCount = 0;     For each otherPoint {         FindShortestPaths();         double geodesicDistance = ComputeShortestDistance();         totalDistance += geodesicDistance;         ++totalCount;     }     double averageGeodesicDistance = totalDistance / totalCount;     averageGeodesicDistance = normalize(averageGeodesicDistance); }

| 123456789101112 | For each point {    double totalDistance = 0;    int totalCount = 0;    For each otherPoint {        FindShortestPaths();        double geodesicDistance = ComputeShortestDistance();        totalDistance += geodesicDistance;        ++totalCount;    }    double averageGeodesicDistance = totalDistance / totalCount;    averageGeodesicDistance = normalize(averageGeodesicDistance);} |
| --------------- | ------------------------------------------------------------ |
|                 |                                                              |

下面是实际项目程序中用  Average Geodesic Distance  作为每个点的几何特征值的可视化结果。首先，由于项目以点云作为输入，所以要对三维模型进行采样，为了保证点云的数量和兼具计算效率，采样点的数量设为20000。但在计算点云中点的 Average  Geodesic Distance 的过程中，需要比直接处理三维网格多一步，那就是要先建立点云中点之间的图，然后再去计算点与点之间的  Geodesic Distance，并得到最终的 Average Geodesic  Distance。最后，将该几何特征值归一化后，用红色代表最远值（1.0），蓝色代表最近值（0.0）。

![samples_feature_AGD](Average Geodesic Distance.assets/samples_feature_AGD.png)

## 参考文献

Noyel  G, Angulo J, Jeulin D. Fast computation of all pairs of geodesic  distances[J]. Image Analysis, Stereology, 2011, 30(2): 101-109.

Surazhsky  V, Surazhsky T, Kirsanov D, et al. Fast exact and approximate geodesics  on meshes[C]//ACM transactions on graphics (TOG). ACM, 2005, 24(3):  553-560.

Novotni M, Klein R. Gomputing geodesic distances on triangular meshes[J]. 2002.

Skiena  S. Dijkstra’s algorithm[J]. Implementing Discrete Mathematics:  Combinatorics and Graph Theory with Mathematica, Reading, MA:  Addison-Wesley, 1990: 225-227.

Geodesic. <https://en.wikipedia.org/wiki/Geodesic>

Distance (graph theory). <https://en.wikipedia.org/wiki/Distance_(graph_theory)>

Triangulated Surface Mesh Shortest Paths. <http://doc.cgal.org/latest/Surface_mesh_shortest_path/index.html>
