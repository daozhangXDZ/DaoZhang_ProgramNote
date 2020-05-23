## 状态模式 State Pattern

允许对象在当内部状态改变时改变其行为，就好像此对象改变了自己的类一样。

### 

### 要点

- 状态模式用来解决当控制一个对象状态转换的条件表达式过于复杂的情况，它把状态的判断逻辑转移到表示不同的一系列类当中，可以把复杂的逻辑判断简单化。
- 状态模式的实现分为三个要点：
  - 为状态定义一个接口。
  - 为每个状态定义一个类。
  - 恰当地进行状态委托。
- 通常来说，状态模式中状态对象的存放有两种实现存放的思路：
  - 静态状态。初始化时把所有可能的状态都new好，状态切换时通过赋值改变当前的状态。
  - 实例化状态。每次切换状态时动态new出新的状态。

### 

### 使用场合

在游戏开发过程中，涉及到复杂的状态切换时，可以运用状态模式以及状态机来高效地完成任务。

有限状态机的实现方式，有两种可以选择：

- 用枚举配合switch case语句。
- 用多态与虚函数（即状态模式）。

有限状态机在以下情况成立时可以使用：

- 有一个行为基于一些内在状态的实体。
- 状态可以被严格的分割为相对较少的不相干项目。
- 实体可以响应一系列输入或事件。

### 

### 参考与引申

- Hierarchical State Machines分层状态机：<http://www.eventhelix.com/RealtimeMantra/HierarchicalStateMachine.htm#.WAHM3Y996Uk>
- Pushdown Automata下推自动机：<https://en.wikipedia.org/wiki/Pushdown_automaton>
- 状态模式的Unity版本实现：<https://github.com/QianMo/Unity-Design-Pattern/tree/master/Assets/Creational%20Patterns/Singleton%20Pattern>
- 本节内容相关的英文原文：<http://gameprogrammingpatterns.com/state.html>
- 本节内容相关的中文翻译：<http://gpp.tkchu.me/state.html>
