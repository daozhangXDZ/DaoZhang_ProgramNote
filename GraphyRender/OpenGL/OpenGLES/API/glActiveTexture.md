# glActiveTexture和glBindTexture的关系

今天在做`glsl`渲染`yuv`图像时，因为对`glActiveTexture`和`glBindTexture`的不熟，遇到了麻烦。经过试验，有了新的理解，并基于此理解解决了问题。

之前用到纹理，都是传`GL_RGB`或者`GL_RGBA`类型的数据进去的，只需要使用一张纹理，完全不用设置`glActiveTexture`的，所以对`glActiveTexture`的理解很浅

渲染yuv就不同了。
 ffmpeg解码出来的yuv一般是以`yuv420p`的格式，分别存放在`AVFrame->data`二维数组中。其中

> data[0] => y
>  data[1] => u
>  data[2] => v

这样格式的数据，需要使用三张纹理，分别传输到显卡中。

## glBindTexture

我的理解是，`glBindTexture(GL_TEXTURE_2D, tex_id)` 有以下几个涵义:

1. 表示 tex_id是一个二维纹理，设置过一次后，tex_id的类型就不可变了
2. `opengl`采用状态机的设计，`glBindTexture`告诉opengl说，我选择tex_id作为当前纹理，后续对纹理的操作都将作用在此纹理上。

## glActiveTexture

我们已经通过·glGenTextures`在显卡上开辟了一张纹理， 然后使用`glBindTexture`将该纹理选为当前操作目标， 接着也调用了`glTexParameter`函数族设置了纹理的属性

那么问题来了，纹理是怎么和`glsl`上的`sampler2D`关联起来的？

### 假如

假如是自己来设计，会怎么设计：

> 将`glGenTextures`生成的`tex_id`赋值给`sampler2D`变量就好了

### 实际上

我也不理解为什么。实际上`opengl`在这块关联上绕了下路。
 纹理与`sampler2D`变量的关联是通过索引来关联的。
 我们可以给`sampler2D`变量赋int值。

```c
GLuint tex_loc = glGetUniformLocation(program, "tex");
glUniform1i(tex_loc, 1);
```

