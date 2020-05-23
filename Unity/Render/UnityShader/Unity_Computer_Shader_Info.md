# Unity Compute Shader详解



# 开始用compute shader

 我喜欢vertex/fragment shaders的简单，他们只是做一件事（把顶点和颜色输出到屏幕上去），他们做得非常好，但是有时这种简单限制了你，当你的cpu拼了命的循环那些矩阵，算出并储存在贴图上。。。

![img](Unity_Computer_Shader_Info.assets/20150308131338959.png)

 



Compute Shader能用来控制粒子群的位置

# 什么是compute shader？

 简单地说， compute shader是一个在GPU中执行的程序，不需要操作网格mesh和贴图texture数据，在OpenGL或DirectX存储空间中工作（不像OpenCL有自己的存储空间），并且能输出数据的缓冲或贴图，跨线程的执行分享存储。



# 用了它有什么好处与坏处？

 两个词：数学与并行化。任何问题都包含相同的（没有条件转移conditional branching





# 懂了？那我们开始吧

 当我们使用DirectX时，unity的compute shader需要使用HLSL编程语言，但是他几乎不能辨别其他shader语言，所以如果你能写CG或者GLSL你也会用好的。



```
#pragma kernel CSMain RWTexture2D<float4> Result; [numthreads(8,8,1)]void CSMain (uint3 id : SV_DispatchThreadID){    Result[id.xy] = float4(id.x & id.y, (id.x & 15)/15.0, (id.y & 15)/15.0, 0.0);}
```



 这是一个搞清楚compute shader的好例子，所以我们一行一行的看
这指定了这个程序的入口函数（compute shader的main函数），一个compute shader能定义许多函数，你能从脚本中随意调用。

这声明了一个变量，它包含的数据是shader程序将要用到的。我们不需要用到网格mesh数据，你需要像这样明确的声明，你的compute shader需要写入读出什么数据。数据类型名前面的“RW”指定了shader可以进行读写操作。



```
[numthreads(8,8,1)]
```

这一行指定了compute  shader创建的线程组的大小。GPU利用了大量的并行处理使得GPU创建的一些线程可以同时运行。线程组指定如何组织线衍生程们 spawned  threads，在上面的代码中，我们指定我们想要每组线程组包含64个线程，可以使用像一个二维数组。



# 实际运行shader

 显然我们不能把compute shader加入到网格中导出运行，尤其是它没有网格数据。compute shader实际上要用脚本来调用，看起来像这样：

```
public ComputeShader shader; void RunShader(){int kernelHandle = shader.FindKernel("CSMain"); RenderTexture tex = new RenderTexture(256,256,24);tex.enableRandomWrite = true;tex.Create(); shader.SetTexture(kernelHandle, "Result", tex);shader.Dispatch(kernelHandle, 256/8, 256/8, 1);}
```



 这里标记了一些东西。首先在你创建renderTexture前先设置了enableRandomWrite标记。这使你的compute shader 有权写入贴图。如果你不设置这个标记你就不能在你的shader中作为一个写入目标使用贴图。 然后我们需要一种方法来确定我们想要在compute  shader中调用什么函数。FindKernel函数使用一个字符串类的名字，与我们一开始在compute  shader中设置的核心kernel的名字相同。记住，在一个compute shader文件中， 可以有多个核心kernel （函数）。 ComputeShader.SetTexture让我们把CPU的数据传到GPU。在不同的存储空间中移动数据会在你的程序中产生延迟，你传值越多延迟越明显。对于这个原因，如果你想每帧都执行compute shader，你需要优化实际操作的数据。 三个整数通过Dispatch指定需要产生的线程组的数量，在compute shader中 numthreads块中指定取消每个线程组的大小，所以在上面的例子中，我们产生的线程的总数是： 32*32个线程组 * 64个线程每组 = 65536个线程。 这结束了相当于在render texture中的一个线程一个像素，使场景核心函数调用只能操作一个像素。 所以现在我们知道写一个compute shader能操作贴图内存，让我们看看我们能让他去做什么。

 修饰贴图数据很像vert/frag shader，是时候释放我们的GPU让他操作数据了，是的，这是可行的，听起来非常好。 一个Structured Buffer 只是一种数据类型的一个数组的数据。可以设置conditional branching为浮点或整型。你可以在comepute shader中像这样声明：
数据类型也可以是结构体，在本文的第二个例子会讲到 在我们的例子中，我们将通过我们的compute shader中的一组点，每个都有一个矩阵被我们变换。我们可以用两个分开的缓冲完成它（一个是Vector3s另一个是Matrix4x4s）， 但是将一个点或矩阵在一个结构体中，处理起来会很简单





```
#pragma kernel Multiply struct VecMatPair{	float3 pos;	float4x4 mat;}; RWStructuredBuffer<VecMatPair> dataBuffer; [numthreads(16,1,1)]void Multiply (uint3 id : SV_DispatchThreadID){    dataBuffer[id.x].pos = mul(dataBuffer[id.x].mat,     				float4(dataBuffer[id.x].pos, 1.0));}
```



 注意我们的线程组现在组织成一个空间的数组。这对于线程组的维数没有性能影响，所以你可以在你的程序中自由的选择。 在我们刚才的贴图例子中，在一个脚本中构建一个structured  buffer有点困难。对于一个buffer，你需要指定在这个buffer中一个元素要多大的字节，并且储存信息和数据本身一起在一个compute  buffer物体中。在我们的结构体例子中，字节数大小仅仅是我们存储的  float值的大小（3个vector，16个matrix）乘以一个float的大小（4bytes），对于在一个结构体中一个总数达到76bytes。在compute  shader 中设置他看起来是这样的：

```
public ComputeShader shader;	void RunShader(){	VecMatPair[] data = new VecMatPair[5];	//INITIALIZE DATA HERE		ComputeBuffer buffer = new ComputeBuffer(data.Length, 76);	int kernel = shader.FindKernel("Multiply");	shader.SetBuffer(kernel, "dataBuffer", buffer);	shader.Dispatch(kernel, data.Length, 1,1);}
```



 现在我们需要让这个改进数据回到一个格式，使我们能在脚本中使用。不像我们上面render Texture的例子，structured buffers 需要明确的从GPU的存储空间中被转移到CPU中。在我的经验中，当使用compute  shader时，你要注意这是一个最大的性能消耗，我找到的只有一种方法来减轻它是优化你的缓冲，所以他们要尽可能的小，直到存在可用，并且只有从你的shader中把拉数据出来时你才完全需要它。 得到数据到你的CPU中的实际的代码很简单。你需要的只是一个有着相同的数据类型で数组并且大小和写入缓冲的数据相同，如果我们改进上面的脚本去写数据到一个第二数组，看起来像是这样：