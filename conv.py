
# %%

import pya
import sys
import os

sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import paintlib


layout, top = paintlib.IO.Start("guiopen")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离


# %%
layer = layout.layer(10, 10)  
layer1 = layout.layer(10, 3)  
layer2 = layout.layer(10, 2)  

cell = layout.create_cell("Cavity1")  
top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))

# 接口大致为
#   NewGDS = generateNewLayer(GDSFileRow,NewLayerSize,Layer1Name, Layer1Distance, Layer2Name, Layer2Distance,...)
#   将NewLayerSize的图形在原来基础上，扣掉要避开的图层及边缘拓展区域。

# %% input

cell=cell
layer=layer
layerList=[(2,0)]
distanceList=[20000]
numberList=[70]
box = pya.Box(-4000000, -4000000, 4000000, 4000000)

# %% call
Collision=paintlib.Collision
BasicPainter=paintlib.BasicPainter
IO=paintlib.IO
from math import cos, sin, pi
def convfunc(cell,layer,layerList,distanceList,numberList,box):
    layers = Collision.getLayers(layerList=layerList, layermod='in')
    outregion = pya.Region(box)
    inregions = []
    region = pya.Region()

    for layeri,radius,number in zip(layers,distanceList,numberList):
        inregion = pya.Region()
        s = IO.top.begin_shapes_rec_touching(layeri, box)
        inregion.insert(s)
        inregion.merge()
        xys = [(radius*cos(2*pi*ii/number), radius*sin(2*pi*ii/number)) for ii in range(number)]
        for x, y in xys:
            region += inregion.transformed(pya.Trans(int(x), int(y)))
            region.merge()
        region += inregion
        region.merge()
    region &= outregion 

    fregion = pya.Region()

    for polygon in region.each():
        
        pts=list(polygon.each_point_hull())
        npts=[]
        for ii,pt in enumerate(pts):
            if ii%2==0 or ii==len(pts)-1:
                npts.append(pt)
                continue
            if pt.distance(pts[ii+1])>10000 or pt.distance(pts[ii-1])>10000:
                npts.append(pt)
                continue
        fregion.insert(pya.Polygon(npts))
        # xx=[]
        # yy=[]
        # for pt in polygon.to_simple_polygon().each_point():
        #     xx.append(str(pt.x))
        #     yy.append(str(pt.y))
        # pushln('xx_=['+','.join(xx)+'];')
        # pushln('yy_=['+','.join(yy)+'];')
        # pushln(vname+'{end+1}={xx_,yy_};')


    BasicPainter.Draw(cell, layer, fregion)



convfunc(cell,layer,layerList,distanceList,numberList,box)

# %%输出
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#

