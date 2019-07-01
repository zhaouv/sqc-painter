import paintlib
import pya
from math import cos,sin,pi,ceil,floor
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
        
        inregion.merge()

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
            inregion.merge()
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
        return FillRectangle._merge_and_draw(cell,layer,outregion,inregion,regions,cutbool)

    @staticmethod
    def getRegionFromLayer(layerInfo):
        region=pya.Region()
        if type(layerInfo)==str:
            layer=IO.layout.find_layer(layerInfo)
        else:
            layer=IO.layout.find_layer(layerInfo[0],layerInfo[1])
        region.insert(IO.top.begin_shapes_rec(layer))
        region.merge()
        return region

    @staticmethod
    def DrawBoxesInRegion(cell,layer,region,dlength,dgap,dx=0,dy=0):
        
        d=dlength+dgap
        area=region.bbox()

        dx=dx%d
        dy=dy%d

        left=floor((area.left-dx)/d)
        bottom=floor((area.top-dy)/d)
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
        
""" 
import fillrectangle
reload(fillrectangle)
box=pya.Box(-848740,-212112,40934,424224)
region=fillrectangle.FillRectangle.DrawFillRegion(cell=cell6,layer=layer5,radius=20000,number=70,layerlist=None,layermod='not in',box=box,cutbool=True)
fillrectangle.FillRectangle.DrawBoxesInRegion(cell=cell7,layer=layer6,region,dlength=80000,dgap=2000,dx=0,dy=0)
 """