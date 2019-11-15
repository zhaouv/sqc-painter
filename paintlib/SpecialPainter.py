# -*- coding: utf-8 -*-

from math import cos,sin,pi,tan,atan2,sqrt,ceil,floor

import pya

from .IO import IO
from .CavityBrush import CavityBrush
from .Painter import Painter
from .BasicPainter import BasicPainter
from .CavityPainter import LinePainter,CavityPainter
from .Collision import Collision
from .Interactive import Interactive

class SpecialPainter(Painter):
    ''' 画一些较复杂图形的静态类 '''
    @staticmethod
    def Connection(x,widin=16000, widout=114000, linewid=5000, slength1=16000, slength2=16000, clength=30000, cwid=54000 ,clengthplus=0, turningRadiusPlus=5000,y=0,angle=0):
        ''' 画腔到比特的连接(更复杂的版本),第一个参数是笔刷或坐标,返回图形 '''
        if isinstance(x,CavityBrush):
            brush=x
            tr=brush.DCplxTrans
        else:
            tr=pya.DCplxTrans(1,angle,False,x,y)
        rp=turningRadiusPlus
        r=turningRadiusPlus+linewid/2
        polygons=[]
        pts=[
            pya.DPoint(0,widin/2),
            pya.DPoint(slength1,widin/2),
            pya.DPoint(slength1,widout/2),
            pya.DPoint(0,widout/2),
        ]
        polygons.append(pya.DPolygon(pts))
        pts=[
            pya.DPoint(0,-widin/2),
            pya.DPoint(slength1,-widin/2),
            pya.DPoint(slength1,-widout/2),
            pya.DPoint(0,-widout/2),
        ]
        polygons.append(pya.DPolygon(pts))
        dx=widout/2-cwid/2-2*linewid
        tangle=90-atan2(clengthplus,dx)*180/pi
        lp=LinePainter(pointl=pya.DPoint(slength1,widout/2),pointr=pya.DPoint(slength1,widout/2-linewid))
        #
        lp.Straight(slength2+clength-rp*tan(tangle/2*pi/180))
        lp.Turning(r,tangle)
        lp.Straight(-rp*tan(tangle/2*pi/180)+dx/sin(tangle*pi/180)-rp/tan(tangle/2*pi/180))
        lp.Turning(r,180-tangle)
        lp.Straight(-rp/tan(tangle/2*pi/180)+clengthplus+clength-linewid)
        #
        lp.Turning(-linewid/2,90)
        lp._Straight(-linewid)
        lp.Straight(linewid+cwid)
        lp.Turning(-linewid/2,90)
        lp._Straight(-linewid)
        lp.Straight(linewid)
        #
        lp.Straight(-rp/tan(tangle/2*pi/180)+clengthplus+clength-linewid)
        lp.Turning(r,180-tangle)
        lp.Straight(-rp*tan(tangle/2*pi/180)+dx/sin(tangle*pi/180)-rp/tan(tangle/2*pi/180))
        lp.Turning(r,tangle)
        lp.Straight(slength2+clength-rp*tan(tangle/2*pi/180))
        #
        polygons.extend(lp.outputlist)

        return [p.transformed(tr) for p in polygons]
    @staticmethod
    def ConnectionOnPainter(self,clength=30000,cwid=54000,widout=114000,linewid=5000,slength1=16000,slength2=16000,clengthplus=0, turningRadiusPlus=5000,reverse=False):
        ''' 画腔到比特的连接(更复杂的版本),第一个参数是painter,直接把图形附在腔上 '''
        assert((reverse==False and self.end_ext==0) or (reverse==True and self.bgn_ext==0))
        brush=self.brush.reversed() if reverse else self.brush
        polygons=SpecialPainter.Connection(brush,widin=brush.widin, widout=widout, linewid=linewid, slength1=slength1, slength2=slength2, clength=clength, cwid=cwid, clengthplus=clengthplus, turningRadiusPlus=turningRadiusPlus)
        self.regionlistout.extend(polygons)
    @staticmethod
    def DrawContinueAirbridgePainter(cell,layerup,layerdown,centerlinelist,s1=300000,s2=300000+8500,e1=5200637-15000,e2=5200637-15000-8500,w1=20000,w2=30000,w3=40000,l1=28000,l2=22000,cnum=9):
        ''' 画连续的airbridge构成的同轴线 '''
        gl={1:l1,2:l2}
        wl={1:w3,2:w1}
        def getp(ll,p1,p2):
            bl=p1.distance(p2)
            dx=p2.x-p1.x
            dy=p2.y-p1.y
            k=1.0*ll/bl
            return pya.DPoint(p1.x+k*dx,p1.y+k*dy)
            
        for cpts,brush in centerlinelist:
            distance=0

            downstartindex=0
            downendindex=0

            status=0 # 1宽 2窄
            slength=s2
            si=0
            ei=0
            sp=None
            ep=None
            polygons=[]

            for i,pt in enumerate(cpts[1:-1],1):
                delda=pt.distance(cpts[i-1])
                distance=distance+delda
                # 画下层
                if not downstartindex and distance>=s1:
                    downstartindex=i
                    downstartp=getp(distance-s1,pt,cpts[i-1])
                if not downendindex and distance>=e1:
                    downendindex=i
                    downendp=getp(distance-e1,pt,cpts[i-1])
                    #
                    temp=[downstartp]
                    temp.extend(cpts[downstartindex:downendindex-1])
                    temp.append(downendp)
                    path=pya.DPath(temp,w2,0,0)
                    polygon=path.polygon()
                    BasicPainter.Draw(cell,layerdown,polygon)
                # 画上层
                if not status and distance>=slength:
                    # 进入阶段
                    status=1
                    si=i
                    sp=getp(distance-slength,pt,cpts[i-1])
                    slength+=gl[status]
                    continue
                if distance>=e2:continue
                if status and distance>=slength:
                    ei=i
                    ep=getp(distance-slength,pt,cpts[i-1])
                    if status==1:
                        temp=[sp]
                        temp.extend(cpts[si:ei-1])
                        temp.append(ep)
                    else:
                        temp=cpts[si-1-cnum:ei+cnum]
                    path=pya.DPath(temp,wl[status],0,0)
                    polygon=path.polygon()
                    polygons.append(polygon)
                    si=ei
                    sp=ep
                    status=3-status
                    slength+=gl[status]

            if not len(polygons)%2:polygons.pop()

            for i,polygon in enumerate(polygons):
                BasicPainter.Draw(cell,layerup,polygon)
    @staticmethod
    def DrawParametricCurve(cell,layer,brush,xfunc,yfunc,pointnumber,startlength,deltalength,number,lengthlist):
        ''' 
        沿参数曲线画空心线, 并每一段间隔变宽一小段  
        返回曲线参数为0和参数为1的两端的笔刷 [brush0,brush1]

        lengthlist=[l1,l2,d1,w1,w2] 描述变宽部分, 其内外长度和间隔, 外内宽度  
        xfunc,yfunc 是曲线参数函数, 参数均匀从取0~1中取pointnumber个, pointnumber尽量取大但是也不要大到让程序变慢  
        
        待改进 todo : 智能选点匹配到 IO.pointdistance
        '''
        def getp(ll,p1,p2):
            bl=p1.distance(p2)
            dx=p2.x-p1.x
            dy=p2.y-p1.y
            k=1.0*ll/bl
            return pya.DPoint(p1.x+k*dx,p1.y+k*dy)
        #
        cpts=[pya.DPoint(xfunc(ii/(pointnumber-1)),yfunc(ii/(pointnumber-1))) for ii in range(pointnumber)]
        # todo : cpts智能选点匹配到 IO.pointdistance
        #
        outpolygons=[]
        inpolygons=[]
        #
        path=pya.DPath(cpts,brush.widout,0,0)
        polygon=path.polygon()
        outpolygons.append(polygon)
        path=pya.DPath(cpts,brush.widin,3,3)
        polygon=path.polygon()
        inpolygons.append(polygon)
        #
        l1=lengthlist[0]
        l2=lengthlist[1]
        d1=lengthlist[2]
        w1=lengthlist[3]
        w2=lengthlist[4]
        #
        finishnumber=0

        distance=0

        startchecklength=startlength

        bigstartindex=0
        bigstartp=None
        smallstartindex=0
        smallstartp=None

        status=0 # 1进入大矩阵 2进入小矩阵 3出小矩阵 0出大矩阵

        for i,pt in enumerate(cpts[1:-1],1):
            delda=pt.distance(cpts[i-1])
            distance=distance+delda
            # 进入大矩阵
            if status==0 and distance>=startchecklength:
                status=1
                bigstartindex=i
                bigstartp=getp(distance-startchecklength,pt,cpts[i-1])
            # 进入小矩阵
            if status==1 and distance>=startchecklength+d1:
                status=2
                smallstartindex=i
                smallstartp=getp(distance-startchecklength-d1,pt,cpts[i-1])
            # 出小矩阵
            if status==2 and distance>=startchecklength+d1+l2:
                status=3
                smallendindex=i
                ep=getp(distance-startchecklength-d1-l2,pt,cpts[i-1])
                temp=[smallstartp]
                temp.extend(cpts[smallstartindex:smallendindex-1])
                temp.append(ep)
                path=pya.DPath(temp,w2,0,0)
                polygon=path.polygon()
                inpolygons.append(polygon)
            # 出大矩阵
            if status==3 and distance>=startchecklength+l1:
                status=0
                bigendindex=i
                ep=getp(distance-startchecklength-l1,pt,cpts[i-1])
                temp=[bigstartp]
                temp.extend(cpts[bigstartindex:bigendindex-1])
                temp.append(ep)
                path=pya.DPath(temp,w1,0,0)
                polygon=path.polygon()
                outpolygons.append(polygon)
                startchecklength+=deltalength
                finishnumber+=1
                if finishnumber==number:break

        if status==3:inpolygons.pop() # 状态是最后一个大矩阵未完成, 此时弹出不应有的对应的小矩阵

        region=pya.Region([pya.Polygon.from_dpoly(x) for x in outpolygons])-pya.Region([pya.Polygon.from_dpoly(x) for x in  inpolygons])
        region.transform(pya.ICplxTrans.from_dtrans(brush.DCplxTrans))

        BasicPainter.Draw(cell,layer,region)

        p0=cpts[0]
        p1=cpts[1]
        brush0=CavityBrush(pointc=p0,angle=atan2(p0.y-p1.y,p0.x-p1.x),widout=brush.widout,widin=brush.widin,bgn_ext=0)
        p0=cpts[-1]
        p1=cpts[-2]
        brush1=CavityBrush(pointc=p0,angle=atan2(p0.y-p1.y,p0.x-p1.x),widout=brush.widout,widin=brush.widin,bgn_ext=0)
        return [brush0,brush1]
    @staticmethod
    def _boxes_move_and_copy(inregion,radius,number):
        xys=[(radius*cos(2*pi*ii/number),radius*sin(2*pi*ii/number)) for ii in range(number)]
        regions=[]
        for x,y in xys:
            regions.append(inregion.transformed(pya.Trans(x,y)))
        return regions
    @staticmethod
    def _boxes_merge_and_draw(cell,layer,outregion,inregion,regions,cutbool=True):
        for rr in regions:
            inregion=inregion+rr
            inregion.merge()
        if cutbool:
            region=outregion-inregion
        else:
            region=outregion & inregion
        BasicPainter.Draw(cell,layer,region)
        return region
    @staticmethod
    def DrawFillRegion(cell,layer,radius,number,layerlist=None,layermod='not in',box=None,cutbool=True):
        if type(box)==type(None):box=Interactive._box_selected()
        if not box:raise RuntimeError('no box set')
        outregion,inregion=Collision.getShapesFromCellAndLayer(cellList=[IO.top],layerList=layerlist,box=box,layermod=layermod)
        regions=SpecialPainter._boxes_move_and_copy(inregion,radius,number)
        return SpecialPainter._boxes_merge_and_draw(cell,layer,outregion,inregion,regions,cutbool)
    @staticmethod
    def DrawBoxesInRegion(cell,layer,region,dlength,dgap,dx=0,dy=0): 
        d=dlength+dgap
        area=region.bbox()
        dx=dx%d
        dy=dy%d
        left=floor((area.left-dx)/d)
        bottom=floor((area.bottom-dy)/d)
        right=ceil((area.right-dx)/d)
        top=ceil((area.top-dy)/d)
        x0=left*d+dx
        y0=bottom*d+dy
        boxesregion=pya.Region()
        for ii in range(right-left):
            for jj in range(top-bottom):
                x1=x0+ii*d
                y1=y0+jj*d
                box=pya.Box(x1,y1,x1+dlength,y1+dlength)
                boxesregion.insert(box)
        andRegion= boxesregion & region
        BasicPainter.Draw(cell,layer,andRegion)
        return andRegion
    @staticmethod
    def DrawBoxes(cell,layer,dlength,dgap,radius,number,layerlist=None,layermod='not in',box=None,cutbool=True,dx=0,dy=0):
        fillCell = IO.layout.create_cell("fill")
        IO.auxiliary.insert(pya.CellInstArray(fillCell.cell_index(),pya.Trans()))
        fillRegion=SpecialPainter.DrawFillRegion(cell=fillCell,layer=IO.layer,radius=radius,number=number,layerlist=layerlist,layermod=layermod,box=box,cutbool=cutbool)
        boxesRegion=SpecialPainter.DrawBoxesInRegion(cell=cell,layer=layer,region=fillRegion,dlength=dlength,dgap=dgap,dx=dx,dy=dy)
        return fillCell,fillRegion,boxesRegion
        # box=pya.Box(-170000,-60000,110000,190000)
        # paintlib.SpecialPainter.DrawBoxes(cell=cell7,layer=layer6,dlength=80000,dgap=2000,radius=20000,number=70,layerlist=None,layermod='not in',box=box,cutbool=True,dx=0,dy=0)
    @staticmethod
    def contortion(x,y,angle,width,height,length,radius,widout=20000,widin=10000,strategy='width',infoOnly=False):
        '''
        以某点为中心矩形区域内画定长的腔并产生两个刷子
        '''
        def getbrush():
            painter=CavityPainter(pointc=pya.DPoint(x,y),angle=angle+180,widout=widout,widin=widin,bgn_ext=0,end_ext=0)
            painter.Run('s{}'.format(width/2))
            brush1=painter.brush
            painter=CavityPainter(brush1.reversed())
            painter.Run('s{}'.format(width))
            brush2=painter.brush
            return brush1,brush2
        if width==length:
            brush1,brush2=getbrush()
            return 's'+str(length),brush1,brush2,width,width
        def minlength(n):
            return (n+1)*pi*radius+(width-(n+1)*2*radius)
        def maxlength(n):
            return minlength(n)+(height-4*radius)+(n-1)*(height-2*radius)
        if height<4*radius:
            raise RuntimeError('height<4*radius')
        if width<4*radius:
            raise RuntimeError('width<4*radius')
        maxn=floor(width/(2*radius))-1
        brush1,brush2=getbrush()
        if infoOnly:
            return '',brush1,brush2,minlength(1),maxlength(maxn)
        if length<minlength(1):
            raise RuntimeError('length too small')
        if length>maxlength(maxn):
            raise RuntimeError('length too big')
        if strategy=='width':
            n=maxn
            while length<minlength(n):
                n-=1
        else:
            n=1
            while length>maxlength(n):
                n+=1
        dl=(length-minlength(n))/(2*n)
        path='s{s1} l{r} s{dl} r{r} n{nm}[r{r} s{dl2} l{r},180 s{dl2} r{r}] '
        if n%2==0:
            path+='r{r} s{dl2} l{r},180 s{dl} r{r} '
        else:
            path+='r{r} s{dl} l{r} '
        path+='s{s1}'
        path=path.format(s1=(width-(n+1)*2*radius)/2,r=radius,dl=dl,dl2=dl*2+radius*2,nm=int(floor((n-1)/2)))
        return path,brush1,brush2,minlength(1),maxlength(maxn)
