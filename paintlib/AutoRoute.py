# -*- coding: utf-8 -*-

from math import cos,sin,pi,tan,atan2,sqrt,ceil,floor
import queue

import pya
from .IO import IO
from .CavityPainter import CavityPainter
from .Collision import Collision
from .Interactive import Interactive

class AutoRoute:

    '''处理自动布线的类'''
    @staticmethod
    def _Rasterized(size, box, region):
        '''
        size
            double unit nm
        box
            pya.Box
        region
            pya.Region
        return
            area[x][y] :int[][]
            xyToAreaxy :lambda double,double:int,int
        '''
        dx = 0
        dy = 0
        dx = dx % size
        dy = dy % size
        left = ceil((box.left-dx)/size)
        bottom = ceil((box.bottom-dy)/size)
        right = floor((box.right-dx)/size)
        top = floor((box.top-dy)/size)
        x0 = left*size+dx
        y0 = bottom*size+dy
        area = []
        for ii in range(right-left):
            thisline = []
            for jj in range(top-bottom):
                x1 = x0+ii*size
                y1 = y0+jj*size
                check_box = pya.Box(x1, y1, x1+size, y1+size)
                empty = (pya.Region(check_box) & region).is_empty()
                thisline.append(0 if empty else 1)
            thisline[0] = 1
            thisline[-1] = 1
            area.append(thisline)
        area[0] = [1 for ii in area[0]]
        area[-1] = [1 for ii in area[-1]]

        def xyToAreaxy(px, py):
            px -= x0
            py -= y0
            if px < 0 or py < 0 or px > size*(right-left) or py > size*(top-bottom):
                return -1, -1
            return floor(px/size), floor(py/size)

        def areaxyToXy(x, y):
            return x0+(x+0.5)*size, y0+(y+0.5)*size
        return area, xyToAreaxy, areaxyToXy

    @staticmethod
    def _brushToPair(xyToAreaxy, brushs, area, size):
        pairs0 = []
        pairs = []
        for brush12 in brushs:
            pairs0.append([xyToAreaxy(brush.centerx, brush.centery)
                           for brush in brush12])
            tmp_pair = []
            for brush in brush12:
                tmp_painter = CavityPainter(brush)
                tmp_painter.Run('s'+str(size))
                tmp_brush = tmp_painter.brush
                tmp_pair.append(xyToAreaxy(
                    tmp_brush.centerx, tmp_brush.centery))
            pairs.append(tmp_pair)
        BIGNUMBERPID = 2**20
        for issource,pairs_ in [(False,pairs), (True,pairs0)]:
            for pid, pair in enumerate(pairs_):
                for is1, pt in enumerate(pair, 1):
                    px, py = pt
                    if area[px][py] >= BIGNUMBERPID and not issource:
                        estr = 'conflict, pair '+str(pid)
                        pya.MessageBox.warning(
                            "paintlib.AutoRoute._brushToPair", "Error : "+estr, pya.MessageBox.Ok)
                        return [], estr
                    area[px][py] = is1*BIGNUMBERPID+pid
        return pairs, ''

    @staticmethod
    def _BFSTwoPoint(area, pair):
        '''
        ul u ur
        l    r
        dl d dr
        2 6 3
        8   9
        4 7 5
        '''
        marks = [2, 3, 4, 5, 6, 7, 8, 9]
        ul, ur, dl, dr, u, d, l, r = marks
        BIGNUMBERPID = 2**20
        for vx in area:
            for y, v in enumerate(vx):
                if v in marks:
                    vx[y] = 0
        area[pair[1][0]][pair[1][1]] = 0

        def unvaild(v):
            return v == 1 or v > 9
        q = queue.Queue()
        q.put((0, pair[0]))
        while not q.empty():
            mdistance, pt = q.get()
            px, py = pt
            if pt == pair[1]:
                pair.append(-mdistance)
                mark = area[px][py]
                area[px][py] = area[pair[0][0]][pair[0][1]]+BIGNUMBERPID
                return mark
            for mark, dx, dy in zip([u, d, l, r], [0, 0, -1, 1], [1, -1, 0, 0]):
                if area[px+dx][py+dy] != 0:
                    continue
                area[px+dx][py+dy] = mark
                q.put((mdistance-1, (px+dx, py+dy)))
            for mark, dx, dy in zip([ul, ur, dl, dr], [-1, 1, -1, 1], [1, 1, -1, -1]):
                if area[px+dx][py+dy] != 0:
                    continue
                if unvaild(area[px+dx][py]) and unvaild(area[px][py+dy]):
                    continue
                area[px+dx][py+dy] = mark
                q.put((mdistance-1.4142135623730951, (px+dx, py+dy)))
        area[pair[1][0]][pair[1][1]] = area[pair[0][0]][pair[0][1]]+BIGNUMBERPID
        return 0

    @staticmethod
    def _BFSLinkAllToCheckAndDistance(area, pairs):
        for pid, pair in enumerate(pairs):
            print('paintlib.AutoRoute._BFSLinkAllToCheckAndDistance:',
                  'linking pair', pid)
            if AutoRoute._BFSTwoPoint(area, pair) == 0:
                estr = 'can not link, pair '+str(pid)
                pya.MessageBox.warning(
                    "paintlib.AutoRoute._BFSLinkAllToCheckAndDistance", "Error : "+estr, pya.MessageBox.Ok)
                return estr
        return ''

    @staticmethod
    def _orderDistance(pairs):
        order = sorted(list(enumerate(pairs)), key=lambda x: x[1][2])
        return [arr[0] for arr in order]

    @staticmethod
    def _backtrace(direct, pair, area):
        '''
        ul u ur
        l    r
        dl d dr
        2 6 3
        8   9
        4 7 5
        '''
        dxdy = [
            0, 1,
            (-1, 1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (0, 1),
            (0, -1),
            (-1, 0),
            (1, 0),
        ]
        px, py = pair[1]
        line = [(px, py)]
        rmark = area[pair[0][0]][pair[0][1]]
        while (px, py) != pair[0]:
            area[px][py] = rmark
            dx, dy = dxdy[direct]
            px -= dx
            py -= dy
            line.append((px, py))
            direct = area[px][py]
        return line[::-1]

    @staticmethod
    def _linkInArea(area, pairs, order):
        lines = list(range(len(order)))
        for ii in order:
            print('paintlib.AutoRoute._linkInArea:', 'linking pair', ii)
            pair = pairs[ii]
            while len(pair) > 2:
                pair.pop()
            direct = AutoRoute._BFSTwoPoint(area, pair)
            if direct == 0:
                estr = 'can not link, pair '+str(ii)
                pya.MessageBox.warning(
                    "paintlib.AutoRoute._linkInArea", "Error : "+estr, pya.MessageBox.Ok)
                return estr, []
            lines[ii] = AutoRoute._backtrace(direct, pair, area)
        return '', lines

    @staticmethod
    def _linkLine(cell, layer, line, brush12, areaxyToXy):
        spts = [pya.DPoint(areaxyToXy(x, y)[0], areaxyToXy(x, y)[1])
                for x, y in line[::-1]]
        pathstr = Interactive.link(
            brush1=brush12[1], brush2=brush12[0], spts=spts, print_=False)
        if not pathstr:
            return 'link line fail', 0,pathstr
        if type(cell)!=type(None) and type(layer)!=type(None):
            length=Interactive._show_path(cell, layer, brush12[1], pathstr)
        else:
            length=0
        return '', length, pathstr

    @staticmethod
    def autoRoute(cell, layer, size, cellList, brushs, layerList=None, box=None, layermod='not in', order=None):
        brushs=[[b2,b1] for b1,b2 in brushs]
        if type(box)==type(None):box=Interactive._box_selected()
        if not box:raise RuntimeError('no box set')
        outregion, inregion = Collision.getShapesFromCellAndLayer(
            cellList, layerList=layerList, box=box, layermod=layermod)
        region = outregion & inregion
        area, xyToAreaxy, areaxyToXy = AutoRoute._Rasterized(size, box, region)
        pairs, checkresult = AutoRoute._brushToPair(
            xyToAreaxy, brushs, area, size)
        if checkresult != '':
            return checkresult, [], []
        if order == None:
            order = list(range(len(brushs)))
        elif order == ['distance']:
            checkresult = AutoRoute._BFSLinkAllToCheckAndDistance(area, pairs)
            if checkresult != '':
                return checkresult, [], []
            order = AutoRoute._orderDistance(pairs)
        checkresult, lines = AutoRoute._linkInArea(area, pairs, order)
        if checkresult != '':
            return checkresult, [], []
        lengths = []
        paths=[]
        for line, brush12 in zip(lines, brushs):
            checkresult, length, pathstr = AutoRoute._linkLine(
                cell, layer, line, brush12, areaxyToXy)
            if checkresult:
                return checkresult, [], []
            lengths.append(length)
            paths.append(pathstr)
        return '', lengths, paths

    @staticmethod
    def linkTwoBrush(brush1,brush2,size=150000,enlargesize=600000,layerList=None, box=None,layermod='not in',cellList=None):
        if type(box)==type(None):
            ppp='r{size},180 r{size2},180 r{size2},180'.format(size=enlargesize/2,size2=enlargesize)
            painter=CavityPainter(brush1)
            painter.Run(ppp)
            region=painter.Output_Region()
            painter=CavityPainter(brush2)
            painter.Run(ppp)
            region=region + painter.Output_Region()
            box=region.bbox()
        if cellList==None:
            cellList=[IO.top]
        err,_,paths=AutoRoute.autoRoute(cell=None, layer=None, size=size, cellList=cellList, brushs=[[brush1,brush2]], layerList=layerList, box=box, layermod='not in', order=None)
        if err:raise RuntimeError(err)
        return paths[0]