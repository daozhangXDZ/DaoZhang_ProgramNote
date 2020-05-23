# VSCode配置C/C++环境完整版(附OpenGL配置)

之前分享过一篇关于VSCode配置C/C++的教程：点击跳转
在搭建OpenGL环境的时候，总结一下更完整的教程
准备工作
下载安装Clang

下载地址：点击跳转

QQ截图20190919203852.png

安装目录：C:\LLVM ,

注意选一下 添加环境变量

jdsadh

安装后的目录：

jdsadh
下载MinGW-W64

下载地址：点击跳转

jdsadh

解压(不用安装)目录：C:\mingw64

jdsadh
合并文件

复制C:\mingw64目录下的所有文件，直接粘贴到C:\LLVM(clang安装目录)文件夹下，系统会自动整合同名文件夹下的文件，整合之后：

jdsadh

这时候可以测试一下，是否配置成功: clang -v , gcc -v

jdsadh
下载配置OpenGL相关依赖（glut）

    glut.h：点击跳转
    下载后放到目录：C:\LLVM\include
    glut32.dll：点击跳转
    下载后放到目录：C:\LLVM\bin
    glut32.lib：点击跳转
    下载后放到目录：C:\LLVM\lib

VSCode安装插件

C/C++ : 点击跳转

jdsadh

vscode-clangd : 点击跳转

jdsadh

Code Runner : 点击跳转

jdsadh
VSCode配置文件
用户设置文件：settings-json



    {
      "workbench.colorTheme": "Atom One Dark",
      "files.defaultLanguage": "cpp", // ctrl+N新建文件后默认的语言
      "editor.formatOnType": true, // （对于C/C++）输入分号后自动格式化当前这一行的代码
      "editor.suggest.snippetsPreventQuickSuggestions": false, // clangd的snippets有很多的跳转点，不用这个就必须手动触发Intellisense了
      "editor.acceptSuggestionOnEnter": "off", // 我个人的习惯，按回车时一定是真正的换行，只有tab才会接受Intellisense
      // "editor.snippetSuggestions": "top", // （可选）snippets显示在补全列表顶端，默认是inline
    
      "code-runner.runInTerminal": true, // 设置成false会在“输出”中输出，无法输入
      "code-runner.executorMap": {
          "c": "cd $dir && clang '$fileName' -o '$fileNameWithoutExt.exe' -Wall -g -O2 -static-libgcc --target=x86_64-w64-mingw -std=c11 && &'$dir$fileNameWithoutExt'",
          "cpp": "cd $dir && clang++ '$fileName' -o '$fileNameWithoutExt.exe' -Wall -g -O2 -static-libgcc --target=x86_64-w64-mingw -lglut32 -lglu32 -lopengl32 -std=c++17 && &'$dir$fileNameWithoutExt'"
          // "c": "cd $dir && clang $fileName -o $fileNameWithoutExt.exe -Wall -g -O2 -static-libgcc --target=x86_64-w64-mingw -std=c11 && $dir$fileNameWithoutExt",
          // "cpp": "cd $dir && clang++ $fileName -o $fileNameWithoutExt.exe -Wall -g -O2 -static-libgcc --target=x86_64-w64-mingw -std=c++17 && $dir$fileNameWithoutExt"
      }, // 控制Code Runner命令；未注释的仅适用于PowerShell（Win10默认），文件名中有空格也可以编译运行；注释掉的适用于cmd（win7默认），也适用于PS，文件名中有空格时无法运行
      "code-runner.saveFileBeforeRun": true, // run code前保存
      "code-runner.preserveFocus": true, // 若为false，run code后光标会聚焦到终端上。如果需要频繁输入数据可设为false
      "code-runner.clearPreviousOutput": false, // 每次run code前清空属于code runner的终端消息，默认false
      "code-runner.ignoreSelection": true, // 默认为false，效果是鼠标选中一块代码后可以单独执行，但C是编译型语言，不适合这样用
    
      "C_Cpp.clang_format_sortIncludes": true, // 格式化时调整include的顺序（按字母排序）
      "C_Cpp.errorSquiggles": "Disabled", // 因为有clang的lint，所以关掉；如果你看的是别的答主用的不是vscode-clangd，就不要加这个了
      "C_Cpp.autocomplete": "Disabled", // 同上；这几条也可以考虑放到全局里，否则很多错误会报两遍，cpptools一遍clangd一遍
      "C_Cpp.suggestSnippets": false,
      "explorer.confirmDelete": false,
      "files.associations": {
        "mutex": "cpp"
      }, // 同上
    }

备注："-lpthread" *//在gcc编译的时候，附加要加 -lpthread参数即可解决。* 



项目文件夹下新建-vscode文件夹，新建launch-json、task-json、c-cpp-properties-json文件
launch-json:



    {
      "version": "0.2.0",
      "configurations": [
          {
              "name": "(gdb) Launch", // 配置名称，将会在启动配置的下拉菜单中显示
              "type": "cppdbg", // 配置类型，cppdbg对应cpptools提供的调试功能；可以认为此处只能是cppdbg
              "request": "launch", // 请求配置类型，可以为launch（启动）或attach（附加）
              "program": "${fileDirname}/${fileBasenameNoExtension}.exe", // 将要进行调试的程序的路径
              "args": [], // 程序调试时传递给程序的命令行参数，一般设为空即可
              "stopAtEntry": false, // 设为true时程序将暂停在程序入口处，相当于在main上打断点
              "cwd": "${workspaceFolder}", // 调试程序时的工作目录，此为工作区文件夹；改成${fileDirname}可变为文件所在目录
              "environment": [], // 环境变量
              "externalConsole": false, // 为true时使用单独的cmd窗口，与其它IDE一致；18年10月后设为false可调用VSC内置终端
              "internalConsoleOptions": "neverOpen", // 如果不设为neverOpen，调试时会跳到“调试控制台”选项卡，你应该不需要对gdb手动输命令吧？
              "MIMode": "gdb", // 指定连接的调试器，可以为gdb或lldb。但我没试过lldb
              "miDebuggerPath": "gdb.exe", // 调试器路径，Windows下后缀不能省略，Linux下则不要
              "setupCommands": [
                  { // 模板自带，好像可以更好地显示STL容器的内容，具体作用自行Google
                      "description": "Enable pretty-printing for gdb",
                      "text": "-enable-pretty-printing",
                      "ignoreFailures": false
                  }
              ],
              "preLaunchTask": "Compile" // 调试会话开始前执行的任务，一般为编译程序。与tasks.json的label相对应
          }
      ]
    }

task.json



    {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Compile",
                "command": "clang++",
                "args": [
                    "${file}",
                    "-o",
                    "${fileDirname}/${fileBasenameNoExtension}.exe",
                    "-g",
                    "-Wall",
                    "-static-libgcc",
                    "--target=x86_64-w64-mingw",
                    "-std=c++11",
                    "-lpthread" //在gcc编译的时候，附加要加 -lpthread参数即可解决。 
                ],
                "type": "shell",
                "group": {
                    "kind": "build",
                    "isDefault": true
                },
                "presentation": {
                    "echo": true,
                    "reveal": "always",
                    "focus": false,
                    "panel": "shared"
                }
            },
            {
                "type": "shell",
                "label": "cpp.exe build active file",
                "command": "C:\\Program Files\\LLVM\\bin\\cpp.exe",
                "args": [
                    "-g",
                    "${file}",
                    "-o",
                    "${fileDirname}\\${fileBasenameNoExtension}.exe"
                ],
                "options": {
                    "cwd": "C:\\Program Files\\LLVM\\bin"
                },
                "problemMatcher": [
                    "$gcc"
                ],
                "group": "build"
            }
        ]
    }

c_cpp_properties.json

    {
      "configurations": [
        {
          "name": "MinGW",
          "intelliSenseMode": "clang-x64",
          "compilerPath": "C:/Program Files/LLVM/bin/gcc.exe",
          "includePath": [
            "${workspaceFolder}"
    
          ],
          "defines": [],
          "browse": {
            "path": [
              "${workspaceFolder}"
            ],
            "limitSymbolsToIncludedHeaders": true,
            "databaseFilename": ""
          },
          "cStandard": "c11",
          "cppStandard": "c++11"
        }
      ],
      "version": 4
    }

来个示例代码：



    #include <glut.h>
    void init();
    void display();
    int main(int argc, char* argv[]){
        glutInit(&argc, argv);
        glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE);
        glutInitWindowPosition(800, 150);
        glutInitWindowSize(600, 400);
        glutCreateWindow("OpenGL 3D View");
        init();
        glutDisplayFunc(display);
        glutMainLoop();
        return 0;
    }
    void init(){
        glClearColor(0.0, 0.0, 0.0, 0.0);
        glMatrixMode(GL_PROJECTION);
        glOrtho(-5, 5, -5, 5, 5, 15);
        glMatrixMode(GL_MODELVIEW);
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0);
    }
    void display(){
        glClear(GL_COLOR_BUFFER_BIT);
        glColor3f(0, 1.0, 0);
        glutWireTeapot(3);
        glFlush();
    }

运行一下：

jdsadh

参考链接：
1：https://www.zhihu.com/question/30315894
2：https://www.cnblogs.com/wentao-study/p/10921381.html
————————————————
版权声明：本文为CSDN博主「本该如此」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_40922859/article/details/101039951