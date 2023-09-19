# -*- coding: utf-8 -*-

import re
from math import pi, atan2

from .IO import IO
from .BasicPainter import BasicPainter
from .Painter import Painter, Component
from .TransfilePainter import TransfilePainter
from .SpecialPainter import SpecialPainter

class ComponentPainter(Component, Painter):

    def Draw(self,root):
        root=self.loadifjson(root)
        for statement in root['statement']:
            self.runStatement(statement)
        return self
    
    def runStatement(self,statement):
        # todo 拆分成函数
        if statement['type']=='drawCollection':
            if statement['op']=='regex':
                pa=re.compile(statement['collection']+'$')
                for key in self.collection:
                    ma=re.match(pa,key)
                    if not ma:
                        continue
                    l1=statement['l1']
                    l1=l1 if type(l1)!=str else int(self.regexfill(l1,key,ma.groups()))
                    l2=statement['l2']
                    l2=l2 if type(l2)!=str else int(self.regexfill(l2,key,ma.groups()))
                    cell=self.regexfill(statement['cell'],key,ma.groups())
                    cell=IO.layout.cell(cell)
                    layer=IO.layout.layer(l1, l2)
                    BasicPainter.Draw(cell,layer,self.collection[key])
            elif statement['op']=='operation':
                region=eval(re.sub(r'\w+',lambda ii: "self.collection["+ii.group(0)+"]"),statement['collection'])
                l1=statement['l1']
                l2=statement['l2']
                cell=statement['cell']
                cell=IO.layout.cell(cell)
                layer=IO.layout.layer(l1, l2)
                BasicPainter.Draw(cell,layer,region)
        elif statement['type']=='drawBrush':
            pa=re.compile(statement['brush']+'$')
            for key in self.brush:
                ma=re.match(pa,key)
                if not ma:
                    continue
                name=self.regexfill(statement['name'],key,ma.groups())
                self.brush[key].Draw(name)
        elif statement['type']=='drawAirBridgeOnCenterlines':
            pa=re.compile(statement['centerlines']+'$')
            cell=statement['cell']
            cell=IO.layout.cell(cell)
            newcellname=statement['newcellname']
            filename=statement['filename']
            airbridgedistance=self.eval(statement['airbridgedistance'])
            centerlines=[]
            for key in self.centerlines:
                ma=re.match(pa,key)
                if ma:
                    centerlines.extend(self.centerlines[key])
            painter=TransfilePainter(filename)
            painter.airbridgedistance=airbridgedistance
            painter.DrawAirbridge(cell, centerlines, newcellname)
        elif statement['type']=='drawAirBridgeOnMarks':
            pa=re.compile(statement['marks']+'$')
            cell=statement['cell']
            cell=IO.layout.cell(cell)
            newcellname=statement['newcellname']
            filename=statement['filename']
            pa2=re.compile(statement['match']+'$')
            trlist=[]
            for key in self.marks:
                ma=re.match(pa,key)
                if not ma:
                    continue
                for marks in self.marks[key][::2]:
                    for mark in marks:
                        if not re.match(pa2,mark[2]):
                            continue
                        dx = mark[1].x-mark[0].x
                        dy = mark[1].y-mark[0].y
                        px = mark[1].x/2+mark[0].x/2
                        py = mark[1].y/2+mark[0].y/2
                        tr=tr=pya.DCplxTrans(1, atan2(dy, dx)/pi*180+90, False, px, py)
                        trlist.append(tr)
            painter=TransfilePainter(filename)
            painter.airbridgedistance=airbridgedistance
            painter.DrawGds(cell, newcellname, trlist)
        elif statement['type']=='drawContinueAirBridge':
            pa=re.compile(statement['centerlines']+'$')
            for key in self.centerlines:
                ma=re.match(pa,key)
                if not ma:
                    continue
                layerup=statement['layerup']
                layerup=self.regexfill(layerup,key,ma.groups())
                layerdown=statement['layerdown']
                layerdown=self.regexfill(layerdown,key,ma.groups())
                cell=self.regexfill(statement['cell'],key,ma.groups())
                cell=IO.layout.cell(cell)

                layerup=IO.layout.layer(*[int(ll) for ll in layerup.split('_')])
                layerdown=IO.layout.layer(*[int(ll) for ll in layerdown.split('_')])

                args=statement["args"]
                args=self.regexfill(args,key,ma.groups())
                using=statement["using"]
                using=self.regexfill(using,key,ma.groups())
                args=eval(self.render(args,using))

                SpecialPainter.DrawContinueAirbridgePainter(cell,layerup,layerdown, centerlinelist=self.centerlines[key],**args)
        elif statement['type']=='evalStatement':
            exec(statement['content'])


