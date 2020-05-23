## 名称

glCheckFramebufferStatus - 返回帧缓冲区对象的帧缓冲区完整性状态

## C规范

GLenum **glCheckFramebufferStatus**（GLenum *target*）;

## 参数

*target*

指定目标帧缓冲区对象。 符号常量必须是**GL_FRAMEBUFFER**。

## 描述

**glCheckFramebufferStatus**返回一个符号常量，用于标识当前绑定的帧缓冲是否为帧缓冲完成，如果不是“完成”，则返回违反帧缓冲完整性的哪个规则的标识。

如果帧缓冲完成，则返回**GL_FRAMEBUFFER_COMPLETE**。 如果帧缓冲未完成，则返回值如下：

**GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT**

​    并非所有帧缓冲附加点都是帧缓冲附件完成。  这意味着附加渲染缓冲区或纹理的至少一个附着点的附加对象不再存在，可能是具有宽度或高度为零的附加图像，或者颜色附加点附加了不可着色的图像，  或深度附着点附有非深度可渲染图像，或者模板附着点附有非模板可渲染图像。

​    颜色可渲染格式包括**GL_RGBA4**，**GL_RGB5_A1**和**GL_RGB565**。 **GL_DEPTH_COMPONENT16**是唯一可深度渲染的格式。 **GL_STENCIL_INDEX8**是唯一的模板可渲染格式。

**GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS**

​    并非所有附加图像都具有相同的宽度和高度。

**GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT**

​    没有图像附加到帧缓冲区。

**GL_FRAMEBUFFER_UNSUPPORTED**

​    附加图像的内部格式的组合违反了依赖于实现的一组限制。

如果当前绑定的帧缓冲区不是帧缓冲区完成，则尝试使用帧缓冲区进行写入或读取是错误的。 这意味着渲染命令（[glClear](https://blog.csdn.net/flycatdeng/article/details/82664964)，[glDrawArrays](https://blog.csdn.net/flycatdeng/article/details/82667044)和[glDrawElements](https://blog.csdn.net/flycatdeng/article/details/82667046)）以及读取帧缓冲区（[glReadPixels](https://blog.csdn.net/flycatdeng/article/details/82667296)，[glCopyTexImage2D](https://blog.csdn.net/flycatdeng/article/details/82665029)和[glCopyTexSubImage2D](https://blog.csdn.net/flycatdeng/article/details/82665035)）的命令将在帧缓冲区未完成帧缓冲区时调用时生成错误**GL_INVALID_FRAMEBUFFER_OPERATION**。

## 注意

强烈建议（即使并不需要），应用程序调用**glCheckFramebufferStatus**以查看帧缓冲是否在渲染之前完成。这是因为某些实现可能不支持呈现内部格式的特定组合。 在这种情况下将会返回**GL_FRAMEBUFFER_UNSUPPORTED**。

默认的窗口系统提供的帧缓冲区总是帧缓冲完成，因此当**GL_FRAMEBUFFER_BINDING**为**0**时返回**GL_FRAMEBUFFER_COMPLETE**。

此外，如果发生错误，则返回**0**。

## 错误

**`GL_INVALID_ENUM`** ：如果*target*不是**GL_FRAMEBUFFER**。

## 另见

[glBindRenderbuffer](https://blog.csdn.net/flycatdeng/article/details/82664539)，[glCopyTexImage2D](https://blog.csdn.net/flycatdeng/article/details/82665029)，[glCopyTexSubImage2D](https://blog.csdn.net/flycatdeng/article/details/82665035)，[glDrawArrays](https://blog.csdn.net/flycatdeng/article/details/82667044)，[glDrawElements](https://blog.csdn.net/flycatdeng/article/details/82667046)，[glReadPixels](https://blog.csdn.net/flycatdeng/article/details/82667296)，[glRenderbufferStorage](https://blog.csdn.net/flycatdeng/article/details/82667301)