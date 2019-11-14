# -*- coding: utf-8 -*-


import pya

from .IO import IO
from .BasicPainter import BasicPainter

class Collision(object):
    '''处理图形冲突的类'''
    pointRadius=1000
    def __init__(self):
        self.region=pya.Region()
    def insert(self,polygon):
        if isinstance(polygon,list):
            for x in polygon:
                if isinstance(x,pya.DPolygon):
                    self.region.insert(pya.Polygon.from_dpoly(x))
            return self
        if isinstance(polygon,pya.DPolygon):
            self.region.insert(pya.Polygon.from_dpoly(polygon))
            return self
        if isinstance(polygon,pya.Region):
            self.region=self.region+polygon
            return self
        raise TypeError('Invalid input')
    def conflict(self,other):
        if isinstance(other,Collision):
            return self.region.interacting(other.region)
        if isinstance(other,pya.DPoint):
            region=pya.Region(pya.DPolygon(BasicPainter.arc(other,self.pointRadius,8,0,360)))
            return self.region.interacting(region)
        raise TypeError('Invalid input')
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
    def getShapesFromCellAndLayer(cellList,box,layerList=None,layermod='not in'):
        if layerList==None:layerList=[(0,0),(0,1),(0,2)]
        _layerlist=[]
        for ii in layerList:
            if type(ii)==str:
                if IO.layout.find_layer(ii)!=None:_layerlist.append(IO.layout.find_layer(ii))
            else:
                if IO.layout.find_layer(ii[0],ii[1])!=None:_layerlist.append(IO.layout.find_layer(ii[0],ii[1]))
        layers=[index for index in IO.layout.layer_indices() if index in _layerlist] if layermod=='in' else [index for index in IO.layout.layer_indices() if index not in _layerlist]
        outregion=pya.Region(box)
        inregion=pya.Region()
        for cell in cellList:
            for layer in layers:
                s=cell.begin_shapes_rec_touching(layer,box)
                inregion.insert(s)
        inregion.merge()
        return [outregion,inregion]