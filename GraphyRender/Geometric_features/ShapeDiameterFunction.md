# 几何特征系列：Shape Diameter Function（形状直径函数）



2016-07-19



LEEMANCHIU



[1 Comment](http://lemonc.me/shape-diameter-function.html#comments)



[理工男](http://lemonc.me/category/science-engineering)

这篇文章将介绍  Shape Diameter Function，中文名译作「形状直径函数」。Shape Diameter Function  可以用来表示三维模型体积到其包围网格表面的映射，可直观地理解为模型局部形状的直径，也就是模型上顶点或面片位置上的局部直径。

## Shape Diameter Function 的介绍

Shape  Diameter Function 建立了网格表面和其所在包围体体积的联系，更具体来说，就是定义了网格表面到其所对区域的距离。Shape  Diameter Function  可以看作是网格面片所在包围体的厚度，因此，可用它来区分宽度或厚度不同的区域。其最初的应用，就是根据相似部位具有相似的 Shape  Diameter Function 值，对三维模型进行分割，详情可查看下方参考文献给出的文献：[Consistent mesh partitioning and skeletonisation using the shape diameter function](https://www.semanticscholar.org/paper/Consistent-mesh-partitioning-and-skeletonisation-Shapira-Shamir/64cdd1017e47f2874584f707afe3b7ae228cd918/pdf)。

如下图所示，图片左边是将 Shape  Diameter Function 应用到一个三维大象模型中的结果，Shape Diameter Function  值最高的区域用红色表示，而最低的区域则用蓝色表示。可以看到，在象牙和耳朵区域呈蓝色，Shape Diameter Function  值较低，意味着三维模型这些部位较细或较薄。相反，在身体等较宽的部位则 Shape Diameter Function  更高。在图片右边，则是根据不同区域的 Shape Diameter Function 值进行聚类并分割后的结果。

![sdf-segmentation](Shape Diameter Function.assets/sdf-segmentation.jpg)

当 Shape  Diameter Function  作为三维几何特征时，可以看作是模型表面的每个点对应所在区域形状的直径。当三维模型在受到如平移、旋转、简化等变化，尤其是姿势的变化时，往往仍能维持原有的形状特征。因此，用 Shape  Diameter Function 作为局部特征时，在三维模型进行如姿势的变化变形后并不会受到很大的影响，所以在这种场合 Shape  Diameter Function 具有不错的鲁棒性。如下图所示，展示了 Shape Diameter Function  值和分割结果并不会受到姿势的变化而产生太大的影响。

![sdf-pose_changes](Shape Diameter Function.assets/sdf-pose_changes.png)

## Shape Diameter Function 的原理

接下来将介绍计算每个  Shape Diameter Function  值的过程原理。首先，在三维模型表面网格上选取一个顶点，作一个以该顶点为圆锥顶点、顶点法向量的逆方向为中心线方向的圆锥体。然后，从该顶点上引出若干条圆锥体范围内的射线交于模型的表面网格，并保留与相交点法线方向相同的射线（即夹角小于90°认为是方向相同），这是为了抛弃可能与面错误相交的射线。最后，对所有射线的长度进行加权统计，即可得到该顶点的  Shape Diameter Function 值。

## Shape Diameter Function 的实现

根据实际的经验，圆锥角的角度通常为120°并均匀地取30条射线进行加权统计，求得  Shape Diameter Function  的近似值。但在实际统计的过程中，我们会发现，基于统计的方法会容易受到异常值或离群值的影响。如下图所示的例子，这是两个中心镂空圆环的顶视图。

![SDF_outliers](Shape Diameter Function.assets/SDF_outliers.jpg)

图的左边是我们预期从内部发出射线的结果，而图的右边则是从外部发出射线时，出现了离群值的情况，那么这时候就会导致内侧的  Shape Diameter Function 值与外部的 Shape Diameter Function  值相差较大的情况。理论上，内侧和外侧的 Shape Diameter Function 值应该相同，但从结果来看这里产生了不合定义逻辑的结果。

所以，在实际的过程中会添加很多判断条件来尽可能地确保 Shape Diameter Function 值的准确性，如移除一些离群值或去掉一些错误的相交射线等。但这里为了能更直观地展示实现流程，就选择了比较基本的实现方法，参考的伪代码如下：

coneRange = rad(60.0f); numRays = 30; For each sourcePoint {     totalValue = 0;     totalWeight = 0;     For each ray {         random direction on unit sphere         if (ray direction within coneRange) {             if (ray intersects with mesh) {                 rayLength = getRayIntersection();                 totalValue += rayLength;                 rayWeight = dot(radyDir, -normarlDirection);                 totalWeight += rayWeight;             }         }     }     SDFValue = totalValue / totalWeight; }

| 123456789101112131415161718 | coneRange = rad(60.0f);numRays = 30;For each sourcePoint {    totalValue = 0;    totalWeight = 0;    For each ray {        random direction on unit sphere        if (ray direction within coneRange) {            if (ray intersects with mesh) {                rayLength = getRayIntersection();                totalValue += rayLength;                rayWeight = dot(radyDir, -normarlDirection);                totalWeight += rayWeight;            }        }    }    SDFValue = totalValue / totalWeight;} |
| --------------------------- | ------------------------------------------------------------ |
|                             |                                                              |

另外，对于计算三维点云的  Shape Diameter Function  值时会稍有不同，因为没有面片的信息，所以无法得到射线相交的一系列结果。所以，实现时可以通过点云上的点与圆锥范围内的点相连来模拟从一个点射出射线。判断的条件与网格的情况类似，但更为复杂，因为需要考虑到两个相连的点，是否真正在局部相对。

## 参考文献

Shapira  L, Shamir A, Cohen-Or D. Consistent mesh partitioning and  skeletonisation using the shape diameter function[J]. The Visual  Computer, 2008, 24(4): 249-259.

Triangulated Surface Mesh Segmentation. <http://doc.cgal.org/latest/Surface_mesh_segmentation/index.html>

More details on the Shape Diameter Function filter in MeshLab. <http://3dgraphicsprogramming.blogspot.jp/2011/08/meshlab-plugin-development-depth.html>

[![LEEMANCHIU](Shape Diameter Function.assets/gintama.jpeg)](http://lemonc.me)



### [LEEMANCHIU](http://lemonc.me)



香港科技大学在读博士研究生，曾是中国科学院大学的硕士研究生
[联系邮箱](mailto:i@lemonc.me) | [Personal Homepage](https://www.cse.ust.hk/~wlibs/)
