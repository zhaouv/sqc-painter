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

如图所示提供了树根图块, 变量定义图块, 方向指定图块, 碰撞盒放置图块, 坐标导入图块, 以及各种基础图形的图块

### 变量定义图块

默认值可以直接使用其他变量来计算, 例如填`xx*2**0.5`  
在执行语句时如果该id的变量已经存在则不再计算.  
借此来实现传入的值覆盖默认值.  
使用其他变量来计算的场合, 该变量是传入的值时, 使用的是传入的值.  

### 方向指定图块

箭头对应取上一个碰撞盒的相应的角落

### 碰撞盒放置图块

箭头对应放在附着点的哪个方向  
内部放置一个基础图形图块

### 坐标导入图块

用从已存在的图形直接提取坐标  
使用绝对坐标时指定的是相对与附着点的偏移  
使用相对坐标时指定的是相对与上一个点的偏移  

### 基础图形图块

提供了
+ 笔刷
+ 半弧, 弧顶与长边相切, 圆心在箭头指向的方向
+ 四边形, 分别指定上右下左的点距离其逆时针方向的碰撞盒的顶点的距离
+ 四边形, 分别指定上右下左的点距离其顺时针方向的碰撞盒的顶点的距离
+ 直角三角形, 直角边在箭头指向的方向
+ 矩形

### 构图流程

![](img_md/attachmenttreeflow.png)

以一个比较复杂的结构来讲解流程,  
首先需要想清楚需要的结构的样子, 可以画在演草纸上  
分解成基础结构, 一般来说用减法的构造比每个局部一片片加简单  
把所有参数列出来  
把图形拼出来  
最后计算参数的依赖关系  

### 构造脚本

使用文件名或者python字典对象均可, 直接粘贴作为对象使用时, 要注意先定义`true=True`和`false=False`来兼容json的写法

`component=paintlib.AttachmentTree().load('AttachmentTreeDemo.json',{'yy':90000}).transform(pya.DCplxTrans(1,0,False,-904000,728000)).transform(pya.DCplxTrans(1,0,False,-904000,728000))`  

`component=paintlib.AttachmentTree().attachAtBrush('AttachmentTreeDemo.json',brush1,{'yy':90000})`  

绘制的部分在ComponentPainter

## Combiner



- - -

- [Start Page](README.md)  
- [脚本绘图基础](base.md)  
- **绘制库的建立和使用**  
- [demo](demo.md)  