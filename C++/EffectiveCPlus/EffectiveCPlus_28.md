# Effective C++读书笔记(28): 避免返回指向对象内部的handle

**守则28: 避免返回指向对象内部成员的"句柄"**

> "Avoid returning 'handles' to object internals"

------

***本篇关键词: handle，封装，野指针***

------

假如你在给一个应用写一个表示矩形的类，这个矩形由左上角和右下角的顶点坐标表示。为了表示这两个点，我们写一个表示点的类:

```text
class Point{   
  public:
     Point(int x, int y);
     void setX(int newVal);
     void setY(int newVal);
   ... 
};
```

为了让我们的矩形对象的体积小一点，我们把这两个顶点装在另一个结构体中，并用指针指向它:

```text
struct RectData{
  Point ulhc; //左上角upper left-hand corner   
  Point lrhc; //右下角lower right-hand corner 
};  

class Rectangle{
  ...   
  private:     
    std::shared_ptr<RectData> pData; //智能指针见第13章 
};
```

因为用户想要得到点的坐标，所以让我们的矩形类要提供返回这两个点的函数。因为是自定义的类，[第20章](https://zhuanlan.zhihu.com/p/77753938)讲过对于自定义的类，引用传递比值传递更高效，所以我们让这两个函数返回引用:

```text
class Rectangle{
   public:
     ...
     Point& upperLeft(){return pData->ulhc;}
     Point& lowerRight(){return pData->lrhc;}
   ... 
};
```

以上的设计虽然可以编译，但其实是有矛盾的！首先我们的upperLeft和lowerRight函数被声明为了const，因为我们希望它只返回一个对象而别的什么都不做。可是两个函数都返回了指向私有成员的引用，调用的人就能通过这个引用来改变对象！

```text
Point coord1(0,0);
Point coord2(100,100); 
const Rectangle rec(coord1,coord2); //我们希望它是一个const对象 
rec.upperLeft().setX(50);  //现在通过引用能改变const对象的状态！
```

我们从以上能得到两点教训:

- 数据成员的最好封装性取决于最能破坏封装的函数。虽然我们的ulhc和lrhc两个点都声明为了私有，但因为这两个返回引用的函数的存在，它们其实相当于是公有的
- 如果一个函数返回了指向**储存在对象外部**的数据成员的引用，即使这个函数声明为了const，调用这个函数的人也能修改这个成员(见[第3章](https://zhuanlan.zhihu.com/p/63609476)bitwise constness的局限性)

除了引用，返回指针和迭代器也是相同的结果，相同的原因。引用，指针，迭代器都是我们这里所讲的"句柄"(handle)，即接触对象的某种方式。直接返回句柄总会带来破坏封装的风险，这也导致声明为const的函数并不是真正的const。

------

还要注意的是，"内部成员"除了内部数据还包括内部函数，即声明为私有(private)或保护(protected)的函数，因此对于内部函数也是一样，也不要返回它们的句柄，否则用户也可以通过返回的函数指针来调用它们，这样私有的成员函数也相当于变成了公有。


现在回到我们的例子，如果要解决返回引用会导致数据成员被改变的问题，只需要给函数的返回类型加上一个const:

```text
class Rectangle{
  public:     
    //现在返回的是const Point&     
    const Point& upperLeft() const{return pData->ulhc;}
    const Point& lowerRight() const{return pData->lrhc;}
  ... 
};
```

这样用户就只能对其进行读操作而不能进行写操作了，给函数声明的const也就不会骗人了。至于封装问题，让用户知道这个矩形的位置是完全合情合理的，所以我们给封装提供了有限的放宽，让用户可以读到私有数据，但坚决不能让用户执行写操作。

------

可是即使这样，返回句柄依然会导致一个问题，就是**"野句柄"**(dangling handle)，即这个句柄指向的对象不存在了。最常见的场景是函数返回值。假如我们在给某个GUI对象写一个返回它边界框的函数，返回类型是我们的Rectangle:

```text
class GUIObject{...}; //某个GUI对象 
const Rectangle boundingBox(const GUIObject& obj)); //见第3章为什么返回const
```

用户可能会这样使用代码:

```text
GUIObject* pgo; 
... 
const Point* pUpperLeft = &(boundingBox(*pgo).upperLeft());
```

现在有意思的事发生了，取址运算符括号里面的boundingBox函数会返回一个新的，**临时**的Rectangle对象，我们叫它temp。有了这个临时对象之后，我们会取得指向它左上角Point对象，然后pUpperLeft自然就获得了这个Point对象的地址。可是temp毕竟是临时对象！在这行代码执行完后，temp会被销毁，它所包含的Point对象也就会被销毁，最后pUpperLeft存了指向一个不存在的对象的指针。


所以这就是为什么返回指向内部成员"句柄"的函数是危险的，不管你的"句柄"是指针，引用还是迭代器，不管你的返回值是不是const，不管你的函数是不是const。但这不代表要杜绝这种做法，有时候不得不这样做，例如索引[]操作符，用来拿出容器(比如std::vector)里的某个对象，它返回的是指向容器里的数据的引用，来让你完成写操作，见[第3章](https://zhuanlan.zhihu.com/p/63609476)，但在我们自己的程序里，还是能避免就不要这么做。


**总结:**

- 避免返回指向内部成员的"句柄"，包括指针，引用，迭代器。不返回"句柄"能增强封装性，让const函数真正const，也能减少"野句柄"。