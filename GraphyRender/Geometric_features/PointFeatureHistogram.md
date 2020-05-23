# 几何特征系列：Point Feature Histogram（点特征直方图）



2016-07-23



LEEMANCHIU



[1 Comment](http://lemonc.me/point-feature-histogram.html#comments)



[理工男](http://lemonc.me/category/science-engineering)

对于点云中的特定点，表面的法向和估算曲率是基本的几何特征描述。虽然计算简单且快速，但在大部分情况的点云中会包含很多相似或相同的特征值，导致不能获得更多的信息和特性。因此，这篇文章将介绍一个常用的点云几何特征描述算子  Point Feature Histogram，中文名译作「点特征直方图」，通常被简称为 PFH。PFH  该几何特征能同时结合了三维坐标轴数据和表面法线的信息，所以能捕获到点云中更多的信息，下面将对 PFH 作更进一步的介绍。

## Point Feature Histogram 的介绍

PFH 是对中心点邻域范围内空间差异的一种量化，通过数理统计的方法获得一个用于描述中心点邻域几何信息的直方图。PFH   的目的是将一个点的邻域均值曲率几何特性编码到多维的直方图中，这样的高维数据提供了非常具有信息量的特征表达。对点云不仅在六维变换（旋转及平移各三维）下具有不变性，还能很好地适应不同程度的采样或不同程度的噪声影响。

一个点特征直方图的表达基于点与其 *k* 邻域之间的关系和它们的法线，简单来说，它会通过考虑法线之间所有的相互作用，尽可能地去捕获采样表面的变化情况，以描述它的几何特征。可见，点云的法线质量对于该几何特征尤为重要。

## Point Feature Histogram 的原理

接下来，将通过一些示意图来讲述 PFH 的计算原理。下图中显示了一个中心点 (*p**q*) 的 PFH 计算影响区域，其中该点是 (*p**q*) 是三维空间中半径为 *r* 的球体中心点，即红色点所示。该中心点与其所有在半径为 *r* 的球体内部的 *k* 个邻域点两两互相连接组成一个网络，最终的 PFH 几何特征将通过计算邻域内这些所有点对之间的变化关系而得到的直方图。因此，计算每个点的 PFH 的计算复杂度为 *O*(*k*2)。

![pfh_diagram](Point Feature Histogram.assets/pfh_diagram.png)

为了计算两点之间的相对差异，给定两点 *p*1 和 *p*2 ，且各自的法向分别为 *n*1 和 *n*2，并在其中一个点上定义了一个局部的坐标系，三个单位向量 *u*、*v*、*w* 的建立规则如下：



*u*=*n*1





*v*=*u*×*p*2−*p*1∥*p*2−*p*1∥2





*w*=*u*×*v*



 其中，

∥*p*2−*p*1∥2

 的含义是两点 

*p*1

 和 

*p*2

 之间的欧式距离。然后利用上述的 

*u**v**w*

 坐标系，

*n*1

 和 

*n*2

 的差异可用三个角度

(*α*,*ϕ*,*θ*)

 来表达，其中的创建规则如下：



*a*=*v*⋅*n*2





*u*⋅*p*2−*p*1∥*p*2−*p*1∥2





*θ*=arctan(*w*⋅*n*2,*u*⋅*n*2)





两点的空间坐标系如下图所示。

![pff_uvw](Point Feature Histogram.assets/pff_uvw.png)

随后，对于 *k* 邻域内的所有点对，计算这个三元组⟨*α*,*ϕ*,*θ*⟩。可见，这种表达方式仅仅用了3个参数，就能涵盖两个点原本信息中的12个参数（每个点的位置和法线各需要3个参数表达空间信息）。最后，将三元组⟨*α*,*ϕ*,*θ*⟩ 放入到直方图的各个子区间之中，以形成最终的 PFH 特征表达。

## Point Feature Histogram 的实现

计算完中心点领域内 *n* 个点之间的所有三元组，一共会得到 *C*2*n* 个三元组。通常情况下，三元组中的每个特征值会被分成 *b* 等分，所以该三元组会形成一个 *b*3 维的直方图，每一个维代表了其中某个值的某一个范围区间。然后，再去统计出现在各个子区间的频率即可。在实际项目中计算 PFH 时，我们的设置 *b*=5，即把每个特征值分为5等分，因此 PFH 是一个125维的向量。

在下图中，展示了一个点云中不同点的点特征直方图的例子。不同区域或不同物体的点，他们的 PFH 会有很大的区别，而对于相似的区域，则会有着相似的直方图分布。

![pfh_example](Point Feature Histogram.assets/pfh_example.jpg)

利用 PFH 这个几何特征，可根据相似点的特征值会具有相似的直方图这一特性，进行聚类。下图是根据 PFH 特征值，对点云场景中的物体进行分类的应用结果。

![pfh_cluster](Point Feature Histogram.assets/pfh_cluster.png)

## 参考文献

Rusu  R B, Marton Z C, Blodow N, et al. Learning informative point classes  for the acquisition of object model maps[C]//Control, Automation,  Robotics and Vision, 2008. ICARCV 2008. 10th International Conference  on. IEEE, 2008: 643-650.

Zhao X, Wang H, Komura T. Indexing 3d  scenes using the interaction bisector surface[J]. ACM Transactions on  Graphics (TOG), 2014, 33(3): 22.

Wahl E, Hillenbrand U, Hirzinger  G. Surflet-pair-relation histograms: a statistical 3D-shape  representation for rapid classification[C]//3-D Digital Imaging and  Modeling, 2003. 3DIM 2003. Proceedings. Fourth International Conference  on. IEEE, 2003: 474-481.

Point Feature Histograms (PFH) descriptors. <http://pointclouds.org/documentation/tutorials/pfh_estimation.php>

Overview and Comparison of Features. <https://github.com/PointCloudLibrary/pcl/wiki/Overview-and-Comparison-of-Features>
