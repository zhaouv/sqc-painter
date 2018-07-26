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
    def _get_region_cell_port_from_resonator_and_transmissionline(region,brush,layerlist,boxx,boxy,deltaangle=0):
        '''先把图像逆时针转deltaangle角度后沿着平直截取'''
        painter=CavityPainter(brush)
        painter.Run(lambda painter:painter._Straight(10)+painter._Straight(-10))
        _pb=[region.bbox(),painter.Output_Region().bbox()]
        _pbr=pya.Region()
        for ii in _pb:_pbr.insert(ii)
        pc=_pbr.bbox().center()
        
        # tr1=pya.DCplxTrans(1,-deltaangle,False,-pc.x,-pc.y)

        box=pya.Box(pc.x-boxx/2,pc.y-boxy/2,pc.x+boxx/2,pc.y+boxy/2)# .transformed(pya.ICplxTrans.from_dtrans(tr1))
        outregion,inregion=Interactive.cut(layerlist=layerlist,layermod='in',box=box,mergeanddraw=False)
        painter.Run(lambda painter:painter._Straight(-boxx-boxy))
        painter.Run(lambda painter:painter.Straight(2*boxx+2*boxy))
        inregion=inregion+painter.Output_Region()

        #计算端口
        br=painter.brush
        pt=pya.DPoint(br.centerx,br.centery)
        angle=br.angle
        edge=pya.DEdge(pt.x,pt.y,pt.x-(2*boxx+2*boxy)*cos(angle/180*pi),pt.y-(2*boxx+2*boxy)*sin(angle/180*pi))
        edges=[ #左,上,右,下
            pya.DEdge(pc.x-boxx/2,pc.y-boxy/2,pc.x-boxx/2,pc.y+boxy/2),
            pya.DEdge(pc.x-boxx/2,pc.y+boxy/2,pc.x+boxx/2,pc.y+boxy/2),
            pya.DEdge(pc.x+boxx/2,pc.y+boxy/2,pc.x+boxx/2,pc.y-boxy/2),
            pya.DEdge(pc.x+boxx/2,pc.y-boxy/2,pc.x-boxx/2,pc.y-boxy/2)
        ]
        ports=[ee.crossing_point(edge) for ee in edges if ee.crossed_by(edge)]
        
        final_region,cell,tr=Interactive._merge_and_draw(outregion,inregion)

        ports=[[pt.x-tr[0],pt.y-tr[1]] for pt in ports]
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
    def resonator_transmissionline(region,brush,layerlist,boxx,boxy,name,startfrequency,endfrequency,stepfrequency,deltaangle=0):
        '''
        frequency单位GHz
        '''
        final_region,cell,ports=Simulation._get_region_cell_port_from_resonator_and_transmissionline(
            region=region,brush=brush,layerlist=layerlist,boxx=boxx,boxy=boxy,deltaangle=deltaangle
        )
        cell.name=name
        prefix=''
        output=Simulation._format_region_into_matlab_code(region=final_region,name=name,prefix=prefix)
        def pushln(ss):
            output.append(prefix+ss+'\n')
        pushln(name+'_ports='+str(ports)+';')
        pushln(name+'_boxsize='+str([boxx,boxy])+';')
        pushln(name+'_sweep='+str([startfrequency,endfrequency,stepfrequency])+';')
        pushln('project_name_=\''+name+'\';')
        pushln(Simulation.matlabfiletpl.replace('\n','\n'+prefix).replace('TBD_projectname',name))
        ss=''.join(output)
        with open('sonnet_'+name+'.m','w') as fid:
            fid.write(ss)
            print('sonnet_'+name+'.m')