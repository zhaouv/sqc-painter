# -*- coding: utf-8 -*-

# 初始化
import sys
import os
#
# sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
if 1:
    import pya
    import paintlib

layout, top = paintlib.IO.Start("guiopen")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
paintlib.IO.SetWoringDir(__file__)
TBD = paintlib.TBD.init(68765787)
filepath = paintlib.IO.path+'/demos/'


# 创建cell和layer的结构
layerobstacle = layout.layer(1, 1)
layerlines = layout.layer(10, 10)

cellobstacle = layout.create_cell("obstacle")
top.insert(pya.CellInstArray(cellobstacle.cell_index(), pya.Trans()))

celllines = layout.create_cell("lines")
top.insert(pya.CellInstArray(celllines.cell_index(), pya.Trans()))


# 画障碍物

opts = []
rangex = 15
rangey = 15
for xx in range(-rangex, rangex+1):
    for yy in range(-rangey, rangey):
        pt = pya.DPoint(xx*3000000/2,
                        (yy+0.5*(xx % 2 == 1))*1732000)
        opts.append(pt)

for pt in opts:
    pts = paintlib.BasicPainter.arc(pt, 0.25*1000000, 3*4+1, 0, 360)
    hole = pya.DPolygon(pts)
    paintlib.BasicPainter.Draw(cellobstacle, layerobstacle, hole)


# 连线

brush1 = [paintlib.CavityBrush(pointc=pya.DPoint(-8259000, 17202000-1347000*ii),
                               angle=0, widout=20000, widin=10000, bgn_ext=0) for ii in range(10)]
brush2 = [paintlib.CavityBrush(pointc=pya.DPoint(10012000, 17202000-1347000*(
    5+ii)), angle=-180, widout=20000, widin=10000, bgn_ext=0) for ii in range(10)]
brushs = zip(brush1, brush2)

cell = celllines
layer = layerlines
size = 150000
cellList = [top]
brushs = brushs
layerList = []
box = pya.Box(-12787000, -11127000, 12063000, 18757000)
layermod = 'not in'
order = None

err, lengths, paths = paintlib.AutoRoute.autoRoute(cell, layer, size, cellList, brushs,
                                                   layerList, box, layermod, order)
if not err:
    print(lengths)

args = {
    "brush1": paintlib.CavityBrush(pointc=pya.DPoint(-4564152, -5268197), angle=0, widout=20000, widin=10000, bgn_ext=0),
    "brush4": paintlib.CavityBrush(pointc=pya.DPoint(5899409, -9638130), angle=180, widout=20000, widin=10000, bgn_ext=0),
    "cacheId": "",
    "testMode": True,
    "strategy": "max",
    "length": 0,

    "x0": 0,
    "y0": 0,
    "pre": "",
    "manual": "",
    "post": "",
    "_pass": [
        {
            "x": 1491604,
            "y": -3433796,
            "angle": -30,
            "height": 700000,
            "width": 1111000,
            "pre": "",
            "manual": "",
            "post": ""
        },
        {
            "x": -1732074,
            "y": -7056598,
            "angle": 180,
            "height": 800000,
            "width": 600000
        }
    ],
    "radius": 50000,
    "linksize": 150000,
    "enlargesize": 600000,
    "layerList": []
}
path = paintlib.AutoRoute.linkTwoBrushWithPass(**args)
paintlib.Interactive._show_path(cell, layer, args['brush1'], path)

# 输出
print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#
