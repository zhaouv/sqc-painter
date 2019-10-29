# -*- coding: utf-8 -*-
#KLayout 0.24.8
#python 3.4
import paintlib
from imp import reload
reload(paintlib)
from paintlib import *

# 以某点为中心矩形区域内画定长产生两个刷子 done but not tested yet
class _SpecialPainter(Painter):
    @staticmethod
    def DrawContortion(cell,layer,x,y,angle,width,height,length,radius,widout=20000,widin=10000,strategy='width'):
        def minlength(n):
            return (n+1)*2*pi*radius/4+(width-(n+1)*2*radius)
        def maxlength(n):
            return minlength(n)+(height-4*radius)+(n-1)*(height-2*radius)
        if height<4*radius:
            raise RuntimeError('height<4*radius')
        if width<4*radius:
            raise RuntimeError('width<4*radius')
        if length<2*pi*radius+width-4*radius:
            raise RuntimeError('length too small')
        maxn=floor(width/(2*radius))-1
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
        painter=CavityPainter(pointc=pya.DPoint(x,y),angle=angle+180,widout=widout,widin=widin,bgn_ext=0,end_ext=0)
        painter.Run('s{}'.format(width/2))
        brush1=painter.brush
        painter=CavityPainter(brush1.reversed())
        painter.Run(path)
        painter.Draw(cell,layer)
        brush2=painter.brush
        return painter,brush1,brush2

# 连线程序只在第二个点检测冲突 done

# 更正确的处理终点处的平行以及在起点附近的无交点情况 done but not tested yet
class _Interactive:
    @staticmethod
    def link(brush1=None, brush2=None, spts=None, print_=True):
        '''
        输入两个CavityBrush作为参数, 并点击图中的一个路径, 生成一个连接两个brush的路径的函数  
        缺省时会在Interactive.searchr内搜索最近的brush
        第二个brush可为None, 此时取path的终点作为路径终点
        '''
        deltaangle = Interactive.deltaangle
        maxlength = Interactive.maxlength

        def boundAngle(angle):
            '''
            (-180,180]
            '''
            while angle<=-180:
                angle+=360
            while angle>180:
                angle-=360
            return angle
        def gridAngle(angle):
            return boundAngle(round(angle/deltaangle)*deltaangle)

        if spts == None:
            spts = Interactive._pts_path_selected()
        if spts == False:
            return
        if brush1 == None:
            brush1 = Interactive._get_nearest_brush(spts[0].x, spts[0].y)
        if brush2 == None:
            brush2 = Interactive._get_nearest_brush(spts[-1].x, spts[-1].y)

        if not isinstance(brush1, CavityBrush):
            pya.MessageBox.warning("paintlib.Interactive.link",
                                "Argument 1 must be CavityBrush", pya.MessageBox.Ok)
            return
        if not isinstance(brush2, CavityBrush) and brush2 != None:
            pya.MessageBox.warning("paintlib.Interactive.link",
                                "Argument 2 must be CavityBrush or None", pya.MessageBox.Ok)
            return
        angles = [boundAngle(brush1.angle)]
        pts = [pya.DPoint(brush1.centerx, brush1.centery)]
        edges = [pya.DEdge(pts[0].x, pts[0].y, pts[0].x+maxlength *
                        cos(angles[0]/180*pi), pts[0].y+maxlength*sin(angles[0]/180*pi))]
        das = []
        lastpt = None

        for ii in range(1, len(spts)):
            pt = spts[ii]
            pt0 = spts[ii-1]
            angle0 = angles[-1]
            edge0 = edges[-1]
            angle = gridAngle(atan2(pt.y-pt0.y, pt.x-pt0.x)/pi*180)
            da=boundAngle(angle0 - angle)
            if(da == 0):
                continue
            if(da == 180):
                pya.MessageBox.warning(
                    "paintlib.Interactive.link", "Error : Turn 180 degrees", pya.MessageBox.Ok)
                return
            edge = pya.DEdge(pt.x+maxlength*cos(angle/180*pi), pt.y+maxlength*sin(angle/180*pi),
                            pt.x-maxlength*cos(angle/180*pi), pt.y-maxlength*sin(angle/180*pi))
            if not edge.crossed_by(edge0):
                if len(das)==0:
                    continue
                print('point ', ii)
                print(angle)
                print(angle0)
                pya.MessageBox.warning(
                    "paintlib.Interactive.link", "Error : Invalid path leads to no crossing point", pya.MessageBox.Ok)
                return
            lastpt = [pt.x, pt.y]
            angles.append(angle)
            das.append(da)
            pts.append(edge.crossing_point(edge0))
            edges.append(edge)

        if(brush2 != None):
            angle0 = angles[-1]
            edge0 = edges[-1]
            angle = boundAngle(brush2.angle+180)
            pt = pya.DPoint(brush2.centerx, brush2.centery)
            _angle = gridAngle(angle)
            if(_angle == angle0 and len(das)>0):
                # 规整化后与终点平行, 放弃最后一个点, 从而不再平行
                angles.pop()
                das.pop()
                pts.pop()
                edges.pop()
                angle0 = angles[-1]
                edge0 = edges[-1]
            da = boundAngle(angle0 - angle)
            _da = boundAngle(angle0 - _angle)
            if(_da == 180):
                pya.MessageBox.warning(
                    "paintlib.Interactive.link", "Error : Turn 180 degrees", pya.MessageBox.Ok)
                return
            lastpt = [pt.x, pt.y]
            edge = pya.DEdge(pt.x, pt.y, pt.x-maxlength *
                            cos(angle/180*pi), pt.y-maxlength*sin(angle/180*pi))
            if(angle == angle0 and len(das)==0):
                # 只有起点和终点且平行
                dis=edge0.distance(pt)
                if abs(dis)<10:
                    # 直连无需转弯
                    pass
                else:
                    # 需转弯, 此处多生成两个点和两个角度, 如果dis小于2-sqrt(2)的转弯半径, 生成路径时会报错
                    pt0=pts[-1]
                    dse=pt0.distance(pt)
                    dp=sqrt(dse**2-dis**2)
                    l1=(dp-dis)/2
                    if dis<0:
                        das.extend([-45,45])
                        angles.extend([angle+45,angle])
                    else:
                        das.extend([45,-45])
                        angles.extend([angle-45,angle])
                    pt1=pya.DPoint(pt0.x+l1*cos(angle/180*pi),pt0.y+l1*sin(angle/180*pi))
                    pt2=pya.DPoint(pt.x-l1*cos(angle/180*pi),pt.y-l1*sin(angle/180*pi))
                    pts.extend([pt1,pt2])
                    edges.extend([pya.DEdge(pt1,pt2),edge])
            else:
                angles.append(angle)
                das.append(da)
                if not edge.crossed_by(edge0):
                    print('brush2')
                    print(angle)
                    print(angle0)
                    pya.MessageBox.warning(
                        "paintlib.Interactive.link", "Error : Invalid path leads to no crossing point", pya.MessageBox.Ok)
                    return
                pts.append(edge.crossing_point(edge0))
                edges.append(edge)
        pts.append(pya.DPoint(lastpt[0], lastpt[1]))
        ss = Interactive._generatepath(pts, das)
        if print_:
            print('##################################')
            print(ss)
            print('##################################')
            Interactive._show_path(IO.link, IO.layer, brush1, ss)
        return ss

