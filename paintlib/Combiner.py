
import re

import pya
from .IO import IO
from .CavityBrush import CavityBrush
from .Painter import Component
from .AttachmentTree import AttachmentTree
from .TransfilePainter import GDSLoader
from .CavityPainter import TraceRunner, CavityPainter
from .AutoRoute import BrushLinker

class Combiner(Component):
    def __init__(self):
        super().__init__()
        self.dispatchedObj = {}
        self.metal = {}
        self.increasingIndexForStatement=0

    def load(self, root, metal={}, args={}):
        root=self.loadifjson(root)
        self.metal.update(metal)
        self.vars.update(args)
        for statement in root['statement']:
            self.execStatement(statement)
        return self

    def attachAtBrush(self,root,brush, metal={},args={}):
        root=self.loadifjson(root)
        self.metal.update(metal)
        self.vars.update(args)
        self.vars.update({"widin":brush.widin,"widout":brush.widout})
        for statement in root['statement']:
            self.execStatement(statement)
        self.transform(pya.CplxTrans.from_dtrans(brush.DCplxTrans))
        return self

    def execStatement(self,statement):
        # todo: split complex cases to function
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
                path = self.render(statement["value"],statement["using"])
                if statement['reverse']:
                    path=TraceRunner.reversePath(path)
                if statement['mirror']:
                    path=TraceRunner.mirrorPath(path)
                self.trace[statement["id"]] = path
        elif statement['type']=='dispatch':
            self.dispatch(statement['keytype'],statement['id'],statement['value'])
                    
        elif statement['type']=='structureAt':
            content=statement['content']
            outids=content['outputid'].split(',')
            brush=self.brush[statement['brushid']]
            if statement['reverse']:
                brush=brush.reversed()
            self.structureAt(content,brush)
            
        elif statement['type']=='forStatement':
            # 1.用递归处理不定层数的循环->效率太低, 改为最多2层, 想再多手动嵌套 
            # 2.叶子函数内部处理导入导出执行内容
            ids=statement['ids'].split(',')
            svars=statement['svars'].split(',')
            evars=statement['evars'].split(',')
            if len(ids)>=3:
                raise RuntimeError('loop vars of forStatement more that 2')
            loopvars={}
            s1,e1,id1=self.eval(svars[0]),self.eval(evars[0])+1,ids[0]
            for ii in range(s1,e1):
                self.vars[id1]=loopvars[id1]=ii
                if len(ids)==2:
                    s2,e2,id2=self.eval(svars[1]),self.eval(evars[1])+1,ids[1]
                else:
                    s2,e2,id2=0,1,'a_will_not_used_name'
                for jj in range(s2,e2):
                    self.vars[id2]=loopvars[id2]=jj
                    self.forStatementOne(loopvars,statement['imports'],statement['statement'],statement['exports'])

        elif statement['type']=='evalStatement':
            exec(statement['content'])
    
    def forStatementOne(self,loopvars,imports,statements,exports):
        self.increasingIndexForStatement+=1
        thisid='forstructure_'+str(self.increasingIndexForStatement)
        self.structure[thisid]=Combiner().update(vars=loopvars,metal=self.metal)
        for statement in imports:
            key,inids,outids=statement['keytype'],statement['id'],statement['value']
            # https://stackoverflow.com/questions/47339121/how-do-i-convert-a-string-into-an-f-string
            inids=eval(f'f"""{inids}"""',{},loopvars)
            outids=','.join([thisid+'@'+inid for outids in outids.split(',')])
            self.dispatch(key,inids,outids)
        for statement in statements:
            self.structure[thisid].execStatement(statement)
        for statement in exports:
            key,inids,outids=statement['keytype'],statement['id'],statement['value']
            inids=','.join([thisid+'@'+inid for inids in inids.split(',')])
            outids=eval(f'f"""{outids}"""',{},loopvars)
            self.dispatch(key,inids,outids)

    def dispatch(self,key,inids,outids):
        op='set'
        if '.' in key:
            key,op=key.split('.')
        
        if ',' not in outids:
            pairs=[]
            # try use re to find pairs
            k0,k1='',inids
            tomatchdict=self.__getattribute__(key)
            if '@' in inids:
                k0,k1=inids.split('@')
                tomatchdict=self.structure[k0].__getattribute__(key)
                k0=k0+'@'
            pa=re.compile(k1+'$')
            for kk in tomatchdict:
                ma=re.match(pa,kk)
                if not ma:
                    continue
                pairs.append([k0+kk,self.regexfill(outids,kk,ma.groups())])
        else:
            pairs=zip(inids.split(','),outids.split(','))

        if key == 'variable':
            key = 'vars'
        for k,v in pairs:
            self.dispatchOne(key,op,k,v)

    def dispatchOne(self,key,op,k,v):

        if '@' in k:
            k0,k1=k.split('@')
            todispatch=self.structure[k0].__getattribute__(key)[k1]
        else:
            todispatch=self.__getattribute__(key)[k]
        if op=='length':
            key='vars'
        if '@' in v:
            v0,v1=v.split('@')
            if v0 in self.structure:
                tok,tov=self.structure[v0].__getattribute__(key),v1
            else:
                self.dispatchedObj[v0] = self.dispatchedObj.get(v0,Component())
                tok,tov=self.dispatchedObj[v0].__getattribute__(key),v1
        else:
            tok,tov=self.__getattribute__(key),v
        if op=='length':
            tok[tov]=TraceRunner.calculatePath(todispatch)
        elif op=='set':
            tok[tov]=todispatch
        else: # op=='merge'
            # collection.merge marks.merge centerlines.merge
            self.mergeOne(tok,tov,todispatch,key)
    
    def mergeOne(self,tok,tov,todispatch,key):
        # todo在同一层merge后transform仍可能会触发多次调用的问题, 以后还是要引入tr计数的机制才能完美解决
        if tov not in tok:
            tok[tov]=todispatch
        else:
            if key=='collection':
                tok[tov].insert(todispatch)
            else:
                tok[tov].extend(todispatch)

    def structureAt(self,content,brush):
        outids=content['outputid'].split(',')
        if content['type']=='component':
            args={}
            if content['args']:
                args=eval(self.render(content["args"],content["using"]))
                self.addComponent(outids,content['componentType'],brush,args,content['collection'])
        elif content['type']=='attachmentTree':
            self.structure[outids[0]]=AttachmentTree().update(self.dispatchedObj.get(outids[0],Component())).attachAtBrush(self.metal[content['id']],brush)
        elif content['type']=='gdsLoader':
            self.structure[outids[0]]=GDSLoader().attachAtBrush(self.metal[content['id']],brush)
        elif content['type']=='combinercontent':
            self.structure[outids[0]]=Combiner().update(self.dispatchedObj.get(outids[0],Component())).attachAtBrush(self.metal[content['id']],brush,metal=self.metal)
        elif content['type']=='linkBrush':
            brush2=self.brush[content['id']]
            if content['reverse']:
                brush2=brush2.reversed()
            path = BrushLinker.link(brush, brush2, linktype=content['linktype'])
            painter=CavityPainter(brush)
            painter.Run(path)
            if outids[0]:
                self.trace[outids[0]] = path
            painter.Output_Region(notmerge=True)
            if outids[1]:
                self.mergeOne(self.collection,outids[1],painter.regionout,'collection')
            if outids[2]:
                self.mergeOne(self.collection,outids[2],painter.regionin,'collection')
            if outids[3]:
                self.mergeOne(self.centerlines,outids[3],painter.Getcenterlineinfo(),'centerlines')
            if outids[4]:
                self.mergeOne(self.marks,outids[4],painter.Getmarks(),'marks')
            if outids[5]:
                self.vars[outids[5]]=painter._length
        elif content['type']=='trace':
            path=self.trace[content['traceid']]
            if content['reverse']:
                path=TraceRunner.reversePath(path)
            if content['mirror']:
                path=TraceRunner.mirrorPath(path)
            painter=CavityPainter(brush)
            painter.Run(path)
            if outids[0]:
                self.brush[outids[0]]=painter.brush
            painter.Output_Region(notmerge=True)
            if outids[1]:
                self.mergeOne(self.collection,outids[1],painter.regionout,'collection')
            if outids[2]:
                self.mergeOne(self.collection,outids[2],painter.regionin,'collection')
            if outids[3]:
                self.mergeOne(self.centerlines,outids[3],painter.Getcenterlineinfo(),'centerlines')
            if outids[4]:
                self.mergeOne(self.marks,outids[4],painter.Getmarks(),'marks')
            if outids[5]:
                self.vars[outids[5]]=painter._length


    def addComponent(self,outids,componentType,brush,args,collection):
        if componentType in ['Electrode','Connection','Narrow','InterdigitedCapacitor']:
            painter=CavityPainter(brush)
            eval(f'painter.{componentType}(**args)')
            self.brush[outids[0]]=painter.brush
            self.mergeOne(self.collection,collection,painter.Output_Region(),'collection')





