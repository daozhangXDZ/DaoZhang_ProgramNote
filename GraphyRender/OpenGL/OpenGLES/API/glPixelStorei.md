# GLES2.0中文API-glPixelStorei

## 名称

glPixelStorei - 设置像素存储模式

## C规范

void **glPixelStorei**（GLenum *pname*,

​                    GLint *param*）;

## 参数

*pname*

指定要设置的参数的符号名称。 一个值会影响像素数据到内存的打包：**GL_PACK_ALIGNMENT**。 另一个影响从内存中解压缩像素数据：**GL_UNPACK_ALIGNMENT**。

*param*

指定*pname*设置为的值。

## 描述

**glPixelStorei**设置像素存储模式，这些模式会影响后续[glReadPixels](https://blog.csdn.net/flycatdeng/article/details/82667296)的操作以及纹理模式的解包（请参阅[glTexImage2D](https://blog.csdn.net/flycatdeng/article/details/82667350)和[glTexSubImage2D](https://blog.csdn.net/flycatdeng/article/details/82667353)）。

*pname*是一个符号常量，表示要设置的参数，*param*是新值。 一个存储参数会影响像素数据返回客户端内存的方式：

**GL_PACK_ALIGNMENT**

  指定内存中每个像素行开头的对齐要求。允许值为1（字节对齐），2（行与偶数字节对齐），4（字对齐）和8（行从双字边界开始）。

另一个存储参数会影响从客户端内存中读取像素数据的方式：

**GL_UNPACK_ALIGNMENT**

  指定内存中每个像素行开头的对齐要求。 允许值为1（字节对齐），2（行与偶数字节对齐），4（字对齐）和8（行从双字边界开始）。

下表给出了可以使用**glPixelStorei**设置的每个存储参数的类型，初始值和有效值范围。

| *pname*                 | 类型 | 初始值 | 可用值  |
| ----------------------- | ---- | ------ | ------- |
| **GL_PACK_ALIGNMENT**   | 整型 | 4      | 1,2,4,8 |
| **GL_UNPACK_ALIGNMENT** | 整型 | 4      | 1,2,4,8 |

 

如果param为0，则布尔参数设置为false，否则设置为true。

## 错误

**`GL_INVALID_ENUM`** ：如果*pname*不是可接受的值。

**`GL_INVALID_VALUE`** ：如果指定对齐不是1,2,4或8。

## 相关Gets

[glGet](https://blog.csdn.net/flycatdeng/article/details/82595295) 参数**`GL_PACK_ALIGNMENT`** 或**`GL_UNPACK_ALIGNMENT`**

## 另见

[glReadPixels](https://blog.csdn.net/flycatdeng/article/details/82667296)，[glTexImage2D](https://blog.csdn.net/flycatdeng/article/details/82667350)，[glTexSubImage2D](https://blog.csdn.net/flycatdeng/article/details/82667353)