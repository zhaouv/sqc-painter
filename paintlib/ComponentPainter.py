# -*- coding: utf-8 -*-

import re

from .IO import IO
from .BasicPainter import BasicPainter
from .Painter import Painter, Component

class ComponentPainter(Component, Painter):

    def Draw(self,root):
        root=self.loadifjson(root)
        for statement in root['statement']:
            self.runStatement(statement)
        return self
    
    def runStatement(self,statement):
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

        elif statement['type']=='evalStatement':
            exec(statement['content'])


