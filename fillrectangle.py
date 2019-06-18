import paintlib
import pya
from math import cos,sin,pi
import json
Interactive=paintlib.Interactive
CavityPainter=paintlib.CavityPainter
IO=paintlib.IO
Collision=paintlib.Collision
BasicPainter=paintlib.BasicPainter

class FillRectangle:

    @staticmethod
    def _get_shapes(layerlist=None,layermod='not in',box=None):
        if layerlist==None:layerlist=[(0,0)]
        if type(box)==type(None):box=Interactive._box_selected()
        if not box:return None

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

        return [outregion,inregion]

    @staticmethod
    def _move_and_copy(inregion,radius,number):
        xys=[(radius*cos(2*pi*ii/number),radius*sin(2*pi*ii/number)) for ii in range(number)]
        regions=[]
        for x,y in xys:
            regions.append(inregion.transformed(pya.Trans(x,y)))
        return regions
    
    @staticmethod
    def _merge_and_draw(cell,layer,outregion,inregion,regions,cutbool=True):
        for rr in regions:
            inregion=inregion+rr
        if cutbool:
            region=outregion-inregion
        else:
            region=outregion-(outregion-inregion)
        BasicPainter.Draw(cell,layer,region)
        return region

    @staticmethod
    def DrawFillRegion(cell,layer,radius,number,layerlist=None,layermod='not in',box=None,cutbool=True):
        outregion,inregion=FillRectangle._get_shapes(layerlist,layermod,box)
        regions=FillRectangle._move_and_copy(inregion,radius,number)
        FillRectangle._merge_and_draw(cell,layer,outregion,inregion,regions,cutbool)

# import fillrectangle
# reload(fillrectangle)
# box=pya.Box(-848740,-212112,40934,424224)
# fillrectangle.FillRectangle.DrawFillRegion(cell=cell6,layer=layer5,radius=20000,number=70,layerlist=None,layermod='not in',box=box,cutbool=True)