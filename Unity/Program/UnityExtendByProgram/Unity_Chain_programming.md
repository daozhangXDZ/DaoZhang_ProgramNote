

# Unity 游戏框架搭建 (十八) 静态扩展 + 泛型实现transform的链式编程

本篇文章介绍如何实现如下代码的链式编程:

```c
            this.Position(Vector3.one)          
                .LocalScale(1.0f)               
                .Rotation(Quaternion.identity); 
```

以上代码中,this为MonoBehaviour类型的对象。

#### 如何实现?

通过上篇文章介绍的return this + 静态扩展很容易做到,实现代码如下所示:

```c
        public static MonoBehaviour Position(this MonoBehaviour selfBehaviour, Vector3 position) 
        {
            selfBehaviour.transform.position = position;
            return selfBehaviour;
        }
        
        public static MonoBehaviour LocalScale(this MonoBehaviour selfBehaviour, float xyz)
        {
            selfBehaviour.transform.localScale = Vector3.one * xyz;
            return selfBehaviour;
        }
        
        public static MonoBehaviour Rotation(this MonoBehaviour selfBehaviour, Quaternion rotation)
        {
            selfBehaviour.transform.rotation = rotation;
            return selfBehaviour;
        }
```

很容易实现对吧?但是这样有个问题，由于静态扩展方法返回的是MonoBehaviour类而不是this所属的类型，所以接下来链式方法中只能使用MonoBehaviour的方法。不能像如下方式使用。

```c
            this.Position(Vector3.one)          
                .LocalScale(1.0f)               
                .Rotation(Quaternion.identity)
                .DoSomething(); 
```

以上代码中,this为MonoBehaviour类型的对象。

如何解决这个问题呢?答案是引入泛型。

#### 引入泛型

实现代码如下所示:

```c
        public static T Position<T>(this T selfBehaviour, Vector3 position) where T : MonoBehaviour
        {
            selfBehaviour.transform.position = position;
            return selfBehaviour;
        }
        
        public static T LocalScale<T>(this T selfBehaviour, float xyz) where T : MonoBehaviour
        {
            selfBehaviour.transform.localScale = Vector3.one * xyz;
            return selfBehaviour;
        }
        
        public static T Rotation<T>(this T selfBehaviour, Quaternion rotation) where T : MonoBehaviour
        {
            selfBehaviour.transform.rotation = rotation;
            return selfBehaviour;
        }
```

实现很简单，只是把之前代码中的MonoBehaivour改成泛型T,然后增加一个约束: where T :  MonoBehaviour。表示这个泛型一定要继承自MonoBehaviour。这样之前例子中的this可以使用MonoBehaviour之外的方法实现链式编程了。

#### 进一步完善

不只是自己实现的MonoBehaviour脚本像UGUI的Image等都要支持transform的链式编程。那么就要找到transfom到底是哪个类？最后找到了如下代码。

```c
namespace UnityEngine
{
  /// <summary>
  ///   <para>Base class for everything attached to GameObjects.</para>
  /// </summary>
  [RequiredByNativeCode]
  public class Component : Object
  {
    /// <summary>
    ///   <para>The Transform attached to this GameObject.</para>
    /// </summary>
    public extern Transform transform { [MethodImpl(MethodImplOptions.InternalCall)] get; }
...
```

最终定位到,transform是Component的属性器。
 所以可以将之前的实现改为如下代码:

```c
        public static T Position<T>(this T selfComponent, Vector3 position) where T : Component
        {
            selfComponent.transform.position = position;
            return selfComponent;
        }
        
        public static T LocalScale<T>(this T selfComponent, float xyz) where T : Component
        {
            selfComponent.transform.localScale = Vector3.one * xyz;
            return selfComponent;
        }
        
        public static T Rotation<T>(this T selfComponent, Quaternion rotation) where T : Component
        {
            selfComponent.transform.rotation = rotation;
            return selfComponent;
        }
```

通过此种方式实现Graphfic,Component等类，最后可以实现如下方式的链式编程。

```c
            Image image = null;

            image.LocalPosition(Vector3.back)
                .ColorAlpha(0.0f)
                .Hide();
```

当然，去查看一个属性到底是哪个类实现的这个过程也是一个很好的学习方式 : ) ，有很多类都可以实现链式编程，不过剩下的要靠大家自己了，当然也可以参考QFramework里的实现方式，不过QFramework也只是对笔者常用的类进行了实现。

OK,本篇介绍到这里。