Clange 编译问题

一、Clang 编译无法找到 SDK头文件

MAC

```shell
xcode-select --install  #重点
或者
clang test.c -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk #重点是-isysroot
```



