# -*- coding: utf-8 -*-

#初始化
import pya
import paintlib
from imp import reload
reload(paintlib)
layout,top = paintlib.IO.Start("guiopen")#在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001#设置单位长度为1nm
paintlib.IO.pointdistance=2000#设置腔的精度,转弯处相邻两点的距离
TBD=paintlib.TBD.init(686587)



layer1 = layout.layer(10, 10)#创建新层

#画电极传输线
cell3 = layout.create_cell("TR1")#创建一个子cell
top.insert(pya.CellInstArray(cell3.cell_index(),pya.Trans()))

painter5=paintlib.CavityPainter(pya.DPoint(-600000,24000),angle=180,widout=20000,widin=10000,bgn_ext=0,end_ext=0)

def path(painter):
    painter.Straight(500000)
    painter.Turning(-20000)
    painter.Turning(20000,180)
    painter.Turning(-20000)
    painter.Straight(500000)
    return 0
painter5.Run(path)
painter5.Draw(cell3,layer1)
def path(painter):
    painter.Turning(20000,180)
    painter.Straight(500000)
    return 0
painter5.Run(path)

#
import simulation
reload(simulation)
Simulation=simulation.Simulation

layerlist=[(10,10)]
# box=pya.Box(-848740,-212112,40934,424224)
# paintlib.Interactive.cut(layerlist=layerlist,layermod='in',box=box)
Simulation.resonator_transmissionline(painter5.region,painter5.brush,layerlist,500000,500000,'TBD_projectname',4,8,4,0)

#输出
print(TBD.isFinish())
paintlib.IO.Show()#输出到屏幕上
#paintlib.IO.Write()#输出到文件中
#

