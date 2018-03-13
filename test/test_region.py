# -*- coding: utf-8 -*-
#测试pcell
import pya

layout = pya.Layout()
cell1 = layout.create_cell("Cell")
layer1 = layout.layer(1, 1)


#Polygon
#DPolygon要先转成Polygon
pts=[pya.Point(0,0),pya.Point(50000,0),pya.Point(50000,50000),pya.Point(40000,60000),pya.Point(0,50000)]
polygon1=pya.Polygon(pts)
pts2=[pya.Point(20000,0),pya.Point(60000,0),pya.Point(60000,50000),pya.Point(50000,60000),pya.Point(20000,50000)]
polygon2=pya.Polygon(pts2)

region1=pya.Region([polygon1,polygon2])
region2=pya.Region([polygon1])
#region1.merge()

cell1.shapes(layer1).insert(region1-region2)

import time
strtime=time.strftime("%Y%m%d_%H%M%S")
print (strtime)

layout.write("[pythonout%s].gds"%strtime)

print (time.strftime("%H:%M:%S"))
#