
# %%

import pya
import sys
import os

sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import paintlib
import imp
for moduleName in [
    # 'AutoRoute',
    # 'BasicPainter',
    # 'CavityBrush',
    # 'CavityPainter',
    # 'Collision',
    # 'Interactive',
    # 'IO',
    # 'Painter',
    'PcellPainter',
    'SpecialPainter',
    # 'TBD',
    # 'TransfilePainter',
]:
    pass
    asdasfaese = imp.load_source(
        'paintlib.'+moduleName, 'paintlib\\'+moduleName+'.py')
    imp.reload(asdasfaese)
imp.reload(paintlib)

layout, top = paintlib.IO.Start("guinew")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
TBD = paintlib.TBD.init(676987)
# %%[markdown]
# list:

# + [ ] ?几个碰撞检测或基于已有图形的例子和最佳实践
# + [ ] ?碰撞检测的ab, 通过切分来优化速度

# + [ ] DrawContinueAirbridgePainter 想要超出腔的说明
# + [x] DrawContinueAirbridgePainter 圆角
# + [ ] DrawContinueAirbridgePainter 圆角 textcover/文档
# %%
layer = layout.layer(10, 10)  
layer1 = layout.layer(10, 3)  
layer2 = layout.layer(10, 2)  

cell = layout.create_cell("Cavity1")  
top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))

# %% 联通的ab两端延长
# extended ContinueAirbridge demo
path='r50000 s1000000 r50000'
path='s500000'
path='n5[r50000 s50000 l50000]'
a=paintlib.CavityPainter(pya.DPoint(0, 24000), angle=90, widout=16000, widin=8000)
b=paintlib.CavityPainter(a.brush.reversed())
a.cavityLength=a.Run(path)
a.Draw(cell,layer)
p1='s100000'
p2='s100000'
b.Run(paintlib.TraceRunner.reversePath(p1))
b=paintlib.CavityPainter(b.brush.reversed())
paintlib.IO.pointdistance = 3000
b.cavityLength=b.Run(p1+path+p2)
paintlib.IO.pointdistance = 1000
# b.Draw(cell,layer)
centerlineinfo=b.Getcenterlineinfo()
paintlib.SpecialPainter.DrawContinueAirbridgePainter(
    cell, layer1, layer2, centerlineinfo, s1=70000, s2=70000+85000, e1=b.cavityLength-15000, e2=b.cavityLength-15000-8500,rounded=0,cnum=1)
paintlib.SpecialPainter.DrawContinueAirbridgePainter(
    cell, layer1, layer2, centerlineinfo, s1=70000, s2=70000+85000, e1=b.cavityLength-15000, e2=b.cavityLength-15000-8500,rounded=1000,cnum=1)
paintlib.SpecialPainter.DrawContinueAirbridgePainter(
    cell, layer1, layer2, centerlineinfo, s1=70000, s2=70000+85000, e1=b.cavityLength-15000, e2=b.cavityLength-15000-8500,rounded=5000,cnum=1)
# %% round
a=pya.DPolygon(paintlib.BasicPainter.rectangle(pya.DPoint(),pya.DPoint(0,50000),1000000)[0])
paintlib.BasicPainter.Draw(cell,layer,a)
b=paintlib.PcellPainter().round(a,300,10000)
paintlib.BasicPainter.Draw(cell,layer,b)
# %%输出
print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#

