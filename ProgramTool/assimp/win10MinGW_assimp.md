# 在Windows下使用MinGW静态编译Assimp

使用MinGW静态编译Assimp
 

到了5月份了，没有写一篇日志，于是自己从知识库里面拿出一篇文章充数吧。这次将要讲解如何在Windows下使用MinGW静态编译Assimp。

  Assimp是目前比较全的3D格式解析库了，熟悉3D游戏开发的同行都知道，3D的格式非常混乱，各种3D格式在不同场合都有他们特定的应用，游戏引擎只能够解析少部分3D格式，更多实用的格式来自游戏公司自定义的格式。而在开源领域，Assimp算是比较全的3D格式导入库了。它对3D格式理解深入，很适合整合至3D图形引擎中，让你们的程序支持更多3D的格式。  
 要静态编译Assimp，首先需要准备Assimp的源码、cmake和MinGW。MinGW我选用的是Qt自带的库，大家可以自己选择合适的MinGW或是TDM-MinGW。这里我将Assimp的源码和cmake分享一下，以便自己日后查阅。  

​     Assimp下载地址：[这里](http://yunpan.cn/QiTLeqUm854rQ)（提取码：60c5）

​     Cmake的下载地址：[这里](http://yunpan.cn/Q47DnXRBpfy8R)（提取码：46ac）

 下载Assimp后，解压之，放在合适的位置，我这里放在E:/Develop中。  
 同时下载cmake后，解压之，放在合适的位置。我这里放在E:/Develop中。  
 然后cmd进入命令行，我们主要在命令行进行编译。  
 1、 首先设置环境变量，我这里是这么设置的：  

```
set path=%path%;E:/Develop/cmake-2.8.12.1-win32-x86/bin;E:/Develop/Qt5.3/Tools/mingw482_32/bin
```

 2、然后到assimp库的根目录下  

```
cd $${Assimp目录}
```

 3、使用cmake进行构建  

```
cmake -G "MinGW Makefiles" ^
-DENABLE_BOOST_WORKAROUND=ON -DBUILD_STATIC_LIB=ON ^
-DCMAKE_RC_COMPILER=E:/Develop/Qt5.3/Tools/mingw482_32/bin/windres.exe ^
-DCMAKE_MAKE_PROGRAM=E:/Develop/Qt5.3/Tools/mingw482_32/bin/mingw32-make.exe ^
-DCMAKE_LFLAGS=-static ^
-DCMAKE_LFLAGS_DLL=-static ^
-DDX9_INCLUDE_PATH=E:/Develop/Qt5.3/Tools/mingw482_32/i686-w64-mingw32/include ^
-DD3D9_LIBRARY=E:/Develop/Qt5.3/Tools/mingw482_32/i686-w64-mingw32/lib/libd3d9.a ^
-DD3DX9_LIBRARY=E:/Develop/Qt5.3/Tools/mingw482_32/i686-w64-mingw32/lib/libd3dx9.a .
```

如果你的计算机安装了DirectX库，那么cmake会查找头文件以及库文件，不必设置DX9_INCLUDE_PATH、D3D9_LIBRARY和D3DX9_LIBRARY。  
 4、在mingw32-make之前，修改一下源代码。因为编译会出现错误：  
 在$${Assimp目录}/include/assimp/types.h中修改：  
 在52行后添加#include <string.h>，就行了。  
  5、修改$${Assimp目录}/tools/assimp_view/CMakeFiles/assimp_viewer.dir/build.make中418行，删除$(RC_FLAGS)；修改$${Assimp目录}/tools/assimp_cmd/CMakeFiles/assimp_cmd.dir/build.make中的58行，删除$(RC_FLAGS)  
 6、mingw32-make -j 4进行构建。如果顺利的话，libassimp.a以及assimp_cmd.exe和assimp_viewer.exe都会顺利地构建。  

最后如果想要使用assimp_cmd.exe和assimp_viewer.exe的话，需要libgcc_s_dw2-1.dll、libstdc++-6.dll以及libwinpthread-1.dll，这些都可以在MinGW目录中找到，想要使用assimp_viewer的话还需要有d3dx9_43.dll。当然，我这里也分享了一份assimp_viewer，下载地址在[这里](http://download.csdn.net/detail/jiangcaiyang123/7033489)。





> 推荐：[windows下使用Mingw编译x264](http://www.itkeyword.com/doc/990965308208009644/windows)
>
> \1. 下载mingw并安装  http://sourceforge.net/projects/mingw/files/，下载mingw-get-inst-20120426.exe并安装 2. 下载最新版x264 http://download.videolan.org/

使用MinGW静态编译Assimp 到了5月份了，没有写一篇日志，于是自己从知识库里面拿出一篇文章充数吧。这次将要讲解如何在Windows下使用MinGW静态编译Assimp。 Assimp是目前比较全的3D格式解析库了