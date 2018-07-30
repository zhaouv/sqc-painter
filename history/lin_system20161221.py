# -*- coding: utf-8 -*-
#
import history.paintlib20161221 as paintlib
layout = pya.Layout()
cell = layout.create_cell("Cell")

layer1 = layout.layer(10, 10)
painter3=paintlib.CavityPainter(pya.DPoint(0,0),pya.DPoint(0,4000))
painter3.Straight(1000000)
painter3.Turning(-400000)
painter3.Turning(-400000)
painter3.Straight(1000000)
painter3.Turning(400000)
painter3.Turning(400000)

painter3.pointr=pya.DPoint(0,8000)
painter3.pointl=pya.DPoint(0,12000)
painter3.Straight(1000000)
painter3.TurningInterpolation(-400000+8000)
painter3.TurningInterpolation(-400000+8000)
painter3.Straight(1000000)
painter3.TurningInterpolation(400000+8000)
painter3.TurningInterpolation(400000+8000)

painter3.Output(cell,layer1)



def guize(strin):
    strout=[]
    for i in strin:
        if i=='X':
            strout.extend(['-','Y','F','+','X','F','X','+','F','Y','-'])
        elif i=='Y':
            strout.extend(['+','X','F','-','Y','F','Y','-','F','X','+'])
        else:
            strout.append(i)
    return strout
str1=guize(['X'])
str2=guize(str1)
str3=guize(str2)
str4=guize(str3)
str5=guize(str4)
str6=guize(str5)
str7=guize(str6)
str8=guize(str7)




r=pya.DPoint(-2000,0)
l=pya.DPoint(-2000,4000)
painter1=paintlib.CavityPainter(r,l)
painter1.pointdistance=50
for i in str3:
    if i=='F':
        painter1.Straight(12000)
    if i=='-':
        painter1.TurningInterpolation(-6000)
    if i=='+':
        painter1.Turning(6000)


painter1.Output(cell,layer1)

layer2 = layout.layer(1, 1)
painter2=paintlib.ObjectPainter()
painter2.DrawBorder(4000,250000,250000)


painter2.Output(cell,layer2)
layout.write(paintlib.IOsettings.Getfilename())


#