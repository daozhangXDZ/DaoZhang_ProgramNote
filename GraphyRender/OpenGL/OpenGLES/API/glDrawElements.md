# GLES2.0中文API-glDrawElements

## 名称

glDrawElements - 从数组数据中渲染图元

## C规范

void **glDrawElements**（GLenum *mode*，

​                GLsizei *count，*

​                GLenum *type*,

​                const GLvoid * *indices*）;

## 参数

*mode*

指定要渲染的图元类型。 接受符号常量**GL_POINTS**，**GL_LINE_STRIP**，**GL_LINE_LOOP**，**GL_LINES**，**GL_TRIANGLE_STRIP**，**GL_TRIANGLE_FAN**和**GL_TRIANGLES**。

*count*

指定要渲染的元素数。

*type*

指定*indices*中值的类型。 必须是**GL_UNSIGNED_BYTE**或**GL_UNSIGNED_SHORT**。

*indices*

指定指向存储索引的位置的指针。[特别注意和VertexBufferObject  VertexArrayObject的结合]

## 描述

**glDrawElements**指定了几个子例程调用的几何图元。你可以使用[glVertexAttribPointer](https://blog.csdn.net/flycatdeng/article/details/82667374)预先指定单独的顶点，法线和颜色数组，而不是调用GL过程来传递每个单独的顶点属性并使用它们通过单次调用**glDrawElements**来构造图元序列。

当调用**glDrawElements**时，它使用来自启用数组的计数顺序元素，从索引开始构造几何图元序列。mode指定构造什么类型的图元以及数组元素如何构造这些图元。 如果启用了多个数组，则使用每个数组。

要启用和禁用通用顶点属性数组，请调用[glEnableVertexAttribArray](https://blog.csdn.net/flycatdeng/article/details/82667052)和[glDisableVertexAttribArray](https://blog.csdn.net/flycatdeng/article/details/82667052)。

## 注意

如果[glUseProgram](https://blog.csdn.net/flycatdeng/article/details/82667360)设置的当前程序对象无效，则渲染结果未定义。 但是，这种情况不会产生错误。

## 错误

**GL_INVALID_ENUM**：*mode*不是一个可接收的值

*GL_INVALID_ENUM：type*不是**GL_UNSIGNED_BYTE**或**GL_UNSIGNED_SHORT**

**GL_INVALID_VALUE**：*count*是负数

**GL_INVALID_FRAMEBUFFER_OPERATION**：如果当前绑定的帧缓冲区不是帧缓冲区完成状态（即[glCheckFramebufferStatus](https://blog.csdn.net/flycatdeng/article/details/82664955)的返回值不是**GL_FRAMEBUFFER_COMPLETE**）。

## 另见

[glCheckFramebufferStatus](https://blog.csdn.net/flycatdeng/article/details/82664955)，[glEnableVertexAttribArray](https://blog.csdn.net/flycatdeng/article/details/82667052)，[glDisableVertexAttribArray](https://blog.csdn.net/flycatdeng/article/details/82667052)，[glDrawArrays](https://blog.csdn.net/flycatdeng/article/details/82667044)，[glUseProgram](https://blog.csdn.net/flycatdeng/article/details/82667360)，[glVertexAttribPointer](https://blog.csdn.net/flycatdeng/article/details/82667374)