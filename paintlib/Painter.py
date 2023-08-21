# -*- coding: utf-8 -*-
import re

class Painter(object):
    pass

class Component(object):
    def __init__(self):
        self.collection = {}
        self.brush = {}
        self.vars = {}
        self.trace = {}
        self.structure = {}

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
        