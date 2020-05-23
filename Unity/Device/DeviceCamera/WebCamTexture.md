# WebCamTexture 调用外部摄像头

一:Unity 中使用WebCamTexture 调用摄像头实现拍照和摄像。



```csharp
using UnityEngine;
using System.Collections;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime .Serialization.Formatters.Binary;
using System.Threading;

public class takePhoto : MonoBehaviour 
{
	public string deviceName;
	//接收返回的图片数据
	WebCamTexture tex;
	public Texture2D _tex;
	void OnGUI()
	{
		if (GUI.Button(new Rect(10, 20, 100, 40), "开启摄像头"))
		{
			// 调用摄像头
			StartCoroutine(start());
		}

		if(GUI.Button(new Rect(10,70,100,40),"捕获照片"))
		{
			//捕获照片
			tex.Pause();
			StartCoroutine(getTexture());
		}

		if(GUI.Button(new Rect(10,120,100,40),"再次捕获"))
		{

			//重新开始
			tex.Play();



		}



		



		if(GUI.Button(new Rect(120,20,80,40),"录像"))



		{



			//录像



			StartCoroutine(SeriousPhotoes());



		}



		



		if(GUI.Button(new Rect(10,170,100,40),"停止"))



		{



			//停止捕获镜头



			tex.Stop ();



			StopAllCoroutines();



		}



		



		if(tex!=null)



		{



			// 捕获截图大小               —距X左屏距离   |   距Y上屏距离  



			GUI.DrawTexture(new Rect(Screen.width/2-150,Screen.height/2-190,280,200),tex); 



		}



		



	}



	



	/// <summary>



	/// 捕获窗口位置



	/// </summary>



	public IEnumerator start()



	{



		yield return Application.RequestUserAuthorization(UserAuthorization.WebCam);



		if (Application.HasUserAuthorization(UserAuthorization.WebCam))



		{



			WebCamDevice[] devices = WebCamTexture.devices;



			deviceName= devices[0].name;



			tex=new WebCamTexture(deviceName,300,300,12);



			tex.Play();



		}



	}



	



	/// <summary>



	/// 获取截图



	/// </summary>



	/// <returns>The texture.</returns>



	public IEnumerator getTexture()



	{



		yield return new WaitForEndOfFrame();



		Texture2D t=new Texture2D(400,300);



		t.ReadPixels( new Rect(Screen.width/2-200,Screen.height/2-50,360,300),0,0,false);



		//距X左的距离        距Y屏上的距离



		// t.ReadPixels(new Rect(220, 180, 200, 180), 0, 0, false);



		t.Apply();



		byte[] byt=t.EncodeToPNG();



//		File.WriteAllBytes(Application.dataPath+"/Photoes/"+Time.time+".jpg",byt);



		tex.Play();



	}



	



	/// <summary>



	/// 连续捕获照片



	/// </summary>



	/// <returns>The photoes.</returns>



	public IEnumerator SeriousPhotoes()



	{



		while (true)



		{



			yield return new WaitForEndOfFrame();



			Texture2D t = new Texture2D(400, 300, TextureFormat.RGB24, true);



			t.ReadPixels(new Rect(Screen.width/2-180,Screen.height/2-50,360,300), 0, 0, false);



			t.Apply();



			print(t);



			byte[] byt = t.EncodeToPNG();



//			File.WriteAllBytes(Application.dataPath + "/MulPhotoes/" + Time.time.ToString().Split('.')[0] + "_" + Time.time.ToString().Split('.')[1] + ".png", byt);



			Thread.Sleep(300);



		}



	}



}
```



二:Unity 中使用WebCamTexture 设置背景为摄像头画面

1在unity的场景中新建一个Quad作为背景，可以自行调节缩放和位置。

 2.新建一个Material文件夹用来存放Material，在Material里新建一个Material材质，并命名为CamTex。

 3.选中CamTex材质，在Inspector面板中选择shader的模式为Unlit/Texture。

4.WebCamQuad：Scale X 设置成负的。如下图

![img](https://blog.csdn.net/yupu56/article/details/45363671)

 5.将CamWeb脚本和CamTex材质拖到Quad上

 6.将Quad调至摄像机正对位置。

 7.新建C#脚本，并将其命名为WebCamera，双击脚本进行编辑，添加以下代码：

```csharp
using UnityEngine;



using System.Collections;



using UnityEngine.UI;



 



public class WebCamera : MonoBehaviour{



	



	private WebCamTexture _webcamTexFront;



	private WebCamTexture _webcamTexBack;



 



	//前后摄像头



	public int m_devID = 0;



	//宽高比



	public float aspect = 9f/16f;



	



	private string m_deviceName;



	public string m_photoName;



	public string m_photoPath;



	// Use this for initialization



 



	public delegate void onComplete(Sprite sprite);



 



	public WebCamTexture webCamera



	{



		get{



			m_deviceName=WebCamTexture.devices[m_devID].name;



 



			if(m_devID==0)



			{



				if (_webcamTexBack == null)



				{



					// Checks how many and which cameras are available on the device



					foreach(WebCamDevice device in WebCamTexture.devices){



						if (!device.isFrontFacing){



							m_deviceName = device.name;



							_webcamTexBack = new WebCamTexture (m_deviceName, Screen.width, (int)(Screen.width*aspect));



						}



					}



				}



				return _webcamTexBack;



			}



			else



			{



				if (_webcamTexFront == null)



				{



					// Checks how many and which cameras are available on the device



					foreach(WebCamDevice device in WebCamTexture.devices){



						if (device.isFrontFacing){



							m_deviceName = device.name;



							_webcamTexFront = new WebCamTexture (m_deviceName, Screen.width,(int)(Screen.width*aspect));



						}



					}



				}



				return _webcamTexFront;



			}



		}



	}



 



	public void cameraSwitch(){



		// Checks how many and which cameras are available on the device



		foreach(WebCamDevice device in WebCamTexture.devices){



			if (m_deviceName!=device.name) 



			{	



				webCamera.Stop();



				m_devID++;



				if(m_devID>=2) m_devID=0;



				m_deviceName=device.name;



 



				Debug.Log("m_devID"+m_devID);



				Debug.Log("m_deviceName"+m_deviceName);



 



				webCamera.Play();



				break;



			}



		}



	}



	



	public void takePicture(onComplete callback){



 



		StartCoroutine(GetTexture(callback));



	}



 



	//捕获照片



	//获取截图



	public IEnumerator GetTexture(onComplete callback)



	{



		webCamera.Pause();



		yield return new WaitForEndOfFrame();



		



		//save



		Texture2D t=new Texture2D(Screen.width,(int)(Screen.width*aspect));



		t.ReadPixels(new Rect(0,0,Screen.width,(int)(Screen.width*aspect)),0,0,false);



		t.Apply();



		byte[] byt = t.EncodeToPNG();



		m_photoName = Time.time+".png";



		m_photoPath = Application.persistentDataPath+"/"+m_photoName;



		System.IO.File.WriteAllBytes(m_photoPath,byt);



 



		//load image



		WWW www = new WWW("file://"+m_photoPath);



		yield return www;



		



		Sprite sprite = Sprite.Create(www.texture, new Rect(0, 0,Screen.width,(int)(Screen.width*aspect)),new Vector2(0.5f, 0.5f));



		//回调



		callback(sprite);



	}



 



	// 录像



	// 连续捕获照片



	public IEnumerator SeriousPhotoes()



	{



		while (true)



		{



			yield return new WaitForEndOfFrame();



			Texture2D t = new Texture2D(400, 300, TextureFormat.RGB24, true);



			t.ReadPixels(new Rect(0,0,Screen.width, (int)(Screen.width*aspect)), 0, 0, false);



			t.Apply();



			print(t);



			byte[] byt = t.EncodeToPNG();



			System.IO.File.WriteAllBytes(Application.dataPath + "/MulPhotoes/" + Time.time.ToString().Split('.')[0] + "_" + Time.time.ToString().Split('.')[1] + ".png", byt);



//			using System.Threading;



//			Thread.Sleep(300);



		}



	}



 



}
```

 8.再新建C#脚本，并将其命名为WebCameManager，双击脚本进行编辑，添加以下代码

```csharp
using UnityEngine;



using System.Collections;



using DG.Tweening;



using UnityEngine.UI;



 



public class WebCamManager : MonoBehaviour 



{	



	public WebCamera m_webCamera;



	public Transform m_webCamQuad;



 



	public Image photoPanel;



	public Image photoImg;



 



	private bool m_PhotoIng = false;



 



	private int rotateIndex=1;



 



	void Start () {



 



		//相机的初始化



		m_webCamera=new WebCamera();



		if(Globe.isPad)



			m_webCamera.aspect = 3f/4f;



	}



 



	// Update is called once per frame



	void Update () {



		



		 //设备的翻转，让Quard也翻转



		if(Globe.camering){



			if(m_webCamera.webCamera.videoRotationAngle==180 && rotateIndex==0){



				Debug.Log("videoRotationAngle"+m_webCamera.webCamera.videoRotationAngle);



				rotateIndex=1;



				m_webCamQuad.localScale=new Vector3(m_webCamQuad.localScale.x*(-1),m_webCamQuad.localScale.y*(-1),m_webCamQuad.localScale.z);



			}



			else if(m_webCamera.webCamera.videoRotationAngle==0 && rotateIndex==1){



				Debug.Log("videoRotationAngle"+m_webCamera.webCamera.videoRotationAngle);



				rotateIndex=0;



				m_webCamQuad.localScale=new Vector3(m_webCamQuad.localScale.x*(-1),m_webCamQuad.localScale.y*(-1),m_webCamQuad.localScale.z);



			}



		}



	}



 



	void CameraPlay()



	{



		if(m_webCamQuad.GetComponent<Renderer> ().material.mainTexture!=m_webCamera.webCamera)



		{



			m_webCamQuad.GetComponent<Renderer> ().material.mainTexture =m_webCamera.webCamera;



		}



 



		m_webCamera.webCamera.Play();



	}



 



	void CameraStop()



	{



		m_webCamera.webCamera.Stop();



	}



 



	//拍照按钮



	public void CameraCallBack(GameObject sender){



 



		CameraPlay();



 



		Globe.camering=true;



	}



 



	//返回按钮



	public void ReturnCallBack(GameObject sender){



 



		HidePhotoBackground();



		CameraStop();



 



		Globe.camering=false;



	}



 



	public void PhotoSwitchCallBack(GameObject sender){



 



		m_webCamera.cameraSwitch();



 



		m_webCamQuad.GetComponent<Renderer> ().material.mainTexture =m_webCamera.webCamera;



		m_webCamQuad.localScale=new Vector3(m_webCamQuad.localScale.x*(-1),m_webCamQuad.localScale.y,m_webCamQuad.localScale.z);



	}



	



	public void PhotoShutterCallBack(GameObject sender){



		AudioSource audio=m_webCamQuad.GetComponent<AudioSource>();



		audio.Play();



 



		m_shutterBtn.gameObject.SetActive(false);



		m_swithBtn.gameObject.SetActive(false);



		m_returnBtn.gameObject.SetActive(false);



		watermark.gameObject.SetActive(true);



 



		StartCoroutine(m_webCamera.GetTexture(delegate(Sprite sp){



			watermark.gameObject.SetActive(false);



 



			photoPanel.gameObject.SetActive(true);



			photoImg.sprite=sp;



		}));



	}



 



	public void PhotoCloseCallBack(GameObject sender){



		System.IO.File.Delete(m_webCamera.m_photoPath);



		Resources.UnloadUnusedAssets();



 



		CameraPlay();



		photoPanel.gameObject.SetActive(false);



 



		m_shutterBtn.gameObject.SetActive(true);



		m_swithBtn.gameObject.SetActive(true);



		m_returnBtn.gameObject.SetActive(true);



	}



 



	public void PhotoSaveCallBack(GameObject sender){



		photoPanel.gameObject.SetActive(false);



		Resources.UnloadUnusedAssets();



 



		CameraPlay();



		UnityIOSKit.SaveImageToPhotoAlbum(m_webCamera.m_photoName);



 



		m_shutterBtn.gameObject.SetActive(true);



		m_swithBtn.gameObject.SetActive(true);



		m_returnBtn.gameObject.SetActive(true);



 



	}



 



	void HidePhotoBackground(){



		m_webCamQuad.gameObject.SetActive (false);



		m_WareBeijing.gameObject.SetActive (true);



	}



 



	void ShowPhotoBackground(){



		m_webCamQuad.gameObject.SetActive (true);



		m_WareBeijing.gameObject.SetActive (false);



	}



}
```


 8.点击播放按钮即可调用摄像头，在quad的贴图会显示摄像头中的画面。