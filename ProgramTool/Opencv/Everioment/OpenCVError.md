# 安装OpenCV时提示缺少boostdesc_bgm.i文件的问题解决方案（附带资源）

今天在安装OpenCV时，报了如下错误：

 笔者在网上查找一番后，发现网上大都给出了解决方案，无非就是将以下文件：

boostdesc_bgm.i
boostdesc_bgm_bi.i
boostdesc_bgm_hd.i
boostdesc_lbgm.i
boostdesc_binboost_064.i
boostdesc_binboost_128.i
boostdesc_binboost_256.i
vgg_generated_120.i
vgg_generated_64.i
vgg_generated_80.i
vgg_generated_48.i
拷贝到opencv_contrib/modules/xfeatures2d/src/目录下，而且网上直接可以用的资源并不多。所以本人在这篇文章里分享一下资源。

百度云链接

提取码：z7dp 
————————————————
版权声明：本文为CSDN博主「AlexWang30」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/AlexWang30/article/details/99612188