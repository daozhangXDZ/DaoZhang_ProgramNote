# 使用adb命令如何抓起手机LOG

首先使用USB线连接手机，连接的时候，如果没有打开USB调试，将提示需要打开USB调试。如下图所示。





[![使用adb命令如何抓起手机LOG](https://imgsa.baidu.com/exp/w=500/sign=ee03355e9782d158bb8259b1b00a19d5/9345d688d43f87949bc8fb9ed91b0ef41bd53a4e.jpg)](http://jingyan.baidu.com/album/fd8044fa2df9f25030137a73.html?picindex=1)





USB调试打开后，可以使用adb shell命令查看手机和电脑是否连接成功，如下图所示。

[![使用adb命令如何抓起手机LOG](adb_log_topc.assets/ac6eddc451da81cb71aa307d5966d01609243135.jpg)](http://jingyan.baidu.com/album/fd8044fa2df9f25030137a73.html?picindex=2)



连接成功后，使用exit退出shell,然后使用adb logcat >E:/temp/log.txt.命令抓起手机执行过程。如下图所示

[![使用adb命令如何抓起手机LOG](adb_log_topc.assets/eac4b74543a98226a17298978182b9014b90ebcb.jpg)](http://jingyan.baidu.com/album/fd8044fa2df9f25030137a73.html?picindex=3)



手机操作执行完成后，使用ctrl+c结束抓LOG。如下图所示。

[![使用adb命令如何抓起手机LOG](adb_log_topc.assets/203fb80e7bec54e7d9aea9aeb2389b504ec26ac4.jpg)](http://jingyan.baidu.com/album/fd8044fa2df9f25030137a73.html?picindex=4)



此时LOG已经抓取成功，并且保存在电脑E盘的temp文件夹下，如下图所示。

[![使用adb命令如何抓起手机LOG](adb_log_topc.assets/0b46f21fbe096b634234ece007338744ebf8ac55.jpg)](http://jingyan.baidu.com/album/fd8044fa2df9f25030137a73.html?picindex=5)



打开log.txt可以查找导致问题的原因。

[![使用adb命令如何抓起手机LOG](adb_log_topc.assets/c9fcc3cec3fdfc03a99d5008df3f8794a5c2269c.jpg)步骤阅读](http://jingyan.baidu.com/album/fd8044fa2df9f25030137a73.html?picindex=6)