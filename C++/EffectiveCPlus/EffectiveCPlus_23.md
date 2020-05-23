# Effective C++读书笔记(23): 多用非成员非友元函数

**守则23: 多用非成员非友元函数代替成员函数**

> "Prefer non-member non-friend functions to member functions."

------

***本篇关键词: 封装，成员函数，友元函数，名空间***

------

假如今天你在给浏览器写代码，要用到三个函数，清除下载缓存，清除浏览记录，清除cookies:

```text
class WebBrowser{
  public:
    void clearCache();
    void clearHistory();
    void removeCookies();
  ...
};
```

许多时候为了方便起见我们可以用一键清除，一起执行这三个函数，我们可以再写一个成员函数cleanEverything():

```text
class WebBrowser{
  public:
    ...
    void cleanEverything(); //调用上面的三个函数
  ..
};
```

当然这个函数也可以被写成一个非成员函数:

```text
void cleanBrowser(WebBrowser& wb){
  wb.clearCache();
  wb.clearHistory();
  wb.removeCookies();
}
```

那么我们就有两种选择，那种更好呢?

面向对象的思路告诉我们，数据和操作它们函数需要绑在一起，也就是说写作成员函数更好。

FBI Warning! 这是对面向对象不全面的理解，面向对象要讲究的是数据要**尽可能地被封装起来**，而数据和操作它的函数被绑在一起只是一种结果。

反直觉答案:  其实非成员函数cleanBrowser()是更好的选择，因为它其实比成员函数cleanEverything()提供了更好的封装。此外，当相同的功能可以同时被成员函数和非成员函数实现时，选择非成员函数也能给WebBrowser类相关的功能提供更大的包装弹性，减少编译依赖，增加类的可扩展性。。。。????

迷的话我们一步一步来分析:

先从[上一章](https://zhuanlan.zhihu.com/p/80538530)讲到的**封装**(encapsulation)开始。如果某物是封装的，即对用户是不可见的，它的封装越好，就有越少的东西能直接接触它。有越少的东西能直接接触，我们就有更大的弹性对它做出改动，因为我们的改动直接影响到使用它的代码。因此，越好的封装就意味着越好的可维护性和可扩展性。

至于我们的WebBrowser类，有越少的代码使用它的成员数据，成员数据的封装就越好。我们根据能直接使用成员数据的函数数量作为封装标准，那么*有越多的函数能直接使用成员数据，成员数据的封装就越不好，编译依赖就越多，可扩展性就越差。*

[第22章](https://zhuanlan.zhihu.com/p/80538530)解释了类的数据成员都必须是私有(private)的，因为如果不是私有的话，就会有无限量的函数能直接使用它们，也就基本是零封装。对于私有数据成员，能直接接触它们的函数是:

> *成员函数+友元函数*

因此在能实现相同功能的情况下，在成员函数和非成员非友元函数中做出选择，后者当然能带来更好的封装，那么我们的非成员非友元函数cleanBrowser()会比成员函数cleanEverything()提供更好的封装，是更好的选择。

------

到现在要注意两点:

- 放在封装的大环境下，我们把*成员*函数与***非成员且非友元***函数拿来对比才有意义，而不仅仅是*成员*函数与*非成员*函数，因为友元函数与成员函数对私有成员拥有相同的访问权限，那么对封装的影响也是相同的。如果从别的角度出发，例如下一章说明的隐式转换，*成员*函数与*非成员*函数的对比则是有意义的。



- 以上并不是说这个函数就不能在别的类里。例如我们可以写一个实用类(utility class)，然后把cleanBrowser()作为它的一个静态成员函数，只要这个函数不在WebBrowser类里就不会影响WebBrowser类私有成员的封装。

------

cleanBrowser()是一个便捷函数(convenience  function)，而且既不是成员也不是友元函数，就没有对WebBrowser类成员的特殊访问权限，就不能提供额外的功能。比如即使这个函数不存在，用户也能自己调用它所包含的三个函数来实现一样的功能。

虽然不能作为成员函数，可是为了方便管理，我们还是希望它能与WebBrowser产生某种联系，这样就可以考虑把cleanBrowser()作为非成员非友元函数放在与WebBrowser类相同的一个名空间下，让结构显得自然:

```text
namespace WebBrowserStuff{
  class WebBrowser{...};
  void cleanBrowser(WebBrowser& wb){...}
}
```

其实这样做比仅仅为了自然更有意义。名空间不像类，必须被一次性完整定义，名空间则可以分布在不同的编译单元中，这样你就可以更逻辑地把不同的功能分布在不同的地方，使用类是做不到这一点的:

```text
//对于类，以下是非法操作，会报重定义错误
class SomeClass{
  void f1();
};

class SomeClass{
  void f2();
};

//对于名空间则是合法的，f1与f2属于同一名空间
namespace SomeSpace{
  void f1();
}

namespace SomeSpace{
  void f2();
}
```

像浏览器这样的类可能会有大量类似的便捷函数，比如关于收藏夹，打印，下载等等功能。既然它们都同属为浏览器服务，又想把它们按照功能放在不同的头文件里，最直接的组织方法就是在一个头文件中声明关于收藏夹的便捷函数，然后在另一个头文件中声明关于打印的便捷函数，并把它们纳入同一名空间中:

```text
//webbrowser.h 包含浏览器的核心功能
namespace WebBrowserStuff{
  class WebBrowser{...};
  ...
}

//webbrowserbookmarks.h 包含收藏夹相关功能
namespace WebBrowserStuff{
  ...
}

//webbrowsercookies.h 包含cookies相关功能
namespace WebBrowserStuff{
  ...
}
//以上头文件的代码全部纳入同一名空间
```

其实C++标准库就是这样组织的。C++标准库有各种各样的头文件<vector>,  <memory>等等，每个头文件都给std名空间声明它们自己的函数，而不是使用像<C++StandardLibrary>这样的头文件来包含std名空间所有的东西。如果只需要使用<vector>，我们不需要#include<list>，如果我们不使用<fstream>，就不需要#include<fstream>，这样我们只需要使用整个系统的一小部分，从而减少编译依赖。

使用这种方法还可以让用户轻松地对其进行扩展，例如要想增加保存图片的功能，直接开一个新的头文件，加一行namespace WebBrowserStuff{..}，把写好的功能放在里面就可以了，其它的头文件甚至动都不需要动，你自己的函数就成了那个名空间里的一员。

```text
//只需新增webbrowserimages.h
namespace WebBrowserStuff{
  ...
}
//以上的函数就纳入了我们的名空间
```

这是另一个用类做不到的功能，当然你可以说写一个子类继承父类也可以实现扩展，可是子类依然接触不到父类的私有成员，所以所做的扩展也是有限的，名空间则可以毫无保留地让你接触到所有东西，以及[第7章](https://zhuanlan.zhihu.com/p/65257902)讲到过并不是所有的类都可以拿来当爸爸的Θ◇Θ

**总结:**

- 多用非成员非友元函数替代成员函数，可以增加封装，包装弹性，功能可扩展性。
- 名空间可以分布在不同的编译单元中，实现更逻辑的函数分类和更方便的扩展。