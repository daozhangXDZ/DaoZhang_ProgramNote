## 原型模式 Prototype Pattern

用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。

### 

### 要点

- 原型模式：用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。
- 原型模式是一种比较简单的模式，也非常容易理解，实现一个接口，重写一个方法即完成了原型模式。在实际应用中，原型模式很少单独出现。经常与其他模式混用，他的原型类Prototype也常用抽象类来替代。
- 使用原型模式拷贝对象时，需注意浅拷贝与深拷贝的区别。
- 原型模式可以结合JSON等数据交换格式，为数据模型构建原型。

### 

### 使用场合

- 产生对象过程比较复杂，初始化需要许多资源时。
- 希望框架原型和产生对象分开时。
- 同一个对象可能会供其他调用者同时调用访问时。

### 

### 参考与引申

- 原型模式的Unity版本实现：<https://github.com/QianMo/Unity-Design-Pattern/tree/master/Assets/Creational%20Patterns/Prototype%20Pattern>
- 本节内容相关的英文原文：<http://gameprogrammingpatterns.com/prototype.html>
- 本节内容相关的中文翻译： <http://gpp.tkchu.me/prototype.html>
