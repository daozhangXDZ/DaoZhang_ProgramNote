# Thrift 双向通信实现（C#版）

主要参考了：Apache thrift RPC 双向通信，但是这篇是用Java写的，和C#会有一些不一样，所以写了一个C#版的。此博客使用Thrift 0.10.0版本，不同版本可能会有差异。
如何在C#中引用Thrift这些就不写了，可以翻我之前的博客，现在开始直接通过代码来说明：
编写Thrift IDL文件
编写一个非常简单的功能，输入一个字符串参数，返回值为空：



```c#
//HelloWorldBidirectionService.thrift
service HelloWorldBidirectionService{
    oneway void SayHello(1:string msg);
}
```

oneway不能少，具体oneway的含义可查看我之前的博客，这类似一个异步的实现。
编写服务端代码
HelloWorldBidirectionServer实现了Iface接口用于接收客户端消息，并有一个客户端传输层对象集合用于记录所有已连接的客户端。

```c#
//HelloWorldBidirectionServer.cpp

public class HelloWorldBidirectionServer : HelloWorldBidirectionService.Iface
{
    public void Run(int port)
    {
        try
        {
            TServerTransport transport = new TServerSocket(port);

            TTransportFactory transportFac = new TTransportFactory();

            TProtocolFactory inputProtocolFactory = new TBinaryProtocol.Factory();
            TThreadPoolServer server = new TThreadPoolServer(getProcessorFactory(), transport, transportFac, inputProtocolFactory);

            server.Serve();
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }
    }

    public static List<TTransport> TransportCollection = new List<TTransport>();

    public void SayHello(string msg)
    {
        Console.WriteLine(string.Format("{0:yyyy/MM/dd hh:mm:ss} 服务端接收到消息： {1}", DateTime.Now, msg));
    }

    public void SayToClient(string msg)
    {
        try
        {
            foreach (TTransport trans in TransportCollection)
            {
                TBinaryProtocol protocol = new TBinaryProtocol(trans);
                HelloWorldBidirectionService.Client client = new HelloWorldBidirectionService.Client(protocol);
                //Thread.Sleep(1000);
                client.SayHello(msg);
                Console.WriteLine("发给了客户端哟");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }
    }

    public TProcessorFactory getProcessorFactory()
    {
        return new HelloWorldBidirectionProcessor();
    }
}

```

自定义一个Processor，在每次客户端连接的时候就能监听到，并能获取到客户端的传输层对象TTransport。

```c#
public class HelloWorldBidirectionProcessor : TProcessorFactory
{
    public TProcessor GetProcessor(TTransport trans, TServer server = null)
    {
        if (trans.IsOpen)
        {
            HelloWorldBidirectionServer.TransportCollection.Add(trans);
            Console.WriteLine("有客户端上船啦");
        }

        HelloWorldBidirectionServer srv = new HelloWorldBidirectionServer();
        return new global::HelloWorldBidirectionService.Processor(srv);
    }
}

```

客户端代码
首先定义一个可以接收服务端消息的类，里面只有一个实现Iface接口的方法：

```c#
public class HelloWorldBidirectionFace : HelloWorldBidirectionService.Iface
{
    public void SayHello(string msg)
    {
        Console.WriteLine(string.Format("{0:yyyy/MM/dd hh:mm:ss} 收到服务端响应消息 {1}", DateTime.Now, msg));

    }
}

```

实现客户端，ConnectAndListern方法可以与服务端建立连接，并开启客户端端口监听来自服务端的信息。Say方法可将消息发送至服务端。

```c#
public class HelloWorldBidirectionClient
{
    static HelloWorldBidirectionService.Client client = null;
    public void ConnectAndListern(int port, string ip = "127.0.0.1")
    {
        //Tsocket: TCP/IP Socket接口
        TSocket tSocket = new TSocket(ip, port);
        //消息结构协议
        TProtocol protocol = new TBinaryProtocol(tSocket);
        try
        {
            if (client == null)
            {
                client = new global::HelloWorldBidirectionService.Client(protocol);
                tSocket.Open();//建立连接
                StartListern(tSocket);//启动监听线程
            }
            //cli.SayHello(msg);
            //tSocket.Close();
            //cli.Dispose();
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }
    }

    public void Say(string msg)
    {
        if (client != null)
            client.SayHello(msg);
    }

    void StartListern(TSocket tSocket)
    {
        Thread t = new Thread(new ParameterizedThreadStart(Run));
        t.Start(tSocket);
    }

    public void Run(object tSocket)
    {
        HelloWorldBidirectionService.Processor process = new HelloWorldBidirectionService.Processor(new HelloWorldBidirectionFace());

        try
        {
            while (process.Process(new TBinaryProtocol((TSocket)tSocket), new TBinaryProtocol((TSocket)tSocket)))
            {
                Console.WriteLine("消息接收完成，等下一波，阻塞中......");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("连接断开..." + ex.Message);
        }
    }
}

```

源码地址：
Thrift_HelloWorld_CSharp
--------------------- 
作者：david大伟哥 
来源：CSDN 
原文：https://blog.csdn.net/lwwl12/article/details/77330968 
版权声明：本文为博主原创文章，转载请附上博文链接！