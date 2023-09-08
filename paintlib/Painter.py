# -*- coding: utf-8 -*-
import re
import json

class Painter:
    pass

class Component:
    def __init__(self):
        self.collection = {}
        self.brush = {}
        self.vars = {}
        self.trace = {}
        self.structure = {}
        self.centerlines = {}
        self.marks = {}
    
    def update(self,*aa,**kk):
        if len(aa)>=1: # and type(aa[0])==Component
            for key in ['collection','brush','vars','trace','structure','centerlines','marks']:
                self.__getattribute__(key).update(aa[0].__getattribute__(key))
        for key in kk:
            self.__getattribute__(key).update(kk[key])
        return self

    def loadifjson(self,filename):
        ret=filename
        if type(filename) == type('') and filename.endswith('.json'):
            self.filename=filename
            with open(filename) as fid:
                ret=json.load(fid)
        self.root=ret
        return ret
        
    def eval(self, number):
        if type(number)==str:
            return eval(re.sub(r'[a-zA-Z_]+\w+',lambda ii: str(self.vars[ii.group(0)]),number))
        return number
    
    def render(self, rawString, using):
        if not using:
            return rawString
        words='|'.join(sorted(using.split(','),key=lambda x:-len(x)))
        pa=re.compile(r'(?!")\b('+words+r')\b(?!")')
        return re.sub(pa,lambda ii: str(self.vars.get(ii.group(0),self.trace.get(ii.group(0),0))),rawString)

    def regexfill(self,tofill,g0,groups):
        gs=[g0,*groups]
        for ii,gi in [*enumerate(gs)][::-1]:
            tofill=tofill.replace(f'${ii}',gi)
        return tofill

    def transform(self, tr):
        for k in self.brush:
            self.brush[k].transform(tr)
        for k in self.collection:
            self.collection[k].transform(tr)
        # for k in self.structure: # 会出现多次引用的问题
        #     self.structure[k].transform(tr)
        # todo在同一层merge后transform仍可能会触发多次调用的问题, 以后还是要引入tr计数的机制才能完美解决
        
        # painter.Getcenterlineinfo()
        # [[[pya.DPoint],CavityBrush],]
        for k in self.centerlines:
            for l in self.centerlines[k]:
                for p in l[0]:
                    p.transform(tr)
                l[1].transform(tr)
        # painter.Getmarks()
        # [[[pya.DPoint,pya.DPoint,str],],[[pya.DPoint,pya.DPoint,str],]]
        for k in self.marks:
            for l in self.marks[k]:
                for p in l[0:2]:
                    p.transform(tr)
        
        return self
        