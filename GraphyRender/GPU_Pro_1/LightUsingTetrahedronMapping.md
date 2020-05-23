## 基于四面体映射实现全向光阴影映射 | Shadow Mapping for Omnidirectional Light Using Tetrahedron Mapping

阴影映射（Shadow mapping）是用于三维场景渲染阴影的一种常用方法。William的原始Z-缓冲器阴影映射算法〔[Williams 78]是用于方向光源的，需要一种不同的方法来实现全向光（Omnidirectional Light）的阴影。

有两种流行的方法来接近全向光：一个是立方体映射（cube mapping ）[Voorhies and Foran  94]和另一个是双抛物面映射（dual-paraboloid mapping）[Heidrich and Seidel  98]。而在本章中，提出了一种全新的使用四面体映射（tetrahedron mapping）的全向光阴影映射技术。

[
![img](LightUsingTetrahedronMapping.assets/35e8f5273e7fd46cb0231a8a238a73f6.jpg)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/35e8f5273e7fd46cb0231a8a238a73f6.jpg)

图 四个点光源，并使用四面体阴影映射与模板缓冲和硬件阴影映射得到渲染效果。二维深度纹理尺寸为1024×1024
