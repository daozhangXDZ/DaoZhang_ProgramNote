# [MAC]OpenGL中SOIL库与stbi_load库加载图片，透明黑色问题，遇到的坑及解决办法

介于网上和SOIL相关的问题并不多，记录下自己遇到的问题

坑1： SOIL库的下载及链接，加-m64与加x86的方法都试过，无法解决load_image函数的问题

解决办法：删除官方下载的SOIL库。然后在终端下，git clone https://github.com/DeVaukz/SOIL，（具体mac下如何克隆下载github文件自行google）

然后用cmake(cmake的用法在配置GLFW和GLEW的时候应该已经会用cmake了)按照同样方法配置SOIL库，则在usr/local/include以及usr/local/lib中会

出现相应SOIL文件，然后在xcode中#include<SOIL/SOIL.h>即可

坑2：SOIL库函数没问题，文件路径参数可以直接将图片拖进xcode，运行没问题，但是没图像

解决办法：使用SOIL_last_result()函数，可详细报错

    unsigned char *image = SOIL_load_image("/Users/momo/Desktop/1.png", &texwidth, &texheight, 0, SOIL_LOAD_RGB);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texwidth, texheight, 0, GL_RGB, GL_UNSIGNED_BYTE, image);
        if(image){
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texwidth, texheight, 0, GL_RGB, GL_UNSIGNED_BYTE, image);
            glGenerateMipmap(GL_TEXTURE_2D);
        }
        else
            std::cout<<SOIL_last_result()<<std::endl;
        SOIL_free_image_data(image);
        glBindTexture(GL_TEXTURE_2D,0);

坑3：SOIL_load_image函数只可以加载PNG图片不可以加载JPG图片，报错：JPEG format not supported (progressive)

解决办法：请google:standard jpeg for image，该函数对于JPG图像只支持标准JPEG格式，就算你加载成功了,图像显示灰色且右边被扭曲，所以采用stbi_load库，

这是learnopengl采用stbi_load库写的另一个教程版本：stbi_load库版opengl教程

坑4：SOIL_load_image函数加载PNG函数的时候，透明部分被显示成黑色

解决办法；高级OPENGL-混合参考opengl教程中高级OPENGL之混合部分片段着色器代码，

因为最后用的stbi_load库，所以文章后面会贴上stbi_load解决透明问题的代码版本

坑5：在上述stbi_load库的opengl教程中，下载stb_image.h头文件时可能又需要各种Google，这个不再赘述，但是教程中的代码是存在问题的，贴上我的代码:

        int texwidth,texheight,nrChannels;//nrChannels表示通道数，R/G/B/A，一共4个通道，有些图片只有3个，A即为alpha
        stbi_set_flip_vertically_on_load(true);   //解决图像翻转问题，不需要像SOIL库中片段着色器的position设置为-y
        unsigned char *image = stbi_load("/Users/momo/Desktop/图片/jpeg-home.jpg", &texwidth, &texheight, &nrChannels,STBI_rgb_alpha);//注意这里不是0
        if(image){
            if(nrChannels==3)//rgb 适用于jpg图像
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texwidth, texheight, 0,GL_RGBA, GL_UNSIGNED_BYTE, image);//后面一个是RGBA
            else if(nrChannels==4)//rgba 适用于png图像
                glTexImage2D(GL_TEXTURE_2D, 0,GL_RGBA, texwidth, texheight, 0,GL_RGBA, GL_UNSIGNED_BYTE, image);//注意，两个都是RGBA
            //std::cout<<nrChannels<<std::endl;
            glGenerateMipmap(GL_TEXTURE_2D);
        }
        else
            std::cout<<"Failed to load texture"<<std::endl;
        stbi_image_free(image);
        glBindTexture(GL_TEXTURE_2D,0);


片段着色器代码：主要参考混合那一章的讲述

    const GLchar *FragmentShaderSource="#version 330 core\n"
    "in vec3 ourColor;\n"
    "in vec2 TexCoord;\n"
    "out vec4 color;\n"
    "uniform sampler2D ourTexture;\n"
    "void main()\n"
    "{\n"
    "    vec4 texColor=texture(ourTexture,TexCoord);\n"
    "    if(texColor.a<0.5)\n"
    "        discard;\n"
    "    color=texColor;\n"
    "}\n";

glTexture2D函数中，前一个GL_RGB指的是你希望存储为的格式，后一个GL_RGB是源图像自带的格式，有些JPG图像带有alpha信息，有些不带

至此，PNG图像和JPG图像应该是都能很好的显示出来
————————————————