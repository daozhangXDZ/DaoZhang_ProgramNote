# FTickableGameObject

2019年2月28日

11:22

 

*继承自**UObject**的类，在实例后不会加入引擎中的**Tick**，**AActor**和**UActorComponent**都会加入**Tick**，如果你的对象也需要每帧去**Tick**（一般来说是什么**Mgr**管理器之类的全局单例对象），也非常简单*

再继承多一个抽象类FTickableGameObject

重写实现几个纯虚函数即可

UCLASS()
 class UCoolDownMgr : public UObject, public FTickableGameObject
 {
         GENERATED_BODY()
 public:
         *// Sets default values for this character's properties*
         UCoolDownMgr();
         virtual ~UCoolDownMgr();
  
         *// Begin FTickableGameObject Interface.*
         virtual void Tick(float DeltaTime) override;
         virtual bool IsTickable() const override;
         virtual TStatId GetStatId() const override;
         *// End FTickableGameObject Interface.*
 };

 

来自 <[*http://www.voidcn.com/article/p-fmjruagh-vc.html*](http://www.voidcn.com/article/p-fmjruagh-vc.html)> 

#  
