
# %%

import pya
import sys
import os

# sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import paintlib

layout, top = paintlib.IO.Start("guinew")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
# TBD = paintlib.TBD.init(676987)

# %%
layer = layout.layer(10, 10)  
layer1 = layout.layer(10, 3)  
layer2 = layout.layer(10, 2)  

cell = layout.create_cell("C1")  
top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))

paintlib.GridLayout.Griditem.width=100000
paintlib.GridLayout.Griditem.height=200000
class typea(paintlib.GridLayout.Griditem):
    args=[3]
    def Draw(self):
        paintlib.BasicPainter.Draw(cell,layer,pya.Polygon(paintlib.BasicPainter.arc(self.position('rd'), 100000/self.args[0], 8, 0, 360)))
class types(paintlib.GridLayout.Griditem):
    args=[4]
    def Draw(self):
        paintlib.BasicPainter.Draw(cell,layer,pya.Polygon(paintlib.BasicPainter.arc(self.position(), 100000/self.args[0], 8, 0, 360)))
class typed(paintlib.GridLayout.Griditem):
    args=[4]
    def Draw(self):
        paintlib.BasicPainter.Draw(cell,layer,pya.Polygon(paintlib.BasicPainter.arc(self.position(), 100000/self.args[0], 32, 0, 360)))
class typef(paintlib.GridLayout.Griditem):
    args=[8]
    height=50000
    def Draw(self):
        paintlib.BasicPainter.Draw(cell,layer,pya.Polygon(paintlib.BasicPainter.arc(self.position(), 100000/self.args[0], 32, 0, 360)))

g1=paintlib.GridLayout(
    '''
    # aaa
    as d
       f
     a sddd
    as dd #sdf
    ''',
    {
    'a':typea,
    's':types,
    'd':typed,
    'f':typef,
    }
)
paintlib.GridLayout.Griditem.offsetx=-g1.width/2
paintlib.GridLayout.Griditem.offsety=-g1.height/2
g1.items[0][0].args=[0.5]
print(g1.Draw())

# %%输出
# print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#

