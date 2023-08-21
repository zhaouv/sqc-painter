
import re

from .IO import IO
from .CavityBrush import CavityBrush
from .Painter import Component
from .AttachmentTree import AttachmentTree
from .TransfilePainter import GDSLoader
from .CavityPainter import TraceRunner
from .AutoRoute import BrushLinker

class Combiner(Component):
    def __init__(self):
        super().__init__()
        self.dispatchedvars = {}
        self.metal = {}

    def load(self, root, metal={}, args={}):
        self.metal.update(metal)
        self.vars.update(args)
        for statement in root['statement']:
            self.execStatement(statement)
        return self

    def render(self, rawString, using):
        words='|'.join(sorted(using.split(','),key=lambda x:-len(x)))
        pa=re.compile(r'(?!")\b('+words+r')\b(?!")')
        return re.sub(pa,lambda ii: str(self.vars[ii.group(0)]),rawString)

    def execStatement(self,statement):
        # todo: split each case to a function
        if statement['type']=='variableDefine':
            if statement["id"] in self.vars:
                pass
            else:
                self.vars[statement["id"]] = self.eval(statement["value"])
        elif statement['type']=='brushDefine':
            if statement["id"] in self.brush:
                pass
            else:
                self.brush[statement["id"]] = CavityBrush(pointc=pya.DPoint(self.eval(statement["x"]), self.eval(statement["y"])), angle=self.eval(statement["angle"]), widout=self.eval(statement["widout"]), widin=self.eval(statement["widin"]), bgn_ext=0)
        elif statement['type']=='traceDefine':
            if statement["id"] in self.trace:
                pass
            else:
                self.trace[statement["id"]] = self.render(statement["value"],statement["using"])
        elif statement['type']=='dispatch':
            pairs=zip(statement['id'].split(','),statement['value'].split(','))
            if statement['keytype'] == 'trace.length':
                for k,v in pairs:
                    self.vars[v]=TraceRunner.calculatePath(self.trace[k])
            else:
                key = statement['keytype']
                if statement['keytype'] == 'variable':
                    key = 'vars'
                for k,v in pairs:
                    if '.' in k:
                        k0,k1=k.split('.')
                        todispatch=self.structure[k0].__getattribute__(key)[k1]
                    else:
                        todispatch=self.__getattribute__(key)[k]
                    if '.' in v:
                        v0,v1=v.split('.')
                        if v0 in self.structure:
                            self.structure[v0].__getattribute__(key)[v1]=todispatch
                        else:
                            self.dispatchedvars[v0] = self.dispatchedvars.get(v0,Component())
                            self.dispatchedvars[v0].__getattribute__(key)[v1]=todispatch
                    else:
                        self.__getattribute__(key)[v]=todispatch

        elif statement['type']=='structureAt':
            outids=statement['id'].split(',')
            content=statement['content']
            brush=self.brush[statement['brushid']]
            if statement['reverse']:
                brush=brush.reversed()
            if content['type']=='component':
                args={}
                if content['args']:
                    args=eval(this.render(content["args"],content["using"]))
                raise 'unfinished'
            elif content['type']=='attachmentTree':
                self.structure[outids[0]]=AttachmentTree().attachAtBrush(self.metal[content['id']],brush,args=self.dispatchedvars.get(outids[0],Component()))
            elif content['type']=='gdsLoader':
                self.structure[outids[0]]=GDSLoader().attachAtBrush(self.metal[content['id']],brush)
            elif content['type']=='linkBrush':
                brush2=self.brush[content['id']]
                if content['reverse']:
                    brush2=brush2.reversed()
                self.trace[outids[0]] = BrushLinker.link(brush, brush2, linktype=content['linktype'])
            elif content['type']=='trace':
                path=self.trace[content['traceid']]
                if content['reverse']:
                    path=TraceRunner.reversePath(path)
                if content['mirror']:
                    path=TraceRunner.mirrorPath(path)
                painter=CavityPainter(brush)
                painter.Run(path)
                self.brush[outids[0]]=painter.brush
            
        elif statement['type']=='evalStatement':
            exec(statement['content'])


