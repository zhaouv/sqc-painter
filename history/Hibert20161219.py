# -*- coding: utf-8 -*-


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



import history.paintlib20161219 as paintlib
r=pya.DPoint(-2000,0)
l=pya.DPoint(-2000,4000)
painter1=paintlib.CavityPainter(r,l)
painter1.Straight(4000)
painter1.Straight(-2000)
painter1.outputlist.pop()
for i in str6:
    if i=='F':
        painter1.Straight(14000)
        painter1.Straight(-2000)
        painter1.outputlist.pop()
    if i=='-':
        painter1.Straight(-2000)
        painter1.outputlist.pop()
        painter1.Turning(-2000)
        painter1.outputlist.pop()
        painter1.Straight(-2000)
        painter1.outputlist.pop()
    if i=='+':
        painter1.Straight(-2000)
        painter1.outputlist.pop()
        painter1.Turning(2000)
        painter1.outputlist.pop()
        painter1.Straight(-2000)
        painter1.outputlist.pop()

layout = pya.Layout()
top = layout.create_cell("TOP")
l1 = layout.layer(1, 0)
painter1.Output(top,l1)

layout.write(paintlib.IOsettings.Getfilename())

