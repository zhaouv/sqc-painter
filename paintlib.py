# -*- coding: utf-8 -*-
#KLayout 0.24.8
#python 3.4
import pya
from math import *
import time

class BasicPainter:
    '''用于画基础图形的静态类'''
    @staticmethod
    def rectangle(pointr,pointl,length):
        '''
        给定矩形的右下pointr左下pointl画出指定长度矩形
        pointr,pointl,pointl2,pointr2        
        x1,y1,x2,y2,length,path
        '''
        delta=pointr.distance(pointl)
        xx=length/delta*(pointl.y-pointr.y)
        yy=length/delta*(pointr.x-pointl.x)
        pointl2=pya.DPoint(pointl.x+xx,pointl.y+yy)
        pointr2=pya.DPoint(pointr.x+xx,pointr.y+yy)
        rectangle1=pya.DPolygon([pointr,pointl,pointl2,pointr2])
        return rectangle1,pointr2,pointl2
    @staticmethod
    def arc(point0,r,n,angle0,angle1):
        angles=[angle0+1.0*x/(n-1)*(angle1-angle0) for x in range(n)]
        arcpointlist=[pya.DPoint(point0.x+r*cos(angle*pi/180),point0.y+r*sin(angle*pi/180)) for angle in angles]           
        return arcpointlist
    @staticmethod
    def thickarc(point0,rr,rl,n,angle0,angle1):
        thickarcpointlist=[]
        thickarcpointlist.extend(BasicPainter.arc(point0,rr,n,angle0,angle1))
        thickarcpointlist.extend(BasicPainter.arc(point0,rl,n,angle1,angle0))
        thickarc1=pya.DPolygon(thickarcpointlist)
        return thickarc1,thickarcpointlist[n-1],thickarcpointlist[n]
    @staticmethod
    def NewtonInterpolation(X,Y,high):
        n=len(X)
        a=[Y[0]]
        d=[]
        for j in range(n-1):
            d2=d
            if j==0:
                d2=Y
            d=[]
            for k in range(n-1-j):
                if X[k+j+1]==X[k]:
                    d.append(high.pop(0))
                else:
                    d.append((d2[k+1]-d2[k])/(X[k+j+1]-X[k]))
            a.append(d[0])
        def f(x):
            y=a[0]
            Df=1.0
            for j in range(1,n):
                Df*=(x-X[j-1])
                y+=a[j]*Df
            return y
        return f    
    @staticmethod
    def arc_NewtonInterpolation(n,r1):#(n,r1,r2):
        #
        thetax=0.53977
        thetay=-thetax*tan(pi/180*67.5)
        X=[-1,-1,-1,-thetax,0,thetax,1,1,1]
        Y=[-1,-1,-1,thetay,-sqrt(2),thetay,-1,-1,-1]
        high=[-1,-1,1,1,   0,0]
        #
#        theta=-1.34
#        X=[-1,-1,-1, 0   , 1, 1, 1]
#        Y=[-1,-1,-1,theta,-1,-1,-1]
#        high=[-1,-1,1,1,    0,0]
        #
        f=BasicPainter.NewtonInterpolation(X,Y,high)
        pts1=[pya.DPoint((-1.0+2.0/(n-1)*i)/sqrt(2)*r1,f(-1.0+2.0/(n-1)*i)/sqrt(2)*r1) for i in range(n)]
        return pts1
    @staticmethod
    def Border(leng=3050000,siz=3050000,wed=50000):
        polygons=[]        
        pts=[pya.Point(-siz,-siz),pya.Point(-siz+leng,-siz),pya.Point(-siz+leng,-siz+wed)]
        pts.extend([pya.Point(-siz+wed,-siz+wed),pya.Point(-siz+wed,-siz+leng),pya.Point(-siz,-siz+leng)])
        polygon1=pya.Polygon(pts)
        polygons.append(polygon1)
        polygons.append(polygon1.transformed(pya.Trans(pya.Trans.R90)))
        polygons.append(polygon1.transformed(pya.Trans(pya.Trans.R180)))
        polygons.append(polygon1.transformed(pya.Trans(pya.Trans.R270)))
        return pya.Region(polygons)
    @staticmethod
    def Electrode(*args,**keys):
        if 'brush' in keys or isinstance(args[0],CavityBrush):
            return BasicPainter.Electrode_2(*args,**keys)
        elif 'angle' in keys or (type(args[0]) in [int,float]):
            return BasicPainter.Electrode_1(*args,**keys)
        else:
            raise TypeError('Invalid input')
        return []
    @staticmethod
    def Electrode_1(x,y,angle,widout=20000,widin=10000,wid=368000,length=360000,midwid=200000,midlength=200000,narrowlength=120000):
        tr=pya.DCplxTrans(1,angle,False,x,y)
        pts=[]
        pts.append(pya.DPoint(0,widout/2))
        pts.append(pya.DPoint(0,widin/2))
        pts.append(pya.DPoint(narrowlength,midwid/2))
        pts.append(pya.DPoint(narrowlength+midlength,midwid/2))
        pts.append(pya.DPoint(narrowlength+midlength,-midwid/2))
        pts.append(pya.DPoint(narrowlength,-midwid/2))
        pts.append(pya.DPoint(0,-widin/2))
        pts.append(pya.DPoint(0,-widout/2))
        pts.append(pya.DPoint(narrowlength,-wid/2))
        pts.append(pya.DPoint(length,-wid/2))
        pts.append(pya.DPoint(length,wid/2))
        pts.append(pya.DPoint(narrowlength,wid/2))
        polygon1=pya.DPolygon(pts).transformed(tr)
        return polygon1
    @staticmethod
    def Electrode_2(brush,wid=368000,length=360000,midwid=200000,midlength=200000,narrowlength=120000):
        widout=brush.widout
        widin=brush.widin
        tr=brush.DCplxTrans
        pts=[]
        pts.append(pya.DPoint(0,widout/2))
        pts.append(pya.DPoint(0,widin/2))
        pts.append(pya.DPoint(narrowlength,midwid/2))
        pts.append(pya.DPoint(narrowlength+midlength,midwid/2))
        pts.append(pya.DPoint(narrowlength+midlength,-midwid/2))
        pts.append(pya.DPoint(narrowlength,-midwid/2))
        pts.append(pya.DPoint(0,-widin/2))
        pts.append(pya.DPoint(0,-widout/2))
        pts.append(pya.DPoint(narrowlength,-wid/2))
        pts.append(pya.DPoint(length,-wid/2))
        pts.append(pya.DPoint(length,wid/2))
        pts.append(pya.DPoint(narrowlength,wid/2))
        polygon1=pya.DPolygon(pts).transformed(tr)
        return polygon1
    @staticmethod
    def Connection(x,y=0,angle=0,mod=48):
        if isinstance(x,CavityBrush):
            brush=x
            tr=brush.DCplxTrans
            mod=brush.widout
        else:
            tr=pya.DCplxTrans(1,angle,False,x,y)
        pts=[]
        if mod==48:
            pts.append(pya.DPoint(0,-57000))
            pts.append(pya.DPoint(0,-8000))
            pts.append(pya.DPoint(16000,-8000))
            pts.append(pya.DPoint(16000,-52000))
            pts.append(pya.DPoint(62000,-52000))
            pts.append(pya.DPoint(62000,-32000))
            pts.append(pya.DPoint(32000,-32000))
            pts.append(pya.DPoint(32000,32000))
            pts.append(pya.DPoint(62000,32000))
            pts.append(pya.DPoint(62000,52000))
            pts.append(pya.DPoint(16000,52000))
            pts.append(pya.DPoint(16000,8000))
            pts.append(pya.DPoint(0,8000))
            pts.append(pya.DPoint(0,57000))
            pts.append(pya.DPoint(67000,57000))
            pts.append(pya.DPoint(67000,27000))
            pts.append(pya.DPoint(37000,27000))
            pts.append(pya.DPoint(37000,-27000))
            pts.append(pya.DPoint(67000,-27000))
            pts.append(pya.DPoint(67000,-57000))
        if mod==8:
            pts.append(pya.DPoint(0,-57000))
            pts.append(pya.DPoint(0,-2010))
            pts.append(pya.DPoint(224,-2007))
            pts.append(pya.DPoint(2000,-2000))
            pts.append(pya.DPoint(2000,-52000))
            pts.append(pya.DPoint(60000,-52000))
            pts.append(pya.DPoint(60000,-32000))
            pts.append(pya.DPoint(6000,-32000))
            pts.append(pya.DPoint(6000,32000))
            pts.append(pya.DPoint(60000,32000))
            pts.append(pya.DPoint(60000,52000))
            pts.append(pya.DPoint(2000,52000))
            pts.append(pya.DPoint(2000,2000))
            pts.append(pya.DPoint(0,2000))
            pts.append(pya.DPoint(0,57000))
            pts.append(pya.DPoint(65000,57000))
            pts.append(pya.DPoint(65000,27000))
            pts.append(pya.DPoint(11000,27000))
            pts.append(pya.DPoint(11000,-27000))
            pts.append(pya.DPoint(65000,-27000))
            pts.append(pya.DPoint(65000,-57000))
        polygon1=pya.DPolygon(pts).transformed(tr)
        return polygon1
    @staticmethod
    def Draw(cell,layer,x):
        if isinstance(x,pya.DPolygon):
            cell.shapes(layer).insert(pya.Polygon.from_dpoly(x))
        else:
            cell.shapes(layer).insert(x)
#paintlib.BasicPainter.Draw(cell,layer,x)
        
class Painter(object):
    pass
    
class LinePainter(Painter):
    def __init__(self,pointl=pya.DPoint(0,1000),pointr=pya.DPoint(0,0)):
        '''沿着前进方向，右边pointr，左边pointl'''
        self.outputlist=[]        
        self.pointr=pointr
        self.pointl=pointl
        self.Turning=self.TurningArc
        #pointdistance=IO.pointdistance
        self.centerlinepts=[]
    def Setpoint(self,pointl=pya.DPoint(0,1000),pointr=pya.DPoint(0,0)):       
        self.pointr=pointr
        self.pointl=pointl
        self.centerlinepts=[]
        self.outputlist=[]
    def Straight(self,length):
        n=int(ceil(length/IO.pointdistance))+2
        p1x=self.pointr.x/2+self.pointl.x/2
        p1y=self.pointr.y/2+self.pointl.y/2
        #接下来两行是画矩形，其它行是画中心线
        rectangle1,self.pointr,self.pointl=BasicPainter.rectangle(self.pointr,self.pointl,length)
        self.outputlist.append(rectangle1)
        dx=self.pointr.x/2+self.pointl.x/2-p1x
        dy=self.pointr.y/2+self.pointl.y/2-p1y
        cpts=[pya.DPoint(p1x+1.0*pt/(n-1)*dx,p1y+1.0*pt/(n-1)*dy) for pt in range(n)]
        if self.centerlinepts==[]:
            self.centerlinepts=cpts
        else:
            self.centerlinepts.extend(cpts[1:])
        return length
    def TurningArc(self,radius,angle=90):
        '''radius非负向右，负是向左'''
        if angle<0:
            angle=-angle
            radius=-radius
        delta=self.pointr.distance(self.pointl)
        dx=(self.pointr.x-self.pointl.x)/delta
        dy=(self.pointr.y-self.pointl.y)/delta
        dtheta=atan2(dy,dx)*180/pi
        centerx=self.pointr.x+(radius-delta/2)*dx
        centery=self.pointr.y+(radius-delta/2)*dy
        center=pya.DPoint(centerx,centery)
        n=int(ceil((abs(radius)+delta/2)*angle*pi/180/IO.pointdistance)+2)      
        if radius>=0:
            thickarc1,pointr2,pointl2=BasicPainter.thickarc(center,radius-delta/2,radius+delta/2,n,dtheta+180,dtheta+180-angle)
            cpts=BasicPainter.arc(center,radius,n,dtheta+180,dtheta+180-angle)
        else:
            thickarc1,pointr2,pointl2=BasicPainter.thickarc(center,-radius+delta/2,-radius-delta/2,n,dtheta,dtheta+angle)
            cpts=BasicPainter.arc(center,-radius,n,dtheta,dtheta+angle)
        self.outputlist.append(thickarc1)
        self.pointr=pointr2
        self.pointl=pointl2
        if self.centerlinepts==[]:
            self.centerlinepts=cpts
        else:
            self.centerlinepts.extend(cpts[1:])
        return pi*angle/180*abs(radius)
    def TurningInterpolation(self,radius,angle=90):#有待改进
        '''radius非负向右，负是向左'''
        pass
        if angle<0:
            angle=-angle
            radius=-radius
        angle=90
        delta=self.pointr.distance(self.pointl)
        dx=(self.pointr.x-self.pointl.x)/delta
        dy=(self.pointr.y-self.pointl.y)/delta
        dtheta=atan2(dy,dx)*180/pi
        centerx=self.pointr.x+(radius-delta/2)*dx
        centery=self.pointr.y+(radius-delta/2)*dy        
        n=int(ceil(1.3*(abs(radius)+delta/2)*angle*pi/180/IO.pointdistance)+2)
        #
        rsgn=(radius>0)-(radius<0)
        pointr2=pya.DPoint(centerx-rsgn*(radius-delta/2)*dy,centery+rsgn*(radius-delta/2)*dx)
        pointl2=pya.DPoint(centerx-rsgn*(radius+delta/2)*dy,centery+rsgn*(radius+delta/2)*dx)
        pts1=BasicPainter.arc_NewtonInterpolation(n,abs(radius)+delta/2)
        pts2=BasicPainter.arc_NewtonInterpolation(n,abs(radius)-delta/2)
        pts1.extend(reversed(pts2))
        arc1=pya.DPolygon(pts1)
        trans=pya.DCplxTrans(1,180+dtheta+45*rsgn,False,centerx,centery)
        arc1.transform(trans)
        self.outputlist.append(arc1)
        self.pointr=pointr2
        self.pointl=pointl2
        pts3=BasicPainter.arc_NewtonInterpolation(n,abs(radius))        
        cpts=[pya.DEdge(pya.DPoint(),pt).transformed(trans).p2 for pt in pts3]
        if abs(cpts[-1].distance(self.pointr)-delta/2)<IO.pointdistance:
            if self.centerlinepts==[]:
                self.centerlinepts=cpts
            else:
                self.centerlinepts.extend(cpts[1:])
        else:
            if self.centerlinepts==[]:
                self.centerlinepts=cpts[::-1]
            else:
                self.centerlinepts.extend(cpts[-2::-1])
        return pi*0.5*abs(radius) 
    def Draw(self,cell,layer):
        for x in self.outputlist:
            if isinstance(x,pya.DPolygon):
                cell.shapes(layer).insert(pya.Polygon.from_dpoly(x))
            else:
                cell.shapes(layer).insert(x)
        self.outputlist=[]
    def Output_Region(self):
        polygons=[]
        for x in self.outputlist:
            if isinstance(x,pya.DPolygon):
                polygons.append(pya.Polygon.from_dpoly(x))
        self.outputlist=[]
        return pya.Region(polygons)
    def Getcenterline(self):
        cpts=self.centerlinepts
        self.centerlinepts=[]
        return cpts
        
class CavityBrush(object):
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
        return int(round(self.edgeout.distance_abs(self.edgein.p1)/10))*10
    @property
    def centerx(self):
        return (self.edgeout.p2.x+self.edgeout.p1.x)/2
    @property
    def centery(self):
        return (self.edgeout.p2.y+self.edgeout.p1.y)/2
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

class CavityPainter(Painter):
    def __init__(self,*args,**keys):
        if 'pointc' in keys or (isinstance(args[0],pya.DPoint) and ('angle' in keys or type(args[1]) in [int,float])):
            self.constructors1(*args,**keys)
        elif 'brush' in keys or isinstance(args[0],CavityBrush):
            self.constructors2(*args,**keys)
        else:
            raise TypeError('Invalid input')
    def constructors1(self,pointc=pya.DPoint(0,8000),angle=0,widout=20000,widin=10000,bgn_ext=0,end_ext=0):
        self.__init__(CavityBrush(pointc,angle,widout,widin,bgn_ext),end_ext)
    def constructors2(self,brush,end_ext=0):
        self.regionlistout=[]
        self.regionlistin=[]
        self.path=lambda painter:None
        self.bgn_ext=brush.bgn_ext
        self.end_ext=end_ext
        edgeout=brush.edgeout
        edgein=brush.edgein
        self.painterout=LinePainter(edgeout.p1,edgeout.p2)
        self.painterin=LinePainter(edgein.p1,edgein.p2)
        self.centerlineinfos=[]
    @property
    def brush(self):
        return CavityBrush(self.painterout.pointl,self.painterin.pointl,self.painterin.pointr,self.painterout.pointr)
    def Getinfo(self):
        # return [centerx,centery,angle,widout]
        return self.brush.Getinfo()
    def Run(self,path=None):
        if path==None:
            path=self.path
        self.painterout.Straight(self.bgn_ext)
        result=path(self.painterout)
        self.painterout.Straight(self.end_ext)
        self.regionlistout.extend(self.painterout.outputlist)
        self.painterout.outputlist=[]
        self.bgn_ext=0
        self.end_ext=0
        #1,-1修复最后可能留下1nm线的bug
        self.painterin.Straight(-1)
        self.painterin.Straight(1)
        path(self.painterin)
        self.painterin.Straight(1)
        self.painterin.Straight(-1)
        self.regionlistin.extend(self.painterin.outputlist)
        self.painterin.outputlist=[]
        #把中心线的(点列表,宽度)成组添加
        self.centerlineinfos.append((self.painterin.Getcenterline(),self.brush.angle))
        return result
    def Electrode(self,wid=368000,length=360000,midwid=200000,midlength=200000,narrowlength=120000,reverse=False):
        assert(self.end_ext==0)
        brush=self.brush.reversed() if reverse else self.brush
        polygon=BasicPainter.Electrode(brush,wid=wid,length=length,midwid=midwid,midlength=midlength,narrowlength=narrowlength)
        self.regionlistout.append(polygon)
    def Narrow(self,widout,widin,length=6000):
        assert(self.end_ext==0)
        tr=self.brush.DCplxTrans
        edgeout=pya.DEdge(length,widout/2,length,-widout/2).transformed(tr)
        edgein=pya.DEdge(length,widin/2,length,-widin/2).transformed(tr)
        self.regionlistout.append(pya.DPolygon([self.painterout.pointl,self.painterout.pointr,edgeout.p2,edgeout.p1]))
        self.regionlistin.append(pya.DPolygon([self.painterin.pointl,self.painterin.pointr,edgein.p2,edgein.p1]))
        self.painterout.Setpoint(edgeout.p1,edgeout.p2)
        self.painterin.Setpoint(edgein.p1,edgein.p2)        
        return length   
    def InterdigitedCapacitor(self,number,arg1=85000,arg2=45000,arg3=31000,arg4=4000,arg5=3000,arg6=3000,arg7=2000):
        '''
        number must be odd
        http://www.rfwireless-world.com/calculators/interdigital-capacitor-calculator.html
        '''
        assert(self.end_ext==0)
        if number%2!=1:raise RuntimeError('number must be odd')
        oldbrush=self.brush
        tr=oldbrush.DCplxTrans
        newwidin=arg5*2+(arg4+arg7)*number+arg7
        newwidout=newwidin+arg3*2
        outPolygon=pya.DPolygon([
            pya.DPoint(arg2,newwidout/2),pya.DPoint(arg2,-newwidout/2),
            pya.DPoint(arg2+arg1,-newwidout/2),pya.DPoint(arg2+arg1,newwidout/2)
            ]).transformed(tr)
        inPolygons=[]
        xx=arg1-arg6
        yy=arg4
        ly=arg4+arg7
        for ii in range(1+number>>1):
            dx=0 if ii%2==0 else arg6
            inPolygons.append(pya.DPolygon([
                pya.DPoint(arg2+dx,yy/2+ii*ly),pya.DPoint(arg2+dx,-yy/2+ii*ly),
                pya.DPoint(arg2+dx+xx,-yy/2+ii*ly),pya.DPoint(arg2+dx+xx,yy/2+ii*ly)
                ]).transformed(tr))
            if ii==0:continue
            inPolygons.append(pya.DPolygon([
                pya.DPoint(arg2+dx,yy/2-ii*ly),pya.DPoint(arg2+dx,-yy/2-ii*ly),
                pya.DPoint(arg2+dx+xx,-yy/2-ii*ly),pya.DPoint(arg2+dx+xx,yy/2-ii*ly)
                ]).transformed(tr))
        self.Narrow(newwidout,newwidin,arg2)
        self.regionlistout.append(outPolygon)
        self.regionlistin.extend(inPolygons)
        self.Run(lambda painter:painter.Straight(arg1))
        self.centerlineinfos.pop()
        self.regionlistout.pop()
        self.regionlistin.pop()
        self.Narrow(oldbrush.widout,oldbrush.widin,arg2)
    def Output_Region(self):
        polygonsout=[]
        for x in self.regionlistout:
            if isinstance(x,pya.DPolygon):
                polygonsout.append(pya.Polygon.from_dpoly(x))
        self.regionlistout=[]
        polygonsin=[]
        for x in self.regionlistin:
            if isinstance(x,pya.DPolygon):
                polygonsin.append(pya.Polygon.from_dpoly(x))
        self.regionlistin=[]
        return pya.Region(polygonsout)-pya.Region(polygonsin)
    def Draw(self,cell,layer):
        cell.shapes(layer).insert(self.Output_Region())
    def Getcenterlineinfo(self):
        #中心线的(点列表,宽度)成组添加
        cptinfos=self.centerlineinfos
        self.centerlineinfos=[]
        return cptinfos
        
class PcellPainter(Painter):
    def __init__(self):
        self.outputlist=[]
        self.Basic = pya.Library.library_by_name("Basic")
        self.TEXT_decl = self.Basic.layout().pcell_declaration("TEXT")
    def DrawText(self,cell,layer1,textstr,DCplxTrans1):
        '''
        左下角坐标,每个字宽0.6*倍数高0.7*倍数线宽0.1*倍数  
        tr=pya.DCplxTrans(10,0,False,0,0)
        倍数,逆时针度数,是否绕x翻转,平移x,平移y
        '''
        tr=pya.CplxTrans.from_dtrans(DCplxTrans1)
        textstr="%s"%(textstr)
        param = { 
            "text": textstr, 
            "layer": layer1, 
            "mag": 1 
        }
        pv = []
        for p in self.TEXT_decl.get_parameters():
            if p.name in param:
                pv.append(param[p.name])
            else:
                pv.append(p.default)
        text_cell = IO.layout.create_cell("TEXT(\"%s\")"%(textstr))
        self.TEXT_decl.produce(IO.layout, [ layer1 ], pv, text_cell)        
        cell.insert(pya.CellInstArray(text_cell.cell_index(), tr))
        edge1=pya.DEdge(len(textstr)*0.6,0,len(textstr)*0.6,0.7).transformed(DCplxTrans1)
        return [edge1.p1,edge1.p2]
    
class TransfilePainter(Painter):
    def __init__(self,filename="[insert].gds"):
        self.outputlist=[]
        self.filename=filename
        layout=pya.Layout()
        layout.read(filename)
        names=[i.name for i in layout.top_cells()]
        if(len(names)!=1):raise RuntimeError('insert file must have only one top cell')
        if(names[0]=='TOP'):raise RuntimeError("the name of insert file's cell can not be TOP")
        self.insertcellname=names[0]
        self.airbridgedistance=100000
    def DrawAirbridge(self,cell,centerlinelist,newcellname="Airbige"):
        IO.layout.read(self.filename)
        for icell in IO.layout.top_cells():
            if (icell.name == self.insertcellname):
                icell.name=newcellname
                for cpts in centerlinelist:
                    distance=0
                    if not hasattr(self.airbridgedistance,'__call__'):
                        distance=self.airbridgedistance*0.25
                    dt_int=0
                    for i,pt in enumerate(cpts[1:-1],1):
                        distance=distance+pt.distance(cpts[i-1])
                        if hasattr(self.airbridgedistance,'__call__'):
                            calt_int=self.airbridgedistance(distance)
                        else:
                            calt_int=distance//self.airbridgedistance
                        if calt_int !=dt_int:
                            dx=cpts[i+1].x-cpts[i-1].x
                            dy=cpts[i+1].y-cpts[i-1].y
                            tr=pya.CplxTrans(1,atan2(dy,dx)/pi*180,False,pt.x,pt.y)
                            new_instance=pya.CellInstArray(icell.cell_index(),tr)
                            cell.insert(new_instance)
                            dt_int=dt_int+1
        for icell in IO.layout.top_cells():
            if (icell.name == self.insertcellname):
                icell.flatten(True)
                icell.delete()
    def DrawMark(self,cell,pts,newcellname="Mark"):
        IO.layout.read(self.filename)
        for i in IO.layout.top_cells():
            if (i.name == self.insertcellname):
                i.name=newcellname
                for pt in pts:
                    tr=pya.Trans(pt.x,pt.y)
                    new_instance=pya.CellInstArray(i.cell_index(),tr)
                    cell.insert(new_instance)
        for i in IO.layout.top_cells():
            if (i.name == self.insertcellname):
                i.flatten(True)
                i.delete()
    def DrawGds(self,cell,newcellname,DCplxTrans1):
        '''
        tr=pya.DCplxTrans(1,0,False,0,0)
        倍数,逆时针度数,是否绕x翻转,平移x,平移y
        '''
        tr=pya.CplxTrans.from_dtrans(DCplxTrans1)
        resultcell=None
        IO.layout.read(self.filename)
        for i in IO.layout.top_cells():
            if (i.name == self.insertcellname):
                i.name=newcellname
                resultcell=i
                new_instance=pya.CellInstArray(i.cell_index(),tr)
                cell.insert(new_instance)
        for i in IO.layout.top_cells():
            if (i.name == self.insertcellname):
                i.flatten(True)
                i.delete()
        return resultcell        

class Collision(object):
    '''处理图形冲突的类'''
    pointRadius=1000
    def __init__(self):
        self.region=pya.Region()
    def insert(self,polygon):
        if isinstance(polygon,list):
            for x in polygon:
                if isinstance(x,pya.DPolygon):
                    self.region.insert(pya.Polygon.from_dpoly(x))
            return self
        if isinstance(polygon,pya.DPolygon):
            self.region.insert(pya.Polygon.from_dpoly(polygon))
            return self
        if isinstance(polygon,pya.Region):
            self.region=self.region+polygon
            return self
        raise TypeError('Invalid input')
    def conflict(self,other):
        if isinstance(other,Collision):
            return self.region.interacting(other.region)
        if isinstance(other,pya.DPoint):
            region=pya.Region(pya.DPolygon(BasicPainter.arc(other,self.pointRadius,8,0,360)))
            return self.region.interacting(region)
        raise TypeError('Invalid input')

class TBD:
    '''处理待定数值的静态类'''
    id='not init'
    filename='TBD.txt'
    values=[]
    index=0
    inf=999999
    eps=0.01
    @staticmethod
    def init(id,_str=None):
        if _str==None:
            TBD.id=str(id)
            try:
                with open(TBD.filename) as fid:
                    ss=fid.read()
            except FileNotFoundError as ee:
                with open(TBD.filename,'w') as fid:
                    ss=TBD.id
                    fid.write(ss)
            lines=ss.split('\n')
            if TBD.id != lines[0]:lines=[TBD.id]
        if _str!=None:
            def _set(value,index=-1):
                pass
            TBD.set=_set
            ss=_str
            lines=ss.split('\n')
            lines[0]='not file'
        TBD.id=lines[0]
        TBD.values=[[float(value) for value in line.split(',')] for line in lines[1:]]
        return TBD
    @staticmethod
    def get(index=None):
        if index==None:
            TBD.index+=1
            index=-1
        _index=TBD.index+index if index < 0 else index
        whileBool = len(TBD.values[_index:_index+1])==0
        while whileBool:
            TBD.values.append([0,TBD.inf])
            whileBool = len(TBD.values[_index:_index+1])==0
        return TBD.values[_index][0]
    @staticmethod
    def set(value,index=-1):
        _index=TBD.index+index if index < 0 else index
        TBD.values[_index][1]=value
        TBD.values[_index][0]+=value
        if(value < -TBD.eps):print('Warning : minus value in TBD number '+str(_index))
        return value
    @staticmethod
    def isFinish():
        if TBD.id == 'not init':raise RuntimeError('TBD not init')
        finish=True
        for ii in TBD.values:
            if abs(ii[1]) > TBD.eps:
                finish=False
                break
        if TBD.id == 'not file':return finish
        with open(TBD.filename,'w') as fid:
            ss=TBD.id+'\n'+'\n'.join([','.join([str(jj) for jj in ii]) for ii in TBD.values])
            print('TBD :\n'+ss+'\nTBD END')
            fid.write(ss)
        return finish

class IO:
    '''处理输入输出的静态类'''
    #IO:字母 In Out
    layout=None
    main_window=None
    layout_view=None
    top=None
    pointdistance=2000
    @staticmethod
    def Start(mod="guiopen"):
        if mod=="gds":
            IO.layout=pya.Layout()            
        elif mod=="guinew":
            IO.main_window = pya.Application.instance().main_window()
            IO.layout = IO.main_window.create_layout(1).layout()
            IO.layout_view = IO.main_window.current_view()
            IO.layout_view.rename_cellview("pythonout",0)            
        elif mod=="guiopen":
            IO.main_window = pya.Application.instance().main_window()
            IO.layout_view = IO.main_window.current_view()
            try:
                IO.layout=IO.layout_view.cellview(IO.layout_view.active_cellview_index()).layout()
            except AttributeError as e:
                IO.layout,IO.top=IO.Start("guinew")
        if len(IO.layout.top_cells())>0:
            IO.top=IO.layout.top_cells()[0]
        else:
            IO.top = IO.layout.create_cell("TOP")
        return IO.layout,IO.top    
        ##layout = main_window.load_layout(string filename,int mode)
    @staticmethod
    def Show():
        if IO.layout_view:
            IO.layout_view.select_cell(IO.top.cell_index(), 0)
            IO.layout_view.add_missing_layers()
            IO.layout_view.zoom_fit()
            strtime=time.strftime("%Y%m%d_%H%M%S")
            print(strtime)
    @staticmethod
    def Write(filename=None):
        if filename==None:
            print("[pythonout%s].gds"%(time.strftime("%Y%m%d_%H%M%S")))
            filename="[pythonout%s].gds"%(time.strftime("%Y%m%d_%H%M%S"))
        IO.layout.write(filename)

#v =pya.MessageBox.warning("Dialog Title", "Something happened. Continue?", pya.MessageBox.Yes + pya.MessageBox.No)

#try:
#    b+=1
#except NameError as e:
#    b=0
    
'''
# -*- coding: utf-8 -*-

#初始化
import pya
import paintlib
from imp import reload
reload(paintlib)
layout,top = paintlib.IO.Start("guiopen")#在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001#设置单位长度为1nm
paintlib.IO.pointdistance=2000#设置腔的精度,转弯处相邻两点的距离
TBD=paintlib.TBD.init(6876587)

#画腔
painter3=paintlib.CavityPainter(pya.DPoint(0,24000),angle=180,widout=48000,widin=16000,bgn_ext=48000,end_ext=16000)
#painter3.painterin.Turning=painter3.painterin.TurningInterpolation
#painter3.painterout.Turning=painter3.painterout.TurningInterpolation
def path(painter):#设置内轮廓路径
    painter.Turning(40000)
    painter.Straight(50000)
    painter.Turning(40000)
    for i in range(7):
        painter.Straight(500000)#1
        painter.Turning(-40000)
        painter.Turning(-40000)
        painter.Straight(500000)#2
        painter.Turning(40000)
        painter.Turning(40000)
    painter.Straight(28500)
painter3.Run(path)

layer1 = layout.layer(10, 10)#创建新层
cell2 = layout.create_cell("Cavity1")#创建一个子cell
top.insert(pya.CellInstArray(cell2.cell_index(),pya.Trans()))
painter3.Draw(cell2,layer1)#把画好的腔置入
    #画Crossover
centerlinelist=[]#画腔的中心线并根据中心线画Crossover
centerlinelist.append(painter3.Getcenterlineinfo()[0][0])
painter4=paintlib.TransfilePainter("[Crossover48].gds")
painter4.airbridgedistance=100000#设置Crossover的间距
painter4.DrawAirbridge(top,centerlinelist,"Crossover1")

#画电极传输线
cell3 = layout.create_cell("TR1")#创建一个子cell
top.insert(pya.CellInstArray(cell3.cell_index(),pya.Trans()))
polygon1=paintlib.BasicPainter.Electrode(-600000,24000,angle=0,widout=20000,widin=10000,wid=368000,length=360000,midwid=200000,midlength=200000,narrowlength=120000)
paintlib.BasicPainter.Draw(cell3,layer1,polygon1)
painter5=paintlib.CavityPainter(pya.DPoint(-600000,24000),angle=180,widout=20000,widin=10000,bgn_ext=0,end_ext=0)
def path(painter):
    length=0
    length+=painter.Straight(100000)
    length+=painter.Turning(50000)
    length+=painter.Straight(20000)
    return length
painter5.Run(path)
painter5.InterdigitedCapacitor(9)
dy=TBD.get()
dx=TBD.get()
def path(painter):
    length=0
    length+=painter.Straight(200000+dy)
    length+=painter.Turning(50000)
    length+=painter.Straight(dx)
    return length
painter5.Run(path)
painter5.Narrow(8000,4000,6000)
painter5.end_ext=2000
painter5.Run(lambda painter:painter.Straight(50000))
TBD.set(-500000-painter5.brush.centerx)
TBD.set(600000-painter5.brush.centery,-2)
painter5.Draw(cell3,layer1)

#画边界
layer2 = layout.layer(1, 1)
border=paintlib.BasicPainter.Border(leng=3050000,siz=3050000,wed=50000)
paintlib.BasicPainter.Draw(top,layer2,border)

#画文字
painter2=paintlib.PcellPainter()
painter2.DrawText(top,layer2,"Python",pya.DCplxTrans(100,15,False,1000000,0))

#画Mark
painter1=paintlib.TransfilePainter("[Mark3inch_jiguangzhixie].gds")
pts=[pya.Point(1000000,500000),pya.Point(-500000,-500000),pya.Point(1000000,-1000000)]
painter1.DrawMark(top,pts,"Mark_laserwrite")

#
painter6=paintlib.TransfilePainter("[Xmon_20170112].gds")
tr=pya.DCplxTrans(1,-90,False,400000,-400000)
painter6.DrawGds(top,"Qubit",tr)

#输出
print(TBD.isFinish())
paintlib.IO.Show()#输出到屏幕上
paintlib.IO.Write()#输出到文件中
#
'''
