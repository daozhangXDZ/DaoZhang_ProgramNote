# VSCode运行多文件C++教程：使用CMake

事先说明

这篇文章是一个CMake工具的简单使用介绍。缘起是因为上个学期上编译原理的课程要求做课程设计，用C++实现。

一直以来出于一种奇妙心态的我非常厌恶使用 Visual Studio 这种笨重的IDE，向来用VScode作为C++主力编辑器，然而很遗憾VSCode自身不怎么支持C++多文档的编译(很麻烦，要不停的修改json配置文件)，无奈为了寻求出路就稍微学了一下CMake来组织工程。

本文只对CMake最基本的用法做介绍，不涉及太高深的内容，比较适合像我一样的小白食用。也可以当做在VSCode上开发C++的进阶参考。

至于如何在VSCode上配置最基本的C++程序运行，在很多地方比如知乎或者其他博客里都讲的很详细了。大体无非几步: 下载MinGW、配置.vscode/tasks.json、配置.vscode/launch.json、配置.vscode/c_cpp_properties.json，不做赘述。
CMake是什么

你或许听过好几种 Make 工具，例如 GNU Make ，QT 的 qmake ，微软的 MS nmake，BSD Make（pmake），Makepp，等等。这些 Make 工具遵循着不同的规范和标准，所执行的 Makefile 格式也千差万别。这样就带来了一个严峻的问题：如果软件想跨平台，必须要保证能够在不同平台编译。而如果使用上面的 Make 工具，就得为每一种标准写一次 Makefile ，这将是一件让人抓狂的工作。

CMake就是针对上面问题所设计的工具：它首先允许开发者编写一种平台无关的 CMakeList.txt 文件来定制整个编译流程，然后再根据目标用户的平台进一步生成所需的本地化 Makefile 和工程文件，如 Unix 的 Makefile 或 Windows 的 Visual Studio 工程。从而做到“Write once, run everywhere”。显然，CMake 是一个比上述几种 make 更高级的编译配置工具。一些使用 CMake 作为项目架构系统的知名开源项目有 VTK、ITK、KDE、OpenCV、OSG 等。

一般使用 CMake 生成 Makefile 并编译的流程如下：

    编写 CMake 配置文件 CMakeLists.txt
    执行命令 cmake PATH 或者 ccmake PATH 生成 Makefile(ccmake 和 cmake 的区别在于前者提供了一个交互式的界面)，其中， PATH 是 CMakeLists.txt 所在的目录
    使用 make 命令进行编译

最简单的用法
演示

假设现在我们在这么一个目录: Demo1

.
├── Build
├── CMakeLists.txt
└── main.cpp

1 directory, 2 files

    1
    2
    3
    4
    5
    6

main.cpp的内容如下:

#include <iostream>

int main(int argc, char** argv)
{
    int a = -2;
    std::cout << a << std::endl;
    return 0;
}

    1
    2
    3
    4
    5
    6
    7
    8

为了编译这个文件，我们编辑CMakeLists.txt文件为:

# CMake 最低版本号要求
cmake_minimum_required (VERSION 2.8)

#项目名称, 参数值是 Demo1, 该命令表示项目的名称是 Demo1
project(Main)

# 显示指定使用的C++编译器 
set(CMAKE_CXX_COMPILER "g++")

# 指定生成目标
add_executable(Demo1 main.cpp)

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11

然后进入Build目录，执行cmake

cd Build/
cmake -G "MinGW Makefiles" ..

    1
    2

然后我们就会发现在Buile/目录下多了一大堆东西:

.
├── Build
│   ├── CMakeCache.txt
│   ├── CMakeFiles
│   │   ├── 3.12.3
│   │   │   ├── CMakeCCompiler.cmake
│   │   │   └── <略>
│   │   ├── cmake.check_cache
│   │   ├── CMakeDirectoryInformation.cmake
│   │   ├── CMakeOutput.log
│   │   ├── CMakeTmp
│   │   ├── Demo1.dir
│   │   │   ├── build.make
│   │   │   └── <略>
│   │   ├── feature_tests.bin
│   │   │   └── <略>
│   ├── cmake_install.cmake
│   └── Makefile
├── CMakeLists.txt
└── main.cpp

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20

注意到Build目录下现在多了一个Makefile文件。接着我们只需要在Build目录下执行命令:

make

    1

然后我们就会发现Build目录下多了一个Demo1.exe文件，编译完成。
解释
CMakeLists语法

    cmake_minimum_required

语法格式为:

cmake_minimum_required(VERSION <min>[...<max>] [FATAL_ERROR])

    1

用于设置最低版本号要求, 需要放在文件最开头位置。

    project(Main)
    
    Sets project details such as name, version, etc. and enables languages

project(<PROJECT-NAME> [LANGUAGES] [<language-name>...])

    1

project命令会创建一些相关变量，例如:

    PROJECT_SOURCE_DIR: 整个项目的根目录，即包含PROJECT()的最近一个CMakeLists.txt文件所在的目录
    PROJECT_BINARY_DIR: Build路径，在这里就是 **、Demo1/Build
    
    set()

set用于设置变量的值，格式为:

set(<variable> <value>... [PARENT_SCOPE])

    1

如果<variable>不存在，那就回创建一个新的变量, 不过这里的变量是系统预定义的变量。

文件中涉及到的变脸有两个.

一个是CMAKE_CXX_COMPILER，指的是C++的编译器，这是一个内置的变量, 准确来讲它应该是以CMAKE_<LANG>_COMPILER 为模版的一个实例, <LANG>指的是语言,官方对它的解释是:

    The full path to the compiler for LANG

比如如果我们想要设置C语言的编译器，那就是 CMAKE_C_COMPILER, 而C++的就是 CMAKE_CXX_COMPILER。

等等，为什么C++在这里是CXX? 这就涉及到不同平台下C++程序的后缀名问题了，在Windows下我们常用的就是一个.cpp扩展名，但在其他标准中，还有很多种不同扩展名，比如 C cc cxx 等等都是C++文件的扩展名, 详情见C++后缀名的问题

另外一个是CMAKE_CXX_FLAGS，它指的是编译的可选参数，同样，它也是CMAKE_<LANG>_FLAGS的一个实例，这里我们设置了 -g 参数，表明保留调试信息。

set (CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -g")

    1

咦? ${CMAKE_CXX_FLAGS}是什么东西? 其实很好理解，${<variable>} 指的就是取变量的值，我们可以利用 message() 函数来看看一个变量的值是什么，它可以把参数代表的值打印出来:

# 输出 -g
message(${CMAKE_CXX_FLAGS})
# 输出 E:/my_programming/C++_Program/UseCMake/Demo1
message(${PROJECT_SOURCE_DIR})

    1
    2
    3
    4
    
    add_executable(Demo1 main.cpp)

add_executable(<name> [WIN32] [MACOSX_BUNDLE]
               [EXCLUDE_FROM_ALL]
               [source1] [source2 ...])

    1
    2
    3

该命令指定了将源文件输出到可执行文件 <name>，比如在Windows平台上，就会生成一个 <name>.exe 文件。

默认情况下，可执行文件将会在Build路径下被创建。如果要改变这个位置，有很多种办法，最简单的是修改 EXECUTABLE_OUTPUT_PATH 变量的值，比如:

# 设置exe文件输出的 Bin 目录下
set(EXECUTABLE_OUTPUT_PATH  ${PROJECT_SOURCE_DIR}/Bin)

    1
    2

额外说明

    之所以使用一个Build目录就是因为cmake出来的东西太多，最好放到一个专门的目录下
    
    cmake 的格式是 cmake <dir> , 其中 <dir> 中必须有 CMakeLists.txt 文件
    
    由于我现在是在Windows下, 如果直接使用 cmake .. 会默认使用 Visual Studio 的编译器，可以通过 -G 指定，这里我们使用的是MinGW
    
    make 程序在Windows上没有，可以使用 MinGW 中的 bin/mingw32-make.exe 替代，比如我们可以复制一份此程序，然后改名为 make.exe

多文件处理

以上我们演示了在只有一个源文件的情况下的使用方法，现在我们看一看多文件的情况，在Demo2文件夹里，目录结构是这样的:

.
├── a.cxx
├── a.h
├── b.cxx
├── Bin
├── Build
├── build.bat
└── CMakeLists.txt

2 directories, 5 files

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10

build.bat只是把之前build的命令写到脚本里，不去管它，我们先来看一看a.h, a.cxx, b.cxx 的内容:

// a.h
#ifndef A_H
#define A_H
int square(int a);
#endif // !A_H

//a.cxx
#include "a.h"
int square(int a)
{
    return a * a;
}

//b.cxx
#include "a.h"
#include <iostream>
using namespace std;
int main()
{
    int a = -7;
    cout << a << ": " << square(a) << endl;
    return 0;
}

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23

显然这是一组相互依赖的程序，我们来看一看怎么处理。
方法1

cmake_minimum_required (VERSION 2.8)
project(Demo2)
set(CMAKE_CXX_COMPILER "g++")
set (CMAKE_CXX_FLAGS  "-g -fexec-charset=GBK")
set(EXECUTABLE_OUTPUT_PATH  ${PROJECT_SOURCE_DIR}/Bin)
add_executable(Demo2 a.cxx b.cxx)

    1
    2
    3
    4
    5
    6

可以看到，和之前的几乎没有区别，只不过 add_executable 的 <source> 参数变成了两个。
方法2

上面的方法存在着一个问题，如果源文件很多的话，那我们将每个CPP文件手动加到 add_executable 中也不合适，而且不利于动态的增加文件，要解决这个问题，我们需要用一些小技巧:

cmake_minimum_required (VERSION 2.8)
project(Demo2)
set(CMAKE_CXX_COMPILER "g++")
set (CMAKE_CXX_FLAGS  "-g  -fexec-charset=GBK")
set(EXECUTABLE_OUTPUT_PATH  ${PROJECT_SOURCE_DIR}/Bin)
# 注意这里
aux_source_directory(./ SrcFiles)
add_executable(Demo2 ${SrcFiles})

    1
    2
    3
    4
    5
    6
    7
    8

在这里我们使用了 aux_source_directory 这个函数，来看看它的官方解释:

aux_source_directory(<dir> <variable>)

    1
    
    Collects the names of all the source files in the specified directory and stores the list in the <variable> provided.

要注意的是，这里强调了只有源文件才会被加入，比如在这个例子中，只有 a.cxx b.cxx 被加入了，而其余的 a.h CMakeLists.txt 都不会被加进去。
多目录的情况

在实际的使用之中，我们往往都不会把所有代码放在一个目录之下，现在我们来看看当存在多个目录时怎么办。

假设我们现在有三个文件:

//./Include/a.h
#ifndef A_H
#define A_H
extern int x;
void f();
#endif // !A_H

//./a.cpp
#include "a.h"
#include <iostream>
int x = 0;
void f()
{
    std::cout << "This is f()" << std::endl;
}

//./main.cpp
#include "a.h"
using namespace std;
int main()
{
    f();
    return 0;
}

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24

Case 1

先看一个最简单的情况:

.
├── a.cpp
├── Bin
├── Build
├── CMakeLists.txt
├── Include
│   └── a.h
└── main.cpp

3 directories, 4 files

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10

在这个例子中，我们的源文件还是在工程根目录下，而 a.h 头文件被放在了一个子目录 ./Include 中。

这一次如果我们还是用之前的那个 CMakeLists.txt 的话就会出错(准确来讲是cmake可以过，但make时就会报错):

E:\my_programming\C++_Program\UseCMake\Demo3\a.cpp:1:15: fatal error: a.h: No such file or directory
 #include "a.h"
               ^

    1
    2
    3

include_directories([AFTER|BEFORE] [SYSTEM] dir1 [dir2 ...])

    1

使用这个方法就可以把新的目录添加到工程的Include路径当中来，现在我们的 CMakeLists.txt 长这个样子:

cmake_minimum_required (VERSION 2.8)
project(Demo3)
set(CMAKE_CXX_COMPILER "g++")
set (CMAKE_CXX_FLAGS  "-g -fexec-charset=GBK")
# 添加include路径
include_directories(${PROJECT_SOURCE_DIR}/Include)
aux_source_directory(./ SrcFiles)
set(EXECUTABLE_OUTPUT_PATH  ${PROJECT_SOURCE_DIR}/Bin)
add_executable(Demo3 ${SrcFiles})

    1
    2
    3
    4
    5
    6
    7
    8
    9

运行cmake+make，搞定!

顺便说个题外话，一开始在a.h文件里我写了一个int x = 0;，结果直接报错了，后来一查才发现问题出在哪里，详见multiple definition of 问题解决方法
Case 2

第二种情况:

.
├── Bin
├── Build
├── CMakeLists.txt
├── Include
│   └── a.h
└── Src
    ├── a.cpp
    └── main.cpp

4 directories, 4 files

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11

头文件和源文件分属不同的目录，编译结果输出到./Bin/目录下，这也是很常用的一种组织方式。看上去很麻烦，然而实际上很简单，改一下SrcFiles就行了。

cmake_minimum_required (VERSION 2.8)
project(Demo4)
set(CMAKE_CXX_COMPILER "g++")
set (CMAKE_CXX_FLAGS  "-g -fexec-charset=GBK")
include_directories(${PROJECT_SOURCE_DIR}/Include)
aux_source_directory(./Src SrcFiles)
set(EXECUTABLE_OUTPUT_PATH  ${PROJECT_SOURCE_DIR}/Bin)
add_executable(Demo4 ${SrcFiles})

    1
    2
    3
    4
    5
    6
    7
    8

和VSCode集成起来

有了上述的基础，我们可以在VSCode中愉快地使用了。以我编译原理的作业为例，我的文件结构是这样的：

.
├── Bin
│   └── Compile.exe
├── Build
│   └── <略>
├── build.bat
├── CMakeLists.txt
├── f.c
├── Include
│   ├── Global.h
│   ├── Grammar.h
│   ├── Lexical.h
│   └── Tool.h
├── sample.c
└── Src
    ├── Global.cpp
    ├── Grammar.cpp
    ├── Lexical.cpp
    ├── main.cpp
    └── Tool.cpp

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20

为了便于使用我在根目录下编写build.bat文件:

@echo off
cd .\Build
cmake -G "MinGW Makefiles" .. > TriffleInfo
make

    1
    2
    3
    4

还记得.vscode下有个task.json文件吗，把它改成这样:

{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "compile",
            "type": "shell",
            "command": ".\\build.bat",
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14

task.json只执行编译过程，所以launch.json也得改:

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/Bin/Compile.exe",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": true,
            "MIMode": "gdb",
            "miDebuggerPath": "D:\\MinGW\\MinGW_Location\\bin\\gdb.exe",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
            //"preLaunchTask": "compile"
        }
    ]
}

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26

然后按Ctrl+Shift+B执行编译，按F5运行即可。要是想一步到位，可以把上面那行"preLaunchTask": "compile"的注释取消了，按F5就可以一次性编译运行了，不过这样不太好，万一编译错了你运行的程序还是之前未作修改的那个。
结语

CMake的简单用法就到这里了，它当然还有更多更复杂的用法，比如链接第三方库什么的，这些内容由于我没用到所以也懒得去学了，想要了解的可以参考官方文档，或者大批CMake教程，这里我只介绍最简单的。
————————————————
版权声明：本文为CSDN博主「frostime」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/frostime/article/details/86756983