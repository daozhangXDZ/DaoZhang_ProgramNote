# 点云概念与点云处理

点云概念

点云与三维图像的关系：三维图像是一种特殊的信息表达形式，其特征是表达的空间中三个维度的数据，表现形式包括：深度图（以灰度表达物体与相机的距离），几何模型（由CAD软件建立），点云模型（所有逆向工程设备都将物体采样成点云）。和二维图像相比，三维图像借助第三个维度的信息，可以实现天然的物体——背景解耦。点云数据是最为常见也是最基础的三维模型。点云模型往往由测量直接得到，每个点对应一个测量点，未经过其他处理手段，故包含了最大的信息量。这些信息隐藏在点云中需要以其他提取手段将其萃取出来，提取点云中信息的过程则为三维图像处理。
点云的概念：点云是在同一空间参考系下表达目标空间分布和目标表面特性的海量点集合，在获取物体表面每个采样点的空间坐标后，得到的是点的集合，称之为“点云”（Point Cloud）。
点云的获取设备：RGBD设备是获取点云的设备，比如PrimeSense公司的PrimeSensor、微软的Kinect、华硕的XTionPRO。
点云的内容：根据激光测量原理得到的点云，包括三维坐标（XYZ）和激光反射强度（Intensity），强度信息与目标的表面材质、粗糙度、入射角方向，以及仪器的发射能量，激光波长有关。
根据摄影测量原理得到的点云，包括三维坐标（XYZ）和颜色信息（RGB）。
结合激光测量和摄影测量原理得到点云，包括三维坐标（XYZ）、激光反射强度（Intensity）和颜色信息（RGB）。
点云的属性：空间分辨率、点位精度、表面法向量等。
点云存储格式：*.pts; *.asc ; *.dat; .stl ; [1] .imw；.xyz；.las。LAS格式文件已成为LiDAR数据的工业标准格式，LAS文件按每条扫描线排列方式存放数据,包括激光点的三维坐标、多次回波信息、强度信息、扫描角度、分类信息、飞行航带信息、飞行姿态信息、项目信息、GPS信息、数据点颜色信息等。

C–class（所属类）
F一flight（航线号）
T一time（GPS时间）
I一intensity（回波强度）
R一return（第几次回波）
N一number of return（回波次数）
A一scan angle（扫描角）
RGB一red green blue（RGB颜色值）
点云的数据类型：
（1）pcl::PointCloudpcl::PointXYZ
PointXYZ 成员：float x，y，z;表示了xyz3D信息，可以通过points[i].data[0]或points[i].x访问点X的坐标值
（2）pcl::PointCloudpcl::PointXYZI
PointXYZI成员：float x, y, z, intensity; 表示XYZ信息加上强度信息的类型。
（3）pcl::PointCloudpcl::PointXYZRGB
PointXYZRGB 成员：float x,y,z,rgb; 表示XYZ信息加上RGB信息，RGB存储为一个float。
（4）pcl::PointCloudpcl::PointXYZRGBA
PointXYZRGBA 成员：float x , y, z; uint32_t rgba; 表示XYZ信息加上RGBA信息，RGBA用32bit的int型存储的。
（5） PointXY 成员：float x,y;简单的二维x-y点结构
（6）Normal结构体：表示给定点所在样本曲面上的法线方向，以及对应曲率的测量值，用第四个元素来占位，兼容SSE和高效计算。
点云的处理

点云处理的三个层次：Marr将图像处理分为三个层次，低层次包括图像强化，滤波，关键点/边缘检测等基本操作。中层次包括连通域标记（label），图像分割等操作。高层次包括物体识别，场景分析等操作。工程中的任务往往需要用到多个层次的图像处理手段。
PCL官网对点云处理方法给出了较为明晰的层次划分，如图所示。

此处的common指的是点云数据的类型，包括XYZ，XYZC，XYZN，XYZG等很多类型点云，归根结底，最重要的信息还是包含在pointpcl::point::xyz中。可以看出，低层次的点云处理主要包括滤波（filters），关键点（keypoints）/边缘检测。点云的中层次处理则是特征描述（feature），分割（segmention）与分类。高层次处理包括配准（registration），识别（recognition）。可见，点云在分割的难易程度上比图像处理更有优势，准确的分割也为识别打好了基础。
低层次处理方法:
①滤波方法：双边滤波、高斯滤波、条件滤波、直通滤波、随机采样一致性滤波。②关键点：ISS3D、Harris3D、NARF，SIFT3D
中层次处理方法：
①特征描述：法线和曲率的计算、特征值分析、SHOT、PFH、FPFH、3D Shape Context、Spin Image
②分割与分类：
分割：区域生长、Ransac线面提取、全局优化平面提取
　　　K-Means、Normalize Cut（Context based）
　　　3D Hough Transform(线、面提取)、连通分析
分类：基于点的分类，基于分割的分类，基于深度学习的分类（PointNet，OctNet）
高层次处理方法：
①配准：点云配准分为粗配准（Coarse Registration）和精配准（Fine Registration）两个阶段。
精配准的目的是在粗配准的基础上让点云之间的空间位置差别最小化。应用最为广泛的精配准算法应该是ICP以及ICP的各种变种（稳健ICP、point to plane ICP、Point to line ICP、MBICP、GICP、NICP）。
粗配准是指在点云相对位姿完全未知的情况下对点云进行配准，可以为精配准提供良好的初始值。当前较为普遍的点云自动粗配准算法包括基于穷举搜索的配准算法和基于特征匹配的配准算法。
基于穷举搜索的配准算法：遍历整个变换空间以选取使误差函数最小化的变换关系或者列举出使最多点对满足的变换关系。如RANSAC配准算法、四点一致集配准算法（4-Point Congruent Set, 4PCS）、Super4PCS算法等……
基于特征匹配的配准算法：通过被测物体本身所具备的形态特性构建点云间的匹配对应，然后采用相关算法对变换关系进行估计。如基于点FPFH特征的SAC-IA、FGR等算法、基于点SHOT特征的AO算法以及基于线特征的ICL等…
②SLAM图优化
Ceres（Google的最小二乘优化库，很强大）， g2o、LUM、ELCH、Toro、SPA
SLAM方法：ICP、MBICP、IDC、likehood Field、NDT
③三维重建
泊松重建、 Delaunay triangulations、表面重建，人体重建，建筑物重建，树木重建。结构化重建：不是简单的构建一个Mesh网格，而是为场景进行分割，为场景结构赋予语义信息。场景结构有层次之分，在几何层次就是点线面。实时重建：重建植被或者农作物的4D（3D+时间）生长态势；人体姿势识别；表情识别；
④点云数据管理：点云压缩，点云索引（KD、Octree），点云LOD（金字塔），海量点云的渲染

（此帖主要是进行知识点梳理，方便自己与大家的学习进步，大量引用了拜读过的网友的帖子内容，若有描述不当或引用有争议的地方，欢迎广大网友批评指正……每周五晚上更帖，求进步）

