#      Unity for Android 云锚点快速入门   

使用云锚点可以打造 Android 和 iOS 用户能够共享的 AR 体验。

## 先决条件

- 如果您对锚点的使用不熟悉，请参阅[使用锚点](https://developers.google.cn/ar/develop/developer-guides/anchors?hl=zh-cn)，查看介绍。

- 以下步骤假定您已安装 ARCore SDK for Unity，并将其配置为以 Android 为目标。 

   否则，请参阅 ARCore SDK [Android 快速入门](https://developers.google.cn/ar/develop/unity/quickstart-android?hl=zh-cn)中的安装和环境配置说明。

## 要求

请参阅 [Android 快速入门](https://developers.google.cn/ar/develop/unity/quickstart-android?hl=zh-cn)中的[要求](https://developers.google.cn/ar/develop/unity/quickstart-android?hl=zh-cn#requirements)。

## 使用云锚点

针对使用云锚点设置您的开发环境并试用示例应用。

### 关于云锚点 ID 共享

具有云锚点功能的应用需要一种在设备之间共享云锚点 ID 的方式。

**CloudAnchors** 示例应用使用 [Unity 的网络功能](https://docs.unity3d.com/Manual/UNetOverview.html)在同一个网络上的设备之间共享云锚点 ID。  您可以在自己的应用中使用不同的解决方案。

### 添加 API 密钥

要在您的应用中使用 ARCore Cloud Anchor API，您需要一个 API 密钥。

1. 获取一个 API 密钥。 如果您对 API 密钥的使用不熟悉，请参阅 Google Cloud Platform Console 帮助中心中的[设置 API 密钥](https://support.google.com/cloud/answer/6158862?ref_topic=6262490&hl=zh-cn)。
2. 为您的 Google Cloud Platform 项目[启用 ARCore Cloud Anchor API](https://console.cloud.google.com/apis/library/arcorecloudanchor.googleapis.com?hl=zh-cn)  。
3. 将您的 API 密钥添加到项目中：
   - 在 Unity 中，转到 **Edit > Project Settings > ARCore**
   - 将您的 API 密钥添加到 **Cloud Services API Key** 字段中。

### 打开示例

**CloudAnchors** 示例包含在 ARCore SDK for Unity 中。

1. 在 Unity 的 **Project** 窗口中，您可以在以下位置找到 **CloudAnchor.unity** 场景： 
     **Assets > GoogleARCore > Examples > CloudAnchor > Scenes**

### 试用示例应用

构建并运行 **CloudAnchors** 示例应用，尝试托管和解析云锚点。

1. 确保按照 ARCore SDK [Unity 快速入门](https://developers.google.cn/ar/develop/unity/quickstart-android?hl=zh-cn)的[配置构建设置](https://developers.google.cn/ar/develop/unity/quickstart-android?hl=zh-cn#configure_build_settings)步骤中的说明配置您的构建和播放器设置。

2. 确保在您的手机上启用[开发者选项和调试](https://developer.android.google.cn/studio/debug/dev-options.html?hl=zh-cn)。

3. 通过 USB 将您的手机连接到开发计算机。

4. 在 Unity 中点击 **Play**。

5. 示例应用将使用 [Instant Preview](https://developers.google.cn/ar/develop/unity/instant-preview?hl=zh-cn) 在您的手机上启动。

6. 来回移动您的手机，直至 ARCore 开始检测和显示平面。

7. 点按某个平面，在上面锚定一个 Andy Android 物体。

8. 点按 **HOST** 按钮，托管锚点。

   将向 Google 云锚点服务发送一个托管请求。 托管请求包含表示锚点相对于附近可视特征的位置的数据。 成功的托管请求将在此处创建一个云锚点，并为其分配一个云锚点 ID。

   在托管请求成功后，应用将显示一个房间代码。 您可以在同一个设备或其他设备上使用这个代码访问此房间之前托管的云锚点。

9. 点按 **RESOLVE** 并输入之前返回的房间代码，访问此房间的托管云锚点。

   将向 Google 云锚点服务发送一个解析请求，如果成功，将返回房间中当前托管的云锚点。 示例应用使用返回的云锚点的转换来渲染连接到这些锚点的 Andy Android 物体。

## 后续步骤

- [云锚点开发者指南](https://developers.google.cn/ar/develop/unity/cloud-anchors/developer-guide-unity?hl=zh-cn)
- ARCore SDK for [Unity API 参考](https://developers.google.cn/ar/reference/unity?hl=zh-cn)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see our [Site Policies](https://developers.google.cn/terms/site-policies?hl=zh-cn). Java is a registered trademark of Oracle and/or its affiliates.

​              上次更新日期：一月 14, 2019     