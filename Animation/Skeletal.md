# （原）Skeletal

2018年10月9日 星期二

14:49

@author: 白袍小道

@来源:     Advanced Animation with DirectX,  游戏引擎架构 

 

[TOC]

引言：

​         3D模型动画的基本原理是让**模型中各顶点的位置随时间变化**。主要种类有**Morph动画**，**关节动画**和**骨骼蒙皮动画**(Skinned Mesh)。从动画数据的角度来说，三者一般都采用关键帧技术，即只给出关键帧的数据，其他帧的数据使用插值得到。但由于这三种技术的不同，关键帧的数据 是不一样的。

​         1、Morph（渐变，变形）动画是直接指定动画每一帧的顶点位置，其动画关键中存储的是Mesh所有顶点在关键帧对应时刻的位置。

​         2、关节动画的模型不是一个整体的Mesh,而是分成很多部分(Mesh)，通过一个父子层次结构将这些分散的Mesh组织在一起，父Mesh带动其下子 Mesh的运动，各Mesh中的顶点坐标定义在自己的坐标系中，这样各个Mesh是作为一个整体参与运动的。动画帧中设置各子Mesh相对于其父Mesh 的变换（主要是旋转，当然也可包括移动和缩放），通过子到父，一级级的变换累加（当然从技术上，如果是矩阵操作是累乘）得到该Mesh在整个动画模型所在 的坐标空间中的变换（从本文的视角来说就是世界坐标系了，下同），从而确定每个Mesh在世界坐标系中的位置和方向，然后以Mesh为单位渲染即可。关节 动画的问题是，各部分Mesh中的顶点是固定在其Mesh坐标系中的，这样在两个Mesh结合处就可能产生裂缝。

​         3、骨骼蒙皮动画即Skinned Mesh了，骨骼蒙皮动画的出现解决了关节动画的裂缝问题，而且效果非常酷。骨骼动画的基本原理可概括为：在骨骼控制下，通过顶点混合动态计算蒙皮网格的顶点，而骨骼的运动相对于其 父骨骼，并由动画**关键帧数据驱动**一个骨骼动画通常包括骨骼层次结构数据，网格(Mesh)数据，网格蒙皮数据(skin info)和骨骼的动画(关键帧)数据。下面将具体分析。

![计算机生成了可选文字: Pelvis Joint 图1L5：角色的髋关节连接了个其他关节（脊椎下部、尾、双腿），因而产生了4根骨头。](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image004.jpg)

#  

#  

# SKeletal相关知识点简介

## 一、骨骼系统

1、骨骼

骨骼节点可理解为一个坐标空间。

关节可理解为骨骼坐标空间的原点，既决定了骨骼空间的位置，又是骨骼空间的旋转和缩放中心。

（Mesh，Skin，Bone）：Mesh是利用Skin依附在Bone上，或者说Bone通过Skin驱动了Mesh。

 

2、骨骼层次

骨骼层次就是**嵌套**的坐标空间，为何？方便和搞笑，容易转换传递

根骨骼：整个骨骼体系在世界坐标系中的位置在微软X文件中，一般有一个Scene_Root节点，这算一个额外的骨骼 吧，他的变换矩阵为单位阵，表示他初始位于世界原点，而真正骨骼的根Bip01，作为Scene_root的子骨骼，其变换矩阵表示相对于root的位置.

![计算机生成了可选文字: root splne_02 splne_03 ÷cVic」 -'•y•upperarm」 ÷lowerarm」 D•y•i'记e一01」 ）pinky-Ol」 ）．新tm妇一01」 ．新“訕m」wist_01」 *upperarm_twist_01」 clavicle_r *upperarm_twist_ol_r neck_01 •i•thlgh_l *thigh_r ．；．Ik_hand_root](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image006.jpg)

 

3、骨骼变化

某个骨骼的变换（TransformMatrix）变了，这时就要根据新的变换来计算，所以 这个过程一般称作UpdateBoneMatrix。因为骨骼的变换都是相对父的，要变换顶点必须使用世界变换矩阵，所以这个过程是根据更新了的某些骨骼 的骨骼变换矩阵（TransformMatrix）计算出所有骨骼的世界变换矩阵（也即CombinedMatrix）

 

3、蒙皮和权重

Skinned Mesh中Mesh是作为皮肤使用，蒙在骨骼之上的。为了让普通的Mesh具有蒙皮的功能，必须添加蒙皮信息，即Skin info。我们知道Mesh是由顶点构成的，建模时顶点是定义在模型自身坐标系的，即相对于Mesh原点的，而骨骼动画中决定模型顶点最终世界坐标的是骨 骼，所以要让骨骼决定顶点的世界坐标，这就要将顶点和骨骼联系起来，Skin info正是起了这个作用。

Skin info的作用是使用各个骨骼的变换矩阵对顶点进行变换并乘以权重，这样某块骨骼只能对该顶点产生部分影响。各骨骼权重之和应该为1

 

4、顶点平移变化

骨骼动画中决定模型顶点最终世界坐标的是骨骼，所以要让骨骼决定顶点的世界坐标

mesh vertex (defined in mesh space)---<BoneOffsetMatrix>---Bone space---<BoneCombinedTransformMatrix>---World

5、顶点混合

顶点混合后得到了顶点新的 世界坐标，对所有的顶点执行vertex blending后，从Mesh的角度看，Mesh deform(变形)了，变成动画需要的形状了。

对于多块骨骼，对每块骨骼执行这个过程并将结果根据权重混合(即vertex blending)就得到顶点最终的世界坐标

另外值得一说（骨骼动画的精髓消除了关节处的裂缝）。

 

 

![计算机生成了可选文字: 0 0 0AnimationNotlfies CurveName Type 厶佣mCurves Weight 0 AutiBones](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image008.jpg)

骨骼数据结构

![计算机生成了可选文字: StructJoint Matrix4x3minvBindPose; m_name生 //绑定姿势之逆变换 ／/人类可读的关节名字 巳些二二二二二二二二二二二二二二@婴些鼕苎0皇些二二二二二二二二二?乙二苎苎堕]或OxFF代表根关节 Skeleton Struct U32 Joint* m_jointCount; m_aJoa.nt 关节薮目 关节数组](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image010.jpg)

##  

## 二、骨骼动画

 

3D模型动画的基本原理是让模型中各顶点的位置**随时间变化**。

 

驱动：骨骼的位置随时间变化，顶点位置随骨骼变化。

2.1      所以动画数据 中必然包含的是骨骼的运动信息，可以在动画帧中包含某时刻骨骼的Transform Matrix。

2.2     播放动画时，给出当前播放的时间值，对于每块需要动画的骨骼，根据这个值找出该骨骼前后两个关键帧信息，根据时间差进行适合的插值运算。

(这里就出现关键帧，插值，以及后续出现的混合，蒙太奇等问题和需求，）

 

## 三、姿势和动画片段

### 1、绑定姿势

把网格当作正常的、没有蒙皮、完全不涉及骨骼的三角形网格来渲染的姿势。

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image012.jpg)

 

### 2、局部姿势

使用局部姿势来描述关节姿势相对于父的姿势，局部姿势几乎都可以用SQT格式存储。

![计算机生成了可选文字: 数学上，关节姿势就是一个仿射变换(affinetransformation)力第j个关节可表示 为4×4仿射变换矩阵pj，此矩阵由一个平移矢量T丿、3×3对角缩放矩阵S尸及3x3旋转矩 VfR所构成。整个骨髂的姿势pskel可写成所有姿势P丿的集合，当中j的范围是0、N一1： P](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image014.jpg)

未完待续:接着是动画片段，关键帧、动画融合(Blend，分层，叠加，程序化动画【IK\物理】）部分

 

 

（原）骨骼动画-关键帧

2018年10月9日 星期二

15:12

 

 

（原）骨骼动画-融合

2018年10月9日 星期二

15:13

 

 

（原）骨骼动画-蒙太奇

2018年10月9日 星期二

15:13
