# -*- coding: utf-8 -*-

import re

import pya
from .IO import IO
from .CavityBrush import CavityBrush
from .Combiner import Combiner

'''
config of each grid item
+ width
+ height
+ how to draw
  - args

+ xindex
+ yindex
'''

'''
config
[
    {
        "condition":"string template with {xindex}{yindex}{mark} and or not True False",
        "vars":{"a":1}
    },
    {
        "condition":"1",
        "vars":{"a":1}
    },
    {
        "condition":"{mark}=='a' and {xindex}<=4",
        "export":[["brush","b1,b2","b1_{xindex}_{yindex}_{mark},b2"],["collection.merge","1,2,10_0","1,2,3"],...]
    },
]
types
{
    "a":{"width":xxx,"height":xxx,"id":xxx}
}
gridString
"""
    # aaa
    as d
       f
     a sddd
    as dd #sdf
"""
'''

class Griditem(Combiner):
    offsetx=0
    offsety=0
    mark=' '
    width=0
    height=0
    xindex=0
    yindex=0
    basex=0
    basey=0
    def position(self,posstr=''):
        x=self.offsetx+self.basex+self.width/2
        y=self.offsety+self.basey+self.height/2
        if 'l' in posstr:
            x-=self.width/2
        if 'r' in posstr:
            x+=self.width/2
        if 'u' in posstr:
            y+=self.height/2
        if 'd' in posstr:
            y-=self.height/2
        return pya.DPoint(x,y)

GridNone=Griditem()
GridNone.mark='None'

class GridLayout(Combiner):

    Griditem=Griditem
    GridNone=GridNone
    GridNameTemplate="Grid_{xindex}_{yindex}_{mark}"
    
    def gridString(self,gridStr):
        lines=re.split(r'[\r\n]+',gridStr)
        pattern = re.compile(r'^\s*(#.*)?$')
        lines=[line.split('#')[0] for line in lines if not re.match(pattern,line)]
        pattern = re.compile(r'^(\s*)(.*?)(\s*)$')
        spans=[[len(ss) for ss in re.match(pattern,line).groups()] for line in lines]
        starti=min([arr[0] for arr in spans])
        endi=max([arr[0]+arr[1] for arr in spans])
        ret = [list((line+' '*endi)[starti:endi]) for line in lines]
        for ai in list(range(len(ret[0])))[::-1]:
            if all([arr[ai]==' ' for arr in ret]):
                for arr in ret:
                    arr.pop(ai)
        return ret

    def buildGrid(self):
        self.xlength = len(self.grid[0])
        self.ylength = len(self.grid)
        self.innerX=[-1 for xx in self.grid[0]]
        self.innerY=[-1 for yy in self.grid]
        self.items=[[GridNone for xx in self.grid[0]] for yy in self.grid]
        for yy in range(self.ylength):
            for xx in range(self.xlength):
                mark=self.grid[yy][xx]
                newitemtype=self.types[mark]
                if mark== ' ':
                    continue
                if self.innerX[xx] < 0:
                    self.innerX[xx]=newitemtype["width"]
                elif self.innerX[xx]!=newitemtype["width"]:
                    raise RuntimeError(f'grid no match at ({xx},{yy}) with width: {newitemtype["width"]}')
                if self.innerY[yy] < 0:
                    self.innerY[yy]=newitemtype["height"]
                elif self.innerY[yy]!=newitemtype["height"]:
                    raise RuntimeError(f'grid no match at ({xx},{yy}) with height: {newitemtype["height"]}')
        for yy in range(self.ylength):
            for xx in range(self.xlength):
                mark=self.grid[yy][xx]
                # if mark== ' ':
                #     continue
                item=Griditem()
                self.items[yy][xx]=item
                item.vars['mark']=item.mark=mark
                item.vars['xindex']=item.xindex=xx
                item.vars['yindex']=item.yindex=yy
                item.vars['width']=item.width=self.innerX[xx]
                item.vars['height']=item.height=self.innerY[yy]
                item.basex=sum(self.innerX[0:xx])
                item.basey=sum(self.innerY[0:yy])

    def buildConfig(self):
        for yy in range(self.ylength):
            for xx in range(self.xlength):
                mark=self.grid[yy][xx]
                if mark== ' ':
                    continue
                item=items[yy][xx]
                item.export=[]
                item.name=self.GridNameTemplate.format(xindex=xx,yindex=yy,mark=mark)
                for cc in self.config:
                    condition=cc['condition'].format(xindex=xx,yindex=yy,mark=mark)
                    if eval(condition):
                        item.vars.update(cc.get('vars',{}))
                        item.export.extend(cc.get('export',[]))

    def __init__(self,gridStr,types,config):
        super().__init__()
        if type(gridStr) == str:
            self.grid=self.gridString(gridStr)[::-1]
        else:
            self.grid=gridStr[::-1]
        self.types=types
        self.config=config
        self.buildGrid()
        self.buildConfig()

    @property
    def width(self):
        return sum(self.innerX)
    @property
    def height(self):
        return sum(self.innerY)

    def buildStructure(self):
        Griditem.offsetx=-self.width/2
        Griditem.offsety=-self.height/2
        for yy in range(self.ylength):
            for xx in range(self.xlength):
                mark=self.grid[yy][xx]
                if mark== ' ':
                    continue
                item=items[yy][xx]
                self.structure[item.name]=Combiner().update(item).load(self.metal[self.types[mark]['id']],metal=self.metal).transform(pya.Trans(item.position()))
                for export in item.export:
                    key,inids,outids=export
                    outids=outids.format(xindex=xx,yindex=yy,mark=mark)
                    inids=','.join([item.name+'@'+inid for inid in inids.split(',')])
                    self.dispatch(key,inids,outids)


    def load(self, root, metal={}, args={}):
        root=self.loadifjson(root)
        self.metal.update(metal)
        self.vars.update(args)
        self.vars.update({"width":self.width,"height":self.height})
        self.buildStructure()
        for statement in root['statement']:
            self.execStatement(statement)
        return self

    def attachAtBrush(self,root,brush, metal={},args={}):
        root=self.loadifjson(root)
        self.metal.update(metal)
        self.vars.update(args)
        self.vars.update({"widin":brush.widin,"widout":brush.widout})
        self.vars.update({"width":self.width,"height":self.height})
        self.buildStructure()
        for statement in root['statement']:
            self.execStatement(statement)
        self.transform(pya.CplxTrans.from_dtrans(brush.DCplxTrans))
        return self

