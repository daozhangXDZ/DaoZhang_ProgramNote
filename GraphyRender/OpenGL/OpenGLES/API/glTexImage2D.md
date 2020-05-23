# GLES2.0中文API-glTexImage2D

# 名称

glTexImage2D- 指定一个二维的纹理图片

## C规范

 

`void **glTexImage2D**(`GLenum *target*, 

​                    GLint *level*, 

​                    GLint *internalformat*, 

​                    GLsizei *width*, 

​                    GLsizei *height*, 

​                    GLint *border*, 

​                    GLenum *format*, 

​                    GLenum *type*, 

​                    const GLvoid * *data*`)`;

## 参数

*target*

指定活动纹理单元的目标纹理。必须是GL_TEXTURE_2D,GL_TEXTURE_CUBE_MAP_POSITIVE_X,GL_TEXTURE_CUBE_MAP_NEGATIVE_X,GL_TEXTURE_CUBE_MAP_POSITIVE_Y,GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,GL_TEXTURE_CUBE_MAP_POSITIVE_Z,或GL_TEXTURE_CUBE_MAP_NEGATIVE_Z.

*level*

  指定细节级别，0级表示基本图像，n级则表示Mipmap缩小n级之后的图像（缩小2^n）

*internalformat*

  指定纹理内部格式，必须是下列符号常量之一：GL_ALPHA，GL_LUMINANCE，GL_LUMINANCE_ALPHA，GL_RGB，GL_RGBA。

*width height*

  指定纹理图像的宽高，所有实现都支持宽高至少为64 纹素的2D纹理图像和宽高至少为16 纹素的立方体贴图纹理图像 。

*border*

  指定边框的宽度。必须为0。

*format*

  指定纹理数据的格式。必须匹配internalformat。下面的符号值被接受：GL_ALPHA，GL_RGB，GL_RGBA，GL_LUMINANCE，和GL_LUMINANCE_ALPHA。

*type*

  指定纹理数据的数据类型。下面的符号值被接受：GL_UNSIGNED_BYTE，GL_UNSIGNED_SHORT_5_6_5，GL_UNSIGNED_SHORT_4_4_4_4，和GL_UNSIGNED_SHORT_5_5_5_1。

*data*

  指定一个指向内存中图像数据的指针。

## 描述

  纹理将指定纹理图像的一部分映射到纹理化为活动的每个图形基元上。当前片段着色器或顶点着色器使用内置纹理查找函数时，纹理处于活动状态。

  要定义纹理图像，请调用glTexImage2D。参数描述纹理图像的参数，如高度，宽度，细节级别（详见[glTexParameter](https://blog.csdn.net/flycatdeng/article/details/82595267)）以及格式。最后三个参数描述了图像在内存中的表示方式。

   数据从data一系列无符号字节或短路中读取，具体取决于type。当type是GL_UNSIGNED_BYTE，每个字节被解释为一个颜色分量。当type是以下当中的一个GL_UNSIGNED_SHORT_5_6_5，GL_UNSIGNED_SHORT_4_4_4_4或GL_UNSIGNED_SHORT_5_5_5_1，各无符号短值被解释为包含所有组件用于单个纹素，利用根据设置在颜色分量format。颜色分量被视为一个，两个，三个或四个值的组，也是基于format。组件组被称为纹理元素（纹素）。

  width × height个纹素将从内存中读取（起始位置就是*data*的起始地址）。默认情况下，这些纹素是从相邻的内存位置获取的，除了在读取所有width个纹素后，读指针前进到下一个四字节边界。[glReadPixels](https://blog.csdn.net/flycatdeng/article/details/82667296)使用参数GL_UNPACK_ALIGNMENT指定四字节行对齐，并且可以将其设置为一个，两个，四个或八个字节。

  第一个元素对应于纹理图像的左下角。后续元素从左到右通过纹理图像的最低行中的剩余纹素进行，然后在纹理图像的连续更高行中进行。 最后一个元素对应于纹理图像的右上角。

  *format*决定*data*中每个元素的组成。 它可以是以下符号值之一：

GL_ALPHA

  每个元素都是单个alpha分量。 GL将其转换为浮点并通过将rgb三通道赋值为0组装成RGBA元素。 然后将每个元素的值范围截断于[0,1]。

GL_RGB

  每个元素都是RGB三元组。 GL将其转换为浮点，并通过为alpha赋值为1将其组装成RGBA元素。 然后将每个元素的值范围截断于[0,1]。

GL_RGBA

  每个元素包含所有四个组件。 GL将其转换为浮点，然后将每个元素的值范围截断于[0,1]。

GL_LUMINANCE

  每个元素是单个亮度值。 GL将其转换为浮点，然后通过将亮度值复制三次（红色，绿色和蓝色）并将为alpha赋值为1来将其组合成RGBA元素。然后将每个元素的值范围截断于[0,1]。

GL_LUMINANCE_ALPHA

  每个元素是“亮度-α”对。 GL将其转换为浮点，然后通过将亮度值复制三次（红色，绿色和蓝色）将其组装成RGBA元素。 然后将每个元素的值范围截断于[0,1]。

 颜色组件根据*type*转换为浮点。当*type*是GL_UNSIGNED_BYTE时，每个组件除以2 8 - 1。当*type*为GL_UNSIGNED_SHORT_5_6_5，GL_UNSIGNED_SHORT_4_4_4_4或GL_UNSIGNED_SHORT_5_5_5_1时，每个分量除以2 N-1，其中N是位域中的位数。

## 注意

*internalformat*必须匹配*format*。纹理图像处理期间不支持格式之间的转换。 *type*可以用作提示来指定所需的精度，但GL实现可以选择以任何内部分辨率存储纹理数组。

*data*可能是一个空指针。在这种情况下，会分配纹理内存以适应宽度*width*和高度的纹理*height*。然后你可以下载子文本来初始化这个纹理内存。如果用户尝试将纹理图像的未初始化部分应用于基元，则图像未定义。

glTexImage2D是用来指定 由[glActiveTexture](https://blog.csdn.net/flycatdeng/article/details/82595253)指定的 纹理单元 是二维纹理还是立体贴图纹理的。

## 错误

GL_INVALID_ENUM：如果*target*不是`GL_TEXTURE_2D`，`GL_TEXTURE_CUBE_MAP_POSITIVE_X`， `GL_TEXTURE_CUBE_MAP_NEGATIVE_X`，`GL_TEXTURE_CUBE_MAP_POSITIVE_Y`， `GL_TEXTURE_CUBE_MAP_NEGATIVE_Y`， `GL_TEXTURE_CUBE_MAP_POSITIVE_Z`，或 `GL_TEXTURE_CUBE_MAP_NEGATIVE_Z。`

GL_INVALID_ENUM：如果*`format`*`或`*`type`*`不是可接受的值。`

GL_INVALID_VALUE：如果*target*是立方体贴图中的一个2维贴图，但是宽和高却不相等。（立方体贴图每个维度都是相等的）

GL_INVALID_VALUE：*`level`*比0小。

GL_INVALID_VALUE：如果*level*大于log以2为低⁡max的对数。（max是*target*为GL_TEXTURE_2D时GL_MAX_TEXTURE_SIZE的返回值，或者当target不是GL_TEXTURE_2D时GL_MAX_CUBE_MAP_TEXTURE_SIZE的返回值）

GL_INVALID_VALUE：当*internalformat*是一个不可接收的值。

GL_INVALID_VALUE：当*height*或*width*的值value或者当*target*为GL_TEXTURE_2D时value大于GL_MAX_TEXTURE_SIZE，或者当target不为GL_TEXTURE_2D时value大于GL_MAX_CUBE_MAP_TEXTURE_SIZE。

GL_INVALID_VALUE：当*border*的值不为0时。

GL_INVALID_OPERATION：*format*和*internalformat*不匹配。

GL_INVALID_OPERATION：*type*是GL_UNSIGNED_SHORT_5_6_5但是*format*不是GL_RGB。

GL_INVALID_OPERATION：*type*是GL_UNSIGNED_SHORT_4_4_4_4或者GL_UNSIGNED_SHORT_5_5_5_1但*format*不是GL_RGBA。

## 相关Gets

[glGet](https://blog.csdn.net/flycatdeng/article/details/82595295) `GL_MAX_TEXTURE_SIZE` 或`GL_MAX_CUBE_MAP_TEXTURE_SIZE`

## 另见

[glActiveTexture](https://blog.csdn.net/flycatdeng/article/details/82595253),[glCompressedTexImage2D](https://blog.csdn.net/flycatdeng/article/details/82665015),[glCompressedTexSubImage2D](https://blog.csdn.net/flycatdeng/article/details/82665024),[glCopyTexImage2D](https://blog.csdn.net/flycatdeng/article/details/82665029),[glCopyTexSubImage2D](https://blog.csdn.net/flycatdeng/article/details/82665035),[glPixelStorei](https://blog.csdn.net/flycatdeng/article/details/82667285),[glTexSubImage2D](https://blog.csdn.net/flycatdeng/article/details/82667353),[glTexParameter](https://blog.csdn.net/flycatdeng/article/details/82595267)