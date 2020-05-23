# 【C++】STL常用容器总结之八：映射map



映射map

Map是键-值对的集合，map中的所有元素都是pair，可以使用键作为下标来获取一个值。Map中所有元素都会根据元素的值自动被排序，同时拥有实值value和键值key，pair的第一元素被视为键值，第二元素被视为实值，同时map不允许两个元素有相同的键值。要使用map对象，必须包含map的头文件#include<map>。
1、map的构造函数

在定义map对象时，必须分别指明键和值的类型。Map建立key-value的一种映射。

1.map<key, value> m;

    1

创建一个名为m的空map对象，其键和值的类型分别为key和value。

2.map<key, value> m(m2);

    1

创建m2的副本m，m与m2必须有相同的键类型和值类型。

3.map<key, value> m(b,e);

    1

创建map类型的对象m，存储迭代器b和e标记的范围内所有元素的副本，元素的类型必须能转换为pair

4.map<key, value, comp> mp;

    1

comp可选，为键值对存放策略，即键的比较函数，默认标准库使用键类型定义的 < 操作符来实现键的比较。所用的比较函数必须在键类型上定义严格的弱排序，可将其理解为键类型数据上的“小于”关系。在实际应用中，键类型必须能定义 < 操作符。对于键类型，其唯一的约束就是必须支持 < 操作符。
2、map定义的类型

map<key, value> ::key_type;  // 在map容器中，用作索引的键的类型
map<key, value> ::mapped_type;  // 在map容器中，键所关联的值的类型
map<key, value> ::value_type;  // 一个pair类型，它的first元素具有const map<key, value> ::key_type类型，而second元素则为map<key, value> :: mapped_type类型。

    1
    2
    3

在学习map接口时，谨记其value_type是pair类型，它的值成员可以修改（second成员），但键成员不能修改。这个value_type相当于map的元素类型，而不是键所对应的值的类型。
对map迭代器进行解引用将产生pair类型的对象，它的first成员存放键，为const，而second成员存放值。
3、map容器的一些操作

给map容器添加元素可通过两种方式实现：
1. 通过insert成员函数实现。
2. 通过下标操作符获取元素，然后给获取的元素赋值。
  map对象的访问可通过下标和迭代器两种方式实现：
3. map的下标是键，返回的是特定键所关联的值。
4. 使用迭代器访问，iter->first指向元素的键，iter->second指向键对应的值。
  使用下标访问map容器与使用下标访问vector的行为截然不同：用下标访问map中不存在的元素将导致在map容器中添加一个新的元素，这个元素的键即为该下标值，键所对应的值为空。
  4、map容器与哈希表

对于map容器，使用其下标行为一次访问一系列的相同类型的元素，则可以将这个过程理解为构造了这些元素的一个哈希表，以统计输入单词的出现次数为例：



    map<string, int> word_count;
    string word;
    while(cin>>word)
    ++word_count[word];  // 相当于生成了一个哈希表word_count

在单词的第一次出现时，会在word_count中创建并插入一个以该单词为索引的新元素，同时将它的值初始化为0。然后其值立即加1，所以每次在map中添加新元素时，所统计的次数正好从1开始。需要注意的是，使用map创建的哈希表已经按键值进行了排序，所以序列的顺序已经不再是原始的输入顺序了。
5、map的成员函数
1、不修改map对象的查询操作：

    m.count(k);  // 返回m中键值等于k的元素的个数。
    m.find(k);  // 如果m中存在按k索引的元素，则返回指向该元素的迭代器。如果不存在，则返回结束游标end()。

对于map对象，由于map中不存在相同的两个或者多个键，所以count成员的返回值只能是0或者1，用于检查map对象中某键是否存在。find成员返回的是指向元素的迭代器，如果元素不存在，则返回end迭代器，用于读取元素而又不插入元素。
2、从map对象中删除元素

    m.erase(k);  // 删除m中键为k的元素，返回size_type类型的值，表示删除元素的个数。
    m.erase(p);  // 从m中删除迭代器p所指向的元素，p必须指向m中确实存在的元素，而且不能等于m.end()，返回void类型。
    m.erase(iterator first, iterator last);  // 删除一个范围，返回void类型。

3、map容器提供的insert操作：

m.insert(e) ;
e是一个用在m上的value_type类型的值。如果键e.first不在m中，则插入一个值为e.second的新元素；如果该键在m中已存在，那么不进行任何操作。该函数返回一个pair类型对象，包含指向键为e.first的元素的map迭代器，以及一个bool类型的对象，表示是否插入了该元素。
m.insert(beg, end);
beg和end是标记元素范围的迭代器，对于该范围内的所有元素，如果它的键在m中不存在，则将该键及其关联的值插入到m。 返回void类型。
m.insert(iter, e);
e是value_type类型的值，如果e.first不在m中，则创建新元素，并以迭代器iter为起点搜索新元素存储的位置，返回一个迭代器，指向m中具有给定键的元素。
在添加新的map元素时，使用insert成员可避免使用下标操作符带来的副作用：不必要的初始化。
--------------------- 
作者：长相忆兮长相忆 
来源：CSDN 
原文：https://blog.csdn.net/hero_myself/article/details/52313451 
版权声明：本文为博主原创文章，转载请附上博文链接！
