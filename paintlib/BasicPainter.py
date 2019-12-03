# -*- coding: utf-8 -*-
import pya
from math import cos, sin, pi, tan, atan2, sqrt, ceil, floor

from .CavityBrush import CavityBrush


class BasicPainter:
    '''用于画基础图形的静态类'''
    @staticmethod
    def rectangle(pointr, pointl, length):
        '''
        给定矩形的右下pointr左下pointl画出指定长度矩形
        pointr,pointl,pointl2,pointr2        
        x1,y1,x2,y2,length,path
        '''
        delta = pointr.distance(pointl)
        xx = length/delta*(pointl.y-pointr.y)
        yy = length/delta*(pointr.x-pointl.x)
        pointl2 = pya.DPoint(pointl.x+xx, pointl.y+yy)
        pointr2 = pya.DPoint(pointr.x+xx, pointr.y+yy)
        rectangle1 = pya.DPolygon([pointr, pointl, pointl2, pointr2])
        return rectangle1, pointr2, pointl2

    @staticmethod
    def arc(point0, r, n, angle0, angle1):
        angles = [angle0+1.0*x/(n-1)*(angle1-angle0) for x in range(n)]
        arcpointlist = [pya.DPoint(
            point0.x+r*cos(angle*pi/180), point0.y+r*sin(angle*pi/180)) for angle in angles]
        return arcpointlist

    @staticmethod
    def thickarc(point0, rr, rl, n, angle0, angle1):
        thickarcpointlist = []
        thickarcpointlist.extend(
            BasicPainter.arc(point0, rr, n, angle0, angle1))
        thickarcpointlist.extend(
            BasicPainter.arc(point0, rl, n, angle1, angle0))
        thickarc1 = pya.DPolygon(thickarcpointlist)
        return thickarc1, thickarcpointlist[n-1], thickarcpointlist[n]

    @staticmethod
    def NewtonInterpolation(X, Y, high):
        n = len(X)
        a = [Y[0]]
        d = []
        for j in range(n-1):
            d2 = d
            if j == 0:
                d2 = Y
            d = []
            for k in range(n-1-j):
                if X[k+j+1] == X[k]:
                    d.append(high.pop(0))
                else:
                    d.append((d2[k+1]-d2[k])/(X[k+j+1]-X[k]))
            a.append(d[0])

        def f(x):
            y = a[0]
            Df = 1.0
            for j in range(1, n):
                Df *= (x-X[j-1])
                y += a[j]*Df
            return y
        return f

    @staticmethod
    def arc_NewtonInterpolation(n, r1):  # (n,r1,r2):
        #
        thetax = 0.53977
        thetay = -thetax*tan(pi/180*67.5)
        X = [-1, -1, -1, -thetax, 0, thetax, 1, 1, 1]
        Y = [-1, -1, -1, thetay, -sqrt(2), thetay, -1, -1, -1]
        high = [-1, -1, 1, 1,   0, 0]
        #
        # theta=-1.34
        # X=[-1,-1,-1, 0   , 1, 1, 1]
        # Y=[-1,-1,-1,theta,-1,-1,-1]
        # high=[-1,-1,1,1,    0,0]
        #
        f = BasicPainter.NewtonInterpolation(X, Y, high)
        pts1 = [pya.DPoint((-1.0+2.0/(n-1)*i)/sqrt(2)*r1,
                           f(-1.0+2.0/(n-1)*i)/sqrt(2)*r1) for i in range(n)]
        return pts1

    @staticmethod
    def Border(leng=3050000, siz=3050000, wed=50000):
        polygons = []
        pts = [pya.Point(-siz, -siz), pya.Point(-siz+leng, -
                                                siz), pya.Point(-siz+leng, -siz+wed)]
        pts.extend([pya.Point(-siz+wed, -siz+wed), pya.Point(-siz +
                                                             wed, -siz+leng), pya.Point(-siz, -siz+leng)])
        polygon1 = pya.Polygon(pts)
        polygons.append(polygon1)
        polygons.append(polygon1.transformed(pya.Trans(pya.Trans.R90)))
        polygons.append(polygon1.transformed(pya.Trans(pya.Trans.R180)))
        polygons.append(polygon1.transformed(pya.Trans(pya.Trans.R270)))
        return pya.Region(polygons)

    @staticmethod
    def Electrode(*args, **keys):
        if 'brush' in keys or isinstance(args[0], CavityBrush):
            return BasicPainter.Electrode_2(*args, **keys)
        elif 'angle' in keys or (type(args[0]) in [int, float]):
            return BasicPainter.Electrode_1(*args, **keys)
        else:
            raise TypeError('Invalid input')
        return []

    @staticmethod
    def Electrode_1(x, y, angle, widout=20000, widin=10000, wid=368000, length=360000, midwid=200000, midlength=200000, narrowlength=120000):
        tr = pya.DCplxTrans(1, angle, False, x, y)
        pts = []
        pts.append(pya.DPoint(0, widout/2))
        pts.append(pya.DPoint(0, widin/2))
        pts.append(pya.DPoint(narrowlength, midwid/2))
        pts.append(pya.DPoint(narrowlength+midlength, midwid/2))
        pts.append(pya.DPoint(narrowlength+midlength, -midwid/2))
        pts.append(pya.DPoint(narrowlength, -midwid/2))
        pts.append(pya.DPoint(0, -widin/2))
        pts.append(pya.DPoint(0, -widout/2))
        pts.append(pya.DPoint(narrowlength, -wid/2))
        pts.append(pya.DPoint(length, -wid/2))
        pts.append(pya.DPoint(length, wid/2))
        pts.append(pya.DPoint(narrowlength, wid/2))
        polygon1 = pya.DPolygon(pts).transformed(tr)
        return polygon1

    @staticmethod
    def Electrode_2(brush, wid=368000, length=360000, midwid=200000, midlength=200000, narrowlength=120000):
        widout = brush.widout
        widin = brush.widin
        tr = brush.DCplxTrans
        pts = []
        pts.append(pya.DPoint(0, widout/2))
        pts.append(pya.DPoint(0, widin/2))
        pts.append(pya.DPoint(narrowlength, midwid/2))
        pts.append(pya.DPoint(narrowlength+midlength, midwid/2))
        pts.append(pya.DPoint(narrowlength+midlength, -midwid/2))
        pts.append(pya.DPoint(narrowlength, -midwid/2))
        pts.append(pya.DPoint(0, -widin/2))
        pts.append(pya.DPoint(0, -widout/2))
        pts.append(pya.DPoint(narrowlength, -wid/2))
        pts.append(pya.DPoint(length, -wid/2))
        pts.append(pya.DPoint(length, wid/2))
        pts.append(pya.DPoint(narrowlength, wid/2))
        polygon1 = pya.DPolygon(pts).transformed(tr)
        return polygon1

    @staticmethod
    def Connection(x, widin=16000, widout=114000, linewid=5000, slength1=16000, slength2=16000, clength=30000, cwid=54000, y=0, angle=0):
        if isinstance(x, CavityBrush):
            brush = x
            tr = brush.DCplxTrans
        else:
            tr = pya.DCplxTrans(1, angle, False, x, y)
        pts = [
            pya.DPoint(0, widin/2),
            pya.DPoint(slength1, widin/2),
            pya.DPoint(slength1, widout/2-linewid),
            pya.DPoint(slength1+slength2+clength, widout/2-linewid),
            pya.DPoint(slength1+slength2+clength, cwid/2+linewid),
            pya.DPoint(slength1+slength2, cwid/2+linewid),
            #
            pya.DPoint(slength1+slength2, -(cwid/2+linewid)),
            pya.DPoint(slength1+slength2+clength, -(cwid/2+linewid)),
            pya.DPoint(slength1+slength2+clength, -(widout/2-linewid)),
            pya.DPoint(slength1, -(widout/2-linewid)),
            pya.DPoint(slength1, -widin/2),
            pya.DPoint(0, -widin/2),
            #
            pya.DPoint(0, -widout/2),
            pya.DPoint(slength1+slength2+clength+linewid, -widout/2),
            pya.DPoint(slength1+slength2+clength+linewid, -cwid/2),
            pya.DPoint(slength1+slength2+linewid, -cwid/2),
            #
            pya.DPoint(slength1+slength2+linewid, cwid/2),
            pya.DPoint(slength1+slength2+clength+linewid, cwid/2),
            pya.DPoint(slength1+slength2+clength+linewid, widout/2),
            pya.DPoint(0, widout/2),
        ]
        polygon1 = pya.DPolygon(pts).transformed(tr)
        return polygon1

    @staticmethod
    def Draw(cell, layer, x):
        if isinstance(x, pya.DPolygon):
            cell.shapes(layer).insert(pya.Polygon.from_dpoly(x))
        else:
            cell.shapes(layer).insert(x)
    # paintlib.BasicPainter.Draw(cell,layer,x)
