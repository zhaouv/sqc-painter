# -*- coding: utf-8 -*-

#初始化
import pya
import paintlib
from imp import reload
reload(paintlib)
layout,top = paintlib.IO.Start("guiopen")#在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001#设置单位长度为1nm
paintlib.IO.pointdistance=2000#设置腔的精度,转弯处相邻两点的距离
TBD=paintlib.TBD.init(6876587)
filepath=paintlib.IO.path+'/demos/'

#画腔
painter3=paintlib.CavityPainter(pya.DPoint(0,24000),angle=180,widout=48000,widin=16000,bgn_ext=48000,end_ext=16000)
#painter3.painterin.Turning=painter3.painterin.TurningInterpolation
#painter3.painterout.Turning=painter3.painterout.TurningInterpolation
def path(painter):#设置内轮廓路径
    painter.Turning(40000)
    painter.Straight(50000)
    painter.Turning(40000)
    for i in range(7):
        painter.Straight(500000)#1
        painter.Turning(-40000)
        painter.Turning(-40000)
        painter.Straight(500000)#2
        painter.Turning(40000)
        painter.Turning(40000)
    painter.Straight(28500)
painter3.Run(path)

layer1 = layout.layer(10, 10)#创建新层
cell2 = layout.create_cell("Cavity1")#创建一个子cell
top.insert(pya.CellInstArray(cell2.cell_index(),pya.Trans()))
painter3.Draw(cell2,layer1)#把画好的腔置入
    #画Crossover
centerlinelist=[]#画腔的中心线并根据中心线画Crossover
centerlinelist.append(painter3.Getcenterlineinfo()[0][0])
painter4=paintlib.TransfilePainter(filepath+"crossover.gds")
painter4.airbridgedistance=100000#设置Crossover的间距
painter4.DrawAirbridge(top,centerlinelist,"Crossover1")

#画电极传输线与Qubit的连接
cell3 = layout.create_cell("TR1")#创建一个子cell
top.insert(pya.CellInstArray(cell3.cell_index(),pya.Trans()))

painter7=paintlib.CavityPainter(pya.DPoint(-450000,600000),angle=0,widout=48000,widin=16000,bgn_ext=0,end_ext=0)
painter7.Connection(clength=50000)
painter7.Draw(cell3,layer1)

painter5=paintlib.CavityPainter(pya.DPoint(-600000,24000),angle=180,widout=20000,widin=10000,bgn_ext=0,end_ext=0)
painter5.Electrode(reverse=True)
def path(painter):
    length=0
    length+=painter.Straight(100000)
    length+=painter.Turning(50000)
    length+=painter.Straight(20000)
    return length
painter5.Run(path)
painter5.InterdigitedCapacitor(9)
dy=TBD.get()
dx=TBD.get()
def path(painter):
    length=0
    length+=painter.Straight(200000+dy)
    length+=painter.Turning(50000)
    length+=painter.Straight(dx)
    return length
painter5.Run(path)
painter5.Narrow(8000,4000,6000)
painter5.end_ext=2000
painter5.Run(lambda painter:painter.Straight(50000))
TBD.set(-500000-painter5.brush.centerx)
TBD.set(600000-painter5.brush.centery,-2)
painter5.Draw(cell3,layer1)

#画边界
layer2 = layout.layer(1, 1)
border=paintlib.BasicPainter.Border(leng=3050000,siz=3050000,wed=50000)
paintlib.BasicPainter.Draw(top,layer2,border)

#画文字
painter2=paintlib.PcellPainter()
painter2.DrawText(top,layer2,"Python",pya.DCplxTrans(100,15,False,1000000,0))

#画Mark
painter1=paintlib.TransfilePainter(filepath+"mark.gds")
pts=[pya.Point(1000000,500000),pya.Point(-500000,-500000),pya.Point(1000000,-1000000)]
painter1.DrawMark(top,pts,"Mark_laserwrite")

#
painter6=paintlib.TransfilePainter(filepath+"xmon.gds")
tr=pya.DCplxTrans(1,-90,False,400000,-400000)
painter6.DrawGds(top,"Qubit",tr)

#输出
print(TBD.isFinish())
paintlib.IO.Show()#输出到屏幕上
paintlib.IO.Write()#输出到文件中
#