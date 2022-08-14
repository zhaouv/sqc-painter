# -*- coding: utf-8 -*-

import re

import pya
from .IO import IO
from .Collision import Collision
from .Interactive import Interactive

'''
config of each grid item
+ width
+ height
+ how to draw
  - args

+ xindex
+ yindex
'''

class Griditem:
    offsetx=0
    offsety=0
    mark=' '
    width=0
    height=0
    xindex=0
    yindex=0
    basex=0
    basey=0
    def Draw(self):
        pass
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

class GridLayout:

    Griditem=Griditem
    GridNone=GridNone
    
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
                if mark!= ' ':
                    if self.innerX[xx] < 0:
                        self.innerX[xx]=newitemtype.width
                    elif self.innerX[xx]!=newitemtype.width:
                        raise RuntimeError(f'grid no match at ({xx},{yy}) with width: {newitemtype.width}')
                    if self.innerY[yy] < 0:
                        self.innerY[yy]=newitemtype.height
                    elif self.innerY[yy]!=newitemtype.height:
                        raise RuntimeError(f'grid no match at ({xx},{yy}) with height: {newitemtype.height}')
        for yy in range(self.ylength):
            for xx in range(self.xlength):
                mark=self.grid[yy][xx]
                newitem=self.types[mark]()
                self.items[yy][xx]=newitem
                newitem.mark=mark
                newitem.xindex=xx
                newitem.yindex=yy
                newitem.width=self.innerX[xx]
                newitem.height=self.innerY[yy]
                newitem.basex=sum(self.innerX[0:xx])
                newitem.basey=sum(self.innerY[0:yy])

    def Draw(self):
        return [[ai.Draw() for ai in arr] for arr in self.items]

    def __init__(self,gridStr,types):
        if type(gridStr) == str:
            self.grid=self.gridString(gridStr)[::-1]
        else:
            self.grid=gridStr[::-1]
        types[' ']=Griditem
        self.types=types
        self.buildGrid()
    
    @property
    def width(self):
        return sum(self.innerX)
    @property
    def height(self):
        return sum(self.innerY)

