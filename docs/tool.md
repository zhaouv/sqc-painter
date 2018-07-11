# tool

## 路径函数生成器

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