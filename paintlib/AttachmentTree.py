# -*- coding: utf-8 -*-
import re
import json
from math import cos, sin, pi, tan, atan2, sqrt, ceil, floor

import pya

from .IO import IO
from .CavityBrush import CavityBrush
from .Painter import Component
from .BasicPainter import BasicPainter

class AttachmentTree(Component):

    def load(self, root, args={}):
        root=self.loadifjson(root)
        self.vars.update(args)
        self.loadvars(root["define"])
        self.walk(root["structure"])
        return self

    def attachAtBrush(self,root,brush,args={}):
        root=self.loadifjson(root)
        self.vars.update(args)
        self.vars.update({"widin":brush.widin,"widout":brush.widout})
        self.loadvars(root["define"])
        self.walk(root["structure"])
        self.transform(brush.DCplxTrans)
        return self

    def loadvars(self, defineList):
        for element in defineList:
            if element["id"] in self.vars:
                pass
            else:
                self.vars[element["id"]] = self.eval(element["value"])

    def addto(self, shape, collection):
        self.collection[collection] = self.collection.get(collection, pya.Region())
        self.collection[collection].insert(pya.Polygon.from_dpoly(shape))

    def walk(self, structures):
        self.xx = 0
        self.yy = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.traversal([{'type': 'attachment', 'side': 'ul', 'structure': structures}])

    def traversal(self, attachments):
        walker = self
        pos = [walker.xx, walker.yy]

        for attachment in attachments:
            if attachment["type"] != 'attachment':
                continue
            walker.xx =walker.x1 if attachment["side"][1] == 'l' else walker.x2
            walker.yy =walker.y1 if attachment["side"][0] == 'd' else walker.y2
            for structure in attachment["structure"]:
                if structure["type"] == 'structurenone':
                    continue
                pos12 = [walker.x1, walker.y1, walker.x2, walker.y2]
                if structure["type"] == 'structure':
                    width = walker.eval(structure["width"])
                    height = walker.eval(structure["height"])

                    walker.x1 =walker.xx - width if structure["side"][1] == 'l' else walker.xx
                    walker.y1 =walker.yy - height if structure["side"][0] == 'd' else walker.yy
                    walker.x2 = walker.x1 + width
                    walker.y2 = walker.y1 + height

                    walker.buildshape(structure["shape"], width, height, structure["collection"])
                else: # structure["type"] == 'structurefrompts'
                    ptsstr=re.split(r'[\s,]+', structure['points'])
                    pts=[]
                    walker.x1=walker.y1=float('inf')
                    walker.x2=walker.y2=float('-inf')
                    scale=walker.eval(structure['scale'])
                    while ptsstr:
                        xx=walker.xx+scale*walker.eval(ptsstr.pop(0))
                        yy=walker.yy+scale*walker.eval(ptsstr.pop(0))
                        walker.x1=min(walker.x1,xx)
                        walker.x2=max(walker.x2,xx)
                        walker.y1=min(walker.y1,yy)
                        walker.y2=max(walker.y2,yy)
                        if not structure['absolute']:
                            walker.xx=xx
                            walker.yy=yy
                        pts.append(pya.DPoint(xx,yy))
                    dshape=pya.DPolygon(pts)
                    walker.addto(dshape, structure['collection'])
                walker.traversal(structure["attachment"])
                [walker.x1,walker.y1,walker.x2,walker.y2]=pos12

        [walker.xx,walker.yy]=pos

    def buildshape(self, shape, width, height, collection):
        if shape["type"] == 'brush':
            self.brush[shape['brushid']]=CavityBrush(pointc=pya.DPoint((self.x1 + self.x2) / 2,(self.y1 + self.y2) / 2),angle=shape['angle'],widout=shape['widout'],widin=shape['widin'])
            return
        elif shape["type"] == 'arc':
            aa,bb,wbigger=height,width,True
            if width<height:
                aa,bb,wbigger=width,height,False
            radius=(bb**2/aa+aa)/2
            angle=atan2(bb,radius-aa)*180/pi
            ptsi = {'ul': 0, 'ur': 1, 'dr': 2, 'dl': 3}[shape["side"]]
            cases={
                (0,True):[pya.DPoint(self.x1, self.y2),pya.DPoint(self.x1, self.y1+radius),-90,-90+angle],
                (1,True):[pya.DPoint(self.x2, self.y2),pya.DPoint(self.x2, self.y1+radius),-90,-90-angle],
                (2,True):[pya.DPoint(self.x2, self.y1),pya.DPoint(self.x2, self.y2-radius),90,90+angle],
                (3,True):[pya.DPoint(self.x1, self.y1),pya.DPoint(self.x1, self.y2-radius),90,90-angle],
                (0,False):[pya.DPoint(self.x1, self.y2),pya.DPoint(self.x2-radius, self.y2),0,0-angle],
                (1,False):[pya.DPoint(self.x2, self.y2),pya.DPoint(self.x1+radius, self.y2),180,180+angle],
                (2,False):[pya.DPoint(self.x2, self.y1),pya.DPoint(self.x1+radius, self.y1),180,180-angle],
                (3,False):[pya.DPoint(self.x1, self.y1),pya.DPoint(self.x2-radius, self.y1),0,0+angle],
            }
            ptconner,ptcenter,angle0,angle1=cases[(ptsi,wbigger)]
            n = int(ceil(radius*angle*pi/180/IO.pointdistance)+2)
            arc=BasicPainter.arc(ptcenter, radius, n, angle0, angle1)
            arc.append(ptconner)
            
            dshape=pya.DPolygon(arc)
        elif shape["type"] == 'quadrilateral':
            dshape=pya.DPolygon([
                pya.DPoint(self.x1 + self.eval(shape['ul']),self.y2),
                pya.DPoint(self.x2,self.y2 - self.eval(shape['ur'])),
                pya.DPoint(self.x2 - self.eval(shape['dr']),self.y1),
                pya.DPoint(self.x1,self.y1 + self.eval(shape['dl'])),
            ])
        elif shape["type"] == 'quadrilateraldagger':
            dshape=pya.DPolygon([
                pya.DPoint(self.x2 - self.eval(shape['ur']),self.y2),
                pya.DPoint(self.x2,self.y1 + self.eval(shape['dr'])),
                pya.DPoint(self.x1 + self.eval(shape['dl']),self.y1),
                pya.DPoint(self.x1,self.y2 - self.eval(shape['ul'])),
            ])
        elif shape["type"] == 'triangle':
            pts = [
                pya.DPoint(self.x1,self.y2),
                pya.DPoint(self.x2,self.y2),
                pya.DPoint(self.x2,self.y1),
                pya.DPoint(self.x1,self.y1),
            ]*3
            ptsi = {'ul': 0, 'ur': 1, 'dr': 2, 'dl': 3}[shape["side"]]
            dshape=pya.DPolygon(pts[ptsi + 3:ptsi + 3 + 3])
        else:  # 'rectangle'
            dshape=pya.DPolygon([
                pya.DPoint(self.x1,self.y2),
                pya.DPoint(self.x2,self.y2),
                pya.DPoint(self.x2,self.y1),
                pya.DPoint(self.x1,self.y1),
            ])
        self.addto(dshape, collection)

