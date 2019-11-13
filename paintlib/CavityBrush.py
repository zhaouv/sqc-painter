# -*- coding: utf-8 -*-

import pya
from math import atan2,pi

class CavityBrush(object):
    last=[None,None]
    def __init__(self,*args,**keys):
        if 'pointc' in keys or (isinstance(args[0],pya.DPoint) and ('angle' in keys or type(args[1]) in [int,float])):
            self.constructors1(*args,**keys)
        elif 'edgeout' in keys or isinstance(args[0],pya.DEdge):
            self.constructors2(*args,**keys)
        elif 'pts' in keys or isinstance(args[0],pya.DPoint):
            self.constructors3(*args,**keys)
        elif type(args[0]) in [list,tuple]:
            self.constructors3(*args[0],**keys)
        else:
            raise TypeError('Invalid input')
        if abs(self.edgeout.distance(self.edgein.p1)-self.edgeout.distance(self.edgein.p2))>10:
            raise RuntimeError('not parallel')
        CavityBrush.last.pop()
        CavityBrush.last.insert(0,self)
    def constructors1(self,pointc=pya.DPoint(0,0),angle=0,widout=20000,widin=10000,bgn_ext=0):
        tr=pya.DCplxTrans(1,angle,False,pointc)
        self.edgeout=pya.DEdge(0,widout/2,0,-widout/2).transformed(tr)
        self.edgein=pya.DEdge(bgn_ext,widin/2,bgn_ext,-widin/2).transformed(tr)
    def constructors2(self,edgeout=pya.DEdge(0,20000/2,0,-20000/2),edgein=pya.DEdge(0,0,0,0)):
        self.edgeout=edgeout
        self.edgein=edgein
    def constructors3(self,pointoutl,pointinl,pointinr,pointoutr):
        self.edgeout=pya.DEdge(pointoutl,pointoutr)
        self.edgein=pya.DEdge(pointinl,pointinr)
    def transform(self,tr):
        self.edgeout=self.edgeout.transformed(tr)
        self.edgein=self.edgein.transformed(tr)
        return self
    def transformed(self,tr):
        edgeout=self.edgeout.transformed(tr)
        edgein=self.edgein.transformed(tr)
        newCavityBrush = CavityBrush(edgeout,edgein)
        return newCavityBrush
    def reversed(self):
        pts=[]
        pts.append(self.edgeout.p2)
        pts.append(self.edgein.p2)
        pts.append(self.edgein.p1)
        pts.append(self.edgeout.p1)
        newCavityBrush = CavityBrush(pts)
        return newCavityBrush
    @property
    def bgn_ext(self):
        return int(round(self.edgeout.distance(self.edgein.p1)/10))*10
    @property
    def centerx(self):
        return (self.edgein.p2.x+self.edgein.p1.x)/2
    @property
    def centery(self):
        return (self.edgein.p2.y+self.edgein.p1.y)/2
    @property
    def angle(self):
        return 90+180/pi*atan2(self.edgeout.p2.y-self.edgeout.p1.y,self.edgeout.p2.x-self.edgeout.p1.x)
    @property
    def widout(self):
        return int(round(self.edgeout.length()/10))*10
    def Getinfo(self):
        centerx=self.centerx
        centery=self.centery
        angle=self.angle
        widout=self.widout
        return [centerx,centery,angle,widout]
    @property
    def widin(self):
        return int(round(self.edgein.length()/10))*10
    @property
    def DCplxTrans(self):
        return pya.DCplxTrans(1,self.angle,False,self.centerx,self.centery)
