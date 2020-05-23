# Win10电脑虚拟安装苹果MacOS无敌完整版.



应该有不少小伙伴想体验苹果电脑，或者想学习苹果软件开发，但是苦于苹果机价格昂贵烦恼不已。其实，想体验苹果系统，不一定非要苹果机，大多数的Windows电脑都可以通过虚拟技术来几乎完美地体验苹果的系统，即MacOS。今天我就来做个简单而又详细的教程，让人人都可以体验到流畅的苹果Mac系统。

[![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/8601a18b87d6277f90cefac423381f30e824fc6a.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=1)



## 工具/原料

- 硬件：一台安装了Windows 10系统的电脑，台式机笔记本都行。
- 软件（文中有下载链接）：拟机软件VMware Workstation Pro 12.5.5、虚拟机MacOS破解工具Unlocker、Python、MacOS Seirra10.12.4镜像
- 一颗坚持到底、勇于解决问题的心。

## 第一步 检查CPU是否支持虚拟化

- 第一种方法，右键计算机（此电脑）→属性，查看自己的CPU型号。如下图，我使用的这台电脑是Inter Core i5 6500，然后再百度中输入“Inter Core i5 6500是否支持虚拟化”，然后就明白了。

  [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/d31b0ef41bd5ad6e11e0ae168acb39dbb6fd3c35.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=2)

- 第二种方法，进入BIOS设置中，寻找关于虚拟化的选项，一般在CPU设置里，含有“Virtualization”的选项，有的话就说明支持，默认是关闭的，打开之后重启电脑准备下一步。如下图所示：

  [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/7acb0a46f21fbe0950fd09e860600c338644adaf.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=3)

- 如果以上两种方法都说明你的CPU不支持的话，有两个选择，一是关闭此教程，二是换电脑。o(´^｀)o

  END

## 第二步 准备所需要的工具软件以及系统镜像

1. 1

   \1.     虚拟机软件**VMware Workstation Pro 12.5.5**

   下载：http://pan.baidu.com/s/1c2kroAW    

   密码：pwad

   \2.     虚拟机MacOS破解工具**Unlocker**

   下载：http://pan.baidu.com/s/1o7B1aum    

   密码：hul0

   \3.     我不知道是干嘛用但是很重要的工具**Python**

   下载：http://pan.baidu.com/s/1kV8z7nx    

   密码：jeo7

   \4.     **MacOS  Seirra10.12.4**镜像

   下载：http://pan.baidu.com/s/1o8hVdbk    

   密码：sez1

   END

## 第三步 虚拟机的安装及MacOS破解

1. 1

   打开虚拟机软件，按照下图一步一步安装完成。

   到第三张图的时候点击许可证，打开云盘下载的文件夹中的Vm激活码文本文档，随便找一个复制进去，不行就下一个，再不行就在百度里找，很容易激活的。

   到最后一步，大家还是选择还是重启一下。

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/0b46f21fbe096b63cd536bad07338744eaf8ac80.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=4)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/ca1349540923dd54c12b9295da09b3de9d8248f6.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=5)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/f31fbe096b63f62457170cfe8c44ebf81b4ca380.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=6)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/a044ad345982b2b7b47b0c393aadcbef77099b62.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=7)

2. 2

   插件工具安装

   重启后，打开任务管理器（右键状态栏→任务管理器），找到服务项，将框中关于VMware全部右键停止运行。如下图一。

   接着双击文件夹中的python 2.7.9.msi文件，除了第一步权限选择外，其他都是“下一步”，直到安装完成。如下图二。

   然后打开Unlocker2.0.7文件夹，找到win-install.cmd，右键编辑。在打开的文档中，找到“echo   Patching...”这一项，将这一项的下一行，改为“C:\Python27\python.exe unlocker.py”，然后保存。其实刚修改的就是python.exe的路径后面加上 unlocker.py（注意前面有空格），只要前面的步骤没有错，这一步就没有任何问题。如图三。

   改完之后保存。

   然后右键“win-install.cmd”，以管理员身份运行，等待其完成。

   到这里，虚拟机的安装破解工作就完成了。

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/500fd9f9d72a60596165d5e72334349b023bbad1.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=8)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/472309f790529822409f0d3edcca7bcb0b46d49a.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=9)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/a71ea8d3fd1f41343f4a31832e1f95cad0c85ec9.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=10)

   END

## 第四步 安装MacOS Sierra

1. 1

   双击打开桌面上的虚拟机软件VMware Workstation Pro，按照以下步骤操作。

   在这里要说明一下，选择光盘映像文件时，需要把文件类型切换为所有文件，因为MacOS的镜像格式是cdr，不是默认的iso。

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/4ec2d5628535e5dd9e7794227dc6a7efcf1b62f7.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=11)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/d8f9d72a6059252d96172cf93f9b033b5ab5b9ce.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=12)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/6159252dd42a283470a607f650b5c9ea14cebfce.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=13)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/9c16fdfaaf51f3de36e988999feef01f3b2979f7.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=14)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/ca1349540923dd54c5289695da09b3de9d8248f7.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=15)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/562c11dfa9ec8a1378b7661dfc03918fa1ecc099.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=16)

2. 2

   安装完成后，点击“开启虚拟机”，如果没有报错，那么恭喜你，不过不报错是不可能的。一般前面的步骤只要正确，接下来只会报一种错误，如下图一。

   这时候不要慌，离成功只差一步了。找到你的MacOS虚拟机所在目录（不是VMware的安装目录，是Mac系统所在的目录），找到虚拟机系统文件目录，进入到文件夹下，找到Macos  10.12.vmx（.vmx前面是你之前设置的虚拟机名称），右键编辑，在 smc.present = "TRUE"  后添加“smc.version= 0”(建议复制，不包括引号)后保存，问题即可解决。见图二图三。

   接下来重新启动虚拟机，就回看到久违的苹果开机画面。见图四。

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/eac4b74543a982263f0b1ada8182b9014b90eb01.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=17)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/f636afc379310a5558acef09bc4543a983261046.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=18)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/faedab64034f78f01133aa0e72310a55b3191c16.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=19)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/f636afc379310a55591cee09bc4543a982261016.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=20)

3. 3

   正式开始MacOS Sierra系统的安装。

   按照下图的步骤一步一步操作就好。

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/7aec54e736d12f2ec8399d9d44c2d5628535680a.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=21)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/9c16fdfaaf51f3de34cc8a999feef01f3b2979d4.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=22)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/4ec2d5628535e5dd901096227dc6a7efce1b620a.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=23)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/e4dde71190ef76c6ddeec8d69616fdfaaf51670a.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=24)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/b58f8c5494eef01fbe6a2b38ebfe9925bd317dd4.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=25)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/f31fbe096b63f6245d070afe8c44ebf81b4ca3f0.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=26)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/3b292df5e0fe992534725aad3fa85edf8cb171d4.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=27)

4. 4

   安装过程比较漫长，你可以去跑、去跳、去做一个漂亮的倒挂金钩，反正我的固态硬盘也等了大概三十多分钟的样子，去尽情的放纵自己或者发朋友圈吧。

   安装完成后，我们需要一系列的设置，才能正常使用MacOS。

   图二也可以选择不连接互联网，因为你选以太网也不一定能连上，连上了后面还需要输Apple ID，连不上就只需要本地账户。

   图三显示果然连不上，我也很无奈啊，我能怎么办啊。不过别担心，系统做好后，还是可以设置网络的。所以安心创建本地连接吧。

   图四到图七之后，只需等待几秒钟，全新的MacOS Sierra系统出现在了眼前，激动么？

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/18d8bc3eb13533fa1f04a1d3a3d3fd1f40345b98.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=28)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/64380cd7912397ddf868aaf95282b2b7d0a2873d.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=29)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/91ef76c6a7efce1be71df537a451f3deb48f651c.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=30)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/63d9f2d3572c11dfbf278dde682762d0f603c25c.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=31)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/622762d0f703918fbc270f375a3d269758eec45c.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=32)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/a6efce1b9d16fdfad2a5f413bf8f8c5495ee7b05.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=33)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/95eef01f3a292df5650a9ee8b7315c6035a87305.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=34)

5. 5

   接下来就需要安装一个很重要的工具了，Vmware Tools。

   说明：VMware虚拟机中安装VMware Tools，可支持自由拖拽的功能，鼠标也可在虚拟机与主机之前自由移动（不用再按ctrl+alt），且虚拟机屏幕也可实现全屏化和独占，让电脑直接成为Mac电脑。好处多多，总之安装就是了。

   图二双击安装VMware Tools，然后就是继续→安装→输入之前设置的本地账户密码→安装软件→继续安装→安装成功后重新启动。

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/4bed2e738bd4b31c78fea9468cd6277f9f2ff809.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=35)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/a08b87d6277f9e2f040821f51430e924b899f309.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=36)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/63d0f703918fa0ec144559f02d9759ee3c6ddb48.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=37)

6. 6

   到此，完整的虚拟机安装MacOS就完成了。待重启后，输入本地账户密码，就可以体验MacOS了。本期的教程就到这里了，谢谢大家耐心的阅读。

   END

## 哦对了！网络还没连接好！

1. 1

   解决办法：在主机上右键状态栏网络图标→打开网络与共享中心→点击连接后面的，是以太网或是WLAN，点就可以了→属性→共享→允许其他用户通过此计算机的Internet来连接打钩→选择VMware  Network Adapter  VMnet1→下面那一项也打钩→确定。主机设置完了，我们现在来设置虚拟机，进入VM软件→工具栏选择虚拟机→设置→网络适配器→仅主机模式→MacOS系统的设置→网络→以太网自分配的IP→使用DHCP。

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/9213b07eca80653858a998ee9cdda144ac34828f.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=38)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/d50735fae6cd7b894ece067e042442a7d8330ea8.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=39)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/faf2b2119313b07e98106cf507d7912396dd8c99.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=40)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/cb8065380cd79123c14da889a6345982b3b78099.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=41)

   [![Win10电脑虚拟安装苹果MacOS无敌完整版](MacOS_InWin10.assets/8b82b9014a90f6038250a0ba3212b31bb151ed6f.jpg)](http://jingyan.baidu.com/album/c74d6000b3ca190f6a595d37.html?picindex=42)

2. 2

    这些设置完成后，你的Mac电脑就可以上网了。启用独占模式后，你插入的U盘、光盘都可以在Mac中读取。不过，Mac对NTFS的U盘是只读的。

   OK！Win10虚拟机安装MacOS的教程到这里就结束啦，我们一路过关斩将，解决这么多问题，是不是很有成就感呢？

   最后，记得别忘了给自己注册一个Apple ID 哦！