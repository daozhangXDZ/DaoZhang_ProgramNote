# VSCode 安装使用和配置CMake工程



## .下载安装

支持跨平台，微软产品.
 下载地址：https://code.visualstudio.com/
 安装勾选需要的选项，傻瓜安装即可。

## 2.VSCode设置中文语言显示

先安装的插件【Ctrl+Shift+x】，搜索Chinese (Simplified) Language Pack for Visual Studio Code，选择安装；
 使用快捷键组合【Ctrl+Shift+p】，在搜索框中输入“configure display language”，点击确定；
 修改locale.json文件下的属性“locale”为“zh-CN”;
 重启VSCode；

## 3.VSCode C/C++配置

1.安装MinGw，配置bin目录的环境变量；
 2.安装插件C/C++;





![img](VSCode_CMake.assets/15412525-95115cd5715563af.png)

image.png



3.VSC不支持单文件编译，需要创建一个目录，在这个目录下进行编译，例如TEST，写一个简单的main.cpp文件保存在这各目录下；
 4.使用【Ctrl+Shift+p】，输入C/Cpp:Edit Configurations生成配置文件 c_cpp_properties.json

```json
{
    "configurations": [
        {
            "name": "Win32",
            "includePath": [
                "${workspaceFolder}/**"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "compilerPath": "D:\\MinGw\\mingw64\\bin\\gcc.exe",
            "cStandard": "c11",
            "cppStandard": "c++17",
            "intelliSenseMode": "clang-x64"
        }
    ],
    "version": 4
}
```

5.使用【Ctrl+Shift+p】，输入Tasks: Configure task生成配置文件 tasks.json

```bash
{
    "version": "2.0.0",
    "command": "g++",
    "args": ["-g","${file}","-o","${fileBasenameNoExtension}.exe"], // 编译命令参数
    "problemMatcher": {
        "owner": "cpp",
        "fileLocation": ["relative", "${workspaceRoot}"],
        "pattern": {
            "regexp": "^(.*):(\\d+):(\\d+):\\s+(warning|error):\\s+(.*)$",
            "file": 1,
            "line": 2,
            "column": 3,
            "severity": 4,
            "message": 5
        }
    }
}
```

6.使用【Ctrl+Shift+p】，输入Open launch.json生成配置文件launch.json

```bash
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceRoot}/${fileBasenameNoExtension}.exe",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "D:/MinGw/mingw64/bin/gdb.exe",
            "preLaunchTask": "g++",
            // "preLaunchTask": "compile", // task.json 中的 label
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
    
}
```

7.默认生成的.vscode就是用来管理你的项目的设置，可以直接使用F5进行调试，或者点击调试按钮选择在不调试的情况下启动（直接编译运行），**编译调试的时候需要切换到自己的main.cpp文件**；
 8.生成的.exe文件也可以像linux中一样使用./main.exe进行运行。

## 4.配置Cmake管理C/C++项目

1.下载安装cmake，并添加到环境变量；
 2.安装Cmake插件，以下两个





![img](VSCode_CMake.assets/15412525-65b8e531e483f406.png)

image.png



3.安装后配置用户配置文件，当中cmake的两项，其余的一些都是在这里配置

```json
{
    "workbench.sideBar.location": "left",
    "workbench.colorTheme": "Monokai Dimmed",
    "explorer.confirmDelete": false,
    "cmake.cmakePath": "C:/Program Files/CMake/bin/cmake",
    "cmake.configureOnOpen": true,
    "editor.fontSize": 15,
}
```

4.直接以打开文件夹的方式打开你的cmake工程目录，比如test2，test2下包含CMakeList.txt文件；