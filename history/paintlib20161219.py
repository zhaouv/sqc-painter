# -*- coding: utf-8 -*-
#
import pya
from math import *
import time

class BasicPainter:#用于画基础图形的静态类
    @staticmethod
    def rectangle(pointr,pointl,length):
        #给定矩形的右下pointr左下pointl画出指定长度矩形
        #pointr,pointl,pointl2,pointr2        
        #x1,y1,x2,y2,length,path
        delta=pointr.distance(pointl)
        xx=length/delta*(pointl.y-pointr.y)
        yy=length/delta*(pointr.x-pointl.x)
        pointl2=pya.DPoint(pointl.x+xx,pointl.y+yy)
        pointr2=pya.DPoint(pointr.x+xx,pointr.y+yy)
        rectangle1=pya.DPolygon([pointr,pointl,pointl2,pointr2])
        return rectangle1,pointr2,pointl2
    @staticmethod
    def arc(point0,r,n,angle0,angle1):
        arcpointlist=[]
        angles=[angle0+1.0*x/(n-1)*(angle1-angle0) for x in range(n)]
        for angle in angles:
            arcpointlist.append(pya.DPoint(point0.x+r*cos(angle*pi/180),point0.y+r*sin(angle*pi/180)))            
        return arcpointlist        
        #lambda x:x*x
        #map(fxx,[1,2,3,4])
    @staticmethod
    def thickarc(point0,rr,rl,n,angle0,angle1):
        thickarcpointlist=[]
        thickarcpointlist.extend(arc(point0,rr,n,angle0,angle1))
        thickarcpointlist.extend(arc(point0,rl,n,angle1,angle0))
        thickarc1=pya.DPolygon(thickarcpointlist)
        return thickarc1,thickarcpointlist(n-1),thickarcpointlist(n)
    @staticmethod
    def arc_NewtonInterpolation():
        pass

class CavityPainter(object):
    def __init__(self,pointr,pointl):
        self.outputlist=[];        
        self.pointr=pointr
        self.pointl=pointl
        #沿着前进方向，右边pointr，左边pointl
    def Straight(self,length):
        rectangle1,self.pointr,self.pointl=BasicPainter.rectangle(self.pointr,self.pointl,length)
        self.outputlist.append(rectangle1)
    def Turning(self,radius,angle=90):
        #radius正是向右，负是向左,不能为0
        delta=self.pointr.distance(self.pointl)
        dx=(self.pointr.x-self.pointl.x)/delta
        dy=(self.pointr.y-self.pointl.y)/delta
        centerx=self.pointr.x+(radius-delta/2)*dx
        centery=self.pointr.y+(radius-delta/2)*dy        
        if angle==90:
            #
            rsgn=(radius>0)-(radius<0)
            pointr2=pya.DPoint(centerx-rsgn*(radius-delta/2)*dy,centery+rsgn*(radius-delta/2)*dx)
            pointl2=pya.DPoint(centerx-rsgn*(radius+delta/2)*dy,centery+rsgn*(radius+delta/2)*dx)
            self.outputlist.append(pya.DPolygon([self.pointr,self.pointl,pointl2,pointr2]))
            self.pointr=pointr2
            self.pointl=pointl2
        else:
            pass
    def Output(self,cell,layer):
        for x in self.outputlist:
            cell.shapes(layer).insert(pya.Polygon.from_dpoly(x))

class AirbrigePainter(object):
    def __init__(self,CenterlineList):
        self.CenterlineList=CenterlineList
        pass
    def Func(self):
        pass

class IOsettings:
    @staticmethod
    def Getfilename():
        strtime=time.strftime("%Y%m%d_%H%M%S")
        print(strtime)
        return "[pythonout%s].gds"%strtime



'''
import paintlib
painter1=paintlib.CavityPainter(pya.DPoint(0,0),pya.DPoint(0,4))
painter1.Straight(100)
painter1.Turning(-5)
painter1.Straight(100)
painter1.Turning(5)
layout = pya.Layout()
top = layout.create_cell("TOP")
l1 = layout.layer(1, 0)
painter1.Output(top,l1)
#top.shapes(l1).insert(pya.Polygon.from_dpoly(x))
layout.write(paintlib.IOsettings.Getfilename())#"[pythonout].gds"
'''
