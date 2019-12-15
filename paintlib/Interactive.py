# -*- coding: utf-8 -*-


from math import cos,sin,pi,tan,atan2,sqrt,ceil,floor

import pya

from .IO import IO
from .CavityBrush import CavityBrush
from .BasicPainter import BasicPainter
from .CavityPainter import CavityPainter
from .PcellPainter import PcellPainter
from .Collision import Collision

class Interactive:
    '''处理交互的类'''
    #v =IO.warning.warning("Dialog Title", "Something happened. Continue?", pya.MessageBox.Yes + pya.MessageBox.No)
    deltaangle=45
    maxlength=1073741824
    turningr=50000
    brushlist=[]
    searchr=500000
    extendlength=10000

    @staticmethod
    def show(brush):
        Interactive.brushlist.append(brush)
        polygon=BasicPainter.Electrode(brush.reversed())
        BasicPainter.Draw(IO.link,IO.layer,polygon)
        return brush
    
    @staticmethod
    def _show_path(cell, layer, brush, pathstr):
        painter = CavityPainter(brush)
        length = painter.Run(pathstr)
        painter.Draw(cell, layer)
        return length

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
            spts=[pya.DPoint(pt.x,pt.y) for pt in shape.path.each_point()]
            return spts
        IO.warning.warning("paintlib.Interactive.link", "Please select a Path", pya.MessageBox.Ok)
        return []

    @staticmethod
    def _generatepath(pts,das):
        turningr=Interactive.turningr
        output=[]
        last=0
        for ii,da in enumerate(das):
            sda=(da>0)-(da<0)
            da*=sda
            dl=turningr*tan(da/180*pi/2)
            ll=pts[ii].distance(pts[ii+1])-last-dl
            last=dl
            if(ll<0 and IO.warning.minus_stright):
                IO.warning.warning("paintlib.Interactive.link", "Error : Straight less than 0", pya.MessageBox.Ok)
                return
            output.append('s {length} '.format(length=ll))
            output.append('r {radius},{angle} '.format(radius=sda*turningr,angle=da))
        output.append('s {length} '.format(length=pts[-1].distance(pts[-2])-last))
        return ''.join(output)
    
    @staticmethod
    def _link_define_utils():
        deltaangle = Interactive.deltaangle
        maxlength = Interactive.maxlength
        extendlength=Interactive.extendlength
        turningr=Interactive.turningr
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
        return deltaangle,maxlength,boundAngle,gridAngle,extendlength,turningr

    @staticmethod
    def link(brush1=None, brush2=None, spts=None, print_=True):
        '''
        输入两个CavityBrush作为参数, 并点击图中的一个路径, 生成一个连接两个brush的路径的函数  
        缺省时会在Interactive.searchr内搜索最近的brush
        第二个brush可为None, 此时取path的终点作为路径终点
        '''
        deltaangle,maxlength,boundAngle,gridAngle,extendlength,turningr=Interactive._link_define_utils()

        if spts == None:
            spts = Interactive._pts_path_selected()
        if spts == []:
            return
        if brush1 == None:
            brush1 = Interactive._get_nearest_brush(spts[0].x, spts[0].y)
        if not isinstance(brush1, CavityBrush):
            IO.warning.warning("paintlib.Interactive.link",
                                "Argument 1 must be CavityBrush", pya.MessageBox.Ok)
            return
        if brush2 == None:
            brush2 = Interactive._get_nearest_brush(spts[-1].x, spts[-1].y)
            if brush2==None:
                brush2=CavityBrush(pointc=pya.DPoint(spts[-1].x,spts[-1].y), angle=gridAngle(atan2(spts[-2].y-spts[-1].y, spts[-2].x-spts[-1].x)/pi*180),widout=brush1.widout,widin=brush1.widin,bgn_ext=0)
                spts.pop()

        if not isinstance(brush2, CavityBrush):
            IO.warning.warning("paintlib.Interactive.link",
                                "Argument 2 must be CavityBrush or None", pya.MessageBox.Ok)
            return

        ss=Interactive.link_process(brush1=brush1, brush2=brush2, spts=spts)

        if print_:
            print('##################################')
            print(ss)
            print('##################################')
            Interactive._show_path(IO.link, IO.layer, brush1, ss)
        return ss

    @staticmethod
    def link_process(brush1, brush2, spts):
        
        '''
        主流程:
        + 起点到终点走一轮, 扫出所有转向的角度和边(直线/射线)
        + 起点到终点挪一轮点
        + 终点到起点挪一轮点
        + 渲染成路径字符串

        扫角度:
        如果发现起点终点只有两个有效点且平行, 改为额外的处理

        挪边:
        在一个点转向后, 如果线段不够长, 把这个转向后的边向冲突的线段方向延长至足够且增加额外延长extendlength
        '''

        angles,pts,edges,das=Interactive._link_scan_angles(brush1, brush2, spts)

        moved,angles,pts,edges,das=Interactive._link_move_edges(angles,pts,edges,das,reverse=False)
        if moved:
            moved,angles,pts,edges,das=Interactive._link_move_edges(angles,pts,edges,das,reverse=True)

        ss = Interactive._generatepath(pts, das)

        return ss
    
    @staticmethod
    def _link_scan_angles(brush1, brush2, spts):
        '''
        扫角度
        '''
        deltaangle,maxlength,boundAngle,gridAngle,extendlength,turningr=Interactive._link_define_utils()

        #起点
        angles = [boundAngle(brush1.angle)]
        pts = [pya.DPoint(brush1.centerx, brush1.centery)]
        edges = [pya.DEdge(pts[0].x, pts[0].y, pts[0].x+maxlength *
                        cos(angles[0]/180*pi), pts[0].y+maxlength*sin(angles[0]/180*pi))]
        das = [] 
        #这四个数组最终长度: n个角度, n+1个点, n条边, n-1个角度变化

        #经过的点
        for ii in range(1, len(spts)):
            pt = spts[ii]
            pt0 = spts[ii-1]
            angle0 = angles[-1]
            edge0 = edges[-1]
            angle = gridAngle(atan2(pt.y-pt0.y, pt.x-pt0.x)/pi*180)
            da=boundAngle(angle0 - angle) # 默认的右转是顺时针, 计算出的逆时针的角度要取反
            if(da == 0):
                continue
            if(da == 180):
                IO.warning.warning(
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
                IO.warning.warning(
                    "paintlib.Interactive.link", "Error : Invalid path leads to no crossing point", pya.MessageBox.Ok)
                return
            angles.append(angle)
            das.append(da)
            pts.append(edge.crossing_point(edge0))
            edges.append(edge)
        
        #终点
        if True:
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
                IO.warning.warning(
                    "paintlib.Interactive.link", "Error : Turn 180 degrees", pya.MessageBox.Ok)
                return
            lastpt = pt
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
                    IO.warning.warning(
                        "paintlib.Interactive.link", "Error : Invalid path leads to no crossing point", pya.MessageBox.Ok)
                    return
                pts.append(edge.crossing_point(edge0))
                edges.append(edge)
            pts.append(lastpt)
        return angles,pts,edges,das

    @staticmethod
    def _link_move_edges(angles,pts,edges,das,reverse=False):
        '''
        挪边
        '''
        deltaangle,maxlength,boundAngle,gridAngle,extendlength,turningr=Interactive._link_define_utils()

        n=len(edges)
        if not reverse:
            argsArr=[0,1,(lambda ii:ii<n-2),0,1,0,1,1,1] 
        else:
            argsArr=[n,-1,(lambda ii:ii>2),-2,-1,-1,-2,-2,-2]
        initii,iid,condition,dad,dld,angle0d,angled,ptd,eid=argsArr
        
        ii=initii
        last=0
        moved=False
        while condition(ii):
            da=das[ii+dad]
            sda=(da>0)-(da<0)
            da*=sda
            dl=turningr*tan(da/180*pi/2)
            ll=pts[ii].distance(pts[ii+dld])-last-dl
            last=dl
            if(ll<0):
                # move pt
                angle0=angles[ii+angle0d]
                angle=angles[ii+angled]
                pt=pts[ii+ptd]
                ei=ii+eid
                edges[ei]=pya.DEdge(
                    pt.x+maxlength*cos(angle/180*pi)+(extendlength-ll)*cos(angle0/180*pi), 
                    pt.y+maxlength*sin(angle/180*pi)+(extendlength-ll)*sin(angle0/180*pi),
                    pt.x-maxlength*cos(angle/180*pi)+(extendlength-ll)*cos(angle0/180*pi), 
                    pt.y-maxlength*sin(angle/180*pi)+(extendlength-ll)*sin(angle0/180*pi))
                if not all([edges[ei].crossed_by(edges[ei-1]),edges[ei].crossed_by(edges[ei+1])]):
                    IO.warning.warning(
                        "paintlib.Interactive.link", "Error : Invalid path leads to no crossing point when adjusting conflict", pya.MessageBox.Ok)
                    return
                pts[ei]=edges[ei].crossing_point(edges[ei-1])
                pts[ei+1]=edges[ei].crossing_point(edges[ei+1])
                moved=True
            ii+=iid
        return moved,angles,pts,edges,das




    @staticmethod
    def _box_selected():
        for obj in IO.layout_view.each_object_selected():
            #只检查第一个选中的对象
            shape=obj.shape
            if not shape.is_box():break
            return shape.box
        IO.warning.warning("paintlib.Interactive.cut", "Please select a Box", pya.MessageBox.Ok)
        return False

    @staticmethod
    def _merge_and_draw(outregion,inregion,tr_to=None,cell=None,cutbool=True):
        if cutbool:
            region=outregion-inregion
        else:
            region=outregion & inregion
        #
        if type(cell)==type(None):
            if type(tr_to)==type(None):
                center=outregion.bbox().center()
                region.transform(pya.Trans(int(-center.x),int(-center.y)))
                tr=pya.Trans(int(center.x),int(center.y))
            else:
                tr=tr_to
            cut = IO.layout.create_cell("cut")
            IO.auxiliary.insert(pya.CellInstArray(cut.cell_index(),tr))
        else:
            cut = cell
        BasicPainter.Draw(cut,IO.layer,region)
        return region,cut

    @staticmethod
    def cut(layerlist=None,layermod='not in',box=None,mergeanddraw=True):
        if type(box)==type(None):box=Interactive._box_selected()
        if not box:raise RuntimeError('no box set')
        outregion,inregion=Collision.getShapesFromCellAndLayer(cellList=[IO.top],layerList=layerlist,box=box,layermod=layermod)

        if not mergeanddraw:
            return outregion,inregion

        return Interactive._merge_and_draw(outregion,inregion)[0]
    
    @staticmethod
    def scanBoxes(cellList=None,layerList=None,layermod='in',position='leftdown'):
        if cellList==None:cellList=[IO.top]
        if layerList==None:layerList=[(0,1)]
        _layerlist=[]
        for ii in layerList:
            if type(ii)==str:
                if IO.layout.find_layer(ii)!=None:_layerlist.append(IO.layout.find_layer(ii))
            else:
                if IO.layout.find_layer(ii[0],ii[1])!=None:_layerlist.append(IO.layout.find_layer(ii[0],ii[1]))
        layers=[index for index in IO.layout.layer_indices() if index in _layerlist] if layermod=='in' else [index for index in IO.layout.layer_indices() if index not in _layerlist]

        region=pya.Region()
        for cell in cellList:
            for layer in layers:
                s=cell.begin_shapes_rec(layer)
                region.insert(s)
        region.merge()
        pts=[]
        for polygon in region.each():
            print(polygon)
            try:
                polygon=polygon.bbox()
            finally:
                pass
            print(polygon)
            pt=polygon.p1 if position=='leftdown' else polygon.center()
            pts.append(pt)
        output=[]
        layer=IO.layout.layer(0, 2)
        cell=IO.layout.create_cell("boxMarks")
        IO.auxiliary.insert(pya.CellInstArray(cell.cell_index(),pya.Trans()))
        painter=PcellPainter()
        for index,pt in enumerate(pts,1):
            name="M"+str(index)
            painter.DrawText(cell,layer,name,pya.DCplxTrans(100,0,False,pt.x,pt.y))
            output.append([name,{"x":pt.x,"y":pt.y}])
        return output

    
