# -*- coding: utf-8 -*-
#KLayout 0.24.8
#python 3.4
import pya
from math import cos,sin,pi,tan,atan2,sqrt,ceil
import re
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
    def Connection(x,widin=16000, widout=114000, linewid=5000, slength1=16000, slength2=16000, clength=30000, cwid=54000,y=0,angle=0):
        if isinstance(x,CavityBrush):
            brush=x
            tr=brush.DCplxTrans
        else:
            tr=pya.DCplxTrans(1,angle,False,x,y)
        pts=[
            pya.DPoint(0,widin/2),
            pya.DPoint(slength1,widin/2),
            pya.DPoint(slength1,widout/2-linewid),
            pya.DPoint(slength1+slength2+clength,widout/2-linewid),
            pya.DPoint(slength1+slength2+clength,cwid/2+linewid),
            pya.DPoint(slength1+slength2,cwid/2+linewid),
            #
            pya.DPoint(slength1+slength2,-(cwid/2+linewid)),
            pya.DPoint(slength1+slength2+clength,-(cwid/2+linewid)),
            pya.DPoint(slength1+slength2+clength,-(widout/2-linewid)),
            pya.DPoint(slength1,-(widout/2-linewid)),
            pya.DPoint(slength1,-widin/2),
            pya.DPoint(0,-widin/2),
            #
            pya.DPoint(0,-widout/2),
            pya.DPoint(slength1+slength2+clength+linewid,-widout/2),
            pya.DPoint(slength1+slength2+clength+linewid,-cwid/2),
            pya.DPoint(slength1+slength2+linewid,-cwid/2),
            #
            pya.DPoint(slength1+slength2+linewid,cwid/2),
            pya.DPoint(slength1+slength2+clength+linewid,cwid/2),
            pya.DPoint(slength1+slength2+clength+linewid,widout/2),
            pya.DPoint(0,widout/2),
        ]
        polygon1=pya.DPolygon(pts).transformed(tr)
        return polygon1
    @staticmethod
    def Draw(cell,layer,x):
        if isinstance(x,pya.DPolygon):
            cell.shapes(layer).insert(pya.Polygon.from_dpoly(x))
        else:
            cell.shapes(layer).insert(x)
#paintlib.BasicPainter.Draw(cell,layer,x)
        
class TraceRunner:
    patternNames=['straight','turning','repeatStart','repeatEnd']

    straight_pattern=re.compile(r'^s_?(-?\d+\.?\d*)')
    turning_pattern=re.compile(r'^(l|r|t)_?(-?\d+\.?\d*)(?:,(-?\d+\.?\d*))?')
    repeatStart_pattern=re.compile(r'^n(\d+)\[')
    repeatEnd_pattern=re.compile(r'^\]')

    straight='straight'
    turning='turning'
    repeatStart='repeatStart'
    repeatEnd='repeatEnd'

    top='top'

    def __init__(self):
        self.Node.tr=self
        self.patterns={}
        for name in self.patternNames:
            self.patterns[name]=self.__getattribute__(name+'_pattern')

    def run(self,rawString):
        AST=self.buildAST(rawString)
        pathString=self.traversalAST(AST)
        localscope={'path':None}
        exec(pathString,None,localscope)
        self.pathFunction=localscope['path']
        return self.pathFunction

    def buildAST(self,rawString):
        self.rawString=rawString
        self.string=self.preConvert(rawString)
        self.start=0
        self.AST=self.Node(isTop=True,type=self.top)
        self.currentNode=self.AST
        self.parse()
        if self.currentNode.type!=self.top:
            raise RuntimeError('barket not match')
        return self.AST
    def preConvert(self,rawString):
        string=re.sub(r'\s','',rawString)
        return string

    class Node:
        def __init__(self,isTop=False,parentNode=None,**k):
            self.children=[]
            self.isTop=isTop
            if parentNode==None and not isTop:
                parentNode=self.tr.currentNode
            self.parentNode=parentNode
            if parentNode:
                parentNode.addChild(self)
            for key,value in k.items():
                self.__setattr__(key,value)
        def addChild(self,node):
            self.children.append(node)
        def getChildren(self):
            return self.children

    def parse(self):
        match=None
        patternName=''
        currentString=self.string[self.start:]
        if not currentString:return
        for name in self.patternNames:
            match=self.patterns[name].match(currentString)
            if match:
                patternName=name
                break
        if match==None:
            raise RuntimeError('invaild trace at '+currentString)
        if patternName==self.repeatStart:
            times=int(match.group(1))
            node=self.Node(match=match,type=patternName,times=times)
            self.currentNode=node
        if patternName==self.repeatEnd:
            self.currentNode=self.currentNode.parentNode
            if self.currentNode==None:
                raise RuntimeError('barket not match at '+currentString)
            node=self.Node(match=match,type=patternName)
        if patternName==self.straight:
            length=float(match.group(1))
            enableMinus='_' in match.group(0)
            node=self.Node(match=match,type=patternName,length=length,enableMinus=enableMinus)
        if patternName==self.turning:
            left=-1 if match.group(1)=='l' else 1
            radius=float(match.group(2))
            angle=match.group(3)
            angle=90.0 if angle==None else float(angle)
            enableMinus='_' in match.group(0)
            node=self.Node(match=match,type=patternName,left=left,radius=radius,angle=angle,enableMinus=enableMinus)
        self.start+=len(match.group(0))
        self.parse()
            
    def traversalAST(self,AST):
        output=[]
        prefix=['']
        def pushln(s):
            output.append(prefix[0]+s+'\n')
        def cpre(n=4):
            if n>0:
                prefix[0]=prefix[0]+' '*n
            if n<0:
                prefix[0]=prefix[0][0:-1*n]
        def npre():
            return len(prefix[0])
        pushln('def path(painter):')
        cpre()
        pushln('length=0')
        def traversal(node):
            if node.type==self.top:
                for cn in node.getChildren():
                    traversal(cn)
            if node.type==self.straight:
                pushln('length+=painter.{minus}Straight({length})'.format(minus='_'if node.enableMinus else '',length=node.length))
            if node.type==self.turning:
                pushln('length+=painter.Turning({radius},{angle})'.format(radius=node.left*node.radius,angle=node.angle))
            if node.type==self.repeatStart:
                pushln('for _index{n} in range({times}):'.format(n=npre(),times=node.times))
                cpre()
                for cn in node.getChildren():
                    traversal(cn)
            if node.type==self.repeatEnd:
                cpre(-4)
                
        traversal(AST)
        pushln('return length')
        self.pathString=''.join(output)
        return self.pathString

class Painter(object):
    pass
    
class LinePainter(Painter):
    def __init__(self,pointl=pya.DPoint(0,1000),pointr=pya.DPoint(0,0)):
        '''沿着前进方向，右边pointr，左边pointl'''
        self.outputlist=[]        
        self.pointr=pointr
        self.pointl=pointl
        #pointdistance=IO.pointdistance
        self.centerlinepts=[]
        self.warning=True
    def Setpoint(self,pointl=pya.DPoint(0,1000),pointr=pya.DPoint(0,0)):       
        self.pointr=pointr
        self.pointl=pointl
        self.centerlinepts=[]
        self.outputlist=[]
    def Straight(self,length):
        if length<-10 and self.warning and IO.warning:raise RuntimeError('Straight negative value')
        return self._Straight(length)
    def Turning(self,radius,angle=90):
        if (angle<-361 or angle>361) and self.warning and IO.warning:raise RuntimeError('Turning angle more than 360 degree')
        return self.TurningArc(radius,angle)
    def _Straight(self,length):
        n=int(ceil(length/IO.pointdistance))+2
        if n==1:n=2
        p1x=self.pointr.x/2+self.pointl.x/2
        p1y=self.pointr.y/2+self.pointl.y/2
        #接下来是画矩形，再之后是画中心线
        #修复1nm线的bug
        rectangle1,_,_=BasicPainter.rectangle(self.pointr,self.pointl,length+(length>0)-(length<0))
        _,self.pointr,self.pointl=BasicPainter.rectangle(self.pointr,self.pointl,length)
        self.outputlist.append(rectangle1)
        #
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
        #修复1nm线的bug
        self._Straight(2)
        self._Straight(-2)
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

class CavityPainter(Painter):
    tr=TraceRunner()
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
            pathFunction=self.path
        elif hasattr(path,'__call__'):
            pathFunction=path
        else: # type(path)==str
            pathFunction=self.tr.run(path)
        self.painterout.Straight(self.bgn_ext)
        pathFunction(self.painterout)
        self.painterout.Straight(self.end_ext)
        self.painterout._Straight(-self.end_ext)
        self.regionlistout.extend(self.painterout.outputlist)
        self.painterout.outputlist=[]
        self.bgn_ext=0
        self.end_ext=0
        #修复1nm线的bug
        self.painterin._Straight(-3)
        self.painterin._Straight(3)
        result=pathFunction(self.painterin)
        self.painterin._Straight(3)
        self.painterin._Straight(-3)
        self.regionlistin.extend(self.painterin.outputlist)
        self.painterin.outputlist=[]
        #把中心线的(点列表,笔刷)成组添加
        self.centerlineinfos.append((self.painterin.Getcenterline(),self.brush))
        return result
    def Electrode(self,wid=368000,length=360000,midwid=200000,midlength=200000,narrowlength=120000,reverse=False):
        assert((reverse==False and self.end_ext==0) or (reverse==True and self.bgn_ext==0))
        brush=self.brush.reversed() if reverse else self.brush
        polygon=BasicPainter.Electrode(brush,wid=wid,length=length,midwid=midwid,midlength=midlength,narrowlength=narrowlength)
        self.regionlistout.append(polygon)
    def Connection(self,clength=30000,cwid=54000,widout=114000,linewid=5000,slength1=16000,slength2=16000,reverse=False):
        assert((reverse==False and self.end_ext==0) or (reverse==True and self.bgn_ext==0))
        brush=self.brush.reversed() if reverse else self.brush
        polygon=BasicPainter.Connection(brush,widin=brush.widin, widout=widout, linewid=linewid, slength1=slength1, slength2=slength2, clength=clength, cwid=cwid)
        self.regionlistout.append(polygon)
    def Narrow(self,widout,widin,length=6000):
        assert(self.end_ext==0 and self.bgn_ext==0)
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
        assert(self.end_ext==0 and self.bgn_ext==0)
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
        self.Narrow(newwidout,newwidin,arg1)
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
        self.region=pya.Region(polygonsout)-pya.Region(polygonsin)
        return self.region
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
                for cpts,brush in centerlinelist:
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

class TBD(object):
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
            except FileNotFoundError as _:
                with open(TBD.filename,'w') as fid:
                    ss=TBD.id
                    fid.write(ss)
            lines=[ln for ln in ss.split('\n') if len(ln.strip())>1 and ln.strip()[0] in '-.0123456789']
            if TBD.id != lines[0]:lines=[TBD.id]
        if _str!=None:
            def _set(value,index=-1):
                pass
            TBD.set=_set
            ss=_str
            lines=[ln for ln in ss.split('\n') if len(ln.strip())>1 and ln.strip()[0] in '-.0123456789']
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

class Interactive:
    '''处理交互的类'''
    deltaangle=45
    maxlength=1073741824
    turningr=50000
    indent='    '
    brushlist=[]
    searchr=500000

    @staticmethod
    def show(brush):
        Interactive.brushlist.append(brush)
        polygon=BasicPainter.Electrode(brush.reversed())
        BasicPainter.Draw(IO.link,IO.layer,polygon)
        return brush
    
    @staticmethod
    def _show_path(brush,pathstr):
        l={'path':None}
        exec(pathstr,None,l)
        painter=CavityPainter(brush)
        painter.Run(l['path'])
        painter.Draw(IO.link,IO.layer)

    @staticmethod
    def _get_nearest_brush(x,y):
        bestbrush=None
        bestr=Interactive.searchr
        pt=pya.DPoint(x,y)
        for brush in Interactive.brushlist:
            r=brush.edgein.p1.distance(pt)
            if r<bestr:
                bestr=r
                bestbrush=brush
        return bestbrush

    @staticmethod
    def _pts_path_selected():
        for obj in IO.layout_view.each_object_selected():
            #只检查第一个选中的对象
            shape=obj.shape
            if not shape.is_path():break
            spts=list(shape.path.each_point())
            return spts
        pya.MessageBox.warning("paintlib.Interactive.link", "Please select a Path", pya.MessageBox.Ok)
        return False

    @staticmethod
    def _generatepath(pts,das):
        turningr=Interactive.turningr
        indent=Interactive.indent
        output=['def path(painter):','length=0']
        last=0
        for ii,da in enumerate(das):
            sda=(da>0)-(da<0)
            da*=sda
            dl=turningr*tan(da/180*pi/2)
            ll=pts[ii].distance(pts[ii+1])-last-dl
            last=dl
            if(ll<0):
                pya.MessageBox.warning("paintlib.Interactive.link", "Error : Straight less than 0", pya.MessageBox.Ok)
                return
            output.append('length+=painter.Straight({length})'.format(length=ll))
            output.append('length+=painter.Turning({radius},{angle})'.format(radius=sda*turningr,angle=da))
        output.append('length+=painter.Straight({length})'.format(length=pts[-1].distance(pts[-2])-last))
        output.append('return length')
        return ('\n'+indent).join(output)
    
    @staticmethod
    def link(brush1=None,brush2=None):
        '''
        输入两个CavityBrush作为参数, 并点击图中的一个路径, 生成一个连接两个brush的路径的函数  
        缺省时会在Interactive.searchr内搜索最近的brush
        第二个brush可为None, 此时取path的终点作为路径终点
        '''
        deltaangle=Interactive.deltaangle
        maxlength=Interactive.maxlength

        spts=Interactive._pts_path_selected()
        if spts==False:return
        if brush1==None:brush1=Interactive._get_nearest_brush(spts[0].x,spts[0].y)
        if brush2==None:brush2=Interactive._get_nearest_brush(spts[-1].x,spts[-1].y)

        if not isinstance(brush1,CavityBrush):
            pya.MessageBox.warning("paintlib.Interactive.link", "Argument 1 must be CavityBrush", pya.MessageBox.Ok)
            return
        if not isinstance(brush2,CavityBrush) and brush2!=None:
            pya.MessageBox.warning("paintlib.Interactive.link", "Argument 2 must be CavityBrush or None", pya.MessageBox.Ok)
            return
        angles=[brush1.angle]
        pts=[pya.DPoint(brush1.centerx,brush1.centery)]
        edges=[pya.DEdge(pts[0].x,pts[0].y,pts[0].x+maxlength*cos(angles[0]/180*pi),pts[0].y+maxlength*sin(angles[0]/180*pi))]
        das=[]
        lastpt=None

        for ii in range(1,len(spts)):
            pt=spts[ii]
            pt0=spts[ii-1]
            angle0=angles[-1]
            edge0=edges[-1]
            angle=atan2(pt.y-pt0.y,pt.x-pt0.x)/pi*180
            angle=round(angle/deltaangle)*deltaangle
            angle=0 if angle==360.0 else angle
            if(angle==angle0):continue
            da=-((angle+3600-angle0)%360)
            if(da==-180):
                pya.MessageBox.warning("paintlib.Interactive.link", "Error : Turn 180 degrees", pya.MessageBox.Ok)
                return
            if(da<-180):da=360+da
            lastpt=[pt.x,pt.y]
            angles.append(angle)
            edge=pya.DEdge(pt.x+maxlength*cos(angle/180*pi),pt.y+maxlength*sin(angle/180*pi),pt.x-maxlength*cos(angle/180*pi),pt.y-maxlength*sin(angle/180*pi))
            das.append(da)
            if not edge.crossed_by(edge0):
                print('point ',ii)
                print(angle)
                print(angle0)
                pya.MessageBox.warning("paintlib.Interactive.link", "Error : Invalid path leads to no crossing point", pya.MessageBox.Ok)
                return
            pts.append(edge.crossing_point(edge0))
            edges.append(edge)

        if(brush2!=None):
            angle0=angles[-1]
            edge0=edges[-1]
            angle=brush2.angle+180
            pt=pya.DPoint(brush2.centerx,brush2.centery)
            _angle=round(angle/deltaangle)*deltaangle
            _angle=0 if _angle==360.0 else _angle
            if(_angle==angle0):
                angles.pop()
                das.pop()
                pts.pop()
                edges.pop()
                angle0=angles[-1]
                edge0=edges[-1]
            da=-((angle+3600-angle0)%360)
            _da=-((_angle+3600-angle0)%360)
            if(_da==-180):
                pya.MessageBox.warning("paintlib.Interactive.link", "Error : Turn 180 degrees", pya.MessageBox.Ok)
                return
            if(da<-180):da=360+da
            lastpt=[pt.x,pt.y]
            edge=pya.DEdge(pt.x,pt.y,pt.x-maxlength*cos(angle/180*pi),pt.y-maxlength*sin(angle/180*pi))
            angles.append(angle)
            das.append(da)
            if not edge.crossed_by(edge0):
                print('brush2')
                print(angle)
                print(angle0)
                pya.MessageBox.warning("paintlib.Interactive.link", "Error : Invalid path leads to no crossing point", pya.MessageBox.Ok)
                return
            pts.append(edge.crossing_point(edge0))
            edges.append(edge)
        pts.append(pya.DPoint(lastpt[0],lastpt[1]))
        ss=Interactive._generatepath(pts,das)
        print('##################################')
        print(ss)
        print('##################################')
        Interactive._show_path(brush1,ss)
    
    @staticmethod
    def _box_selected():
        for obj in IO.layout_view.each_object_selected():
            #只检查第一个选中的对象
            shape=obj.shape
            if not shape.is_box():break
            return shape.box
        pya.MessageBox.warning("paintlib.Interactive.cut", "Please select a Box", pya.MessageBox.Ok)
        return False

    @staticmethod
    def _merge_and_draw(outregion,inregion,tr_to=None):
        region=outregion-inregion
        if type(tr_to)==type(None):
            center=outregion.bbox().center()
            region.transform(pya.Trans(-center.x,-center.y))
            tr=pya.Trans(center.x,center.y)
        else:
            tr=tr_to
        cut = IO.layout.create_cell("cut")
        IO.auxiliary.insert(pya.CellInstArray(cut.cell_index(),tr))
        BasicPainter.Draw(cut,IO.layer,region)
        return region,cut

    @staticmethod
    def cut(layerlist=None,layermod='not in',box=None,mergeanddraw=True):
        if layerlist==None:layerlist=[(0,0)]
        if type(box)==type(None):box=Interactive._box_selected()
        if not box:return

        # celllist=[]
        # cells=[]
        # def buildcells(cell):
        #     if cell.name.split('$')[0] in celllist:return
        #     cells.append(cell)
        #     for ii in cell.each_child_cell():
        #         buildcells(layout.cell(ii))
        # buildcells(top)
        # cellnames=[c.name for c in cells]
        cells=[IO.top]

        _layerlist=[]
        for ii in layerlist:
            if type(ii)==str:
                _layerlist.append(IO.layout.find_layer(ii))
            else:
                _layerlist.append(IO.layout.find_layer(ii[0],ii[1]))
        layers=[index for index in IO.layout.layer_indices() if index in _layerlist] if layermod=='in' else [index for index in IO.layout.layer_indices() if index not in _layerlist]

        outregion=pya.Region(box)
        inregion=pya.Region()

        for cell in cells:
            for layer in layers:
                s=cell.begin_shapes_rec_touching(layer,box)
                inregion.insert(s)

        if not mergeanddraw:
            return outregion,inregion

        return Interactive._merge_and_draw(outregion,inregion)[0]

class IO:
    '''处理输入输出的静态类'''
    #IO:字母 Input Output
    path='/'.join(__file__.replace('\\','/').split('/')[:-1])
    warning=True
    layout=None
    main_window=None
    layout_view=None
    top=None
    auxiliary=None
    link=None
    layer=None
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
            except AttributeError as _:
                IO.layout,IO.top=IO.Start("guinew")
                return IO.layout,IO.top
        if len(IO.layout.top_cells())>0:
            IO.top=IO.layout.top_cells()[0]
        else:
            IO.top = IO.layout.create_cell("TOP")
        #
        IO.auxiliary = IO.layout.create_cell("auxiliary")
        IO.top.insert(pya.CellInstArray(IO.auxiliary.cell_index(),pya.Trans()))
        #
        IO.link = IO.layout.create_cell("link")
        IO.auxiliary.insert(pya.CellInstArray(IO.link.cell_index(),pya.Trans()))
        #
        IO.layer=IO.layout.layer(0, 0)
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
            filename="[pythonout%s].gds"%(time.strftime("%Y%m%d_%H%M%S"))
        print(filename)
        IO.layout.write(filename)

#v =pya.MessageBox.warning("Dialog Title", "Something happened. Continue?", pya.MessageBox.Yes + pya.MessageBox.No)
