# tool

## 交互式的路径生成

1. 在绘图过程中, 使用`paintlib.Interactive.show(brush)`标记需要连接的笔刷, 此时笔刷会以电极的形式画在auxiliary中.

2. 选中(0,0)层, 用工具栏中的path点出一条路径并选中.

3. 在命令行中输入`paintlib.Interactive.link()`, 会自动搜索最近的笔刷拟合出路径, 生成路径函数打印在命令行中, 并在auxiliary中画出.

<p>
<img src="./img_md/linkbeforepic.png" width="350" style="float:left">
<span style="float:left">&nbsp;&nbsp;&nbsp;&nbsp;</span>
<img src="./img_md/linkafterpic.png" width="370" style="float:left">
</p><br style="clear:both">

```python
def path(painter):
    length=0
    length+=painter.Straight(493628.3218813461)
    length+=painter.Turning(-50000,45.0)
    length+=painter.Straight(390557.7026663276)
    length+=painter.Turning(-50000,90)
    length+=painter.Straight(630063.254735586)
    length+=painter.Turning(-50000,45)
    length+=painter.Straight(330724.32188134524)
    length+=painter.Turning(50000,90)
    length+=painter.Straight(587893.3218813452)
    length+=painter.Turning(50000,45)
    length+=painter.Straight(545793.0969808981)
    length+=painter.Turning(50000,90)
    length+=painter.Straight(517921.7760936491)
    length+=painter.Turning(-50000,45.0)
    length+=painter.Straight(683581.3218813452)
    return length
```

## 图块化的路径函数生成器

<a href="./tool/pathGenerator.html" style="color:navy;" target="_blank_">点此进入</a>

如下图所示, 拖拽图块, 便可生成路径函数, 画出对应的腔

![](img_md/blocklypic.png)

![](img_md/blocklygenercavity.png)

可以点击`Show XML`, 把生成如下的内容的保存下来. 需要编辑时再在粘贴到输入框中点`Load XML`, 即可恢复图块.

```xml
<xml xmlns="http://www.w3.org/1999/xhtml">
  <variables></variables>
  <block type="pathgenerator" id="PY8{DktMB_WpN|,[8R/F" x="269" y="145">
    <statement name="pathstat_0">
      <shadow type="void" id="Dug+93UZdM];]LS1+?wR"></shadow>
      <block type="leftright" id="9CmP#M$d+WRz4}{xy;v!">
        <field name="LeftRight_List_0">right</field>
        <field name="Number_0">40000</field>
        <field name="Number_1">90</field>
        <next>
          <block type="go" id="ZieE*aY1*=XwS*8N8G)U">
            <field name="Number_0">50000</field>
            <next>
              <block type="leftright" id="yoSi3wS/X}d_*tm%/-h0">
                <field name="LeftRight_List_0">right</field>
                <field name="Number_0">40000</field>
                <field name="Number_1">90</field>
                <next>
                  <block type="repeat" id="74`{P8k_%JjZn^zR]Q=i">
                    <field name="Int_0">7</field>
                    <statement name="pathstat_0">
                      <shadow type="void" id="Uj;.8h?(nXyl`?a==`vc"></shadow>
                      <block type="go" id="@2t1Y[|iuZ/rj+(=k-v`">
                        <field name="Number_0">500000</field>
                        <next>
                          <block type="leftright" id="z0JeN]fam,$JqhA$i{.#">
                            <field name="LeftRight_List_0">left</field>
                            <field name="Number_0">40000</field>
                            <field name="Number_1">180</field>
                            <next>
                              <block type="go" id="DiMW3ma|[A=G.g-@{+)x">
                                <field name="Number_0">500000</field>
                                <next>
                                  <block type="leftright" id="peq2OA6hzFJ_$(wR.8E.">
                                    <field name="LeftRight_List_0">right</field>
                                    <field name="Number_0">40000</field>
                                    <field name="Number_1">180</field>
                                  </block>
                                </next>
                              </block>
                            </next>
                          </block>
                        </next>
                      </block>
                    </statement>
                    <next>
                      <block type="go" id="@|-9I7@_C9K_(-(i!#:R">
                        <field name="Number_0">28500</field>
                      </block>
                    </next>
                  </block>
                </next>
              </block>
            </next>
          </block>
        </next>
      </block>
    </statement>
  </block>
</xml>
```