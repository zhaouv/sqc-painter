# -*- coding: utf-8 -*-
#测试pcell
import pya

layout = pya.Layout()
cell = layout.create_cell("Cell")
child_cell = layout.create_cell("Child_Cell")

cell.insert(pya.CellInstArray(child_cell.cell_index(),pya.Trans()))
cell.insert(pya.CellInstArray(child_cell.cell_index(),pya.CplxTrans(1,0,False,100000,100000)))

layer1 = layout.layer(10, 10)

pts=[pya.Point(0,0),pya.Point(50000,0),pya.Point(50000,50000),pya.Point(40000,60000),pya.Point(0,50000)]
polygon1=pya.Polygon(pts)
pts2=[pya.Point(20000,0),pya.Point(60000,0),pya.Point(60000,50000),pya.Point(50000,60000),pya.Point(20000,50000)]
polygon2=pya.Polygon(pts2)



cell.shapes(layer1).insert(polygon1)
child_cell.shapes(layer1).insert(polygon2)
#cell.flatten(True)
import time
strtime=time.strftime("%Y%m%d_%H%M%S")
print (strtime)

layout.write("[pythonout%s].gds"%strtime)

print (time.strftime("%H:%M:%S"))
#