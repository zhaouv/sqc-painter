# -*- coding: utf-8 -*-
#
import history.paintlib20161222 as paintlib
layout = pya.Layout()
cell = layout.create_cell("Cell")

layer1 = layout.layer(11, 11)

def cavity1(painter):
    painter.Turning(50000)
    painter.Straight(50000)
    painter.Turning(50000)
    for i in range(7):
        painter.Straight(500000)#1
        painter.Turning(-50000)
        painter.Turning(-50000)
        painter.Straight(500000)#2
        painter.Turning(50000)
        painter.Turning(50000)
    
painter3=paintlib.CavityPainter(pya.DPoint(-2238000,252000),pya.DPoint(-2238000,204000))
painter3.pointdistance=500
painter3.Straight(48000)
cavity1(painter3)
painter3.Straight(44500)

region1=painter3.Output_Region()

painter4=paintlib.CavityPainter(pya.DPoint(-2286000,236000),pya.DPoint(-2286000,220000))
painter4.pointdistance=500
cavity1(painter4)
painter4.Straight(28500)

region2=painter4.Output_Region()

painter4.outputlist.append(region1-region2)
painter4.Output(cell,layer1)



#cell.shapes(layer1).insert(pya.Polygon.from_dpoly(pya.DPolygon(pts)))
layout.write(paintlib.IOsettings.Getfilename())#"[pythonout].gds"

#