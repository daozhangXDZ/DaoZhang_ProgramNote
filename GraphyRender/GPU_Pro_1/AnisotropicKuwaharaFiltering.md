## GPU上的各项异性的Kuwahara滤波 | Anisotropic Kuwahara Filtering on the GPU

这章中介绍一种各向异性的Kuwahara滤波器[Kyprianidis et al.  09]。各向异性的Kuwahara滤波器是Kuwahara滤波器的一种广义上的变体，通过调整滤波器的形状，比例和方向以适应输入的局部结构，从而避免了失真。由于这种适应性，定向图像特征被更好地保存和强调，得到了整体更清晰的边缘和更具特色的绘画效果。

[
![img](AnisotropicKuwaharaFiltering.assets/fccbcccfbcbc250aa592f1fe9a61c395.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/fccbcccfbcbc250aa592f1fe9a61c395.png)

图 原始图像（左），对各向异性的Kuwahara滤波输出（右）。沿着局部特征方向产生绘画般的增强效果，同时保留形状边界。

### 

### 12.1 Kuwahara滤波器（Kuwahara Filtering）

Kuwahara滤波器背后的一般思想是将滤波器内核分成四个重叠一个像素的矩形子区域。滤波器的响应由具有最小方差的子区域的平均值来定义。

[
![img](AnisotropicKuwaharaFiltering.assets/7de17304312d5c3977eaeb3bc01054de.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/7de17304312d5c3977eaeb3bc01054de.png)

图 Kuwahara滤波器将滤波器内核分成四个矩形子区域。然后过滤器响应由具有最小方差的子区域的平均值来定义

[
![img](AnisotropicKuwaharaFiltering.assets/089fbc7afe80d3d50f9be009e77f1912.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/089fbc7afe80d3d50f9be009e77f1912.png)

图 Kuwahara滤波器的输出效果图

### 

### 12.2 广义Kuwahara滤波器（Generalized Kuwahara Filtering）

而广义Kuwahara滤波器，为了克服不稳定次区域选择过程的局限性，定义了一个新的标准。结果被定义为次区域平均值的加权总和，而不是选择一个单独的次区域。权重是根据子区域的差异来定义的。  这导致区域边界更平滑并且失真更少。为了进一步改善这一点，矩形子区域被扇区上的平滑权重函数所取代：

[
![img](AnisotropicKuwaharaFiltering.assets/fba981a4c3dcfa4ef47d8b70838ed4a6.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/fba981a4c3dcfa4ef47d8b70838ed4a6.png)

图 广义的Kuwahara滤波器使用定义在光盘扇区上的加权函数。滤波过滤器响应被定义为局部平均值的加权总和，其中对具有低标准偏差的那些平均值赋予更多的权重。

[
![img](AnisotropicKuwaharaFiltering.assets/c266aa1040c5202e07fe01e096ed5554.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/c266aa1040c5202e07fe01e096ed5554.png)

图 广义Kuwahara滤波器的输出效果图

### 

### 12.3 各向异性Kuwahara滤波器（Anisotropic Kuwahara Filtering）

广义的Kuwahara滤波器未能捕获定向特征并会导致集群的失真。而各向异性的Kuwahara滤波器通过使滤波器适应输入的局部结构来解决这些问题。在均匀区域中，滤波器的形状应该是一个圆形，而在各向异性区域中，滤波器应该变成一个椭圆形，其长轴与图像特征的主方向一致。

[
![img](AnisotropicKuwaharaFiltering.assets/5b62cbc4a5323e108f039da9e93b7071.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/5b62cbc4a5323e108f039da9e93b7071.png)

图 各向异性Kuwahara滤波器图示
