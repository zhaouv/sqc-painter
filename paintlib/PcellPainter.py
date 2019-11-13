# -*- coding: utf-8 -*-

import pya

from .IO import IO
from .Painter import Painter


        
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