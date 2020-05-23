## C++中delete[]的实现

在C++中我们可以通过`new`和`new[]`在堆上分配内存，但是有没有考虑过下面这样的问题：

```cpp
class IntClass{
public:
	int v;
	~IntClass(){}
};

int main()
{
	IntClass *i = new IntClass[10];

	delete[] i;
}
```

因为`i`就只是一个普通的指针，所以它没有任何的类型信息，那么`delete[]`的时候怎么知道要回收多少内存呢？

所以肯定是哪里存储了`i`的长度信息！祭出我们的IR代码：

```cpp
; Function Attrs: noinline norecurse optnone uwtable
define dso_local i32 @main() #4 {
  %1 = alloca i32, align 4
  %2 = alloca %class.IntClass*, align 8
  store i32 0, i32* %1, align 4
  %3 = call i8* @_Znay(i64 48) #8
  %4 = bitcast i8* %3 to i64*
  store i64 10, i64* %4, align 8
  %5 = getelementptr inbounds i8, i8* %3, i64 8
  %6 = bitcast i8* %5 to %class.IntClass*
  store %class.IntClass* %6, %class.IntClass** %2, align 8
  %7 = load %class.IntClass*, %class.IntClass** %2, align 8
  %8 = icmp eq %class.IntClass* %7, null
  br i1 %8, label %21, label %9

; <label>:9:                                      ; preds = %0
  %10 = bitcast %class.IntClass* %7 to i8*
  %11 = getelementptr inbounds i8, i8* %10, i64 -8
  %12 = bitcast i8* %11 to i64*
  %13 = load i64, i64* %12, align 4
  %14 = getelementptr inbounds %class.IntClass, %class.IntClass* %7, i64 %13
  %15 = icmp eq %class.IntClass* %7, %14
  br i1 %15, label %20, label %16

; <label>:16:                                     ; preds = %16, %9
  %17 = phi %class.IntClass* [ %14, %9 ], [ %18, %16 ]
  %18 = getelementptr inbounds %class.IntClass, %class.IntClass* %17, i64 -1
  call void @_ZN8IntClassD2Ev(%class.IntClass* %18) #3
  %19 = icmp eq %class.IntClass* %18, %7
  br i1 %19, label %20, label %16

; <label>:20:                                     ; preds = %16, %9
  call void @_ZdaPv(i8* %11) #9
  br label %21

; <label>:21:                                     ; preds = %20, %0
  ret i32 0
}
```

可以看到编译器给我们的`new IntClass[10]`通过`@_Znay(i64 48)`来分配了48个字节的内存！

但是按照`sizeof(IntClass)*10`来算其实之应该有40个字节的内存，多余的8个字节用来存储了数组的长度信息。

```cpp
  %3 = call i8* @_Znay(i64 48) #8
  %4 = bitcast i8* %3 to i64*
  store i64 10, i64* %4, align 8
  %5 = getelementptr inbounds i8, i8* %3, i64 8
  %6 = bitcast i8* %5 to %class.IntClass*
```

可以看到，它把数组的长度写入到了分配内存的前8个字节，在八个字节之后才可以分配真正的对象。

我们真正得到的`i`的地址就是偏移之后的，数组的长度写在第一个元素之前的64位内存中。

```cpp
// 每个x代表一个byte，new IntClass[10]产生的内存布局
|xxxxxxxx|xxxx|xxxx|xxxx|xxxx|xxxx|xxxx|xxxx|xxxx|xxxx|xxxx|
```

既然知道了它存在哪里，所以我们可以修改它（在修改之前我们`delete[] i;`会调用10次析构函数）：

```cpp
IntClass *i = new IntClass[10];
int64_t *ArrayLength = (int64_t*)((char*)(i)-8);
*ArrayLength = 1;
delete[] i;
```

这样修改之后`delete[] i;`只会调用1次析构函数，也印证了我们猜想。