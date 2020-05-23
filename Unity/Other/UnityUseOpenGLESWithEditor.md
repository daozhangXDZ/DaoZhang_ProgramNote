# UnityUseCommand WithEditor

@author: 白袍小道

# Command line arguments

You can run Unity from the command line (from the macOS **Terminal** or the Windows **Command Prompt**).

On **macOS**, type the following into the **Terminal** to launch Unity:

```
/Applications/Unity/Unity.app/Contents/MacOS/Unity
```

On **Windows**, type the following into the **Command Prompt** to launch Unity:

```
C:\Program Files\Unity\Editor\Unity.exe
```

When you launch it like this, Unity receives commands and information on startup, which can be very useful for test suites, automated builds  and other production tasks.
 **Note**: Use the same method to launch standalone Unity games.

## Launching Unity silently

On **macOS**, type the following into the **Terminal** to silently launch Unity:

```
/Applications/Unity/Unity.app/Contents/MacOS/Unity -quit -batchmode -serial SB-XXXX-XXXX-XXXX-XXXX-XXXX -username 'JoeBloggs@example.com' -password 'MyPassw0rd'
```

 **Note**: When activating via the command line using continuous integration (CI) tools like Jenkins, add the `-nographics` flag to prevent a WindowServer error.

On **Windows**, type the following into the **Command Prompt** to silently launch Unity:

```
Windows: C:\Program Files\Unity\Editor\Unity.exe" -batchmode -username name@example.edu.uk - password XXXXXXXXXXXXX -serial E3-XXXX-XXXX-XXXX-XXXX-XXXX –quit
```

## Returning the license to the license server

On **macOS**, type the following into the **Terminal** to return the license:

```
/Applications/Unity/Unity.app/Contents/MacOS/Unity -quit -batchmode -returnlicense
```

On **Windows**, type the following into the **Command Prompt** to return the license:

```
"C:\Program Files\Unity\Editor\Unity.exe" -quit -batchmode -returnlicense
```

## Create activation file and import license file by command

On **macOS**, type the following into the **Terminal**:

```
/Applications/Unity/Unity.app/Contents/MacOS/Unity -batchmode -createManualActivationFile -logfile

/Applications/Unity/Unity.app/Contents/MacOS/Unity -batchmode -manualLicenseFile <yourulffile> -logfile
```

On **Windows**, type the following into the **Command Prompt**:

```
"C:\Program Files\Unity\Editor\Unity.exe" -batchmode -createManualActivationFile -logfile

"C:\Program Files\Unity\Editor\Unity.exe" -batchmode -manualLicenseFile <yourulffile> -logfile
```

Check [Manual Activation Guide](https://docs.unity3d.com/Manual/ManualActivationGuide.html) for more details.  

## Options

You can run the Editor and built Unity games with additional commands and information on startup. This section describes the command line  options available.

| **Command**                        | **Details**                                                  |
| :--------------------------------- | :----------------------------------------------------------- |
| `-assetServerUpdate ]>`            | Force an update of the project in the [Asset Server](https://docs.unity3d.com/Manual/AssetServer.html) given by `IP:port`. The port is optional, and if not given it is assumed to be the standard one (10733). It is advisable to use this command in conjunction with  the `-projectPath` argument to ensure you are working with  the correct project. If you don’t give a project name, then the command  line uses the last project opened by Unity. If no project exists at the  path `-projectPath` gives, then the command line creates one automatically. |
| `-batchmode`                       | Run Unity in batch mode. You should always use this in conjunction with the other command line arguments, because  it ensures no pop-up windows appear and eliminates the need for any  human intervention. When an exception occurs during execution of the  script code, the Asset server updates fail, or other operations fail,  Unity immediately exits with return code **1**.  Note that in batch mode, Unity sends a minimal version of its log output to the console. However, the [Log Files](https://docs.unity3d.com/Manual/LogFiles.html) still contain the full log information. You cannot open a project in  batch mode while the Editor has the same project open; only a single  instance of Unity can run at a time. **Tip**: To check whether you are running the Editor or Standalone Player in batch mode, use the [Application.isBatchMode](https://docs.unity3d.com/ScriptReference/Application-isBatchMode.html) operator.   If the project has not yet been imported when using `-batchmode`, the target platform is the default one. To force a different platform when using `-batchmode`, use the `-buildTarget` option. |
| `-buildLinux32Player `             | Build a 32-bit standalone Linux player (for example, `-buildLinux32Player path/to/your/build`). |
| `-buildLinux64Player `             | Build a 64-bit standalone Linux player (for example, `-buildLinux64Player path/to/your/build`). |
| `-buildLinuxUniversalPlayer `      | Build a combined 32-bit and 64-bit standalone Linux player (for example, `-buildLinuxUniversalPlayer path/to/your/build`). |
| `-buildOSXPlayer `                 | Build a 32-bit standalone Mac OSX player (for example, `-buildOSXPlayer path/to/your/build.app`). |
| `-buildOSX64Player `               | Build a 64-bit standalone Mac OSX player (for example, `-buildOSX64Player path/to/your/build.app`). |
| `-buildOSXUniversalPlayer `        | Build a combined 32-bit and 64-bit standalone Mac OSX player (for example, `-buildOSXUniversalPlayer path/to/your/build.app`). |
| `-buildTarget `                    | Allows the selection of an active build target before loading a project. Possible options are:   standalone, Win, Win64, OSXUniversal, Linux, Linux64, LinuxUniversal,  iOS, Android, Web, WebStreamed, WebGL, XboxOne, PS4, WindowsStoreApps,  Switch, N3DS, tvOS. |
| `-buildWindowsPlayer `             | Build a 32-bit standalone Windows player (for example, `-buildWindowsPlayer path/to/your/build.exe`). |
| `-buildWindows64Player `           | Build a 64-bit standalone Windows player (for example, `-buildWindows64Player path/to/your/build.exe`). |
| `-stackTraceLogType`               | Detailed debugging feature. StackTraceLogging allows you to allow detailed logging. All settings allow **None**, **Script Only** and **Full** to be selected. (for example, `-stackTraceLogType Full`) |
| `-CacheServerIPAddress `           | Connect to the specified Cache Server on  startup, overriding any configuration stored in the Editor Preferences.  Use this to connect multiple instances of Unity to different Cache  Servers. |
| `-createProject `                  | Create an empty project at the given path.                   |
| `-editorTestsCategories`           | Filter editor tests by categories. Separate test categories with a comma. |
| `-editorTestsFilter`               | Filter editor tests by names. Separate test names with a comma. |
| `-editorTestsResultFile`           | Path location to place the result file. If the path is a folder, the command line uses a default file name. If not specified, it places the results in the project’s root folder. |
| `-diag-debug-shader-compiler`      | Unity launches only one instance of the **Shader**  Compiler, and forces its timeout to be one hour. Useful for debugging **Shader** Compiler issues. |
| `-enableCodeCoverage`              | Enables code coverage and allows access to the [Coverage API](https://docs.unity3d.com/ScriptReference/TestTools.Coverage.html). |
| `-executeMethod `                  | Execute the static method as soon as Unity opens the project, and after the optional Asset server update is  complete. You can use this to do tasks such as continous integration,  performing Unit Tests, making builds or preparing data. To return an  error from the command line process, either throw an exception which  causes Unity to exit with return code **1**, or call [EditorApplication.Exit](https://docs.unity3d.com/ScriptReference/EditorApplication.Exit.html) with a non-zero return code. To pass parameters, add them to the command line and retrieve them inside the function using `System.Environment.GetCommandLineArgs`. To use `-executeMethod`, you need to place the enclosing script in an Editor folder. The method you execute must be defined as **static**. |
| `-exportPackage `                  | Export a package, given a path (or set of given paths). In this example `exportAssetPath` is a folder (relative to to the Unity project root) to export from the Unity project, and `exportFileName` is the package name. Currently, this option only exports whole folders  at a time. You normally need to use this command with the `-projectPath` argument. |
| `-force-d3d11` (Windows only)      | Make the Editor use Direct3D 11 for **rendering** . Normally the graphics API depends on **Player** settings (typically defaults to D3D11). |
| `-force-device-index`              | When using Metal, make the Editor use a particular GPU device by passing it the index of that GPU (macOS only). |
| `-force-gfx-metal`                 | Make the Editor use Metal as the default graphics API (macOS only). |
| `-force-glcore`                    | Make the Editor use OpenGL 3/4 core  profile for rendering. The Editor tries to use the best OpenGL version  available and all OpenGL extensions exposed by the OpenGL drivers. If  the platform isn’t supported, Direct3D is used. |
| `-force-glcoreXY`                  | Similar to `-force-glcore`, but requests a specific OpenGL context version. Accepted values for XY: 32, 33, 40, 41, 42, 43, 44 or 45. |
| `-force-gles` (Windows only)       | Make the Editor use OpenGL for Embedded  Systems for rendering. The Editor tries to use the best OpenGL ES  version available, and all OpenGL ES extensions exposed by the OpenGL  drivers. |
| `-force-glesXY` (Windows only)     | Similar to `-force-gles`, but requests a specific OpenGL ES context version. Accepted values for XY: 30, 31 or 32. |
| `-force-clamped`                   | Used with `-force-glcoreXY` to prevent checking for additional OpenGL extensions, allowing it to run between platforms with the same code paths. |
| `-force-free`                      | Make the Editor run as if there is a free Unity license on the machine, even if a Unity Pro license is installed. |
| `-force-low-power-device`          | When using Metal, make the Editor use a low power device (macOS only). |
| `-importPackage `                  | Import the given [package](https://docs.unity3d.com/Manual/HOWTO-exportpackage.html) . No import dialog is shown. |
| `-logFile `                        | Specify where Unity writes the Editor or Windows/Linux/OSX standalone log file. To output to the console, specify `-` for the path name. On Windows, specify `-` option to ensure output goes to `stdout`, which is not the console by default. |
| `-nographics`                      | When running in batch mode, do not  initialize the graphics device at all. This makes it possible to run  your automated workflows on machines that don’t even have a GPU  (automated workflows only work when you have a window in focus,  otherwise you can’t send simulated input commands). Note that `-nographics` does not allow you to bake GI, because **Enlighten**  requires GPU acceleration. |
| `-noUpm`                           | Disables the Unity Package Manager.                          |
| `-password `                       | Enter a password into the log-in form during activation of the Unity Editor. |
| `-projectPath `                    | Open the project at the given path.                          |
| `-quit`                            | Quit the Unity Editor after other commands have finished executing. Note that this can cause error messages to be  hidden (however, they still appear in the Editor.log file). |
| `-returnlicense`                   | Return the currently active license to the license server. Please allow a few seconds before the license file is  removed, because Unity needs to communicate with the license server. |
| `-runEditorTests`                  | Run Editor tests from the project. This argument requires the `projectPath`, and it’s good practice to run it with `batchmode` argument. `quit` is not required, because the Editor automatically closes down after the run is finished. |
| `-serial `                         | Activate Unity with the specified serial key. When using this to automatically activate Unity, you must pass the `-batchmode`, and it is good practice to pass the `-quit` argument. Please allow a few seconds before the license file is  created, because Unity needs to communicate with the license server.  Make sure that license file folder exists, and has appropriate  permissions before running Unity with this argument. If activation  fails, see the [Editor.log](https://docs.unity3d.com/Manual/LogFiles.html) for info. |
| `-setDefaultPlatformTextureFormat` | Sets the default texture compression to  the desired format before importing a texture or building the project.  This is so you don’t have to import the texture again with the format  you want. The available formats are dxt, pvrtc, atc, etc, etc2, and  astc.  Note that this is only supported on Android. |
| `-silent-crashes`                  | Prevent Unity from displaying the dialog  that appears when a Standalone Player crashes. This argument is useful  when you want to run the Player in automated builds or tests, where you  don’t want a dialog prompt to obstruct automation. |
| `-username `                       | Enter a username into the log-in form during activation of the Unity Editor. |
| `-disable-assembly-updater `       | Specify a space-separated list of assembly names as parameters for Unity to ignore on automatic updates.  The space-separated list of assembly names is optional: Pass the  command line options without any assembly names to ignore all  assemblies, as in example 1.  Example 1 `unity.exe -disable-assembly-updater`   Example 2 has two assembly names, one with a pathname. Example 2 ignores `A1.dll`, no matter what folder it is stored in, and ignores `A2.dll` only if it is stored under `subfolder` folder:  Example 2 `unity.exe -disable-assembly-updater A1.dll subfolder/A2.dll`   If you list an assembly in the `-disable-assembly-updater` command line parameter (or if you don’t specify assemblies), Unity logs the following message to [Editor.log](https://docs.unity3d.com/Manual/LogFiles.html):    `[Assembly Updater] warning: Ignoring assembly [assembly_path] as requested by command line parameter.”).`    Use this to avoid unnecessary [API Updater](https://docs.unity3d.com/Manual/APIUpdater.html) overheads when importing assemblies.   It is useful for importing assemblies which access a Unity API when you  know the Unity API doesn’t need updating. It is also useful when  importing assemblies which do not access Unity APIs at all (for example, if you have built your game source code, or some of it, outside of  Unity, and you want to import the resulting assemblies into your Unity  project).    Note: If you disable the update of any assembly that  does need updating, you may get errors at compile time, run time, or  both, that are hard to track. |
| `-accept-apiupdate`                | Use this command line option to specify that APIUpdater should run when Unity is launched in batch mode.   Example:  `unity.exe -accept-apiupdate -batchmode [other params]`  Omitting this command line argument when launching Unity in batch mode results  in APIUpdater not running which can lead to compiler errors. Note that  in versions prior to 2017.2 there’s no way to not run APIUpdater when  Unity is launched in batch mode. |

## Examples

### C#:

```
using UnityEditor;
class MyEditorScript
{
     static void PerformBuild ()
     {
         string[] __scenes__ = { "Assets/MyScene.unity" };
         BuildPipeline.BuildPlayer(scenes, ...);
     }
}
```

The following command executes Unity in batch mode, executes the `MyEditorScript.PerformBuild` method, and then quits upon completion.

**Windows:**

```
C:\program files\Unity\Editor\Unity.exe -quit -batchmode -executeMethod MyEditorScript.PerformBuild
```

 **Mac OS:** 

```
/Applications/Unity/Unity.app/Contents/MacOS/Unity -quit -batchmode -executeMethod MyEditorScript.PerformBuild
```

The following command executes Unity in batch mode, and updates from the **Asset server**
 using the supplied project path. The method executes after all Assets are downloaded and imported from the **Asset server**. After the function has finished execution, Unity automatically quits.

```
/Applications/Unity/Unity.app/Contents/MacOS/Unity -batchmode -projectPath ~/UnityProjects/AutobuildProject -assetServerUpdate 192.168.1.1 MyGame AutobuildUser l33tpa33 -executeMethod MyEditorScript.PerformBuild -quit
```

## Unity Editor special command line arguments

You should only use these under special circumstances, or when directed by Unity Support.

| **Command**                         | **Details**                                                  |
| :---------------------------------- | :----------------------------------------------------------- |
| `-enableIncompatibleAssetDowngrade` | Use this when you have Assets made by a  newer, incompatible version of Unity, that you want to downgrade to work with your current version of Unity. When enabled, Unity presents you  with a dialog asking for confirmation of this downgrade if you attempt  to open a project that would require it.  **Note:** This procedure is unsupported and highly risky, and should only be used as a last resort. |

## Unity Standalone Player command line arguments

Standalone players built with Unity also understand some command line arguments:

| **Command**                               | **Details**                                                  |
| :---------------------------------------- | :----------------------------------------------------------- |
| `-adapter N` (Windows only)               | Allows the game to run full-screen on  another display. The N maps to a Direct3D display adaptor. In most cases there is a one-to-one relationship between adapters and video cards. On cards that support multi-head (that is, they can drive multiple  monitors from a single card) each “head” may be its own adapter. |
| `-batchmode`                              | Run the game in “headless” mode. The game  does not display anything or accept user input. This is mostly useful  for running servers for [networked games](https://docs.unity3d.com/Manual/UNet.html). |
| `-force-d3d11` (Windows only)             | Force the game to use Direct3D 11 for rendering.             |
| `-force-d3d11-singlethreaded`             | Force DirectX 11.0 to be created with a `D3D11_CREATE_DEVICE_SINGLETHREADED` flag. |
| `-force-device-index`                     | Make the Standalone Player use a particular GPU device by passing it the index of that GPU (macOS only). |
| `-force-gfx-metal`                        | Make the Standalone Player use Metal as the default graphics API (macOS only). |
| `-force-glcore`                           | Force the Editor to use **OpenGL core**  profile for rendering. The Editor tries to use the best OpenGL version  available, and all OpenGL extensions exposed by the OpenGL drivers. If  the platform isn’t supported, Direct3D is used. |
| `-force-glcoreXY`                         | Similar to `-force-glcore`, but requests a specific OpenGL context version. Accepted values for XY: 32, 33, 40, 41, 42, 43, 44 or 45. |
| `-force-clamped`                          | Used together with `-force-glcoreXY`, this prevents checking for additional OpenGL extensions, allowing it to run between platforms with the same code paths. |
| `-force-low-power-device`                 | Make the Standalone Player use a low power device (macOS only). |
| `-force-wayland`                          | Activate experimental Wayland support when running a Linux player. |
| `-nographics`                             | When running in batch mode, do not  initialize graphics device at all. This makes it possible to run your  automated workflows on machines that don’t even have a GPU. |
| `-nolog` (Linux & Windows only)           | Do not produce an output log. Normally `output_log.txt` is written in the `*_Data` folder next to the game executable, where [Debug.Log](https://docs.unity3d.com/ScriptReference/Debug.Log.html) output is printed. |
| `-popupwindow`                            | Create the window as a a pop-up window, without a frame. This command is not supported on macOS. |
| `-screen-fullscreen`                      | Override the default full-screen state. This must be 0 or 1. |
| `-screen-height`                          | Override the default screen height. This must be an integer from a supported resolution. |
| `-screen-width`                           | Override the default screen width. This must be an integer from a supported resolution. |
| `-screen-quality`                         | Override the default screen quality. Example usage would be: `/path/to/myGame -screen-quality Beautiful` |
| `-show-screen-selector`                   | Forces the screen selector dialog to be shown.               |
| `-single-instance` (Linux & Windows only) | Allow only one instance of the game to run at the time. If another instance is already running then launching it again with `-single-instance` focuses the existing one. |
| `-parentHWND  delayed` (Windows only)     | Embed the Windows Standalone application  into another application. When using this, you need to pass the parent  application’s window handle (‘HWND’) to the Windows Standalone  application.  When passing `-parentHWND 'HWND' delayed`, the Unity application is hidden while it is running. You must also call [SetParent](https://msdn.microsoft.com/en-us/library/windows/desktop/ms633541(v=vs.85).aspx) from the [Microsoft Developer library](https://msdn.microsoft.com/en-us/library/windows/) for Unity in the application. Microsoft’s `SetParent` embeds the Unity window. When it creates Unity processes, the Unity  window respects the position and size provided as part of the  Microsoft’s [STARTUPINFO](https://msdn.microsoft.com/en-us/library/windows/desktop/ms686331(v=vs.85).aspx) structure.    To resize the Unity window, check its [GWLP_USERDATA](https://msdn.microsoft.com/en-us/library/windows/desktop/ms633585(v=vs.85).aspx) in Microsoft’s `GetWindowLongPtr` function. Its lowest bit is set to 1 when graphics have been  initialized and it’s safe to resize. Its second lowest bit is set to 1  after the Unity splash screen has finished displaying. For more information, see this example: [EmbeddedWindow.zip](https://docs.unity3d.com/uploads/Examples/EmbeddedWindow.zip) |

## Universal Windows Platform command line arguments

Universal Windows Apps don’t accept command line arguments by default, so to pass them you need to call a special function from **MainPage.xaml.cs/cpp** or **MainPage.cs/cpp**. For example:

```
appCallbacks.AddCommandLineArg("-nolog");
```

You should call this before the `appCallbacks.Initialize()` function.

| **Command**                   | **Details**                                                  |
| :---------------------------- | :----------------------------------------------------------- |
| `-nolog`                      | Don’t produce UnityPlayer.log.                               |
| `-force-driver-type-warp`     | Force the DirectX 11.0 driver type WARP device (see Microsoft’s documentation on [Windows Advanced Rasterization Platform](http://msdn.microsoft.com/en-us/library/gg615082.aspx) for more information). |
| `-force-d3d11-singlethreaded` | Force DirectX 11.0 to be created with a `D3D11_CREATE_DEVICE_SINGLETHREADED` flag. |
| `-force-gfx-direct`           | Force single threaded rendering.                             |
| `-force-feature-level-9-3`    | Force DirectX 11.0 feature level 9.3.                        |
| `-force-feature-level-10-0`   | Force DirectX 11.0 feature level 10.0.                       |
| `-force-feature-level-10-1`   | Force DirectX 11.0 feature level 10.1.                       |
| `-force-feature-level-11-0`   | Force DirectX 11.0 feature level 11.0.                       |

------

-  2018–09–07 Page amended 
   
- “accept-apiupdate” command line option added in Unity [2017.2](https://docs.unity3d.com/2017.2/Documentation/Manual/30_search.html?q=newin20172) 
- “-force-clamped” command line argument added in Unity [2017.3](https://docs.unity3d.com/2017.3/Documentation/Manual/30_search.html?q=newin20173) 
- Tizen support discontinued in [2017.3](https://docs.unity3d.com/2017.3/Documentation/Manual/30_search.html?q=newin20173) 
- “noUpm”, “setDefaultPlatformTextureFormat” and “CacheServerIPAddress” command line options added in Unity [2018.1](https://docs.unity3d.com/2018.1/Documentation/Manual/30_search.html?q=newin20181) 
- “Application.isBatchMode” operator added in [2018.2](https://docs.unity3d.com/2018.2/Documentation/Manual/30_search.html?q=newin20182)