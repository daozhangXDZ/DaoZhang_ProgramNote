

# WebCamTexture Constructor



Other Versions

Leave feedback





public WebCamTexture();     

public WebCamTexture(int requestedWidth, int requestedHeight, int requestedFPS);     

public WebCamTexture(int requestedWidth, int requestedHeight);     

public WebCamTexture(string deviceName);     

public WebCamTexture(string deviceName, int requestedWidth, int requestedHeight);     

public WebCamTexture(string deviceName, int requestedWidth, int requestedHeight, int requestedFPS);     

## Parameters

| deviceName      | The name of the video input device to be used. |
| --------------- | ---------------------------------------------- |
| requestedWidth  | The requested width of the texture.            |
| requestedHeight | The requested height of the texture.           |
| requestedFPS    | The requested frame rate of the texture.       |

## Description

Create a WebCamTexture.

Use [WebCamTexture.devices](https://docs.unity3d.com/ScriptReference/WebCamTexture-devices.html)  to get a list of the names of available camera devices. If no device  name is supplied to the constructor or is passed as a null string, the  first device found will be used.

The requested width, height and  framerate specified by the parameters may not be supported by the chosen  camera. In such cases, the closest available values will be used.

Call [Application.RequestUserAuthorization](https://docs.unity3d.com/ScriptReference/Application.RequestUserAuthorization.html) before creating a WebCamTexture.

**Note:** using webcam texture on Android requires a device running Honeycomb (Android 3.0) or later.

**Note:**  If you want to use a WebCamTexture to play the camera stream from a  device connected through Unity Remote, then you must initialize it  through use of the constructor. It is not possible to change the device  later using [WebCamTexture.deviceName](https://docs.unity3d.com/ScriptReference/WebCamTexture-deviceName.html) from a regular device to a remote device and vice versa.

**Note:** For camera devices of kind [WebCamKind.ColorAndDepth](https://docs.unity3d.com/ScriptReference/WebCamKind.ColorAndDepth.html)  (currently these are only dual back and true depth cameras on latest  iOS devices), it is possible to create a WebCamTexture instance to  receive depth data using [WebCamDevice.depthCameraName](https://docs.unity3d.com/ScriptReference/WebCamDevice-depthCameraName.html)  as the deviceName. This WebCamTexture always contains one channel and  is in half-precision floating point format with distance values in  meters.

If required, it is also possible to create a second WebCamTexture instance using [WebCamDevice.name](https://docs.unity3d.com/ScriptReference/WebCamDevice-name.html) as deviceName to receive color data. In this case, both color and depth data will be synchronized.

Currently, iOS supports only limited combinations of color/depth data resolutions. **requestedWidth** and **requestedHeight**  parameters are ignored, when creating WebCamTexture instances for  ColorAndDepth devices. For iPhone 7+/8+ dual back cameras, the size of  the WebCamTexture for color data is 1440x1080 and for iPhone X dual back  and front true depth cameras, it is 1500x1126. The depth data  resolution is always a maximum of 320x240 for iPhone 4+/8+/X dual back  cameras and 640x480 for iPhone X front true depth cameras.