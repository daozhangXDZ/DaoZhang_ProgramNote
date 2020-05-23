# OpenGL中glTexParameteri的相关设置

glTexParameteri即纹理过滤函数

其第一个参数制定纹理类型，一般设置为GL_TEXTURE_2D即操作2D纹理

第二个参数指定响应的模式

GL_TEXTURE_WRAP_S   S方向上的贴图模式

GL_TEXTURE_WRAP_T    T方向上的贴图模式

GL_TEXTURE_MAG_FILTER    放大过滤

GL_TEXTURE_MIN_FILTER    缩小过滤

第三个参数指对应模式的方法

GL_CLAMP    将纹理坐标限制在0.0,1.0的范围之内.如果超出了会如何呢.不会错误,只是会边缘拉伸填充

GL_CLAMP_TO_EDGE    在这种模式下，边框始终被忽略。位于纹理边缘或者靠近纹理边缘的纹理单元将用于纹理计算，但不使用纹理边框上的纹理单元，由于硬件支持原因，多数情况下GL_CLAMP与GL_CLAMP_TO_EDGE效果相同

GL_CLAMP_TO_BORDER    如果纹理坐标位于范围[0,1]之外，那么只用边框纹理单元（如果没有边框，则使用常量边框颜色，我想常量边框颜色就是黑色）

GL_LINEAR    线性过滤, 使用距离当前渲染像素中心最近的4个纹素加权平均值，速度较慢无锯齿

GL_NEAREST    使用纹理中坐标最接近的一个像素的颜色作为需要绘制的像素颜色，速度较快会出现锯齿

GL_LINEAR_MIPMAP_NEAREST    使用GL_NEAREST对最接近当前多边形的解析度的两个层级贴图进行采样,然后用这两个值进行线性插值


大多数情况下我们的设置值为：

glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_MIN_FILTER), GL_LINEAR)

glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_MAG_FILTER), GL_LINEAR)

glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_WRAP_S), GL_CLAMP_TO_EDGE)

glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_WRAP_T), GL_CLAMP_TO_EDGE)
————————————————
版权声明：本文为CSDN博主「Dean_Dream_Design」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/dominiced/article/details/79640058