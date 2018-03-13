# -*- coding: utf-8 -*-
#KLayout 0.24.8
#python 3.4
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
        thetax=0.53977;
        thetay=-thetax*tan(pi/180*67.5)
        X=[-1,-1,-1,-thetax,0,thetax,1,1,1]
        Y=[-1,-1,-1,thetay,-sqrt(2),thetay,-1,-1,-1]
        high=[-1,-1,1,1,   0,0]
        f=BasicPainter.NewtonInterpolation(X,Y,high)
        pts1=[pya.DPoint((-1.0+2.0/(n-1)*i)/sqrt(2)*r1,f(-1.0+2.0/(n-1)*i)/sqrt(2)*r1) for i in range(n)]
        return pts1
    @staticmethod
    def DrawBorder(leng=3050000,siz=3050000,wed=50000):
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
    def DrawElectrode():
        pts=[]
        pts.append(pya.DPoint(-501000,-225000))
        pts.append(pya.DPoint(-621000,-8000))
        pts.append(pya.DPoint(-625000,-8000))
        pts.append(pya.DPoint(-625000,-4000))
        pts.append(pya.DPoint(-621000,-4000))
        pts.append(pya.DPoint(-501000,-125000))
        pts.append(pya.DPoint(-251000,-125000))
        pts.append(pya.DPoint(-251000,125000))
        pts.append(pya.DPoint(-501000,125000))
        pts.append(pya.DPoint(-621000,4000))
        pts.append(pya.DPoint(-625000,4000))
        pts.append(pya.DPoint(-625000,8000))
        pts.append(pya.DPoint(-621000,8000))
        pts.append(pya.DPoint(-501000,225000))
        pts.append(pya.DPoint(-186000,225000))
        pts.append(pya.DPoint(-186000,5000))
        pts.append(pya.DPoint(0,5000))
        pts.append(pya.DPoint(0,-5000))
        pts.append(pya.DPoint(-186000,-5000))
        pts.append(pya.DPoint(-186000,-225000))
        return pya.DPolygon(pts),[pya.DPoint(-625000,8000),pya.DPoint(-625000,4000),pya.DPoint(-625000,-4000),pya.DPoint(-625000,-8000)]
    @staticmethod
    def Output(cell,layer,x):
        if isinstance(x,pya.DPolygon):
            cell.shapes(layer).insert(pya.Polygon.from_dpoly(x))
        else:
            cell.shapes(layer).insert(x)
        
class Painter(object):
    def __init__(self):
        self.outputlist=[]
    def Output(self,cell,layer):
        for x in self.outputlist:
            if isinstance(x,pya.DPolygon):
                cell.shapes(layer).insert(pya.Polygon.from_dpoly(x))
            else:
                cell.shapes(layer).insert(x)
        self.outputlist=[]
#cell.shapes(layer1).insert(pya.Polygon.from_dpoly(pya.DPolygon(pts)))

class CavityPainter(Painter):
    def __init__(self,pointr=pya.DPoint(0,1000),pointl=pya.DPoint(0,0)):
        self.outputlist=[]        
        self.pointr=pointr
        self.pointl=pointl
        self.Turning=self.TurningArc
        self.pointdistance=500
        self.centerlinepts=[]
        #沿着前进方向，右边pointr，左边pointl
    def Setpoint(self,pointr=pya.DPoint(0,1000),pointl=pya.DPoint(0,0)):       
        self.pointr=pointr
        self.pointl=pointl
        self.centerlinepts=[]
    def Straight(self,length):
        n=int(ceil(length/self.pointdistance))+2
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
    def TurningArc(self,radius,angle=90):
        #radius非负向右，负是向左
        delta=self.pointr.distance(self.pointl)
        dx=(self.pointr.x-self.pointl.x)/delta
        dy=(self.pointr.y-self.pointl.y)/delta
        dtheta=atan2(dy,dx)*180/pi
        centerx=self.pointr.x+(radius-delta/2)*dx
        centery=self.pointr.y+(radius-delta/2)*dy
        center=pya.DPoint(centerx,centery)
        n=int(ceil((abs(radius)+delta/2)*angle*pi/180/self.pointdistance)+2)      
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
    def TurningInterpolation(self,radius):
        #radius非负向右，负是向左
        angle=90
        delta=self.pointr.distance(self.pointl)
        dx=(self.pointr.x-self.pointl.x)/delta
        dy=(self.pointr.y-self.pointl.y)/delta
        dtheta=atan2(dy,dx)*180/pi
        centerx=self.pointr.x+(radius-delta/2)*dx
        centery=self.pointr.y+(radius-delta/2)*dy        
        n=int(ceil(1.3*(abs(radius)+delta/2)*angle*pi/180/self.pointdistance)+2)
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
        if abs(cpts[-1].distance(self.pointr)-delta/2)<self.pointdistance:
            if self.centerlinepts==[]:
                self.centerlinepts=cpts
            else:
                self.centerlinepts.extend(cpts[1:])
        else:
            if self.centerlinepts==[]:
                self.centerlinepts=cpts[::-1]
            else:
                self.centerlinepts.extend(cpts[-2::-1])
        
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

class ObjectPainter(Painter):
    def __init__(self,layout):
        self.outputlist=[]
        self.layout=layout
        self.Basic = pya.Library.library_by_name("Basic")
        self.TEXT_decl = self.Basic.layout().pcell_declaration("TEXT");
    def DrawText(self,cell,layer1,textstr,DCplxTrans1):
        #左下角坐标,每个字宽0.6*倍数高0.7*倍数线宽0.1*倍数  
        #tr=pya.DCplxTrans(10,0,False,0,0)
        #倍数,逆时针度数,是否绕x翻转,平移x,平移y
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
        text_cell = self.layout.create_cell("TEXT(\"%s\")"%(textstr))
        self.TEXT_decl.produce(self.layout, [ layer1 ], pv, text_cell)        
        cell.insert(pya.CellInstArray(text_cell.cell_index(), tr))
        edge1=pya.DEdge(len(textstr)*0.6,0,len(textstr)*0.6,0.7).transformed(DCplxTrans1)
        return [edge1.p1,edge1.p2]
    
class TransfilePainter(Painter):
    def __init__(self,layout,filename="[insert].gds",insertcellname="insert"):
        self.outputlist=[]
        self.layout=layout
        self.filename=filename
        self.insertcellname=insertcellname
        self.airbrigedistance=100000
    def DrawAirbrige(self,cell,centerlinelist,newcellname="Airbige"):
        #CavityPainter生成的centerline未测试
        for cpts in centerlinelist:
            self.layout.read(self.filename)#每个腔用一个不同的cell装airbrige原型
            for icell in self.layout.top_cells():
                if (icell.name == self.insertcellname):
                    icell.name=newcellname
                    distance=0
                    dt_int=0
                    for i,pt in enumerate(cpts[1:-1],1):
                        distance=distance+pt.distance(cpts[i-1])
                        if distance//self.airbrigedistance !=dt_int:
                            dx=cpts[i+1].x-cpts[i-1].x
                            dy=cpts[i+1].y-cpts[i-1].y
                            tr=pya.CplxTrans(1,atan2(dy,dx)/pi*180,False,pt.x,pt.y)
                            new_instance=pya.CellInstArray(icell.cell_index(),tr)
                            cell.insert(new_instance)
                            dt_int=dt_int+1
    def DrawMark(self,cell,pts,newcellname="Mark"):
        self.layout.read(self.filename)
        for i in self.layout.top_cells():
            if (i.name == self.insertcellname):
                i.name=newcellname
                for pt in pts:
                    tr=pya.Trans(pt.x,pt.y)
                    new_instance=pya.CellInstArray(i.cell_index(),tr)
                    cell.insert(new_instance)
    def DrawGds(self,cell,newcellname,DCplxTrans1):
        #tr=pya.DCplxTrans(1,0,False,0,0)
        #倍数,逆时针度数,是否绕x翻转,平移x,平移y
        tr=pya.CplxTrans.from_dtrans(DCplxTrans1)
        self.layout.read(self.filename)
        for i in self.layout.top_cells():
            if (i.name == self.insertcellname):
                i.name=newcellname
                new_instance=pya.CellInstArray(i.cell_index(),tr)
                cell.insert(new_instance)

class IO:#处理输入输出的静态类
    #IO:字母 In Out
    layout=None
    main_window=None
    layout_view=None
    cell=None
    @staticmethod
    def Start(mod="gds"):
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
                IO.layout,IO.cell=IO.Start("guinew")
        IO.cell=IO.layout.top_cell()
        if IO.cell==None:
            IO.cell = IO.layout.create_cell("Cell")
        return IO.layout,IO.cell    
        ##layout = main_window.load_layout(string filename,int mode)
    @staticmethod
    def Show(cell):
        if IO.layout_view:
            IO.layout_view.select_cell(cell.cell_index(), 0)
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


'''
# -*- coding: utf-8 -*-
#
import paintlib
layout,cell = paintlib.IO.Start("guiopen")

layout.dbu = 0.001

cell2 = layout.create_cell("Cavity1")
cell.insert(pya.CellInstArray(cell2.cell_index(),pya.Trans()))



layer1 = layout.layer(10, 10)
painter3=paintlib.CavityPainter(pya.DPoint(0,0),pya.DPoint(0,16000))
painter3.pointdistance=500
painter3.Turning=painter3.TurningInterpolation
painter3.Straight(1000000)
painter3.Turning(-400000)
painter3.Turning(-400000)
painter3.Straight(1000000)
painter3.Turning(400000)
painter3.Turning(400000)

region1=painter3.Output_Region()

painter3.Setpoint(pya.DPoint(0,4000),pya.DPoint(0,12000))

painter3.Straight(1000000)
painter3.Turning(-400000)
painter3.Turning(-400000)
painter3.Straight(1000000)
painter3.Turning(400000)
painter3.Turning(400000)

region2=painter3.Output_Region()
paintlib.BasicPainter.Output(cell2,layer1,region1-region2)


centerlinelist=[]
centerlinelist.append(painter3.Getcenterline())
painter4=paintlib.TransfilePainter(layout,"[Airbrige].gds","insert")
painter4.DrawAirbrige(cell,centerlinelist,"Airbige1")


layer2 = layout.layer(1, 1)
border=paintlib.BasicPainter.DrawBorder()
paintlib.BasicPainter.Output(cell,layer2,border)

painter3.outputlist.append(border)
painter3.Output(cell,layer2)



painter2=paintlib.ObjectPainter(layout)
painter2.DrawText(cell,layer2,"TEXT1",pya.DCplxTrans(100,45,False,-1000,-1000))
painter2.Output(cell,layer2)


painter1=paintlib.TransfilePainter(layout,"[Mark3inch_jiguangzhixie].gds","Markinsert")
pts=[pya.Point(500000,500000),pya.Point(-500000,-500000),pya.Point(1000000,-1000000)]
painter1.DrawMark(cell,pts,"Mark_laserwrite")


#cell.shapes(layer1).insert(pya.Polygon.from_dpoly(pya.DPolygon(pts)))
paintlib.IO.Show(cell)
paintlib.IO.Write()
#
'''
