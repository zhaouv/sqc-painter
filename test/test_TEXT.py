# -*- coding: utf-8 -*-
#测试pcell
import pya

layout = pya.Layout()
cell = layout.create_cell("Cell")
child_cell = layout.create_cell("Child_Cell")

cell.insert(pya.CellInstArray(child_cell.cell_index(),pya.Trans()))

layer1 = layout.layer(10, 10)

lib = pya.Library.library_by_name("Basic")
#if lib == None:
#    raise Exception("Unknown lib 'Basic'")
pcell_decl = lib.layout().pcell_declaration("TEXT");
#if pcell_decl == None:
#    raise Exception("Unknown PCell 'TEXT'")

x=-1000
y=-1000
mag=1
#左下角坐标,每个字宽0.6高0.7
param = { 
    "text": "%02d-%06d" % ( 1, 1 ), 
    "layer": layer1, 
    "mag": mag 
}
pv = []
for p in pcell_decl.get_parameters():
    if p.name in param:
        pv.append(param[p.name])
    else:
        pv.append(p.default)

text_cell = layout.create_cell("1T")
pcell_decl.produce(layout, [ layer1 ], pv, text_cell)

cell.insert(pya.CellInstArray(text_cell.cell_index(), pya.Trans(x,y)))




#pts=[pya.Point(0,0),pya.Point(50000,0),pya.Point(50000,50000),pya.Point(40000,60000),pya.Point(0,50000)]
#polygon1=pya.Polygon(pts)
pts2=[pya.Point(20000,0),pya.Point(60000,0),pya.Point(60000,50000),pya.Point(50000,60000),pya.Point(20000,50000)]
polygon2=pya.Polygon(pts2)



#cell.shapes(layer1).insert(polygon1)
child_cell.shapes(layer1).insert(polygon2)

import time
strtime=time.strftime("%Y%m%d_%H%M%S")
print (strtime)

layout.write("[pythonout%s].gds"%strtime)

print (time.strftime("%H:%M:%S"))
#