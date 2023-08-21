# -*- coding: utf-8 -*-

import re
from math import cos, sin, pi, tan, atan2, sqrt, ceil, floor

import pya

from .IO import IO
from .CavityBrush import CavityBrush
from .Painter import Painter
from .BasicPainter import BasicPainter


class TraceRunnerClass:
    patternNames = ['straight', 'turning', 'repeatStart', 'repeatEnd']

    straight_pattern = re.compile(r'^s_?(-?\d+\.?\d*)')
    turning_pattern = re.compile(r'^(l|r|t)_?(-?\d+\.?\d*)(?:,(-?\d+\.?\d*))?')
    repeatStart_pattern = re.compile(r'^n(\d+)\[')
    repeatEnd_pattern = re.compile(r'^\]')

    straight = 'straight'
    turning = 'turning'
    repeatStart = 'repeatStart'
    repeatEnd = 'repeatEnd'

    top = 'top'

    def __init__(self):
        self.Node.tr = self
        self.patterns = {}
        for name in self.patternNames:
            self.patterns[name] = self.__getattribute__(name+'_pattern')

    def getPathFunction(self, rawString):
        AST = self.buildAST(rawString)
        pathString = self.traversalAST(AST)
        localscope = {'path': None}
        exec(pathString, None, localscope)
        self.pathFunction = localscope['path']
        return self.pathFunction

    def buildAST(self, rawString):
        self.rawString = rawString
        self.string = self.preConvert(rawString)
        self.start = 0
        self.AST = self.Node(isTop=True, type=self.top)
        self.currentNode = self.AST
        self.parse()
        if self.currentNode.type != self.top:
            raise RuntimeError('barket not match')
        return self.AST

    def preConvert(self, rawString):
        string = re.sub(r'\s', '', rawString)
        return string

    class Node:
        def __init__(self, isTop=False, parentNode=None, **k):
            self.children = []
            self.isTop = isTop
            if parentNode == None and not isTop:
                parentNode = self.tr.currentNode
            self.parentNode = parentNode
            if parentNode:
                parentNode.addChild(self)
            for key, value in k.items():
                self.__setattr__(key, value)

        def addChild(self, node):
            self.children.append(node)

        def getChildren(self):
            return self.children

    def parse(self):
        match = None
        patternName = ''
        currentString = self.string[self.start:]
        if not currentString:
            return
        for name in self.patternNames:
            match = self.patterns[name].match(currentString)
            if match:
                patternName = name
                break
        if match == None:
            raise RuntimeError('invaild trace at '+currentString)
        if patternName == self.repeatStart:
            times = int(match.group(1))
            node = self.Node(match=match, type=patternName, times=times)
            self.currentNode = node
        if patternName == self.repeatEnd:
            self.currentNode = self.currentNode.parentNode
            if self.currentNode == None:
                raise RuntimeError('barket not match at '+currentString)
            node = self.Node(match=match, type=patternName)
        if patternName == self.straight:
            length = float(match.group(1))
            enableMinus = '_' in match.group(0)
            node = self.Node(match=match, type=patternName,
                             length=length, enableMinus=enableMinus)
        if patternName == self.turning:
            left = -1 if match.group(1) == 'l' else 1
            radius = float(match.group(2))
            angle = match.group(3)
            angle = 90.0 if angle == None else float(angle)
            enableMinus = '_' in match.group(0)
            node = self.Node(match=match, type=patternName, left=left,
                             radius=radius, angle=angle, enableMinus=enableMinus)
        self.start += len(match.group(0))
        self.parse()

    def traversalAST(self, AST):
        output = []
        prefix = ['']

        def pushln(s):
            output.append(prefix[0]+s+'\n')

        def cpre(n=4):
            if n > 0:
                prefix[0] = prefix[0]+' '*n
            if n < 0:
                prefix[0] = prefix[0][0:-1*n]

        def npre():
            return len(prefix[0])
        pushln('def path(painter):')
        cpre()
        pushln('length=0')

        def traversal(node):
            if node.type == self.top:
                for cn in node.getChildren():
                    traversal(cn)
            if node.type == self.straight:
                pushln('length+=painter.{minus}Straight({length})'.format(
                    minus='_'if node.enableMinus else '', length=node.length))
            if node.type == self.turning:
                pushln('length+=painter.Turning({radius},{angle})'.format(
                    radius=node.left*node.radius, angle=node.angle))
            if node.type == self.repeatStart:
                pushln('for _index{n} in range({times}):'.format(
                    n=npre(), times=node.times))
                cpre()
                for cn in node.getChildren():
                    traversal(cn)
            if node.type == self.repeatEnd:
                cpre(-4)

        traversal(AST)
        pushln('return length')
        self.pathString = ''.join(output)
        return self.pathString

    def reversePath(self, rawString):
        AST = self.buildAST(rawString)
        pathString = self.traversalAST_reversePath(AST)
        return pathString

    def traversalAST_reversePath(self, AST):
        output = ['']

        def push(s):
            output.append(s)

        def traversal(node):
            if node.type == self.top:
                for cn in node.getChildren()[::-1]:
                    traversal(cn)
            if node.type == self.straight:
                push('s {minus} {length} '.format(
                    minus='_'if node.enableMinus else '', length=node.length))
            if node.type == self.turning:
                push('t {radius},{angle} '.format(
                    radius=-node.left*node.radius, angle=node.angle))
            if node.type == self.repeatStart:
                push('n{times}[ '.format(times=node.times))
                for cn in node.getChildren()[::-1]:
                    traversal(cn)
                push('] ')
            if node.type == self.repeatEnd:
                pass
        traversal(AST)
        self.pathString = ''.join(output)
        return self.pathString

    def mirrorPath(self, rawString):
        AST = self.buildAST(rawString)
        pathString = self.traversalAST_mirrorPath(AST)
        return pathString

    def traversalAST_mirrorPath(self, AST):
        output = ['']

        def push(s):
            output.append(s)

        def traversal(node):
            if node.type == self.top:
                for cn in node.getChildren():
                    traversal(cn)
            if node.type == self.straight:
                push('s {minus} {length} '.format(
                    minus='_'if node.enableMinus else '', length=node.length))
            if node.type == self.turning:
                push('t {radius},{angle} '.format(
                    radius=-node.left*node.radius, angle=node.angle))
            if node.type == self.repeatStart:
                push('n{times}[ '.format(times=node.times))
                for cn in node.getChildren():
                    traversal(cn)
                push('] ')
            if node.type == self.repeatEnd:
                pass
        traversal(AST)
        self.pathString = ''.join(output)
        return self.pathString

    def calculatePath(self, rawString, a=0, b=None):
        '''
        计算一个路径的长度,
        如果b不为None, 也返回从长度a到长度b之间的路径(还需要函数外部手动检查一下length是否大于想要的b)
        这两个功能本来应该用两个函数分别实现以提高效率, 懒得拆开了
        > print(paintlib.TraceRunner.calculatePath('n3[s1000t50000,360]',800,9700))
        '''
        AST = self.buildAST(rawString)
        length, pathString = self.traversalAST_calculatePath(AST, a=a, b=b)
        if b==None:
            return length
        return length, pathString

    def traversalAST_calculatePath(self, AST, a=0, b=None):
        if b==None:
            b=float('inf')
        output = ['']
        pathLength = [0]

        def saveRate(before,after):
            if before>=after:
                return 1
            if before>=b or after<=a:
                return 0
            if before<=a<=after<=b:
                return (after-a)/(after-before)
            if a<=before<=b<=after:
                return (b-before)/(after-before)
            if before<=a<=b<=after:
                return (b-a)/(after-before)
            return 1

        def push(s):
            output.append(s)

        def traversal(node):
            if node.type == self.top:
                for cn in node.getChildren():
                    traversal(cn)
            if node.type == self.straight:
                tolength=pathLength[0]+node.length
                sr=saveRate(pathLength[0],tolength)
                if sr!=0:
                    push('s {minus} {length} '.format(
                    minus='_'if node.enableMinus else '', length=node.length*sr))

                pathLength[0]=tolength
            if node.type == self.turning:
                tolength=pathLength[0]+pi*abs(node.angle)/180*abs(node.radius)
                sr=saveRate(pathLength[0],tolength)
                if sr!=0:
                    push('t {radius},{angle} '.format(
                    radius=node.left*node.radius, angle=node.angle*sr))
                    
                pathLength[0]=tolength
            if node.type == self.repeatStart:
                for repeatii in range(node.times):
                    for cn in node.getChildren():
                        traversal(cn)
            if node.type == self.repeatEnd:
                pass
        traversal(AST)
        self.pathString = ''.join(output)
        return pathLength[0], self.pathString
    
    def getPathFunction_withMarkTurning(self, rawString):
        AST = self.buildAST(rawString)
        pathString = self.traversalAST_withMarkTurning(AST)
        localscope = {'path': None}
        exec(pathString, None, localscope)
        self.pathFunction = localscope['path']
        return self.pathFunction

    def traversalAST_withMarkTurning(self, AST):
        output = []
        prefix = ['']

        def pushln(s):
            output.append(prefix[0]+s+'\n')

        def cpre(n=4):
            if n > 0:
                prefix[0] = prefix[0]+' '*n
            if n < 0:
                prefix[0] = prefix[0][0:-1*n]

        def npre():
            return len(prefix[0])
        pushln('def path(painter):')
        cpre()
        pushln('length=0')

        def traversal(node):
            if node.type == self.top:
                for cn in node.getChildren():
                    traversal(cn)
            if node.type == self.straight:
                pushln('length+=painter.{minus}Straight({length})'.format(
                    minus='_'if node.enableMinus else '', length=node.length))
            if node.type == self.turning:
                pushln('painter.Markpoint()')
                pushln('length+=painter.Turning({radius},{angle})'.format(
                    radius=node.left*node.radius, angle=node.angle))
                pushln('painter.Markpoint()')
            if node.type == self.repeatStart:
                pushln('for _index{n} in range({times}):'.format(
                    n=npre(), times=node.times))
                cpre()
                for cn in node.getChildren():
                    traversal(cn)
            if node.type == self.repeatEnd:
                cpre(-4)

        traversal(AST)
        pushln('return length')
        self.pathString = ''.join(output)
        return self.pathString

TraceRunner = TraceRunnerClass()


class LinePainter(Painter):
    def __init__(self, pointl=pya.DPoint(0, 1000), pointr=pya.DPoint(0, 0)):
        '''沿着前进方向，右边pointr，左边pointl'''
        self.outputlist = []
        self.pointr = pointr
        self.pointl = pointl
        # pointdistance=IO.pointdistance
        self.centerlinepts = []
        self.marks = []
        self.warning = True

    def Setpoint(self, pointl=pya.DPoint(0, 1000), pointr=pya.DPoint(0, 0)):
        self.pointr = pointr
        self.pointl = pointl
        self.centerlinepts = []
        self.outputlist = []
        self.marks = []

    def Markpoint(self):
        self.marks.append([self.pointl,self.pointr])

    def Straight(self, length, centerline=True):
        if length < -10 and self.warning and IO.warning.minus_stright:
            IO.warning.warning("paintlib.LinePainter.Straight",
                               'Straight negative value', pya.MessageBox.Ok)
        return self._Straight(length, centerline=centerline)

    def Turning(self, radius, angle=90):
        if (angle < -361 or angle > 361) and self.warning and IO.warning.big_angle_turning:
            IO.warning.warning("paintlib.LinePainter.Turning",
                               'Turning angle more than 360 degree', pya.MessageBox.Ok)
        return self.TurningArc(radius, angle)

    def _Straight(self, length, centerline=False):
        n = int(ceil(length/IO.pointdistance))+2
        if n == 1:
            n = 2
        n *= IO.centerlineratio
        p1x = self.pointr.x/2+self.pointl.x/2
        p1y = self.pointr.y/2+self.pointl.y/2
        # 接下来是画矩形，再之后是画中心线
        # 修复1nm线的bug
        rectangle1, _, _ = BasicPainter.rectangle(
            self.pointr, self.pointl, length+2*(length > 0)-2*(length < 0))
        _, self.pointr, self.pointl = BasicPainter.rectangle(
            self.pointr, self.pointl, length)
        self.outputlist.append(rectangle1)
        #
        dx = self.pointr.x/2+self.pointl.x/2-p1x
        dy = self.pointr.y/2+self.pointl.y/2-p1y
        cpts = [pya.DPoint(p1x+1.0*pt/(n-1)*dx, p1y+1.0*pt/(n-1)*dy)
                for pt in range(n)]
        if centerline:
            if self.centerlinepts == []:
                self.centerlinepts = cpts
            else:
                self.centerlinepts.extend(cpts[1:])
        return length

    def TurningArc(self, radius, angle=90):
        '''radius非负向右，负是向左'''
        if angle < 0:
            angle = -angle
            radius = -radius
        delta = self.pointr.distance(self.pointl)
        dx = (self.pointr.x-self.pointl.x)/delta
        dy = (self.pointr.y-self.pointl.y)/delta
        dtheta = atan2(dy, dx)*180/pi
        centerx = self.pointr.x+(radius-delta/2)*dx
        centery = self.pointr.y+(radius-delta/2)*dy
        center = pya.DPoint(centerx, centery)
        n = int(ceil((abs(radius)+delta/2)*angle*pi/180/IO.pointdistance)+2)
        if radius >= 0:
            thickarc1, pointr2, pointl2 = BasicPainter.thickarc(
                center, radius-delta/2, radius+delta/2, n, dtheta+180, dtheta+180-angle)
            cpts = BasicPainter.arc(
                center, radius, n*IO.centerlineratio, dtheta+180, dtheta+180-angle)
        else:
            thickarc1, pointr2, pointl2 = BasicPainter.thickarc(
                center, -radius+delta/2, -radius-delta/2, n, dtheta, dtheta+angle)
            cpts = BasicPainter.arc(
                center, -radius, n*IO.centerlineratio, dtheta, dtheta+angle)
        self.outputlist.append(thickarc1)
        self.pointr = pointr2
        self.pointl = pointl2
        if self.centerlinepts == []:
            self.centerlinepts = cpts
        else:
            self.centerlinepts.extend(cpts[1:])
        # 修复1nm线的bug
        self._Straight(2)
        self._Straight(-2)
        return pi*angle/180*abs(radius)

    def TurningInterpolation(self, radius, angle=90):  # 有待改进
        '''radius非负向右，负是向左'''
        pass
        if angle < 0:
            angle = -angle
            radius = -radius
        angle = 90
        delta = self.pointr.distance(self.pointl)
        dx = (self.pointr.x-self.pointl.x)/delta
        dy = (self.pointr.y-self.pointl.y)/delta
        dtheta = atan2(dy, dx)*180/pi
        centerx = self.pointr.x+(radius-delta/2)*dx
        centery = self.pointr.y+(radius-delta/2)*dy
        n = int(ceil(1.3*(abs(radius)+delta/2)*angle*pi/180/IO.pointdistance)+2)
        #
        rsgn = (radius > 0)-(radius < 0)
        pointr2 = pya.DPoint(centerx-rsgn*(radius-delta/2)
                             * dy, centery+rsgn*(radius-delta/2)*dx)
        pointl2 = pya.DPoint(centerx-rsgn*(radius+delta/2)
                             * dy, centery+rsgn*(radius+delta/2)*dx)
        pts1 = BasicPainter.arc_NewtonInterpolation(n, abs(radius)+delta/2)
        pts2 = BasicPainter.arc_NewtonInterpolation(n, abs(radius)-delta/2)
        pts1.extend(reversed(pts2))
        arc1 = pya.DPolygon(pts1)
        trans = pya.DCplxTrans(1, 180+dtheta+45*rsgn, False, centerx, centery)
        arc1.transform(trans)
        self.outputlist.append(arc1)
        self.pointr = pointr2
        self.pointl = pointl2
        pts3 = BasicPainter.arc_NewtonInterpolation(n, abs(radius))
        cpts = [pya.DEdge(pya.DPoint(), pt).transformed(
            trans).p2 for pt in pts3]
        if abs(cpts[-1].distance(self.pointr)-delta/2) < IO.pointdistance:
            if self.centerlinepts == []:
                self.centerlinepts = cpts
            else:
                self.centerlinepts.extend(cpts[1:])
        else:
            if self.centerlinepts == []:
                self.centerlinepts = cpts[::-1]
            else:
                self.centerlinepts.extend(cpts[-2::-1])
        return pi*0.5*abs(radius)

    def Draw(self, cell, layer):
        for x in self.outputlist:
            if isinstance(x, pya.DPolygon):
                cell.shapes(layer).insert(pya.Polygon.from_dpoly(x))
            else:
                cell.shapes(layer).insert(x)
        self.outputlist = []

    def Output_Region(self):
        polygons = []
        for x in self.outputlist:
            if isinstance(x, pya.DPolygon):
                polygons.append(pya.Polygon.from_dpoly(x))
        self.outputlist = []
        return pya.Region(polygons)

    def Getcenterline(self):
        cpts = self.centerlinepts
        self.centerlinepts = []
        return cpts


class CavityPainter(Painter):
    def __init__(self, *args, **keys):
        if 'pointc' in keys or (isinstance(args[0], pya.DPoint) and ('angle' in keys or type(args[1]) in [int, float])):
            self.constructors1(*args, **keys)
        elif 'brush' in keys or isinstance(args[0], CavityBrush):
            self.constructors2(*args, **keys)
        else:
            raise TypeError('Invalid input')

    def constructors1(self, pointc=pya.DPoint(0, 8000), angle=0, widout=20000, widin=10000, bgn_ext=0, end_ext=0):
        self.__init__(CavityBrush(
            pointc, angle, widout, widin, bgn_ext), end_ext)

    def constructors2(self, brush, end_ext=0):
        self.regionlistout = []
        self.regionlistin = []
        self.path = lambda painter: None
        self.bgn_ext = brush.bgn_ext
        self.end_ext = end_ext
        edgeout = brush.edgeout
        edgein = brush.edgein
        self.painterout = LinePainter(edgeout.p1, edgeout.p2)
        self.painterin = LinePainter(edgein.p1, edgein.p2)
        self.centerlineinfos = []

    @property
    def brush(self):
        return CavityBrush(self.painterout.pointl, self.painterin.pointl, self.painterin.pointr, self.painterout.pointr)

    def Getinfo(self):
        ''' return [centerx,centery,angle,widout] '''
        return self.brush.Getinfo()

    def Run(self, path=None):
        if path == None:
            pathFunction = self.path
        elif hasattr(path, '__call__'):
            pathFunction = path
        else:  # type(path)==str
            pathFunction = TraceRunner.getPathFunction(path)
        # 修复1nm线的bug
        self.painterout._Straight(-0.414)
        self.painterout._Straight(0.414)
        self.painterout.Straight(self.bgn_ext)
        pathFunction(self.painterout)
        self.painterout.Straight(self.end_ext)
        self.painterout._Straight(0.414)
        self.painterout._Straight(-0.414)
        self.painterout._Straight(-self.end_ext)
        self.regionlistout.extend(self.painterout.outputlist)
        self.painterout.outputlist = []
        self.bgn_ext = 0
        self.end_ext = 0
        # 修复1nm线的bug
        self.painterin._Straight(-2.414)
        self.painterin._Straight(2.414)
        result = pathFunction(self.painterin)
        self.painterin._Straight(2.414)
        self.painterin._Straight(-2.414)
        self.regionlistin.extend(self.painterin.outputlist)
        self.painterin.outputlist = []
        # 把中心线的(点列表,笔刷)成组添加
        self.centerlineinfos.append(
            (self.painterin.Getcenterline(), self.brush))
        #
        self._length=result
        return result

    def Electrode(self, wid=368000, length=360000, midwid=200000, midlength=200000, narrowlength=120000, reverse=False):
        assert((reverse == False and self.end_ext == 0)
               or (reverse == True and self.bgn_ext == 0))
        brush = self.brush.reversed() if reverse else self.brush
        polygon = BasicPainter.Electrode(
            brush, wid=wid, length=length, midwid=midwid, midlength=midlength, narrowlength=narrowlength)
        self.regionlistout.append(polygon)

    def Connection(self, clength=30000, cwid=54000, widout=114000, linewid=5000, slength1=16000, slength2=16000, reverse=False):
        assert((reverse == False and self.end_ext == 0)
               or (reverse == True and self.bgn_ext == 0))
        brush = self.brush.reversed() if reverse else self.brush
        polygon = BasicPainter.Connection(brush, widin=brush.widin, widout=widout,
                                          linewid=linewid, slength1=slength1, slength2=slength2, clength=clength, cwid=cwid)
        self.regionlistout.append(polygon)

    def Narrow(self, widout, widin, length=6000):
        assert(self.end_ext == 0 and self.bgn_ext == 0)
        tr = self.brush.DCplxTrans
        edgeout = pya.DEdge(length, widout/2, length, -
                            widout/2).transformed(tr)
        edgein = pya.DEdge(length, widin/2, length, -widin/2).transformed(tr)
        self.regionlistout.append(pya.DPolygon(
            [self.painterout.pointl, self.painterout.pointr, edgeout.p2, edgeout.p1]))
        self.regionlistin.append(pya.DPolygon(
            [self.painterin.pointl, self.painterin.pointr, edgein.p2, edgein.p1]))
        self.painterout.Setpoint(edgeout.p1, edgeout.p2)
        self.painterin.Setpoint(edgein.p1, edgein.p2)
        return length

    def InterdigitedCapacitor(self, number, arg1=85000, arg2=45000, arg3=31000, arg4=4000, arg5=3000, arg6=3000, arg7=2000):
        '''
        number must be odd
        http://www.rfwireless-world.com/calculators/interdigital-capacitor-calculator.html
        '''
        assert(self.end_ext == 0 and self.bgn_ext == 0)
        if number % 2 != 1:
            raise RuntimeError('number must be odd')
        oldbrush = self.brush
        tr = oldbrush.DCplxTrans
        newwidin = arg5*2+(arg4+arg7)*number+arg7
        newwidout = newwidin+arg3*2
        outPolygon = pya.DPolygon([
            pya.DPoint(arg2, newwidout/2), pya.DPoint(arg2, -newwidout/2),
            pya.DPoint(arg2+arg1, -newwidout /
                       2), pya.DPoint(arg2+arg1, newwidout/2)
        ]).transformed(tr)
        inPolygons = []
        xx = arg1-arg6
        yy = arg4
        ly = arg4+arg7
        for ii in range(1+number >> 1):
            dx = 0 if ii % 2 == 0 else arg6
            inPolygons.append(pya.DPolygon([
                pya.DPoint(arg2+dx, yy/2+ii *
                           ly), pya.DPoint(arg2+dx, -yy/2+ii*ly),
                pya.DPoint(arg2+dx+xx, -yy/2+ii *
                           ly), pya.DPoint(arg2+dx+xx, yy/2+ii*ly)
            ]).transformed(tr))
            if ii == 0:
                continue
            inPolygons.append(pya.DPolygon([
                pya.DPoint(arg2+dx, yy/2-ii *
                           ly), pya.DPoint(arg2+dx, -yy/2-ii*ly),
                pya.DPoint(arg2+dx+xx, -yy/2-ii *
                           ly), pya.DPoint(arg2+dx+xx, yy/2-ii*ly)
            ]).transformed(tr))
        self.Narrow(newwidout, newwidin, arg2)
        self.regionlistout.append(outPolygon)
        self.regionlistin.extend(inPolygons)
        self.Narrow(newwidout, newwidin, arg1)
        self.regionlistout.pop()
        self.regionlistin.pop()
        self.Narrow(oldbrush.widout, oldbrush.widin, arg2)

    def Output_Region(self,notmerge=False):
        polygonsout = []
        for x in self.regionlistout:
            if isinstance(x, pya.DPolygon):
                polygonsout.append(pya.Polygon.from_dpoly(x))
        self.regionlistout = []
        polygonsin = []
        for x in self.regionlistin:
            if isinstance(x, pya.DPolygon):
                polygonsin.append(pya.Polygon.from_dpoly(x))
        self.regionlistin = []
        if notmerge:
            self.regionin=pya.Region(polygonsin)
            self.regionout=pya.Region(polygonsin)
            return self.regionout,self.regionin
        self.region = pya.Region(polygonsout)-pya.Region(polygonsin)
        return self.region

    def Draw(self, cell, layer):
        cell.shapes(layer).insert(self.Output_Region())

    def Getcenterlineinfo(self):
        ''' 中心线的(点列表,笔刷)成组添加 '''
        cptinfos = self.centerlineinfos
        self.centerlineinfos = []
        return cptinfos


class TriCavityPainter(CavityPainter):

    def Getexinfo(self):
        #  la lb la lb la
        # p1 p2 p3 p4 p5 p6
        brush = self.brush
        widout = brush.edgeout.length()
        widin = brush.edgein.length()
        p1 = brush.edgeout.p1
        p2 = brush.edgein.p1
        p5 = brush.edgein.p2
        p6 = brush.edgeout.p2
        la = (widout-widin)/2
        lb = (widin-la)/2
        p3 = pya.DPoint((p2.x*(la+lb)+p5.x*lb)/widin,
                        (p2.y*(la+lb)+p5.y*lb)/widin)
        p4 = pya.DPoint((p2.x*lb+p5.x*(la+lb))/widin,
                        (p2.y*lb+p5.y*(la+lb))/widin)
        return dict(p1=p1, p2=p2, p3=p3, p4=p4, p5=p5, p6=p6, la=la, lb=lb)

    def constructors2(self, brush, end_ext=0):
        super().constructors2(brush, end_ext)
        self.regionlistex = []
        _info = self.Getexinfo()
        self.painterex = LinePainter(_info['p3'], _info['p4'])

    def Run(self, path=None):
        result = super().Run(path)
        if path == None:
            pathFunction = self.path
        elif hasattr(path, '__call__'):
            pathFunction = path
        else:  # type(path)==str
            pathFunction = TraceRunner.getPathFunction(path)
        # 修复1nm线的bug
        self.painterex._Straight(-0.414)
        self.painterex._Straight(0.414)
        pathFunction(self.painterex)
        self.painterex._Straight(0.414)
        self.painterex._Straight(-0.414)
        self.regionlistex.extend(self.painterex.outputlist)
        self.painterex.outputlist = []
        return result

    def Narrow(self, widout, widin, length=6000):
        super().Narrow(widout, widin, length)
        ex=self.Getexinfo()
        self.regionlistex.append(pya.DPolygon(
            [self.painterex.pointl, self.painterex.pointr, ex['p4'], ex['p3']]))
        self.painterex.Setpoint(ex['p3'], ex['p4'])
        return length

    def Output_Region(self):
        region = super().Output_Region()
        polygonsex = []
        for x in self.regionlistex:
            if isinstance(x, pya.DPolygon):
                polygonsex.append(pya.Polygon.from_dpoly(x))
        self.regionlistex = []
        region2 = pya.Region(polygonsex)
        region2.merge()
        self.region = region2+region
        return self.region

    @property
    def brushl(self):
        _info = self.Getexinfo()
        return CavityBrush(_info['p1'], _info['p2'], _info['p3'], _info['p4'])

    @property
    def brushr(self):
        _info = self.Getexinfo()
        return CavityBrush(_info['p3'], _info['p4'], _info['p5'], _info['p6'])
