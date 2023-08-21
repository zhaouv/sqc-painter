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
    
    def transform(self, tr):
        for k in self.brush:
            self.brush[k].transform(tr)
        for k in self.collection:
            self.collection[k].transform(tr)
        for k in self.structure:
            self.structure[k].transform(tr)
        return self
        