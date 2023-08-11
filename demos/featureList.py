# -*- coding: utf-8 -*-

# %% 初始化
import sys
import os
#
# sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
if 1:
    import pya
    import paintlib

# layout, top = paintlib.IO.Start("guiopen")  # 在当前的图上继续画,如果没有就创建一个新的
layout, top = paintlib.IO.Start("guinew")  # 创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
paintlib.IO.SetWoringDir(__file__)
TBD = paintlib.TBD.init(6876587)
filepath = paintlib.IO.path+'/demos/'

# %% 创建cell和layer的结构
layer1 = layout.layer(10, 10)  # 创建新层

cell2 = layout.create_cell("Cavity1")  # 创建一个子cell
top.insert(pya.CellInstArray(cell2.cell_index(), pya.Trans()))

cell3 = layout.create_cell("TR1")
top.insert(pya.CellInstArray(cell3.cell_index(), pya.Trans()))

layer2 = layout.layer(1, 1)

cell4 = layout.create_cell("Cavity2")
top.insert(pya.CellInstArray(cell4.cell_index(), pya.Trans()))

cell5 = layout.create_cell("Cavity3")
top.insert(pya.CellInstArray(cell5.cell_index(), pya.Trans()))

cell6 = layout.create_cell("Cavity4")
top.insert(pya.CellInstArray(cell6.cell_index(), pya.Trans()))

cell7 = layout.create_cell("AttachmentTree")
top.insert(pya.CellInstArray(cell7.cell_index(), pya.Trans()))

layer3 = layout.layer(2, 0)
layer4 = layout.layer(3, 0)

# %% 画腔+Crossover+基于碰撞检测的Crossover
# 画腔
painter3 = paintlib.CavityPainter(pya.DPoint(
    0, 24000), angle=180, widout=48000, widin=16000, bgn_ext=48000, end_ext=16000)
# painter3.painterin.Turning=painter3.painterin.TurningInterpolation
# painter3.painterout.Turning=painter3.painterout.TurningInterpolation

path = 'r 40000 s 50000 r 40000'
for i in range(7):
    path += f's{500000+40000*i} l 40000,180 s{500000+40000*i} r 40000,180'
path += 's 28500'

painter3.Run(path)  # Run内填字符串来描述的内径的运动
# s <length> 直行 r <radius[,angle]> 右转 l <radius[,angle]> 左转 n<number>[<content>] 重复number次content,可以嵌套循环

painter3.Draw(cell2, layer1)  # 把画好的腔置入
# 画Crossover
painter4 = paintlib.TransfilePainter(filepath+"crossover.gds")
painter4.airbridgedistance = 100000  # 设置Crossover的间距
painter4.DrawAirbridge(cell2, painter3.Getcenterlineinfo(), "Crossover1")

# 画腔
painter13 = paintlib.CavityPainter(pya.DPoint(
    -125000, 350000), angle=90, widout=16000, widin=8000, bgn_ext=0, end_ext=0)
painter13.Run('s 500000 l 50000 r 50000 s200000')
painter13.Draw(cell2, layer1)
# 画基于碰撞检测的Crossover
painter14 = paintlib.TransfilePainter(filepath+"crossover.gds")
painter14.airbridgedistance = 30000  # 设置Crossover的间距
painter14.DrawAirbridgeWithCollisionCheck(cell2, painter13.Getcenterlineinfo(
), "Crossover3", boxY=16000+8000, boxWidth=15000, boxHeight=6000, push=2000, extend=20000)

# %% 画腔+耦合器+精确指定Crossover位置+连续的airbridge构成的同轴线
# 画腔
painter7 = paintlib.CavityPainter(pya.DPoint(
    300000, -900000), angle=180, widout=24000, widin=8000, bgn_ext=0, end_ext=0)
# 画腔到比特的连接
painter7.Connection(clength=50000, reverse=True)
paintlib.IO.centerlineratio = 3
# 画路径
painter7.cavityLength = painter7.Run('''s 184000 r 50000 s 50000 
n3[ r 50000 s 500000 l 50000,180 s 500000 r 50000]
r 50000 s 500000 l 50000,180 s 210000
''')
paintlib.IO.centerlineratio = 1
# 画腔到比特的连接(更复杂的版本)
paintlib.SpecialPainter.ConnectionOnPainter(
    painter7, clengthplus=14000, turningRadiusPlus=2000)
painter7.Draw(cell4, layer1)  # 把画好的腔置入
#画Crossover, 并手动指定位置
centerlineinfo = painter7.Getcenterlineinfo()
painter8 = paintlib.TransfilePainter(filepath+"crossover.gds")
painter8.airbridgeDistanceFunc(0, [50000, 20000, 50000, 20000, 50000, 20000, 50000, 20000,
                                   50000, 20000, 50000, 20000, 50000, 20000, 50000, 20000, 121212])  # 设置Crossover的间距
painter8.airbridgedistance = painter8.airbridgeDistanceFunc
painter8.DrawAirbridge(cell4, centerlineinfo, "Crossover2")
# 画连续的airbridge构成的同轴线
paintlib.SpecialPainter.DrawContinueAirbridgePainter(
    cell4, layer4, layer3, centerlineinfo, s1=700000, s2=700000+85000, e1=painter7.cavityLength-15000, e2=painter7.cavityLength-15000-8500,rounded=1000)

# %% 三平行线的腔
# 画腔
painter10 = paintlib.TriCavityPainter(pya.DPoint(
    800000, 200000), angle=180, widout=48000, widin=36000, bgn_ext=0, end_ext=0)

painter11 = paintlib.CavityPainter(painter10.brushr.reversed())
painter11.Run('s80000 r45000')
# painter11.Electrode()
painter11.Draw(cell6, layer1)  # 把画好的腔置入

painter10.Run('r 40000 s 10000')
painter10.Narrow(24000, 18000, 30000)
painter10.Run('s 10000 r 40000')

painter10.Draw(cell6, layer1)  # 把画好的腔置入

painter12 = paintlib.CavityPainter(painter10.brushl)
painter12.Run('s20000 l45000')
# painter12.Electrode()
painter12.Draw(cell6, layer1)  # 把画好的腔置入


# %% 沿参数曲线画腔
def xfunc(t): return 500000*t


def yfunc(t): return 500000*10*t*(t-0.333)*(t-0.6666)*(t-1)


# lengthlist=[l1,l2,d1,w1,w2]
paintlib.SpecialPainter.DrawParametricCurve(cell5, layer1, paintlib.CavityBrush(pointc=pya.DPoint(800000, -70000), angle=0, widout=24000, widin=8000,
                                                                                bgn_ext=0), xfunc, yfunc, pointnumber=100, startlength=10000, deltalength=100000, number=10, lengthlist=[50000, 40000, 5000, 40000, 20000])
paintlib.PcellPainter().DrawText(cell5, layer2, "y=10*x*(x-0.333)*(x-0.6666)*(x-1)",
                                 pya.DCplxTrans(30, 25, False, 800000, 0))
#


def getSpiralFunc(a, angle0, angle1):
    from math import cos, sin, pi, sqrt

    def f(t):
        return (angle0*(1-t)+angle1*t)/180*pi

    def xfunc(t):
        theta = f(t)
        return a*sqrt(abs(theta))*cos(theta) * (-1 if theta < 0 else 1)

    def yfunc(t):
        theta = f(t)
        return a*sqrt(abs(theta))*sin(theta)
    return xfunc, yfunc


xfunc, yfunc = getSpiralFunc(90000, -720, 720)
# lengthlist=[l1,l2,d1,w1,w2]
paintlib.SpecialPainter.DrawParametricCurve(cell5, layer1, paintlib.CavityBrush(pointc=pya.DPoint(1050000, 900000), angle=0, widout=24000, widin=8000,
                                                                                bgn_ext=0), xfunc, yfunc, pointnumber=3000, startlength=50000, deltalength=100000, number=3000, lengthlist=[50000, 40000, 5000, 30000, 15000])

# %% 画电极传输线
painter5 = paintlib.CavityPainter(
    pya.DPoint(-600000, 24000), angle=180, widout=20000, widin=10000, bgn_ext=0, end_ext=0)
painter5.Electrode(reverse=True)
painter5.Run('s100000 r50000 s20000')
painter5.InterdigitedCapacitor(9)
dy = TBD.get()
dx = TBD.get()
painter5.Run('n3[l20000 r20000,180 l20000] s{} r50000 s{}'.format(dy, dx))
painter5.Narrow(8000, 4000, 6000)
painter5.end_ext = 2000
painter5.Run('s50000')
TBD.set(-500000-painter5.brush.centerx)
TBD.set(600000-painter5.brush.centery, -2)
painter5.Draw(cell3, layer1)

# %% 画边界
border = paintlib.BasicPainter.Border(leng=3050000, siz=3050000, wed=50000)
paintlib.BasicPainter.Draw(top, layer2, border)

# %% 画文字
painter2 = paintlib.PcellPainter()
painter2.DrawText(top, layer2, "Python",
                  pya.DCplxTrans(100, 15, False, 1000000, 0))
painter2.DrawText_LiftOff(top, layer2, '''
sqc-painter

0123456789ab 
z          c
y alphabet d
x          e
w for      f
v lift-off g
u          h
tsrqponmlkji

~!@#$%^&*()-=_+[]
{}\\|;:'\",.<>/?`
'''.strip(), pya.DCplxTrans(30, 0, False, 1350000, 0))

# %% 画Mark
painter1 = paintlib.TransfilePainter(filepath+"mark.gds")
pts = [pya.Point(1000000, 500000), pya.Point(-500000, -500000),
       pya.Point(1000000, -1000000)]
painter1.DrawMark(top, pts, "Mark_laserwrite")

# %% 导入GDS
painter6 = paintlib.TransfilePainter(filepath+"xmon.gds")
tr = pya.DCplxTrans(1, -90, False, 1000000, -300000)
painter6.DrawGds(top, "Qubit", tr)

# %% 在区域内填充网格
box = pya.Box(-140000, -30000, 40000, 190000)
paintlib.SpecialPainter.DrawBoxes(cell=cell5, layer=layer4, dlength=2000, dgap=5000, radius=20000,
                                  number=70, layerlist=None, layermod='not in', box=box, cutbool=True, dx=0, dy=0,filterfunc=lambda pp:pp.area()>=3900000)

# %% 以某点为中心矩形区域内画定长的腔并产生两个刷子
_, brush1, brush2, minlength, maxlength = paintlib.SpecialPainter.contortion(
    x=-752000, y=-813000, angle=0, width=800000, height=473000, length=0, radius=15000, widout=2000, widin=1000, strategy='width', infoOnly=True)
path, _, _, _, _ = paintlib.SpecialPainter.contortion(x=-752000, y=-813000, angle=0, width=800000, height=473000, length=int(
    minlength/2+maxlength/2), radius=15000, widout=2000, widin=1000, strategy='height', infoOnly=False)
painter9 = paintlib.CavityPainter(brush1.reversed())
painter9.Run(path)
painter9.Draw(cell2, layer1)  # 把画好的腔置入

# %% 自动布线连接两个刷子
brush1 = paintlib.CavityBrush(pointc=pya.DPoint(-612000, -500000), angle=90)
brush2 = paintlib.CavityBrush(pointc=pya.DPoint(473000, -900000), angle=-90)
path = paintlib.AutoRoute.linkTwoBrush(brush1, brush2)
paintlib.Interactive._show_path(cell2, layer1, brush1, path)

# 用BrushLinker连接笔刷
paintlib.IO.warning.angle_45_link_fallback=False
for ii,xx,yy,aa in zip([1,2,3,4,5],[1484000,1484000,1484000,1313000,1484000],[-500000,-500000,-530000,-273000,-500000],[135,180,90,225,225]):
    brush1 = paintlib.CavityBrush(pointc=pya.DPoint(1212000, -450000-ii*60000), angle=0)
    brush2 = paintlib.CavityBrush(pointc=pya.DPoint(xx, yy-ii*60000), angle=aa)
    path = paintlib.BrushLinker.link(brush1, brush2)
    paintlib.Interactive._show_path(cell2, layer1, brush1, path)
    path = paintlib.BrushLinker.link(brush1, brush2, linktype='any')
    paintlib.Interactive._show_path(cell2, layer1, brush1, path)

# %% 附着树
import json
with open(filepath+'AttachmentTreeDemo.json') as fid:
    root=json.load(fid)

walker=paintlib.AttachmentTree().load(root,{'yy':90000}).transform(pya.Trans(-904000,728000))

for k in walker.collection:
    paintlib.BasicPainter.Draw(cell7,layout.layer(13, k),walker.collection[k])

# %% 输出
print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#
