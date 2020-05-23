6434950-477e56b5290bdbb9.jpg
前言

鸽了好久的描边，其实一方面自己也是才刚开始学习，不像大佬一样信手捏来，只能跟着各种教程学。另一方面，做出来的效果一直和想象中的有点差距，虽然本人尝试了很多的教程，到目前为止的效果勉强达到及格线吧。分享出来给还是不是很明白的人一起学习。
简介

描边（Outline）或者叫做勾线，简单来说就是给模型加边，在卡通渲染中，给人一种手绘的效果。描边的原理其实是边缘检测（Edge Detection), 在图像处理（Image Processing）中，很多时候我们需要检测边缘。先看边缘检测的定义：

Edge detection includes a variety of mathematical methods that aim at identifying points in a digital image at which the image brightness changes sharply or, more formally, has discontinuities. The points at which image brightness changes sharply are typically organized into a set of curved line segments termededges.

边缘检测（英语：Edge detection）是图像处理和计算机视觉中的基本问题，边缘检测的目的是标识数字图像中亮度变化明显的点。

图像是由像素点组合成的集合，如果把它转换到频域（Frequency Domain)上来看，图像包含了不同频率的信号，边缘则是信号变化最剧烈的地方。所以实际上，边缘检测就是检测到信号变化超过一定阈值的像素点，将其标记为边缘。

现在有很多的信号检测的算法，比较常用的有Sobel， Laplacian， Canny filter等。本人主要研究了前两种，关于它们的具体算法，网上有很多的介绍，这里给两篇本人看过的介绍（边缘检测的三种算法介绍 、The Sobel and Laplacian Edge Detectors）。本文不会介绍太多的算法推导和细节，总结起来，边缘检测其实是信号系统的滤波器的那一套理论。在时域上（Spatial Domain）对信号相乘，相对于在频域上对信号做卷积（convolution）。如果对卷积和傅里叶变换（特别是快速傅里叶变换FFT- Fast Fourier Transform和离散傅里叶变换DFT- Discrete Fourier Transform）感兴趣，可以自行百度谷歌。

上述几个边缘检测算法，其核心在于卷积核（Convolution Kernel), Sobel Kernel通常采用两个3x3的矩阵来表示。由于Sobel滤波是检测一个方向上（一阶）的色彩或者亮度的梯度变化，所以需要在水平和垂直方向进行两次卷积。其两个卷积核(Sobel算子 - Sobel Operator)分别如下：
6434950-236bc40c611352ab.png

我们分别获得水平和垂直的结果后将其相加
6434950-0ab110a5b4a2d8ef.png

,这样通过判断G是否大于一个阈值，我们就能判断这个像素是否属于边缘。

另一方面，Laplacian算子是一个二阶的微分算子，所以只需一个卷积核就能够检测到边缘，其缺点是对于噪声（Noise）比较敏感，如果图像中有比较多的噪声可能处理出来的结果会有很多噪点。
6434950-c8bbd14e2590866a.png
实现

本人在Unreal Engine4（UE4）中尝试实现了这两个描边shader，不过蓝图颇为复杂，不如代码适合学习和展示。所以这次的实现使用Unity Shader来展示。UE4中的结果如果有时间的话可能会在另一篇文章中放出来。

本人在具体实现时大量参考了Manifold Garden，My take on shaders: Edge detection image effect和Unity-Chan（日语原文）的实现方式。毕竟刚开始学习的最好方式就是模仿。

下面分三种方式实现描边Shader： 分别是基于Sobel和色彩（Sobel Color）的实现，基于Sobel和深度纹理的实现（Sobel Depth）和基于Laplacian的深度加上法线（Laplacian Depth and Normal）的实现。

因为边缘检测基本都是在Pixel（Fragment）Shader中实现，因此vertex shader中就不需要做什么处理，我们先把vertex shader的代码放出来。

        Properties
        {
            _MainTex("Texture", 2D) = "white" {}
            _TestColor("Test color", Color) = (1, 1, 1, 1) // For Testing, Mask the background color
        }
     
        CGINCLUDE
        #include"UnityCG.cginc"
     
        uniform sampler2D _MainTex;
        uniform sampler2D _MainTex_ST;
        uniform float4 _MainTex_TexelSize;
        sampler2D_float _CameraDepthTexture;
        sampler2D _CameraDepthNormalsTexture;
     
        uniform float4 _EdgeColor;
        uniform float _Exponent;
        uniform float _SampleDistance; // To control the edge width
        uniform float _FilterPower;
        uniform float _Threshold;
        uniform float4 _TestColor;
        uniform float _BgFade;
        uniform float3 _LightDir; // For toon shading
        uniform int _bToonShader;
     
        struct appdata
        {
            float4 vertex: POSITION;
            float4 normal: NORMAL;
            float2 uv: TEXCOORD0;
        };
     
        struct v2f
        {
            float2 uv: TEXCOORD0;
            float4 vertex: SV_POSITION;
        };
     
        v2f vert(appdata v)
        {
            v2f o;
            o.vertex = UnityObjectToClipPos(v.vertex);
            o.uv = v.uv;
            return o;
        }


Sobel Color

试想，给模型上面不同颜色的边界都描上边，这种形式在2D动画中可以说是最常见的了，将Sobel算法作用在颜色值之上就能够很清楚地检测到颜色值的变化，因此得到颜色的边界。

        float4 fragColor(v2f i) : COLOR
        {        
                    // Sample surrounding 9 pixels
            float2 offsets[9] = {
                float2(-1, 1),
                float2(0, 1),
                float2(1, 1),
                float2(-1, 0),
                float2(0, 0),
                float2(1, 0),
                float2(-1, -1),
                float2(0, -1),
                float2(1, -1)
            };
     
            float3x3 sobelHorizontal = float3x3(
                -1, 0, 1,
                -2, 0, 2,
                -1, 0, 1
                );
            float3x3 sobelVertical = float3x3(
                -1, -2, -1,
                0, 0, 0,
                1, 2, 1
                );
            float4 sobelH = float4(0, 0, 0, 0);
            float4 sobelV = float4(0, 0, 0, 0);
            float2 adjacentPixel = _MainTex_TexelSize.xy * _SampleDistance;
            for (int m = 0; m < 3; m++)
                for (int n = 0; n < 3; n++)
                {
                    sobelH += tex2D(_MainTex, i.uv + offsets[m * 3 + n] * adjacentPixel) * sobelHorizontal[m][n];
                    sobelV += tex2D(_MainTex, i.uv + offsets[m * 3 + n] * adjacentPixel) * sobelVertical[m][n];
                }
     
            float sobel = sqrt(sobelH * sobelH + sobelV * sobelV);
                    // Above steps calculate sobel result of color
     
            float4 sceneColor = tex2D(_MainTex, i.uv);
            // Get edge value based on sobel value and threshold
            float edgeMask = saturate(lerp(0.0f, sobel, _Threshold));
            float3 EdgeMaskColor = float3(edgeMask, edgeMask, edgeMask);
            sceneColor = lerp(sceneColor, _TestColor, _BgFade);
     
            float3 finalColor = saturate((EdgeMaskColor * _EdgeColor.rgb) + (sceneColor.rgb - EdgeMaskColor));
            return float4(finalColor, 1);
     
        }


前半段的代码比较简单，直接实现了让像素点和周围的8个像素点做Sobel卷积，我们通过增加SampleDistance来控制采样点和中心点的距离（可以控制边的粗细）。之后着色的部分稍微复杂。EdgeMask和EdgeMaskColor是通过Sobel值和阈值_Threshold之间的关系来线性插值获得的。

这样的一个float3作为mask作用在最终的颜色上，就能够做到仅仅把EdgeColor显示在边缘部分。

    float3 finalColor = saturate((EdgeMaskColor * _EdgeColor.rgb) + (sceneColor.rgb - EdgeMaskColor));


最后我们得到的结果如下：
6434950-3a3fc4734e6fd495.jpg

当然可以通过增加Threshold等值造成很夸张的效果
6434950-8a42f0dd796c05da.jpg

你也可以使用TestColor把背景颜色遮蔽掉只显示边缘，这样更方便调试也很有素描画的感觉
6434950-f8cb499d2d7a50c8.jpg

我们可以看到不仅人物的内部也能画出轮廓，背景甚至是影子都被描边了。毕竟这个方法是检测颜色的变化，如果不希望其他内容被描边的话，就需要更多地处理了（可能是stencil buffer之类的），这里暂且不提。总体上来看，Sobel color的方法效果相当不错，如果模型比较配合的话（颜色变化明显等），可以带来很棒的视觉效果。
Sobel Depth

我们再看看Sobel Depth，这里我们需要Unity把DepthTexture的模式打开，这样才能在Shader中访问到Depth值。

     Camera.main.depthTextureMode = DepthTextureMode.Depth;


再看看Fragment Shader

    float4 fragDepthSobel(v2f i) : SV_Target
        {
            float2 offsets[9] = {
                float2(-1, 1),
                float2(0, 1),
                float2(1, 1),
                float2(-1, 0),
                float2(0, 0),
                float2(1, 0),
                float2(-1, -1),
                float2(0, -1),
                float2(1, -1)
            };
     
            const float4 horizontalDiagCoef = float4(-1, -1, 1, 1);
            const float4 horizontalAxialCoef = float4(0, -1, 0, 1);
            const float4 verticalDiagCoeff = float4(1, 1, -1, -1);
            const float verticalAxialCoef = float4(1, 0, -1, 0);
            // boardlands implementation of sobel filter
            // diagonal / axial values
            float4 depthDiag;
            float4 depthAxial;
     
            float2 distance = _SampleDistance * _MainTex_TexelSize.xy;
     
            depthDiag.x = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[6] * distance)); // (-1, -1)
            depthDiag.y = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[0] * distance)); // (-1, 1)
            depthDiag.z = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[2] * distance));// (1, 1)
            depthDiag.w = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[8] * distance)); // (1, -1)
     
            depthAxial.x = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[3] * distance)); // (-1, 0)
            depthAxial.y = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[1] * distance)); // (0, 1)
            depthAxial.z = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[5] * distance)); // (1, 0)
            depthAxial.w = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[7] * distance)); // (0, -1)
     
            float centerDepth = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv));
     
            depthDiag /= centerDepth;
            depthAxial -= centerDepth;
     
            float4 sobelHorizontal = horizontalDiagCoef * depthDiag + horizontalAxialCoef * depthAxial;
            float4 sobelVertical = verticalDiagCoeff * depthDiag + verticalAxialCoef * depthAxial;
     
            float sobelH = dot(sobelHorizontal, float4(1, 1, 1, 1));
            float sobelV = dot(sobelVertical, float4(1, 1, 1, 1));
     
            float sobel = sqrt(sobelH * sobelH + sobelV * sobelV);
            sobel = 1.0 - pow(saturate(sobel), _Exponent);
            float4 color = tex2D(_MainTex, i.uv.xy);
            color = _EdgeColor * color * (1 - sobel) + sobel;
            color = color * lerp(tex2D(_MainTex, i.uv.xy), _TestColor, _BgFade);
     
            return color;
        }


这部分的代码大量参考UnityChan描边shader的代码，而貌似这段代码真正的来源出自无主之地（Borderlands）。

比较让人费解的部分是这个

    depthDiag.x = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[6] * distance)); // (-1, -1)
            depthDiag.y = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[0] * distance)); // (-1, 1)
            depthDiag.z = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[2] * distance));// (1, 1)
            depthDiag.w = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[8] * distance)); // (1, -1)
     
            depthAxial.x = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[3] * distance)); // (-1, 0)
            depthAxial.y = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[1] * distance)); // (0, 1)
            depthAxial.z = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[5] * distance)); // (1, 0)
            depthAxial.w = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv + offsets[7] * distance)); // (0, -1)


它对深度的采样分了对角线（Diagonal）和坐标轴方向（Axial）像素两种，最后和中心的深度做了这样的运算

            float centerDepth = Linear01Depth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv));
     
            depthDiag /= centerDepth;
            depthAxial -= centerDepth;


实际测试中即使把两者设置为一样的（都是减去中心深度或者除以中心深度）似乎都能得到最后的结果（当然需要调整一下其他的参数）。单从算式上看似乎是想更多地依赖直接相邻的像素点的深度而不希望对角线的深度差有太大影响。如果有人明白的话希望能在评论下面提出来。

最后的结果是这样
6434950-541b11c0f92b4679.jpg
6434950-7b42b0342680a458.jpg

很显然，Sobel Depth只能检测到外边缘，只用Depth texture很难检测到内边缘，这样描边比较复杂的模型会失去比较多的细节，需要依据具体场景取舍。本人不是很喜欢用它来描边角色模型，不过如果用它来描边物体的话还是挺不错的。
Laplacian Depth and Normal

拉普拉斯算子只要进行一次卷积，比起Sobel方便了一点。想想如果同时检测深度和法线，是否能够更准确地找到边缘？当然这个方法也可以用Sobel算子来实现，不过如果光用Sobel，万一Laplacian比它更加优秀岂不是失去得到更好效果的机会了，所以这里用拉普拉斯算子来做卷积核。

由于shader中需要使用到深度和法线，我们在c#中设置depthtexturemode为：

     Camera.main.depthTextureMode = DepthTextureMode.DepthNormals;


Fragment shader 代码如下

        float4 fragDepthNormalLaplacian(v2f i) : SV_Target
        {
            float4 col = tex2D(_MainTex, i.uv);
            float4 orValue = GetPixelValue(i.uv);
            float2 offsets[9] = {
                    float2(-1, 1),
                    float2(0, 1),
                    float2(1, 1),
                    float2(-1, 0),
                    float2(0, 0),
                    float2(1, 0),
                    float2(-1, -1),
                    float2(0, -1),
                    float2(1, -1)
            };
     
            float4 sampledValue = float4(0, 0, 0, 0);
            float3x3 laplacianOperator = float3x3(
                0, 1, 0,
                1, -4, 1,
                0, 1, 0
                );
            float2 sampleDist = _MainTex_TexelSize * _SampleDistance;
            for (int m = 0; m < 3; m++)
                for (int n = 0; n < 3; n++)
                {
                    sampledValue += GetPixelValue(i.uv + offsets[m * 3 + n] * sampleDist) * laplacianOperator[m][n];
                }
            col = lerp(float4(1, 1, 1, 1), _EdgeColor, 1.0f - saturate(_Threshold - length(orValue - sampledValue)));
            col = col * lerp(tex2D(_MainTex, i.uv), _TestColor, _BgFade);
     
            return col;
        }


这里Getpixelvalue是一个通过uv来获得该点的深度和法线，实现如下

        float4 GetPixelValue(in float2 uv)
        {
            half3 normal;
            float depth;
            DecodeDepthNormal(tex2D(_CameraDepthNormalsTexture, uv), depth, normal);
            return fixed4(normal, depth);
        }


使用了UnityCG.cginc里面的api DecodeDepthNormal
6434950-7864f92eb793b3bb.png

sampleValue里面同时保存了normal（xyz）和depth（w）值，最后对它和阈值进行对比决定是否描边。逻辑上比较简单。

结果如下
6434950-f3470f0954b45133.jpg
6434950-fd39cc6b05aaf740.jpg

我们可以看见，一部分内部的轮廓也被检测了出来。深度加法线的方法确实能够检测到一些内边，不过拉普拉斯算子对于噪声的灵敏也能从结果看出，Unity-chan的模型还好，毕竟是高模，但是妮可的模型很显然有一些噪点。

调低阈值的话，妮可的模型上噪点越多，unitychan倒是效果相当好，甚至超过了Sobel Color的方法。
6434950-9a63f05f8b641a24.jpg

接下来就是通过不停调参数来获取最佳的效果了。我们可以看出，这个方法上限高，下限低，需要模型比较好才能达到理想的效果。
总结

以上就是本人初学描边shader的一些体会，还有很多不太明白的地方，以及上面的一些说法可能也不准确，效果不是很好，这一些都会通过不断地学习慢慢改进。最近我还在学习NPR的其他相关技术，有什么想法会再写文章来分享。要达到崩崩崩或者是UnityChan的那种卡通渲染的效果果然还是任重而道远。

附一张Unity酱的图片
6434950-bcc1d3edeb403479.jpg
参考（Reference）

    3D animation expression using Unity toon shading
    Unityでのアニメ風表現設定ノウハウ
    边缘检测的三种算法介绍
    The Sobel and Laplacian Edge Detectors
    Edge Detection Shader Deep Dive! Part 1 - Even or Thinner Edges?
    My take on shaders: Edge detection image effect
    Unity-Chan!
---------------------
作者：weixin_34368949 
来源：CSDN 
原文：https://blog.csdn.net/weixin_34368949/article/details/87628049 
版权声明：本文为博主原创文章，转载请附上博文链接！
