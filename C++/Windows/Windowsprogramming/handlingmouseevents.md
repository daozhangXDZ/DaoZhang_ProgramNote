# [Windows编程-处理鼠标事件](https://www.cnblogs.com/bruce81/archive/2013/02/12/2910394.html)

我们这里仅讨论两个简单的消息: WM_MOUSEMOVE和WM_*BUTTON*。

**Parameters:**

***wParam*** 
Indicates whether various virtual keys are down. This parameter can be one or more of the following values. 

| Value       |        | Meaning                          |
| ----------- | ------ | -------------------------------- |
| MK_CONTROL  | 0x0008 | The CTRL key is down.            |
| MK_LBUTTON  | 0x0001 | The left mouse button is down.   |
| MK_MBUTTON  | 0x0010 | The middle mouse button is down. |
| MK_RBUTTON  | 0x0002 | The right mouse button is down.  |
| MK_SHIFT    | 0x0004 | The SHIFT key is down.           |
| MK_XBUTTON1 | 0x0020 | The first X button is down.      |
| MK_XBUTTON2 | 0x0040 | The second X button is down.     |

***lParam***

The low-order word specifies the x-coordinate of the cursor. The  coordinate is relative to the upper-left corner of the client area. The  high-order word specifies the y-coordinate of the cursor. The coordinate is relative to the upper-left corner of the client area.

##### *Return value*

If an application processes this message, it should return zero.

下面的代码给出的是鼠标的x,y位置和左右键状态的例子。

![img](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
// INCLUDES ///////////////////////////////////////////////
#define WIN32_LEAN_AND_MEAN  // just say no to MFC

#include <windows.h>   // include all the windows headers
#include <windowsx.h>  // include useful macros
#include <mmsystem.h>  // very important and include WINMM.LIB too!
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// DEFINES ////////////////////////////////////////////////

// defines for windows 
#define WINDOW_CLASS_NAME "WINCLASS1"

// GLOBALS ////////////////////////////////////////////////
HWND      main_window_handle = NULL; // globally track main window
HINSTANCE hinstance_app      = NULL; // globally track hinstance

// FUNCTIONS //////////////////////////////////////////////
LRESULT CALLBACK WindowProc(HWND hwnd, 
                            UINT msg, 
                            WPARAM wparam, 
                            LPARAM lparam)
{
// this is the main message handler of the system
PAINTSTRUCT        ps;        // used in WM_PAINT
HDC                hdc;    // handle to a device context
char buffer[80];        // used to print strings

// what is the message 
switch(msg)
    {    
    case WM_CREATE: 
        {
        // do initialization stuff here
        // return success
        return(0);
        } break;

    case WM_MOUSEMOVE:
         {
         // get the position of the mouse
         int mouse_x = (int)LOWORD(lparam);
         int mouse_y = (int)HIWORD(lparam);

         // get the button state
         int buttons = (int)wparam;

         // get a graphics context
         hdc = GetDC(hwnd);

         // set the foreground color to green
         SetTextColor(hdc, RGB(0,255,0));
         
         // set the background color to black
         SetBkColor(hdc, RGB(0,0,0));
         
         // set the transparency mode to OPAQUE
         SetBkMode(hdc, OPAQUE);

         // print the ascii code and key state
         sprintf(buffer,"Mouse (X,Y) = (%d,%d)      ",mouse_x,mouse_y);
         TextOut(hdc, 0,0, buffer, strlen(buffer));

         sprintf(buffer,"Right Button = %d  ",((buttons & MK_RBUTTON) ? 1 : 0));
         TextOut(hdc, 0,16, buffer, strlen(buffer));

         sprintf(buffer,"Left Button = %d  ",((buttons & MK_LBUTTON) ? 1 : 0));
         TextOut(hdc, 0,32, buffer, strlen(buffer));

         // release the dc back
         ReleaseDC(hwnd, hdc);

         } break;


    case WM_PAINT: 
        {
        // simply validate the window 
           hdc = BeginPaint(hwnd,&ps);     
        
        // end painting
        EndPaint(hwnd,&ps);

        // return success
        return(0);
           } break;

    case WM_DESTROY: 
        {

        // kill the application, this sends a WM_QUIT message 
        PostQuitMessage(0);

        // return success
        return(0);
        } break;

    default:break;

    } // end switch

// process any messages that we didn't take care of 
return (DefWindowProc(hwnd, msg, wparam, lparam));

} // end WinProc

// WINMAIN ////////////////////////////////////////////////
int WINAPI WinMain(    HINSTANCE hinstance,
                    HINSTANCE hprevinstance,
                    LPSTR lpcmdline,
                    int ncmdshow)
{

WNDCLASSEX winclass; // this will hold the class we create
HWND       hwnd;     // generic window handle
MSG           msg;         // generic message

// first fill in the window class stucture
winclass.cbSize         = sizeof(WNDCLASSEX);
winclass.style            = CS_DBLCLKS | CS_OWNDC | 
                          CS_HREDRAW | CS_VREDRAW;
winclass.lpfnWndProc    = WindowProc;
winclass.cbClsExtra        = 0;
winclass.cbWndExtra        = 0;
winclass.hInstance        = hinstance;
winclass.hIcon            = LoadIcon(NULL, IDI_APPLICATION);
winclass.hCursor        = LoadCursor(NULL, IDC_ARROW); 
winclass.hbrBackground    = (HBRUSH)GetStockObject(BLACK_BRUSH);
winclass.lpszMenuName    = NULL;
winclass.lpszClassName    = WINDOW_CLASS_NAME;
winclass.hIconSm        = LoadIcon(NULL, IDI_APPLICATION);

// save hinstance in global
hinstance_app = hinstance;

// register the window class
if (!RegisterClassEx(&winclass))
    return(0);

// create the window
if (!(hwnd = CreateWindowEx(NULL,                  // extended style
                            WINDOW_CLASS_NAME,     // class
                            "Mouse Tracking Demo", // title
                            WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                             0,0,      // initial x,y
                            400,300,  // initial width, height
                            NULL,      // handle to parent 
                            NULL,      // handle to menu
                            hinstance,// instance of this application
                            NULL)))    // extra creation parms
return(0);

// save main window handle
main_window_handle = hwnd;

// enter main event loop, but this time we use PeekMessage()
// instead of GetMessage() to retrieve messages
while(TRUE)
    {
    // test if there is a message in queue, if so get it
    if (PeekMessage(&msg,NULL,0,0,PM_REMOVE))
       { 
       // test if this is a quit
       if (msg.message == WM_QUIT)
           break;
    
       // translate any accelerator keys
       TranslateMessage(&msg);

       // send the message to the window proc
       DispatchMessage(&msg);
       } // end if
    
    // main game processing goes here
    // Game_Main(); // or whatever your loop is called
    } // end while

// return to Windows like this
return(msg.wParam);

} // end WinMain

///////////////////////////////////////////////////////////
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

如果我们想测试left button的双击事件，可以加入下面的代码：

```
case WM_LBUTTONDBLCLK:
{
    // do something for you

return(0);
}break;
```