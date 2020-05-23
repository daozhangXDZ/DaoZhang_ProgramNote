## mac版CLion编译和运行c++单个文件配置



### 一、添加

![在这里插入图片描述](Clang_Mac.assets/5752050b9e51aefcae362e28e1964e3d.png)

### 二、外部工具配置

#### 1.编译配置

![在这里插入图片描述](Clang_Mac.assets/278ed1c358503be9d573aaaeb6b8a9b7.png)

- Name 和 Description自己随便取
- 参数Program：/Library/Developer/CommandLineTools/usr/bin/c++
- 参数Arguments："$FileName$"
- 参数Working directory:$FileDir$

#### 2.执行配置

![在这里插入图片描述](Clang_Mac.assets/2796f23a651e199b1cbd37816ed951ef.png)

- 参数program: $FileDir$/a.out
- 参数Working directory:$FileDir$

### 三、快捷键配置

![在这里插入图片描述](Clang_Mac.assets/4c3eb4f74760ce7749dacbca3bf56d69.png)

### 四、使用

![在这里插入图片描述](Clang_Mac.assets/e2984b170f683e869932f3cc2235a1f5.png)

- 使用快捷键编译会产生a.out文件
- 使用快捷键运行，可以执行a.out文件

### 五、使用Python执行c++编译的文件

![在这里插入图片描述](Clang_Mac.assets/f5309464b5db493c8e606272738d67ad.png)
a.out文件 放在当前目录，调用





