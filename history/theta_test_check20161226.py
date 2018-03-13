# -*- coding: utf-8 -*-
# create a new view (mode 1) with an empty layout
import paintlib
layout = pya.Layout()



layout.dbu = 0.001
cell = layout.create_cell("Cell")
child_cell1 = layout.create_cell("Theta1")
child_cell2 = layout.create_cell("Theta2")
child_cell3 = layout.create_cell("TEXT")
x=1000000
y=1000000
cell.insert(pya.CellInstArray(child_cell1.cell_index(),pya.Trans(-x,-y)))
cell.insert(pya.CellInstArray(child_cell2.cell_index(),pya.CplxTrans(1,0.00,False,-x,-y)))
cell.insert(pya.CellInstArray(child_cell3.cell_index(),pya.Trans(-x,-y)))

layer1 = layout.layer(10, 10)

paintertext=paintlib.ObjectPainter(layout)
list1=list([0.01*i for i in range(-5,6)])
painter1=paintlib.TransfilePainter(layout)
painter1.filename="[taoke_theta1_test].gds"
painter2=paintlib.TransfilePainter(layout)
painter2.filename="[taoke_theta2_test].gds"
#tr=pya.DCplxTrans(1,0,False,0,0)
#倍数,逆时针度数,是否绕x翻转,平移x,平移y
for i,theta in enumerate(list1):
    dx=25000000
    dy=25000000
    paintertext.DrawText(child_cell3,layer1,theta,pya.DCplxTrans(10,0,False,x+dx+255000,y+dy+i*40000))
    painter1.DrawGds(child_cell1,"theta1_%02d"%(i),pya.DCplxTrans(1,0,False,x+dx,y+dy+i*40000))
    painter2.DrawGds(child_cell2,"theta2_%02d"%(i),pya.DCplxTrans(1,theta,False,x+dx,y+dy+i*40000))
    paintertext.DrawText(child_cell3,layer1,theta,pya.DCplxTrans(10,0,False,x-dx+255000,y-dy+i*40000))
    painter1.DrawGds(child_cell1,"theta1_%02d"%(i),pya.DCplxTrans(1,0,False,x-dx,y-dy+i*40000))
    painter2.DrawGds(child_cell2,"theta2_%02d"%(i),pya.DCplxTrans(1,theta,False,x-dx,y-dy+i*40000))
    



#cell.shapes(layer1).insert(pya.Polygon.from_dpoly(pya.DPolygon(pts)))
layout.write(paintlib.IOsettings.Getfilename())#"[pythonout].gds"

#