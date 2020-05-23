# Unity使用protobuf-net实现的网络框架

设计思想是把协议号和协议类型分别存储起来，当我们向服务端发送协议的时候，会自动根据协议类型加上协议号，并用protobuf序列化后发给服务端，客户端收到服务端发回来的协议后，会根据协议号，用protobuf根按协议类型自动反序列化成相应的对象，并调用相应的回调方法。

首先到https://github.com/mgravell/protobuf-net下载protobuf-net源码，把protobuf-net这个目录拷到Unity工程里，

我的工程目录如下


在Unity的Assest目录下新建一个smcs.rsp文件，里面填入-unsafe，重启Uniyt就可以了，如果使用VS的话，最好设置工程允许不安全代码，不然用VS调试的时候会报错


下面是主要的代码：

ProtoDic.cs 这个是存储协议号和协议类型的文件，这个主要是用代码自动生成，最好不要手动去更改

    using ServerMessage;
    using System;
    using System.Collections.Generic;
     
    namespace Proto
    {
        public class ProtoDic
        {
            private static List<int> _protoId = new List<int>
            {
                1001,
                1002,
                1003
            };
     
            private static List<Type>_protoType = new List<Type>
            {
                typeof(SignUpResponse),
                typeof(TocChat),
                typeof(TosChat),
            };
     
            public static Type GetProtoTypeByProtoId(int protoId)
            {
                int index = _protoId.IndexOf(protoId);
                return _protoType[index];
            }
     
            public static int GetProtoIdByProtoType(Type type)
            {
                int index = _protoType.IndexOf(type);
                return _protoId[index];
            }
     
            public static bool ContainProtoId(int protoId)
            {
                if(_protoId.Contains(protoId))
                {
                    return true;
                }
                return false;
            }
     
            public static bool ContainProtoType(Type type)
            {
                if(_protoType.Contains(type))
                {
                    return true;
                }
                return false;
            }
        }
    }


SocketClient.cs 这个是客户端的socket文件

    using UnityEngine;
    using System;
    using System.IO;
    using System.Net;
    using System.Net.Sockets;
    using System.Collections;
    using System.Collections.Generic;
    using Net;
     
    public enum DisType
    {
        Exception,
        Disconnect,
    }
     
    public class SocketClient
    {
        private TcpClient client = null;
        private NetworkStream outStream = null;
        private MemoryStream memStream;
        private BinaryReader reader;
     
        private const int MAX_READ = 8192;
        private byte[] byteBuffer = new byte[MAX_READ];
     
        // Use this for initialization
        public SocketClient()
        {
        }
     
        /// <summary>
        /// 注册代理
        /// </summary>
        public void OnRegister()
        {
            memStream = new MemoryStream();
            reader = new BinaryReader(memStream);
        }
     
        /// <summary>
        /// 移除代理
        /// </summary>
        public void OnRemove()
        {
            this.Close();
            reader.Close();
            memStream.Close();
        }
     
        /// <summary>
        /// 连接服务器
        /// </summary>
        void ConnectServer(string host, int port)
        {
            client = null;
            client = new TcpClient();
            client.SendTimeout = 1000;
            client.ReceiveTimeout = 1000;
            client.NoDelay = true;
            try
            {
                client.BeginConnect(host, port, new AsyncCallback(OnConnect), null);
            }
            catch (Exception e)
            {
                Close();
                Debug.LogError(e.Message);
            }
        }
     
        /// <summary>
        /// 连接上服务器
        /// </summary>
        void OnConnect(IAsyncResult asr)
        {
            outStream = client.GetStream();
            client.GetStream().BeginRead(byteBuffer, 0, MAX_READ, new AsyncCallback(OnRead), null);
            NetManager.Instance.OnConnect();
        }
     
        /// <summary>
        /// 写数据
        /// </summary>
        void WriteMessage(byte[] message)
        {
            MemoryStream ms = null;
            using (ms = new MemoryStream())
            {
                ms.Position = 0;
                BinaryWriter writer = new BinaryWriter(ms);
                ushort msglen = (ushort)message.Length;
                writer.Write(msglen);
                writer.Write(message);
                writer.Flush();
                if (client != null && client.Connected)
                {
                    byte[] payload = ms.ToArray();
                    outStream.BeginWrite(payload, 0, payload.Length, new AsyncCallback(OnWrite), null);
                }
                else
                {
                    Debug.LogError("client.connected----->>false");
                }
            }
        }
     
        /// <summary>
        /// 读取消息
        /// </summary>
        void OnRead(IAsyncResult asr)
        {
            int bytesRead = 0;
            try
            {
                lock (client.GetStream())
                {         //读取字节流到缓冲区
                    bytesRead = client.GetStream().EndRead(asr);
                }
                if (bytesRead < 1)
                {                //包尺寸有问题，断线处理
                    OnDisconnected(DisType.Disconnect, "bytesRead < 1");
                    return;
                }
                OnReceive(byteBuffer, bytesRead);   //分析数据包内容，抛给逻辑层
                lock (client.GetStream())
                {         //分析完，再次监听服务器发过来的新消息
                    Array.Clear(byteBuffer, 0, byteBuffer.Length);   //清空数组
                    client.GetStream().BeginRead(byteBuffer, 0, MAX_READ, new AsyncCallback(OnRead), null);
                }
            }
            catch (Exception ex)
            {
                //PrintBytes();
                OnDisconnected(DisType.Exception, ex.Message);
            }
        }
     
        /// <summary>
        /// 丢失链接
        /// </summary>
        void OnDisconnected(DisType dis, string msg)
        {
            Close();   //关掉客户端链接
            NetManager.Instance.OnDisConnect();
        }
     
        /// <summary>
        /// 打印字节
        /// </summary>
        /// <param name="bytes"></param>
        void PrintBytes()
        {
            string returnStr = string.Empty;
            for (int i = 0; i < byteBuffer.Length; i++)
            {
                returnStr += byteBuffer[i].ToString("X2");
            }
            Debug.LogError(returnStr);
        }
     
        /// <summary>
        /// 向链接写入数据流
        /// </summary>
        void OnWrite(IAsyncResult r)
        {
            try
            {
                outStream.EndWrite(r);
            }
            catch (Exception ex)
            {
                Debug.LogError("OnWrite--->>>" + ex.Message);
            }
        }
     
        /// <summary>
        /// 接收到消息
        /// </summary>
        void OnReceive(byte[] bytes, int length)
        {
            memStream.Seek(0, SeekOrigin.End);
            memStream.Write(bytes, 0, length);
            //Reset to beginning
            memStream.Seek(0, SeekOrigin.Begin);
            while (RemainingBytes() > 2)
            {
                ushort messageLen = reader.ReadUInt16();
                if (RemainingBytes() >= messageLen)
                {
                    MemoryStream ms = new MemoryStream();
                    BinaryWriter writer = new BinaryWriter(ms);
                    writer.Write(reader.ReadBytes(messageLen));
                    ms.Seek(0, SeekOrigin.Begin);
                    OnReceivedMessage(ms);
                }
                else
                {
                    memStream.Position = memStream.Position - 2;
                    break;
                }
            }
            byte[] leftover = reader.ReadBytes((int)RemainingBytes());
            memStream.SetLength(0);    
            memStream.Write(leftover, 0, leftover.Length);
        }
     
        /// <summary>
        /// 剩余的字节
        /// </summary>
        private long RemainingBytes()
        {
            return memStream.Length - memStream.Position;
        }
     
        /// <summary>
        /// 接收到消息
        /// </summary>
        /// <param name="ms"></param>
        void OnReceivedMessage(MemoryStream ms)
        {
            BinaryReader r = new BinaryReader(ms);
            byte[] message = r.ReadBytes((int)(ms.Length - ms.Position));        
            ByteBuffer buffer = new ByteBuffer(message);
            int mainId = buffer.ReadShort();
            NetManager.Instance.DispatchProto(mainId, buffer);
        }


​     
        /// <summary>
        /// 会话发送
        /// </summary>
        void SessionSend(byte[] bytes)
        {
            WriteMessage(bytes);
        }
     
        /// <summary>
        /// 关闭链接
        /// </summary>
        public void Close()
        {
            if (client != null)
            {
                if (client.Connected) client.Close();
                client = null;
            }
        }
     
        /// <summary>
        /// 发送连接请求
        /// </summary>
        public void SendConnect()
        {
            ConnectServer(AppConst.SocketAddress, AppConst.SocketPort);
        }
     
        /// <summary>
        /// 发送消息
        /// </summary>
        public void SendMessage(ByteBuffer buffer)
        {
            SessionSend(buffer.ToBytes());
            buffer.Close();
        }
    }


NetManager.cs 这个是网络功能的管理文件

    using UnityEngine;
    using System.Collections;
    using Util;
    using System.Collections.Generic;
    using System;
    using Proto;
    using System.IO;
     
    namespace Net
    {
        public class NetManager : SingletonMonoBehaviour<NetManager>
        {
            private Dictionary<Type, TocHandler> _handlerDic;
            private SocketClient _socketClient;
            SocketClient socketClient
            {
                get
                {
                    if (_socketClient == null)
                    {
                        _socketClient = new SocketClient();
                    }
                    return _socketClient;
                }
            }
     
            void Start()
            {
                Init();
            }
     
            public void Init()
            {
                _handlerDic = new Dictionary<Type, TocHandler>();
                socketClient.OnRegister();
            }
     
            /// <summary>
            /// 发送链接请求
            /// </summary>
            public void SendConnect()
            {
                socketClient.SendConnect();
            }
     
            /// <summary>
            /// 关闭网络
            /// </summary>
            public void OnRemove()
            {
                socketClient.OnRemove();
            }
     
            /// <summary>
            /// 发送SOCKET消息
            /// </summary>
            public void SendMessage(ByteBuffer buffer)
            {
                socketClient.SendMessage(buffer);
            }
     
            /// <summary>
            /// 发送SOCKET消息
            /// </summary>
            public void SendMessage(object obj)
            {
                if (!ProtoDic.ContainProtoType(obj.GetType()))
                {
                    Debug.LogError("不存协议类型");
                    return;
                }
                ByteBuffer buff = new ByteBuffer();
                int protoId = ProtoDic.GetProtoIdByProtoType(obj.GetType());
                buff.WriteShort((ushort)protoId);
                MemoryStream ms = new MemoryStream();
                ProtoBuf.Serializer.Serialize(ms, obj);
                byte[] result = ms.ToArray();
                buff.WriteBytes(result);
                SendMessage(buff);
            }
     
            /// <summary>
            /// 连接 
            /// </summary>
            public void OnConnect()
            {
                Debug.Log("======连接========");
            }
     
            /// <summary>
            /// 断开连接
            /// </summary>
            public void OnDisConnect()
            {
                Debug.Log("======断开连接========");
            }
     
            /// <summary>
            /// 派发协议
            /// </summary>
            /// <param name="protoId"></param>
            /// <param name="buff"></param>
            public void DispatchProto(int protoId, ByteBuffer buff)
            {
                if(!ProtoDic.ContainProtoId(protoId))
                {
                    Debug.LogError("未知协议号");
                    return;
                }
                Type protoType = ProtoDic.GetProtoTypeByProtoId(protoId);
                object toc = ProtoBuf.Serializer.Deserialize(protoType, new MemoryStream(buff.ReadBytes()));
                sEvents.Enqueue(new KeyValuePair<Type, object>(protoType, toc));
            }
     
            static Queue<KeyValuePair<Type, object>> sEvents = new Queue<KeyValuePair<Type, object>>();
            /// <summary>
            /// 交给Command，这里不想关心发给谁。
            /// </summary>
            void Update()
            {
                if (sEvents.Count > 0)
                {
                    while (sEvents.Count > 0)
                    {
                        KeyValuePair<Type, object> _event = sEvents.Dequeue();
                        if (_handlerDic.ContainsKey(_event.Key))
                        {
                            _handlerDic[_event.Key](_event.Value);
                        }
                    }
                }
            }
     
            public void AddHandler(Type type, TocHandler handler)
            {
                if (_handlerDic.ContainsKey(type))
                {
                    _handlerDic[type] += handler;
                }
                else
                {
                    _handlerDic.Add(type, handler);
                }
            }
        }
     
    }


最后附上一个简单的测试工程:https://github.com/caolaoyao/Chat

把工程下载下来，用Unity 5.x把开main入口就可以看到效果了
--------------------- 
作者：l_jinxiong 
来源：CSDN 
原文：https://blog.csdn.net/l_jinxiong/article/details/50709745 
版权声明：本文为博主原创文章，转载请附上博文链接！