# -*- coding: utf-8 -*-

import pya

from .IO import IO
from .Painter import Painter
from .BasicPainter import BasicPainter

class PcellPainter(Painter):
    def __init__(self):
        self.outputlist = []
        # DrawText
        self.Basic = pya.Library.library_by_name("Basic")
        self.TEXT_decl = self.Basic.layout().pcell_declaration("TEXT")
        # DrawText_LiftOff
        self.charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ~!@#$%^&*()-=_+[]{}\\|;:'\",.<>/?`"
        self.charfile = IO.path+'/paintlib/gds/chars.gds'
        self.charLayerList = [(10, 10)]

    def DrawText(self, cell, layer1, textstr, DCplxTrans1):
        '''
        左下角坐标,每个字宽0.6*倍数高0.7*倍数线宽0.1*倍数  
        tr=pya.DCplxTrans(10,0,False,0,0)
        倍数,逆时针度数,是否绕x翻转,平移x,平移y
        '''
        tr = pya.CplxTrans.from_dtrans(DCplxTrans1)
        textstr = "%s" % (textstr)
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
        text_cell = IO.layout.create_cell("TEXT(\"%s\")" % (textstr))
        self.TEXT_decl.produce(IO.layout, [layer1], pv, text_cell)
        cell.insert(pya.CellInstArray(text_cell.cell_index(), tr))
        edge1 = pya.DEdge(len(textstr)*0.6, 0, len(textstr)
                          * 0.6, 0.7).transformed(DCplxTrans1)
        return [edge1.p1, edge1.p2]
    
    def DrawText_LiftOff(self, cell, layer1, teststr, DCplxTrans1):
        '''
        左下角坐标,每个字宽0.6*倍数高0.7*倍数线宽0.1*倍数  
        tr=pya.DCplxTrans(10,0,False,0,0)
        倍数,逆时针度数,是否绕x翻转,平移x,平移y
        '''
        reverse=False
        cellname="TEXT(\"%s\")" % (teststr[:30].replace('\n','N'))
        charset=self.charset
        tr = pya.CplxTrans.from_dtrans(DCplxTrans1)

        filename=self.charfile
        layout = pya.Layout()
        layout.read(filename)
        cellList = [ii for ii in layout.top_cells()]

        layerList = self.charLayerList
        _layerlist = []
        for ii in layerList:
            _layerlist.append(layout.find_layer(ii[0], ii[1]))
        layers = [index for index in layout.layer_indices() if index in _layerlist]

        fullregion = pya.Region()
        for layer_ in layers:
            fullregion.insert(cellList[0].begin_shapes_rec(layer_))
        fullregion.merge()

        charshapes=[]
        for ii in range(len(charset)):
            subregion=pya.Region(pya.Box(ii*600,0,ii*600+500,700))
            if not reverse:
                subregion=subregion & fullregion
            else:
                subregion=subregion - fullregion
            subregion.merge()
            subregion.transform(pya.ICplxTrans(1, 0, False, -ii*600, 0))
            charshapes.append(subregion)
            # BasicPainter.Draw(cell,layer1,subregion)
            pass


        ncell = IO.layout.create_cell(cellname)  
        cell.insert(pya.CellInstArray(ncell.cell_index(), tr))

        currentx=0
        currenty=-1

        for cc in teststr.upper():
            if cc=='\n':
                currenty+=1
                currentx=0
                continue
            if cc in charset:
                ii=charset.index(cc)
                BasicPainter.Draw(ncell,layer1,charshapes[ii].transformed(pya.ICplxTrans(1, 0, False, currentx*600, -currenty*800)))
                currentx+=1
                continue
            if cc in '\r\t\b\f':
                continue
            raise RuntimeError(f'"{cc}" is not supported')
