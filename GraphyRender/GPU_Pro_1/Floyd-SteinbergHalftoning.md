## 基于Floyd-Steinberg半色调的环境映射 | Environment Mapping with Floyd-Steinberg Halftoning

这章中提出了一种使用GPU计算重要性采样的算法。该算法巧妙地应用了经典的半色调技术，可用于加速高质量环境映射照明中的重要性采样步骤。

这章想传达的最重要的信息是半色调（halftoning）算法和重要性采样（importance  sampling）是等价的，因此我们可以在重要性采样中使用半色调算法。文中研究了Floyd-Steinberg半色调方法在环境映射中的应用，并得出结论认为，该方法可以比随机抽样更好地对样本进行分配，所以，对的样本计算的积分也会更准确。

[
![img](Floyd-SteinbergHalftoning.assets/51d1539e3fb64bd68b146b421142f974.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/51d1539e3fb64bd68b146b421142f974.png)

图 左图为随机采样加权环境贴图（Sampling weighted environment maps）；右图为弗洛伊德 - 斯坦伯格采样半色调环境映射（Floyd-Steinberg halftoning）

[
![img](Floyd-SteinbergHalftoning.assets/356f60e324fa8b54011adf4a3065348e.png)](https://github.com/QianMo/Game-Programmer-Study-Notes/blob/master/Content/%E3%80%8AGPUPro1%E3%80%8B%E5%85%A8%E4%B9%A6%E6%8F%90%E7%82%BC%E6%80%BB%E7%BB%93/media/356f60e324fa8b54011adf4a3065348e.png)

图 光源采样结果。随机采样基于Floyd-Steinberg半色调映射通过方向光源对兔子模型的漫反射和镜面光照。

### 

### 14.1 核心实现Shader代码

在几何着色器中实现的Floyd-Steinberg采样器Shader代码：

```
[maxvertexcount (32)]
void gsSampler ( inout PointStream <float4 > samples ) {
    uint M = 32; float S = 0;
        [loop]for (uint v = 0; v < R.y; v++)
            [loop]for (uint u = 0; u < R.x; u++)
                S += getImportance(uint2(u, v));
    float threshold = S / 2 / M;
    
    ////发布博客未知错误
    float cPixel = 0, cDiagonal = 0, acc [4];
    [loop]for (uint j = 0; j < R.y; j++) {
        uint kper4 = 0;
        [loop]for (uint k = 0; k < R.x; k += 4) {
        for (uint xi = 0; xi < 4; xi++) {
            float I = getImportance(uint2 (k+xi , j));
            float Ip = I + cRow[kper4 ][xi] + cPixel ;
            if(Ip > threshold) {
                float3 dir = getSampleDir(uint2 (k+xi , j));
                samples .Append ( float4 (dir , I / S) );
                Ip -= threshold * 2;
            }
            acc [xi] = Ip * 0.375 + cDiagonal ;
            cPixel = Ip * 0.375;
            cDiagonal = Ip * 0.25;
        }
        cRow[kper4 ++] = float4 (acc [0], acc [1], acc [2], acc [3]);
    }
    j++; kper4 --;
    [loop]for (int k = R.x -5; k >= 0; k -= 4) {
        for (int xi = 3; xi >= 0; xi--) {
            float I = getImportance(uint2 (k+xi , j));
            float Ip = I + cRow[kper4 ][xi] + cPixel ;
            if(Ip > threshold ) {
                float3 dir = getSampleDir(uint2 (k+xi , j));
                samples .Append ( float4 (dir , I / S) );
                Ip -= threshold * 2;
            }
            acc [xi] = Ip * 0.375 + cDiagonal ;
            cPixel = Ip * 0.375;
            cDiagonal = Ip * 0.25;
        }
        cRow[kper4 --] = float4 (acc [0], acc [1], acc [2], acc [3]);
        }
    }
}
```
