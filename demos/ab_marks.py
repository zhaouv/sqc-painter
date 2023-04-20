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

layer3 = layout.layer(2, 0)
layer4 = layout.layer(3, 0)

# %% 画腔+Crossover+基于碰撞检测的Crossover


# 画腔
painter13 = paintlib.CavityPainter(pya.DPoint(
    -125000, 350000), angle=90, widout=16000, widin=8000, bgn_ext=0, end_ext=0)
painter13.Run(paintlib.TraceRunner.getPathFunction_withMarkTurning('s 500000 l 50000,45 s 800000 r 50000 s200000'))
painter13.Draw(cell2, layer1)


# 画点阵


# for plr in painter13.painterout.marks:
#     for pt in plr:
#         pts=paintlib.BasicPainter.arc(pt,15000,3*4+1,0,360)
#         hole=pya.DPolygon(pts)
#         paintlib.BasicPainter.Draw(cell3,layer1,hole)

# # 画基于碰撞检测的Crossover
# painter14 = paintlib.TransfilePainter(filepath+"crossover.gds")
# painter14.airbridgedistance = 50000  # 设置Crossover的间距
# painter14.DrawAirbridgeWithCollisionCheck(cell2, painter13.Getcenterlineinfo(
# ), "Crossover3", boxY=16000+8000, boxWidth=15000, boxHeight=6000, push=2000, extend=20000)

mixpts=[]
for plr in painter13.painterout.marks:
    pt=pya.DPoint(plr[0].x/2+plr[1].x/2,plr[0].y/2+plr[1].y/2)
    mixpts.append(pt)

    pts=paintlib.BasicPainter.arc(pt,15000,3*4+1,0,360)
    hole=pya.DPolygon(pts)
    paintlib.BasicPainter.Draw(cell3,layer1,hole)

# 画基于碰撞检测的Crossover
painter14 = paintlib.TransfilePainter(filepath+"crossover.gds")
painter14.airbridgedistance = 50000  # 设置Crossover的间距
painter14.DrawAirbridge(cell2, painter13.Getcenterlineinfo(), "Crossover3", avoidpts={'pts': mixpts, 'distance': 15000})

# %% ref


# 画腔
painter13 = paintlib.CavityPainter(pya.DPoint(
    0, 350000), angle=90, widout=16000, widin=8000, bgn_ext=0, end_ext=0)
painter13.Run(paintlib.TraceRunner.getPathFunction_withMarkTurning('s 500000 l 50000,45 s 800000 r 50000 s200000'))
painter13.Draw(cell2, layer1)


# 画Crossover
painter14 = paintlib.TransfilePainter(filepath+"crossover.gds")
painter14.airbridgedistance = 50000  # 设置Crossover的间距
painter14.DrawAirbridge(cell2, painter13.Getcenterlineinfo(
), "Crossover3")

# %% 画边界
border = paintlib.BasicPainter.Border(leng=3050000, siz=3050000, wed=50000)
paintlib.BasicPainter.Draw(top, layer2, border)





# %% 输出
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#
