# GLES2.0中文API-glReadPixels

## 名称

glReadPixels - 从帧缓冲区中读取一个像素块

## C规范

void **glReadPixels**（GLint *x*,

​                  GLint *y*,

​                  GLsizei *width*,

​                  GLsizei *height*,

​                  GLenum *format*,

​                  GLenum *type*,

​                  GLvoid * *data*）;

## 参数

*x，y*

指定从帧缓冲区读取的第一个像素的窗口坐标。 此位置是矩形像素块的**左下角**。

*width,height*

指定像素矩形的尺寸。 一个宽度和高度对应于单个像素。

*format*

指定像素数据的格式。 接受以下符号值：**GL_ALPHA**，**GL_RGB**和**GL_RGBA**。

*type*

指定像素数据的数据类型。 必须是**GL_UNSIGNED_BYTE**，**GL_UNSIGNED_SHORT_5_6_5**，**GL_UNSIGNED_SHORT_4_4_4_4**或**GL_UNSIGNED_SHORT_5_5_5_1**之一。

*data*

返回像素数据。

## 描述

**glReadPixels**从帧缓冲区返回像素数据，从左下角位于（*x，y*）的像素开始，从位置*data*开始返回客户端内存。使用[glPixelStorei](https://blog.csdn.net/flycatdeng/article/details/82667285)命令设置的**GL_PACK_ALIGNMENT**参数会影响像素数据在放入客户端内存之前的处理。

**glReadPixels**返回每个像素的值，左下角为x + i y + j，0 <= i <width，0 <= j <height。 该像素被称为第j行中的第i个像素。 像素按行顺序从最低行返回到最高行，每行从左到右排列。

*format*指定返回像素值的格式; 可接受的值是：

**`GL_ALPHA`**

**`GL_RGB`**

**`GL_RGBA`**

```
从颜色缓冲区读取RGBA颜色分量。 每个颜色分量都转换为浮点，使零强度映射到0.0，全强度映射到1.0。
丢弃不需要的数据。 例如，GL_ALPHA丢弃红色，绿色和蓝色组件，而GL_RGB仅丢弃alpha组件。 最终值被限制在[0 1]的范围内。
最后，组件将转换为由类型指定合适的格式，。 当类型为**GL_UNSIGNED_BYTE**时，每个组件乘以2^8 - 1。 当类型为**GL_UNSIGNED_SHORT_5_6_5**，**GL_UNSIGNED_SHORT_4_4_4_4**或**GL_UNSIGNED_SHORT_5_5_5_1**时，每个分量乘以2^N-1，其中N是位域中的位数。
返回值按如下方式放入内存中。 如果*format*是**GL_ALPHA**，则返回单个值，并且第j行中第i个像素的数据放置在位置j**width* + i中。 **GL_RGB**返回三个值，**GL_RGBA**为每个像素返回四个值，所有值对应于占据数据中连续空间的单个像素。 由`[glPixelStorei](https://blog.csdn.net/flycatdeng/article/details/82667285)`设置的存储参数**GL_PACK_ALIGNMENT**会影响数据写入内存的方式。 有关说明，请参阅`[glPixelStorei](https://blog.csdn.net/flycatdeng/article/details/82667285)`。
```

## 注意

如果当前绑定的帧缓冲区不是默认的帧缓冲区对象，则从附加到**GL_COLOR_ATTACHMENT0**附着点的彩色图像中读取颜色分量。

只有两个*format/type*参数对是可接受的。**GL_RGBA** / **GL_UNSIGNED_BYTE**是始终都可以接受的，另外的就需要查询了：通过查询**GL_IMPLEMENTATION_COLOR_READ_FORMAT**和**GL_IMPLEMENTATION_COLOR_READ_TYPE**来发现其他可接受的对。

位于连接到当前GL上下文的窗口之外的像素值是未定义的。

如果生成错误，则不会更改*data*内容。

## 错误

**`GL_INVALID_ENUM`** ：如果*format*或*type*不是可接受的值。

**`GL_INVALID_VALUE`** ：如果*width*或*height*是负数

**`GL_INVALID_OPERATION`** ：如果*type*为**GL_UNSIGNED_SHORT_5_6_5**且格式不是**GL_RGB**。

**`GL_INVALID_OPERATION`** ：如果*type*为**GL_UNSIGNED_SHORT_4_4_4_4**或**GL_UNSIGNED_SHORT_5_5_5_1**且格式不是**GL_RGBA**。

**`GL_INVALID_OPERATION`** ：如果*format*和*type*分别既不是**GL_RGBA**又不是**GL_UNSIGNED_BYTE**，也不是通过查询**GL_IMPLEMENTATION_COLOR_READ_FORMAT**和**GL_IMPLEMENTATION_COLOR_READ_TYPE**返回的格式/类型对。

**`GL_INVALID_FRAMEBUFFER_OPERATION`** ：如果当前绑定的帧缓冲区不是帧缓冲区完成状态（即[glCheckFramebufferStatus](https://blog.csdn.net/flycatdeng/article/details/82664955)的返回值不是**GL_FRAMEBUFFER_COMPLETE**）。

## 相关Gets

[glGet](https://blog.csdn.net/flycatdeng/article/details/82595295) 参数`**GL_IMPLEMENTATION_COLOR_READ_FORMAT**或`**GL_IMPLEMENTATION_COLOR_READ_TYPE**

[glGet](https://blog.csdn.net/flycatdeng/article/details/82595295) 参数**GL_PACK_ALIGNMENT**

## 另见

[glCheckFramebufferStatus](https://blog.csdn.net/flycatdeng/article/details/82664955)，[glPixelStorei](https://blog.csdn.net/flycatdeng/article/details/82667285)