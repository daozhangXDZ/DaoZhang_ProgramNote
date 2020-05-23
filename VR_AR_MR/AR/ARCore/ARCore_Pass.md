# 深入浅出 ARCore

## 前言

其实关注 ARCore也蛮久了，但一直没有腾出时间来写个总结。正好应朋友之约，我们今天就来好好聊一聊 ARCore.

ARCore的历史以及与苹果ARKit的竞争我就不多讲了，在网上可以搜到一堆信息。但网上深入讲解ARCore的确实不多。

本文主要有两个目的，一是向大家介绍一下ARCore的基本概念，了解这些概念对于大家后续深入的学习 ARCore具有关键的作用。二是深入剖析一下 ARCore的工作机理，这样可以让大家更容易理解 ARCore。

另外，ARCore与ARKit的基本概念很接近，只要了解了其中的一个，基本上也就掌握了另一个。

> 由于本文篇幅有此长，而且很多新概念，所以大家在阅读时要做好心理准备。：）

## ARCore的基本概念

ARCore工作时要做两件事儿，首先跟踪手机的运动轨迹，然后构建出它对现实世界的理解。

ARCore的运动跟踪技术是通过 Camera 标识出特征点，并随着时间的推移跟踪这些特征点是如何移动的。通过这些特征点的运动数据及从手机惯性传感器读到的信息，ARCore计算出手机移动的位置和方向，并称其为姿态。

除了识别出这些特征点外，ARCore还能检测出像地板、桌面等平面信息以及在某个地方的光线强度。这些信息使得ARCore能够构建出自己理解的真实世界。构建出这样一个模型后，可以在上面放置一些虚拟内容了。

ARCore是如何做到的呢？它使用三项关键技术将虚拟内容与真实世界整合到一起，这三种技术分别是：

- **运动跟踪**
- **环境理解**
- **光线评估**

### 运动跟踪



![img](https:////upload-images.jianshu.io/upload_images/5956443-070fa1ebd86bb770.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000)

运动跟踪

ARCore 可以在手机移动的过程中知道，相对于真实世界手机所在的位置和方向（姿势）。

当手机在真实世界移动时，ARCore使用称为并发测距和映射的过程来了解手机与周围世界的相对位置。

ARCore能检测到Camera捕获的图像在视觉上的不同特征，称为特征点。它使用这些点计算其位置变化。随着时间的推移，通过视觉信息与来自IMU设备的惯性测量，ARCore就可以估算出Camera相对于真实世界的姿态（位置和方向）。

通过将渲染的3D虚拟内容与物理Camera的姿势对齐，开发人员就可以从正确的角度渲染虚拟内容。 再通过将虚拟物品的图像渲染到从Camera获得的图像之上，这样看起来就好像虚拟内容是真实世界的一部分似的。

### 环境理解



![img](https:////upload-images.jianshu.io/upload_images/5956443-1994182d706d4afd.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000)

环境理解

ARCore可以让手机检测出一块水平面的位置和大小。如地面、桌子、书架等等。这样就可以将虚拟物体放置到检测出的水平面上了。

它是如何做到的呢？ARCore通过检测特征点和平面不断改善对现实世界环境的理解。

ARCore会查找常见水平表面（如桌面）上的特征点集群，除此之外，ARCore还可以确定每个平面的边界，并将以上信息提供给您的应用程序。 这样，开发人员就可以使用这些信息，并将虚拟物体放置在平坦的表面上了。

由于ARCore使用特征点检测平面，因此可能无法正确检测到没有纹理的平坦表面（如白色桌面）。

### 光线评估



![img](https:////upload-images.jianshu.io/upload_images/5956443-a7871f2b82c835c3.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000)

光线估计

ARCore 可以让手机估算出当前环境的光线强度，这样可以让虚拟物理显示在真实环境中更加逼真。

### 用户交互

ARCore使用 hit testing（命中测试) 获取与手机屏幕相对应的(x,y)坐标（如通过点击屏幕等交互方式），将其投射到 Camera 的3D坐标系中，并返回与命中点射线相交的所有平面和特征点，以及在世界坐标系中该交叉点的姿态。这样就能实现用户与ARCore环境中的对象交互了。

### 锚点与跟踪

ARCore可以改变对自身位置和环境的理解来调整姿态。如我们要在ARCore环境中放置一个虚拟对象，首先要确定一个锚点，以确保ARCore能随着时间的推移不断跟踪对象的位置。通常情况下，会根据命中测试返回的姿势创建一个锚点。

姿势改变这项技术特别关键，只有得到姿势，ARCore才可以随着时间的推移不断更新环境对象（像飞机和特征点）的位置。ARCore将平面和点认为是可跟踪的特殊类型的对象。您可以将虚拟对象锚定到这些可追踪的对象上，以确保在设备移动时，虚拟对象和可跟踪对象之间保持稳定的关系。这就好像您在桌面上放置一个虚拟的花瓶，如果ARCore稍后调整与桌面相关的姿势，那么花瓶仍然会保持在桌面上。

## ARCore 核心类介绍

### Session

`com.google.ar.core.Session`类，Session管理AR系统状态并处理Session生命周期。 该类是ARCore API的主要入口点。 该类允许用户创建Session，配置Session，启动/停止Session，最重要的是接收视频帧，以允许访问Camera图像和设备姿势。

### Config

`com.google.ar.core.Config`类，用于保存Session的设置。

### Frame

`com.google.ar.core.Frame`类，该类通过调用update()方法，获取状态信息并更新AR系统。

### HitResult

`com.google.ar.core.HitResult`类，该类定义了命中点射线与估算的真实几何世界之间的交集。

### Point

`com.google.ar.core.Point`类，它代表ARCore正在跟踪的空间点。 它是创建锚点（调用createAnchor方法）时，或者进行命中检测（调用hitTest方法）时，返回的结果。

### PointCloud



![img](https:////upload-images.jianshu.io/upload_images/5956443-d063b5bfff3f28e4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000)

点云

`com.google.ar.core.PointCloud`类，它包含一组观察到的3D点和信心值。

### Plane



![img](https:////upload-images.jianshu.io/upload_images/5956443-fe05bd29c94f5dbf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/960)

平面

`com.google.ar.core.Plane`类，描述了现实世界平面表面的最新信息。

### Anchor

`com.google.ar.core.Anchor`类，描述了现实世界中的固定位置和方向。 为了保持物理空间的固定位置，这个位置的数字描述信息将随着ARCore对空间的理解的不断改进而更新。

### Pose

`com.google.ar.core.Pose`类, 姿势表示从一个坐标空间到另一个坐标空间位置不变的转换。 在所有的ARCore API里，姿势总是描述从对象本地坐标空间到世界坐标空间的转换。

随着ARCore对环境的了解不断变化，它将调整坐标系模式以便与真实世界保持一致。 这时，Camera和锚点的位置（坐标）可能会发生明显的变化，以便它们所代表的物体处理恰当的位置。

这意味着，每一帧图像都应被认为是在一个完全独立的世界坐标空间中。锚点和Camera的坐标不应该在渲染帧之外的地方使用，如果需考虑到某个位置超出单个渲染框架的范围，则应该创建一个锚点或者应该使用相对于附近现有锚点的位置。

### ImageMetadata

`com.google.ar.core.ImageMetadata`类，提供了对Camera图像捕捉结果的元数据的访问。

### LightEstimate

`com.google.ar.core.LightEstimate`保存关于真实场景光照的估计信息。 通过 getLightEstimate()得到。

### ~~Trackable~~

`com.google.ar.core.Pose`接口类，它是ARCore可以跟踪的，并能与锚点绑定在一起的东西。

### ~~Camera~~

`android.graphics.Camera`类，它提供用于捕获图像的Camera的信息。 Camera是一个长期存活的对象，每次调用Session.update() 都会更新Camera的属性。

## 实例分析

Google发布的 ARCore SDK 中包括了一些例子程序，有了上面的基本知识后，我们就很容易理解他所写的 Demo 程序的流程了。

### 创建 Session 和 Conig

在 Activity中的 onCreate 方法中创建 Session 和 Config是个不错的地方。

```
mSession = new Session(/*context=*/this);

mDefaultConfig = Config.createDefaultConfig();
if (!mSession.isSupported(mDefaultConfig)) {
    Toast.makeText(this, "This device does not support AR", Toast.LENGTH_LONG).show();
    finish();
    return;
}
```

- Session： 是ARCore的管理类，它非常重要。ARCore的打开，关闭，视频帧的获取等都是通过它来管理的。
- Config：存放一些配置信息，如平面的查找模式，光照模式等信息都是记录在该类中。目前该类还比较简单，里边没存多少东西。
- isSupported：该方法主要是对 SDK的版本及机型做控制。目前官方只支持几款Google和三星的机子做测试。其它机型还都不支持ARCore，当然有一些机型通过破解后的SDK是可以使用 ARCore的。该方法中的 Config 参数没有用到。

### 创建 GLSurfaceView 用于AR展示

在 Google 提供的Demo中，AR的展示部分使用的是 GLSurfaceView。做视频开发的同学都清楚，Android 可以使用三种View进行视频渲染。分别是：

- SurfaceView
- GLSurfaceView
- TextureView

其中，SurfaceView最灵活，效率也最高，但使用起来比较烦锁。而GLSurfaceView相对 SurfaceView就是简单很多，只需要实现它的 Render 接口即可。而 TextureView使用最简单，很多工作都由 Android 的窗口管理器帮你做了，但灵活性相对较差。

> ~~更为详细的信息请参考我的另一篇文章~~

为了渲染的高效，Google在Demo中大量使用了OpenGL技术。由于OpenGL是图像处理非常大的一个领域，无法通过一两篇文章讲解清楚，同时也不是我们本文的重点，所以我们这里不对它做详细介绍，有兴趣的同学可以到网上自行学习。

```
mSurfaceView = (GLSurfaceView) findViewById(R.id.surfaceview);
...
mSurfaceView.setPreserveEGLContextOnPause(true);
mSurfaceView.setEGLContextClientVersion(2);
mSurfaceView.setEGLConfigChooser(8, 8, 8, 8, 16, 0); // Alpha used for plane blending.
mSurfaceView.setRenderer(this);     mSurfaceView.setRenderMode(GLSurfaceView.RENDERMODE_CONTINUOUSLY);
```

该段代码首先通过资源文件创建一个GLSurfaceView对象，然后将 GLSurfaceView 与 EGL 上下文关联。并将Activity作为GLSurfaceView的回调对象（也就是说该Activity要实现 GLSurfaceView.Renderer中定义的接口，如onSurfaceCreated、onSurfaceChanged、onDrawFrame等），最后设置 mSurfaceView 的渲染模式为 GLSurfaceView.RENDERMODE_CONTINUOUSLY，即对 GLSurfaceView 持续不断的渲染。

## 创建各种线程

要理解本节内容，首先大家要知道AR的详细工作原理是怎样的。我在这里再向大家做个简要的说明。

**背景展示**

用过AR的人都知道，AR是将一些虚拟物品放到真实的场景中。那么这个真实的场景从哪里来呢？当然是从手机的 Camera上获取。

我们把从 Camera中获取的视频当作 AR的背景。其实，AR 就是将虚拟物品放到视频上，只不过不是简单的放置，而是需要经过大量的计算，找到视频中的平面位置再放置。

而Android中视频的采集相对比较简单，像直播系统，照像机都要使用该技术。

**平台检测**

上面我们已经说了，AR就是实时视频+虚拟物品。但虚拟物不能简单的放到视频上，而是先对视频中的每一帧进行检测，找到视频中的平面，确定好位置后，再将虚拟物品放置上去。这样才算是AR呀：）

**点云**

上面我们知道了，AR=实时视频+平面+虚拟物品。除此之外，它还应该能对虚拟物品进行跟踪，也就是可以在不同的角度观察同一个物品，并得出不同的姿态，所以就有了“点云” 技术。那什么是点云呢？顾名思义，形象的说就是一堆点，这些的形状有点像云。点云中的每个点都是一个特征点，它是通过Camera获得的。

**放置虚拟物品**

找到了平面，有了跟踪手段，我们就可以将准备好的虚拟物品放置到平台上，现在才是真正的AR哈。

好，知道了这些基本原理后，我们来看看Google Demo是如何做的呢？

**创建线程**

对于上面的每一点，Demo都启动了一个线程，代码如下：

```
...

// Create the texture and pass it to ARCore session to be filled during update().
mBackgroundRenderer.createOnGlThread(/*context=*/this);
mSession.setCameraTextureName(mBackgroundRenderer.getTextureId());

// Prepare the other rendering objects.
try {
    mVirtualObject.createOnGlThread(/*context=*/this, "andy.obj", "andy.png");
    mVirtualObject.setMaterialProperties(0.0f, 3.5f, 1.0f, 6.0f);
    ...
} catch (IOException e) {
    Log.e(TAG, "Failed to read obj file");
}
try {
    mPlaneRenderer.createOnGlThread(/*context=*/this, "trigrid.png");
} catch (IOException e) {
    Log.e(TAG, "Failed to read plane texture");
}
mPointCloud.createOnGlThread(/*context=*/this);

...
```

上面的代码中首先创建了一个背景线程，用来将从Camera中获取的视频渲染到屏幕上当背景。数据是从哪里来的呢？就是通过 Session.update 获取 Camera 数据，再通过纹理交给背景线程。

> 对纹理没有概念的同学可以把它想像成一块内存空间。

然后启动虚拟物品线程，用于绘制虚拟物品，及发生角度变化时，更新虚拟物别的姿势。紧接着创建平面线程来绘制平面。最后启动点云线程绘制特征点。

到此，各种线程就创建完毕了。下面我们来说一下如何渲染。

## 命中检测与渲染

**命中检测**

当我们要向背景绘制虚拟物品时，首先要进行命中检测。代码如下：

```
MotionEvent tap = mQueuedSingleTaps.poll();
if (tap != null && frame.getTrackingState() == TrackingState.TRACKING) {
    for (HitResult hit : frame.hitTest(tap)) {
        // Check if any plane was hit, and if it was hit inside the plane polygon.
        if (hit instanceof PlaneHitResult && ((PlaneHitResult) hit).isHitInPolygon()) {
            // Cap the number of objects created. This avoids overloading both the
            // rendering system and ARCore.
            if (mTouches.size() >= 16) {
                mSession.removeAnchors(Arrays.asList(mTouches.get(0).getAnchor()));
                mTouches.remove(0);
            }
            // Adding an Anchor tells ARCore that it should track this position in
            // space. This anchor will be used in PlaneAttachment to place the 3d model
            // in the correct position relative both to the world and to the plane.
            mTouches.add(new PlaneAttachment(
                ((PlaneHitResult) hit).getPlane(),
                mSession.addAnchor(hit.getHitPose())));

            // Hits are sorted by depth. Consider only closest hit on a plane.
            break;
        }
    }
}
```

在例子中，它查看是否有点击事件，且图像处理于跟踪状态？如果是，就对其进行命中检测，看是否可以找到一个平面，如果找到就创建一个锚点并将其与该平台绑定起来。

**渲染背景**

```
// Draw background.
mBackgroundRenderer.draw(frame);
```

通过上面的代码就可以将纹理中的内容推给 EGL，上面创建的渲染线程从 EGL 上下文中获取数据，最终将视频渲染到屏幕上。

**绘制点云**

```
mPointCloud.update(frame.getPointCloud());
mPointCloud.draw(frame.getPointCloudPose(), viewmtx, projmtx);
```

同理，通过上面的代码，就可以将数据传给点云线程进行点云的绘制。

**绘制平面**

```
// Visualize planes.
mPlaneRenderer.drawPlanes(mSession.getAllPlanes(), frame.getPose(), projmtx);
```

通过上面代码将数据传给平面线程进行平面的绘制。

**绘制虚拟物品**

```
for (PlaneAttachment planeAttachment : mTouches) {
    if (!planeAttachment.isTracking()) {
        continue;
    }
    // Get the current combined pose of an Anchor and Plane in world space. The Anchor
    // and Plane poses are updated during calls to session.update() as ARCore refines
    // its estimate of the world.
    planeAttachment.getPose().toMatrix(mAnchorMatrix, 0);

    // Update and draw the model and its shadow.
    mVirtualObject.updateModelMatrix(mAnchorMatrix, scaleFactor);
    mVirtualObjectShadow.updateModelMatrix(mAnchorMatrix, scaleFactor);
}
```

最后，遍历所有的锚点，在每个锚点上绘制虚拟物品。

至此，我们对ARCore的分析就告一段落了。

## 小结

ARCore相对于初学者来说还是有不少难度的。因为里面有很多新概念需要大家消化吸收。

另一方面，ARCore目前只有几款机型可能做测试，而这几款机型在国内用的人不多，所以对于大多数人来说没法做实验，这也增加了学习的难度。

除了以上两点外，ARCore中大量使用了 OpenGL的相关知识。而OpenGL又是一门很深的学问，所以学习的难度更加陡峭了。

通过以上三点，可以说目前学习ARCore的门槛相较于苹果的ARKit要难不少。

希望本文能对您有所帮助，并请多多关注我，谢谢！

## 参考

[ARCore github](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fgoogle-ar%2Farcore-android-sdk.git)

小礼物走一走，来简书关注我

作者：音视频直播技术专家

链接：https://www.jianshu.com/p/0e819c39f3cb

来源：简书

简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。