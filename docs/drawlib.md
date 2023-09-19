# 绘制库的建立和使用

## 绘制库

用标准的形式来绘制具有特定功能的图形模组

**paintlib** 中提供了如下的类, 通过json描述绘制过程:
+ Component : 绘图库的基类
+ GDSLoader : 通过gds文件来导入元件
+ AttachmentTree : 通过描述一些基础图形的碰撞盒的粘附关系, 以附着树的形式来描述元件
+ Combiner : 放置元件并通过轨迹来连接笔刷
+ GridLayout : 以网格的形式放置组合器
+ ComponentPainter : 组合绘制region和空桥等

## 图形界面

仓库 [AttachmentTree](https://github.com/SQCEDA/AttachmentTree) 中提供了图形化的json编辑器

[AttachmentTree](https://sqceda.github.io/AttachmentTree/AttachmentTree/demo.html)

[Combiner](https://sqceda.github.io/AttachmentTree/Combiner/demo.html)

[ComponentPainter](https://sqceda.github.io/AttachmentTree/ComponentPainter/demo.html)

## Component

数据部分包含7个dict来分别储存相应数据
+ collection : region
+ brush : 笔刷
+ vars : 数值
+ trace : 轨迹(字符串)
+ structure : 子结构(Component类以及子类)
+ centerlines : 轨迹的中心线
+ marks : 轨迹的标记

+ 方法`update(vars={"a":1}, trace={"t1":"s 50000"})` 更新数据, 可以同时使用多个数据
+ 方法`update(anotherComponent)` 从另一个Component更新其所有数据
+ 方法`transform(tr)` 执行转换

## GDSLoader

对于部分固定的且已存在的图形, 可以把gds文件直接作为元件库使用. 可以在其中通过gds标准中的Text来指定笔刷

![](img_md/gdsloaderdemo.png)

如图所示的gds加载后会得到一个collection在`0_3` `2_0` `3_0` `17_0`下有region, brush在`couper1`下有个-45度笔刷的对象

`paintlib.GDSLoader().load(filename)`

`paintlib.GDSLoader().attachAtBrush(filename,brush)` 等效于先`load`再执行转换`tr=brush.DCplxTrans`

## AttachmentTree

![](img_md/attachmenttreeview.png)

为了改进通过参数直接计算坐标的效率, 以及实现标准化, 提供一种设计组件的机制

把基础图形放置在一个紧贴着的矩形中, 称为碰撞盒.  
每个碰撞盒再提供四个角作为附着点, 每个附着点的四个方向可以继续放置碰撞盒, 内部嵌入基础图形.  
用这样的树结构来描述图形间的位置关系.

如图所示提供了树根图块, 变量定义图块, 


一个目前比较复杂的结构来讲解流程,
首先需要想清楚需要的结构的样子, 可以画在演草纸上
分解成基础结构, 一般来说用减法的构造比每个局部一片片加简单
把所有参数列出来(最后再计算依赖关系)
把图形拼出来

放置以及参数填入


- - -

- [Start Page](README.md)  
- [脚本绘图基础](base.md)  
- **绘制库的建立和使用**  
- [demo](demo.md)  