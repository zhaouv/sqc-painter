


# %%

import pya
import sys
import os

sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import paintlib
from math import floor, ceil

layout, top = paintlib.IO.Start("guiopen")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离

BasicPainter=paintlib.BasicPainter
Collision=paintlib.Collision
IO=paintlib.IO

box=pya.Box(-1700000,-600000,1100000,1900000)
dots_box=box
sizes=60 *1000
sizec=42 *1000
sizeo=32 *1000
sizei=12 *1000
dots_layers=[
    (0,5),
    (5,0),
    (6,0),
]
check_ignore_layers=[
    (0, 0), 
    (0, 1), 
    (0, 2),
    (0,5),
    (5,0),
    (6,0),
]

# %%
layerc = layout.layer(*dots_layers[0])  
layero = layout.layer(*dots_layers[1])  
layeri = layout.layer(*dots_layers[2])  

try:
    dots_stage+=1
    if dots_stage==2:
        dots_stage=0
except:
    dots_stage=0

if dots_stage==0:

    cell = layout.create_cell("dotsc")  
    top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))

    def DrawDotc(cell, layer, box, sizeo, sizes, dx=0, dy=0, filterfunc=None):
        d = sizes
        area = box
        dx = dx % d
        dy = dy % d
        left = floor((area.left-dx)/d)
        bottom = floor((area.bottom-dy)/d)
        right = ceil((area.right-dx)/d)
        top = ceil((area.top-dy)/d)
        x0 = left*d+dx
        y0 = bottom*d+dy
        boxesregion = pya.Region()
        for ii in range(right-left):
            for jj in range(top-bottom):
                x1 = x0+ii*d
                y1 = y0+jj*d
                box = pya.Box(x1, y1, x1+sizeo, y1+sizeo)
                boxesregion.insert(box)
                # BasicPainter.Draw(cell, layer, box)
        andRegion = boxesregion# & region
        # if filterfunc:
        #     andRegion_ = pya.Region()
        #     for pp in andRegion.each():
        #         if filterfunc(pp):
        #             andRegion_.insert(pp)
        #     andRegion = andRegion_

        BasicPainter.Draw(cell, layer, andRegion)
        return andRegion
    DrawDotc(cell, layerc, dots_box, sizec, sizes, dx=0, dy=0)

if dots_stage==1:
    cell = layout.create_cell("dots")  
    top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))

    def doShapes(cellList, layerList=None):
        _, global_region = Collision.getShapesFromCellAndLayer(
            cellList=[IO.top], layerList=check_ignore_layers, box=dots_box, layermod='not in')
        layers = Collision.getLayers(layerList=layerList, layermod='in')

        for cell in cellList:
            for layer in layers:
                it=paintlib.IO.top.begin_shapes_rec(layer)
                while not it.at_end():
                    shape_=it.shape()
                    tregion = pya.Region()
                    tregion.insert(shape_.bbox())
                    area_=(tregion - global_region).area()
                    
                    if area_ > sizec*sizec*0.999999:
                        # return shape_
                        x1=shape_.bbox().center().x
                        y1=shape_.bbox().center().y
                        
                        box = pya.Box(x1-sizeo/2, y1-sizeo/2, x1+sizeo/2, y1+sizeo/2)
                        BasicPainter.Draw(cell, layero, box)
                        box = pya.Box(x1-sizei/2, y1-sizei/2, x1+sizei/2, y1+sizei/2)
                        BasicPainter.Draw(cell, layeri, box)
                        shape_.delete()
                    else:
                        shape_.delete()
                    it.next()

    doShapes(cellList=[IO.top], layerList=[dots_layers[0]])

# %%输出
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#

