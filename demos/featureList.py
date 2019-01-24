# -*- coding: utf-8 -*-

#初始化
import sys
import os
#
#sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pya
import paintlib
from imp import reload
reload(paintlib)
layout,top = paintlib.IO.Start("guiopen")#在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001#设置单位长度为1nm
paintlib.IO.pointdistance=2000#设置腔的精度,转弯处相邻两点的距离
TBD=paintlib.TBD.init(6876587)
filepath=paintlib.IO.path+'/demos/'

#创建cell和layer的结构
layer1 = layout.layer(10, 10)#创建新层

cell2 = layout.create_cell("Cavity1")#创建一个子cell
top.insert(pya.CellInstArray(cell2.cell_index(),pya.Trans()))

cell3 = layout.create_cell("TR1")
top.insert(pya.CellInstArray(cell3.cell_index(),pya.Trans()))

layer2 = layout.layer(1, 1)

cell4 = layout.create_cell("Cavity2")
top.insert(pya.CellInstArray(cell4.cell_index(),pya.Trans()))

layer3 = layout.layer(2, 0)
layer4 = layout.layer(3, 0)

#画腔_1
painter3=paintlib.CavityPainter(pya.DPoint(0,24000),angle=180,widout=48000,widin=16000,bgn_ext=48000,end_ext=16000)
#painter3.painterin.Turning=painter3.painterin.TurningInterpolation
#painter3.painterout.Turning=painter3.painterout.TurningInterpolation
def path(painter):#设置内轮廓路径
    painter.Turning(40000)
    painter.Straight(50000)
    painter.Turning(40000)
    for i in range(7):
        painter.Straight(500000+40000*i)#1
        painter.Turning(-40000)
        painter.Turning(-40000)
        painter.Straight(500000+40000*i)#2
        painter.Turning(40000)
        painter.Turning(40000)
    painter.Straight(28500)
painter3.Run(path)#Run内填函数(如上)或字符串(见下一个例子)来描述的内径的运动

painter3.Draw(cell2,layer1)#把画好的腔置入
    #画Crossover
painter4=paintlib.TransfilePainter(filepath+"crossover.gds")
painter4.airbridgedistance=100000#设置Crossover的间距
painter4.DrawAirbridge(cell2,painter3.Getcenterlineinfo(),"Crossover1")

#画腔_2
painter7=paintlib.CavityPainter(pya.DPoint(300000,-900000),angle=180,widout=24000,widin=8000,bgn_ext=0,end_ext=0)
    #画腔到比特的连接
painter7.Connection(clength=50000,reverse=True)
paintlib.IO.centerlineratio=3
    #画路径
painter7.cavityLength=painter7.Run('''s 184000 r 50000 s 50000 
n3[ r 50000 s 500000 l 50000,180 s 500000 r 50000]
r 50000 s 500000 l 50000,180 s 210000
''')# s <length> 直行 r <radius[,angle]> 右转 l <radius[,angle]> 左转 n<number>[<content>] 重复number次content,可以嵌套循环
paintlib.IO.centerlineratio=1
    #画腔到比特的连接(更复杂的版本)
paintlib.SpecialPainter.ConnectionOnPainter(painter7,clengthplus=14000, turningRadiusPlus=2000)
painter7.Draw(cell4,layer1)#把画好的腔置入
    #画Crossover, 并手动指定位置
centerlineinfo=painter7.Getcenterlineinfo()
painter8=paintlib.TransfilePainter(filepath+"crossover.gds")
painter8.airbridgeDistanceFunc(0,[50000,20000,50000,20000,50000,20000,50000,20000,50000,20000,50000,20000,50000,20000,50000,20000,121212])#设置Crossover的间距
painter8.airbridgedistance=painter8.airbridgeDistanceFunc
painter8.DrawAirbridge(cell4,centerlineinfo,"Crossover2")
    #画连续的airbridge构成的同轴线
paintlib.SpecialPainter.DrawContinueAirbridgePainter(cell4,layer4,layer3,centerlineinfo,s1=700000,s2=700000+85000,e1=painter7.cavityLength-15000,e2=painter7.cavityLength-15000-8500)

#画电极传输线
painter5=paintlib.CavityPainter(pya.DPoint(-600000,24000),angle=180,widout=20000,widin=10000,bgn_ext=0,end_ext=0)
painter5.Electrode(reverse=True)
painter5.Run('s100000 r50000 s20000')
painter5.InterdigitedCapacitor(9)
dy=TBD.get()
dx=TBD.get()
painter5.Run('n3[l20000 r20000,180 l20000] s{} r50000 s{}'.format(dy,dx))
painter5.Narrow(8000,4000,6000)
painter5.end_ext=2000
painter5.Run('s50000')
TBD.set(-500000-painter5.brush.centerx)
TBD.set(600000-painter5.brush.centery,-2)
painter5.Draw(cell3,layer1)

#画边界
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
tr=pya.DCplxTrans(1,-90,False,1000000,-300000)
painter6.DrawGds(top,"Qubit",tr)

#输出
print(TBD.isFinish())
paintlib.IO.Show()#输出到屏幕上
#paintlib.IO.Write()#输出到文件中
#