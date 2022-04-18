
# %%

import pya
import sys
import os
import re

# sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import paintlib

layout, top = paintlib.IO.Start("guinew")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
paintlib.IO.SetWoringDir(__file__)
TBD = paintlib.TBD.init(6876587)
filepath = paintlib.IO.path+'/demos/'

# %%
layer = layout.layer(10, 10)  
layer1 = layout.layer(10, 3)  
layer2 = layout.layer(10, 2)  


painter6 = paintlib.TransfilePainter(filepath+"CascadeRoutePaths.gds")
tr = pya.DCplxTrans(1, 0, False, 0, 0)
painter6.DrawGds(top, "layout0", tr)

cell = layout.create_cell("border")  
top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans(0,400000)))

border=paintlib.BasicPainter.Border(leng=4550000,siz=4550000,wed=50000)
paintlib.BasicPainter.Draw(cell,layout.layer(0, 3),border)

cell = layout.create_cell("lines")  
top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))


inputs=[ { "section": "Filter1", "PositionIn": [ -2647, 3324, 180, "5105" ], "PositionOut": [ 0, 3310, 90, "5105" ] }, { "section": "Filter2", "PositionIn": [ -2647, -676, 180, "5105" ], "PositionOut": [ 0, -690, 90, "5105" ] }, { "section": "Qubit1", "PositionXY": [ -1936, 1830, 270, "242" ], "PositionZ": [ -2000, 1830, 270, "242" ] }, { "section": "Qubit2", "PositionXY": [ -1236, 1770, 270, "242" ], "PositionZ": [ -1300, 1770, 270, "242" ] }, { "section": "Qubit3", "PositionXY": [ -536, 1800, 270, "242" ], "PositionZ": [ -600, 1800, 270, "242" ] }, { "section": "Qubit4", "PositionXY": [ 664, 1770, 270, "242" ], "PositionZ": [ 600, 1770, 270, "242" ] }, { "section": "Qubit5", "PositionXY": [ 1364, 1830, 270, "242" ], "PositionZ": [ 1300, 1830, 270, "242" ] }, { "section": "Qubit6", "PositionXY": [ 2032, 1960, 270, "242" ], "PositionZ": [ 2000, 1960, 270, "242" ] }, { "section": "Qubit7", "PositionXY": [ -1968, -2040, 270, "242" ], "PositionZ": [ -2000, -2040, 270, "242" ] }, { "section": "Qubit8", "PositionXY": [ -1236, -2200, 270, "242" ], "PositionZ": [ -1300, -2200, 270, "242" ] }, { "section": "Qubit9", "PositionXY": [ -568, -2040, 270, "242" ], "PositionZ": [ -600, -2040, 270, "242" ] }, { "section": "Qubit10", "PositionXY": [ 664, -2170, 270, "242" ], "PositionZ": [ 600, -2170, 270, "242" ] }, { "section": "Qubit11", "PositionXY": [ 1364, -2230, 270, "242" ], "PositionZ": [ 1300, -2230, 270, "242" ] }, { "section": "Qubit12", "PositionXY": [ 2064, -2200, 270, "242" ], "PositionZ": [ 2000, -2200, 270, "242" ] }]

group1=[]
group2=[]
for sec in inputs:
    if sec['section'].startswith('Filter') and int(re.search('\d+',sec['section'])[0])<=1:
        group1.append(sec['PositionIn'])
        group1.append(sec['PositionOut'])
    if sec['section'].startswith('Filter') and int(re.search('\d+',sec['section'])[0])>1:
        group2.append(sec['PositionIn'])
        group2.append(sec['PositionOut'])
    if sec['section'].startswith('Qubit') and int(re.search('\d+',sec['section'])[0])<=6:
        group1.append(sec['PositionXY'])
        group1.append(sec['PositionZ'])
    if sec['section'].startswith('Qubit') and int(re.search('\d+',sec['section'])[0])>6:
        group2.append(sec['PositionXY'])
        group2.append(sec['PositionZ'])


def tostack(arr2):
    return [[pya.DPoint(pt[0]*1000,pt[1]*1000) for pt in arr1] for arr1 in arr2]

def getbrush1(pt,groupi):
    widout=20000
    widin=10000
    if groupi[-1]=='242':
        widout=8000
        widin=4000
    return paintlib.CavityBrush(pointc=pt, angle=groupi[2],widout=widout,widin=widin,bgn_ext=0)
def getbrush2(pt,groupi):
    ax=abs(pt.x)
    ay=abs(pt.y-400000)
    dl=100000
    if ax>=ay and pt.x>=0:
        dx=dl
        dy=0
        angle=180
    if ax>=ay and pt.x<0:
        dx=-dl
        dy=0
        angle=0
    if ax<ay and pt.y>=0:
        dx=0
        dy=dl
        angle=270
    if ax<ay and pt.y<0:
        dx=0
        dy=-dl
        angle=90
    return paintlib.CavityBrush(pointc=pya.DPoint(pt.x+dx,pt.y+dy), angle=angle,widout=20000,widin=10000,bgn_ext=0)

import re
def drawOne(brush1,brush2,pathstr,groupi):
    painter9 = paintlib.CavityPainter(brush1)
    narrow=10000
    s2=[]
    if groupi[-1]=='242':
        pathstr=pathstr
        s,e=list(re.finditer('s \d+(\.\d+)?', pathstr))[1].span()
        sl = float(pathstr[s+2:e])
        painter9.Run(pathstr[:s]+f's {sl/2-narrow/2}')
        s2=painter9.Getcenterlineinfo()
        painter9.Narrow(20000, 10000, narrow)
        painter9.Run(f's {sl/2-narrow/2}'+pathstr[e:])
    else:
        painter9.Run(pathstr)
    s1=painter9.Getcenterlineinfo()
    painter9.Electrode(wid=360000, length=360000, midwid=200000, midlength=200000, narrowlength=120000)
    painter9.Draw(top, layer1)  # 把画好的腔置入
    return s1,s2

# layout, top = paintlib.IO.Start("guiopen")
# [[(pt.x,pt.y) for pt in path.shape.each_dpoint()] for path in paintlib.IO.layout_view.each_object_selected()]

stacks1=[
tostack([[(-2123.8500000000004, 1736.4810000000004), (-500.90800000000013, 414.0840000000001)], [(2137.2070000000003, 1856.6990000000005), (507.5870000000001, 434.1200000000001)], [(-3059.9450000000006, 3235.8040000000005), (-2813.7420000000006, 3564.074000000001)], [(-187.58300000000006, 3868.896000000001), (234.47900000000004, 3868.896000000001)]]

),
tostack([[(-2285.3930000000005, -135.66300000000004), (-2598.4600000000005, 1753.1780000000003)], [(2348.0060000000008, 0.0), (2713.252000000001, 2003.6320000000005)], [(-3339.3870000000006, 3631.583000000001), (-2921.9630000000006, 3913.344000000001)], [(-240.01800000000006, 4205.540000000001), (250.45400000000006, 4195.104000000001)]]

),
tostack([[(-4028.135000000001, 417.4230000000001), (-4038.571000000001, 4424.687000000001)], [(3986.393000000001, 553.0860000000001), (4017.699000000001, 4414.252000000001)], [(-3506.3560000000007, 4424.687000000001), (-2984.5770000000007, 4424.687000000001)], [(-250.45400000000006, 4424.687000000001), (292.1960000000001, 4424.687000000001)]]

),

]

stacks2=[
tostack([[(-3013.230000000001, -490.6270000000001), (-2954.6100000000006, -912.6880000000002)], [(-2195.6470000000004, -2454.4490000000005), (-392.3780000000001, -2487.8430000000008)], [(450.8170000000001, -2504.5400000000004), (2229.0400000000004, -2537.9340000000007)], [(-82.06700000000002, -339.9940000000001), (117.23900000000003, -539.3010000000002)]]

),
tostack([[(-3559.6420000000007, -573.6220000000002), (-3465.851000000001, -1277.0580000000002)], [(-2638.1150000000007, -3078.9140000000007), (2496.1910000000007, -3097.281000000001)], [(928.7670000000002, 20.871000000000006), (1314.8830000000003, -521.7790000000001)]]

),
tostack([[(-4017.4680000000008, -727.2700000000002), (-4005.744000000001, -1782.4240000000004)], [(-4038.571000000001, -3621.147000000001), (4049.0060000000008, -3631.583000000001)], [(4012.804000000001, 218.76100000000005), (4012.804000000001, -590.1900000000002)]]

),

]

sizes=[80000,120000,200000]
saveRates=[3,1.2,1.1]

stacks=stacks1
group=group1
as1=[]
as2=[]
for stacks,group in zip([stacks1,stacks2],[group1,group2]):
    ptsIn=[pya.DPoint(a[0]*1000,a[1]*1000) for a in group]
    selectedStackPts,order=paintlib.CascadeRoute.CascadeRouteStraightforward(cell, layer2, sizes=sizes, potentialRates=[0.2]*len(stacks), saveRates=saveRates,ptsIn=ptsIn, ptsOut=None, stacks=stacks, cellList=[top], layerList=[], box=pya.Box(-5700000, -5700000, 5700000, 5700000), layermod='in')

    paintlib.Interactive.deltaangle=1
    for di in range(len(group)):
        spts=[a[di] for a in selectedStackPts][1:]
        brush1=getbrush1(selectedStackPts[0][di],group[di])
        brush2=getbrush2(spts[-1],group[di])
        pathstr = paintlib.Interactive.link(brush1=brush1, brush2=brush2, spts=spts, print_=False)
        s1,s2=drawOne(brush1,brush2,pathstr,group[di])
        as1.extend(s1)
        as2.extend(s2)
    paintlib.Interactive.deltaangle=45

painter4 = paintlib.TransfilePainter(filepath+"crossover.gds")
painter4.airbridgedistance = 50000  # 设置Crossover的间距
painter4.DrawAirbridge(top, as1, "Crossover5105")

painter5 = paintlib.TransfilePainter(filepath+"crossover.gds")
painter5.airbridgedistance = 50000  # 设置Crossover的间距
painter5.DrawAirbridge(top, as2, "Crossover242")


# %%输出
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中

