# -*- coding: utf-8 -*-
#KLayout 0.24.8
#python 3.4
import paintlib
import pya
from math import cos,sin,pi
Interactive=paintlib.Interactive
CavityPainter=paintlib.CavityPainter
IO=paintlib.IO

with open(IO.path+'/matlabtpl.m') as fid:
    _matlabtpl=fid.read()

class Simulation:
    matlabfiletpl=_matlabtpl

    @staticmethod
    def _get_region_cell_port(region,brush,layerlist,boxx,boxy,offsetx=0,offsety=0,deltaangle=0,absx=None,absy=None,portbrushs=None,transmissionlines=None):
        '''先把图像逆时针转deltaangle角度后沿着平直截取'''
        # if deltaangle>46 or deltaangle<-46:raise RuntimeError('deltaangle more than 45 degree')
        if absx==None or absy==None:
            _pb=[region.bbox()]
            if type(brush)!=type(None):
                painter=CavityPainter(brush)
                painter.Run(lambda painter:painter._Straight(10)+painter._Straight(-10))
                _pb.append(painter.Output_Region().bbox())
            _pbr=pya.Region()
            for ii in _pb:_pbr.insert(ii)
            pc=_pbr.bbox().center()
        else:
            pc=pya.DPoint(absx,absy)
        pc=pya.DPoint(pc.x+offsetx,pc.y+offsety)
        
        def tr_to(obj,itr=False):
            trs=[pya.DCplxTrans(1,-deltaangle,False,pc.x,pc.y)]
            if itr:trs=[pya.ICplxTrans.from_dtrans(tr) for tr in trs]
            for tr in trs:
                obj=obj.transformed(tr)
            return obj
        def tr_back(obj,itr=False):
            trs=[pya.DCplxTrans(1,0,False,-pc.x,-pc.y),
                pya.DCplxTrans(1,deltaangle,False,0,0)]
            if itr:trs=[pya.ICplxTrans.from_dtrans(tr) for tr in trs]
            for tr in trs:
                obj=obj.transformed(tr)
            return obj

        box=tr_to(pya.Box(-boxx/2,-boxy/2,boxx/2,boxy/2),itr=True)
        #
        _,inregion=Interactive.cut(layerlist=layerlist,layermod='in',box=box,mergeanddraw=False)
        inregion=tr_back(inregion,itr=True)
        outregion=pya.Region(pya.Box(-boxx/2,-boxy/2,boxx/2,boxy/2))

        if type(brush)!=type(None):
            painter=CavityPainter(tr_back(brush))
            painter.Run(lambda painter:painter._Straight(-boxx-boxy))
            painter.Run(lambda painter:painter.Straight(2*boxx+2*boxy))
            inregion=inregion+painter.Output_Region()

        #计算端口
        ports=[]
        edges=[ #左,上,右,下
            pya.DEdge(-boxx/2,-boxy/2,-boxx/2,+boxy/2),
            pya.DEdge(-boxx/2,+boxy/2,+boxx/2,+boxy/2),
            pya.DEdge(+boxx/2,+boxy/2,+boxx/2,-boxy/2),
            pya.DEdge(+boxx/2,-boxy/2,-boxx/2,-boxy/2)
        ]
        #
        if type(brush)!=type(None):
            br=painter.brush
            pt=pya.DPoint(br.centerx,br.centery)
            angle=br.angle
            edge=pya.DEdge(pt.x,pt.y,pt.x-(2*boxx+2*boxy)*cos(angle/180*pi),pt.y-(2*boxx+2*boxy)*sin(angle/180*pi))
            ports.extend([ee.crossing_point(edge) for ee in edges if ee.crossed_by(edge)])
        if transmissionlines!=None:
            for transmissionline in transmissionlines:
                for info in transmissionline:
                    cpts=info[0]
                    pt0=cpts[0]
                    for pt in cpts[1:]:
                        edge=tr_back(pya.DEdge(pt0,pt))
                        pt0=pt
                        ports.extend([ee.crossing_point(edge) for ee in edges if ee.crossed_by(edge)])
        if portbrushs!=None:
            portbrushs=[tr_back(brush) for brush in portbrushs]
            ports.extend([[brush.centerx,brush.centery] for brush in portbrushs])
        ports=[[pt.x,pt.y] for pt in ports if abs(pt.x)<boxx/2+10 and abs(pt.y)<boxy/2+10]
        
        final_region,cell=Interactive._merge_and_draw(outregion,inregion,pya.CplxTrans(1,-deltaangle,False,pc.x,pc.y))

        return final_region,cell,ports
    
    @staticmethod
    def _format_region_into_matlab_code(region,name,prefix=''):
        output=[]
        def pushln(ss):
            output.append(prefix+ss+'\n')

        vname=name+'_xy'
        pushln(vname+'={};')
        for polygon in region.each():
            xx=[]
            yy=[]
            for pt in polygon.to_simple_polygon().each_point():
                xx.append(str(pt.x))
                yy.append(str(pt.y))
            pushln('xx_=['+','.join(xx)+'];')
            pushln('yy_=['+','.join(yy)+'];')
            pushln(vname+'{end+1}={xx_,yy_};')
        
        return output

    @staticmethod
    def create(name,startfrequency,endfrequency,stepfrequency,layerlist,boxx,boxy,region,brush,transmissionlines=None,portbrushs=None,offsetx=0,offsety=0,deltaangle=0,absx=None,absy=None):
        '''
        frequency单位GHz
        '''
        final_region,cell,ports=Simulation._get_region_cell_port(
            region=region,brush=brush,layerlist=layerlist,boxx=boxx,boxy=boxy,deltaangle=deltaangle,absx=absx,absy=absy,portbrushs=portbrushs,transmissionlines=transmissionlines
        )
        cell.name=name
        prefix=''
        output=[]
        def pushln(ss):
            output.append(prefix+ss+'\n')
        output.extend(Simulation._format_region_into_matlab_code(region=final_region,name=name,prefix=prefix))
        pushln(name+'_ports='+str(ports)+';')
        pushln(name+'_boxsize='+str([boxx,boxy])+';')
        pushln(name+'_sweep='+str([startfrequency,endfrequency,stepfrequency])+';')
        pushln('project_name_=\''+name+'\';')
        pushln(Simulation.matlabfiletpl.replace('\n','\n'+prefix).replace('TBD_projectname',name))
        ss=''.join(output)
        with open('sonnet_'+name+'.m','w') as fid:
            fid.write(ss)
            print('sonnet_'+name+'.m')