# -*- coding: utf-8 -*-

from math import cos, sin, pi, tan, atan2, asin, sqrt, ceil, floor
import queue

import pya
from .IO import IO
from .CavityBrush import CavityBrush
from .CavityPainter import CavityPainter, TraceRunner
from .Collision import Collision
from .Interactive import Interactive
from .SpecialPainter import SpecialPainter

class BrushLinker:
    '''处理确定性的连接两个笔刷的类, 考虑移动到CavityPainter.py'''

    @staticmethod
    def link(brush1,brush2,radius=50000,pre_straight=0,linktype='45'):
        pathtpl,brush1,brush2=BrushLinker._pre_straight(brush1,brush2,pre_straight)
        if linktype=='45':
            pathstr=BrushLinker.angle45Link(brush1,brush2,radius)
        else: # linktype=='any':
            pathstr=BrushLinker.TurningStraightTurningLink(brush1,brush2,radius)
        return pathtpl.format(pathstr)

    @staticmethod
    def _pre_straight(brush1,brush2,pre_straight):
        if pre_straight!=0:
            def runStraight(brush):
                painter=CavityPainter(brush)
                painter.Run(f's{pre_straight}')
                return painter.brush
            return f's{pre_straight} {{}} s{pre_straight}',runStraight(brush1),runStraight(brush2)
        return '{}',brush1,brush2

    @staticmethod
    def TurningStraightTurningLink(brush1,brush2,radius=50000):
        def getInfo(brush,radius_info=radius):
            centerx, centery, angle, widout=brush.Getinfo()
            lcenter = pya.DPoint(centerx+radius_info*cos(pi/180*(angle+90)),centery+radius_info*sin(pi/180*(angle+90)))
            rcenter = pya.DPoint(centerx+radius_info*cos(pi/180*(angle-90)),centery+radius_info*sin(pi/180*(angle-90)))
            return lcenter,rcenter,centerx,centery,angle
        # 使用一个小的半径来计算应该选取哪两个圆
        def getSide(brush1,brush2):
            info1=getInfo(brush1,radius_info=10)
            info2=getInfo(brush2,radius_info=10)
            # print(info1,info2)
            distances=[]
            for m1 in [0,1]:
                for m2 in [0,1]:
                    distances.append([info1[m1].distance(info2[m2]),m1,m2])
            distance,m1,m2=min(distances)
            # print(distances,[distance,m1,m2])
            return m1,m2
        m1,m2=getSide(brush1,brush2)
        info1=getInfo(brush1)
        info2=getInfo(brush2)
        # m1,m2 0是左侧 1是右侧 
        # 反侧取平行切边, 同侧取内部切边
        centerDistance=info1[m1].distance(info2[m2])
        centerAngle=atan2(-info1[m1].y+info2[m2].y,-info1[m1].x+info2[m2].x)*180/pi
        if m1!=m2:
            # 如果两边的圆半径不一样此处也需要计算一个反正弦. radius1-radius2=0
            deltaAngle=0
            l1=centerDistance
        else:
            # radius1+radius2=2*radius
            if radius*2>=centerDistance:
                if IO.warning.link_brush_too_close:
                    IO.warning.warning("paintlib.BrushLinker.TurningStraightTurningLink", "Warning : brushs too close, using radius/2", pya.MessageBox.Ok)
                return BrushLinker.TurningStraightTurningLink(brush1,brush2,radius=radius/2)
            deltaAngle=asin(radius*2/centerDistance)*180/pi
            l1=sqrt(centerDistance**2-(2*radius)**2)
        def angleDistance(a,b,reverse=0):
            return (b+3600-a)%360 if reverse==0 else (a+3600-b)%360
        # 计算在圆心角上, 那个边更接近
        targetAngle=centerAngle-deltaAngle if angleDistance(info1[4]+90*([-1,1][m1]),centerAngle+90-deltaAngle,m1)<=angleDistance(info1[4]+90*([-1,1][m1]),centerAngle+deltaAngle-90,m1) else centerAngle+deltaAngle
        a1=angleDistance(info1[4],targetAngle,m1)
        a2=angleDistance(targetAngle,info2[4]+180,1-m2)
        # print(['centerAngle,deltaAngle,targetAngle,a1,a2,m1,m2,info1,info2',centerAngle,deltaAngle,targetAngle,a1,a2,m1,m2,info1,info2])
        def lr(mi,reverse=0):
            return ['l','r'][mi if reverse==0 else 1-mi]
        return f'{lr(m1)} {radius},{a1} s {l1} {lr(1-m2)} {radius},{a2}'
    
    @staticmethod
    def _preparelink45(brush1,brush2):
        angle45=abs((brush2.angle-brush1.angle)%45)
        if angle45>22:
            angle45=45-angle45
        if angle45>0.001:
            return False,None,None,None
        brush10=brush1.transformed(brush1.backDCplxTrans)
        brush20=brush2.transformed(brush1.backDCplxTrans)
        mirrorFlag=False
        if brush20.centery<0:
            brush20=CavityBrush(pointc=pya.DPoint(brush20.centerx,-brush20.centery), angle=-brush20.angle,widout=brush20.widout,widin=brush20.widin)
            mirrorFlag=True
        return True,brush10,brush20,mirrorFlag

    @staticmethod
    def _link2Brush45cases(brush1,brush2,radius=50000):
        #cases
        [xx,yy,angle]=[brush2.centerx,brush2.centery,round(brush2.angle)]
        r1=radius
        r2=radius/2**0.5
        rh=r1-r2

        # 1: s [0] l 45 s [1]
        if angle==225 and xx-r2-(yy-rh)>=0 and yy-rh>=0:
            return 's [0] l 45 s [1]',f's {xx-r2-(yy-rh)} l{radius},45 s{(yy-rh)*2**0.5}'
        
        # 2: s [0] l 45 s [1] r 45 s [0]
        if angle==180 and xx-2*r2-(yy-2*rh)>=0 and yy-2*rh>=0:
            return 's [0] l 45 s [1] r 45 s [0]',f's{(xx-2*r2-(yy-2*rh))/2} l{radius},45 s{(yy-2*rh)*2**0.5} r{radius},45 s{(xx-2*r2-(yy-2*rh))/2}'
        
        # 3: s [0] l 45 s [^1] l 45 s [2]
        if angle==270 and xx>=r1 and yy>=r1:
            return 's [0] l 45 s [^1] l 45 s [2]',f's{xx-yy if xx>yy else 0} l{radius},45 s{min(xx,yy)*2**0.5-2*r2} l{radius},45 s{yy-xx if xx<yy else 0}'

        # 4: l 45 s [0] l 45 s [1] r 45
        if angle==225 and xx>=r1+rh and yy>=r1+r2:
            return 'l 45 s [0] l 45 s [1] r 45',f'l{radius},45 s{(xx-r1-rh)*2**0.5} l{radius},45 s{yy-r1-r2-(xx-r1-rh)} r{radius},45'
        
        # 5: s[0] l 45 s[1] r 45 s[0] r 45
        if angle==135 and xx>=3*r2 and yy>=rh:
            return 's[0] l 45 s[1] r 45 s[0] r 45',f's{(xx-3*r2-(yy-rh))/2} l{radius},45 s{(yy-rh)*2**0.5} r{radius},45 s{(xx-3*r2-(yy-rh))/2} r{radius},45'

        return '',''

    @staticmethod
    def angle45Link(brush1,brush2,radius=50000):
        angle45,brush10,brush20,mirrorFlag = BrushLinker._preparelink45(brush1,brush2)
        if not angle45:
            if not IO.warning.angle_45_link_fallback:
                IO.warning.warning("paintlib.BrushLinker.angle45Link", "Error : not 45x angle", pya.MessageBox.Ok)
            return BrushLinker.TurningStraightTurningLink(brush1,brush2,radius=radius)

        case,pathstr = BrushLinker._link2Brush45cases(brush1=brush10,brush2=brush20,radius=radius)
        if not case:
            if not IO.warning.angle_45_link_fallback:
                IO.warning.warning("paintlib.BrushLinker.angle45Link", "Error : no cases match", pya.MessageBox.Ok)
            return BrushLinker.TurningStraightTurningLink(brush1,brush2,radius=radius)
        if mirrorFlag:
            pathstr = TraceRunner.mirrorPath(pathstr)
        return pathstr

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
        for issource, pairs_ in [(False, pairs), (True, pairs0)]:
            for pid, pair in enumerate(pairs_):
                for is1, pt in enumerate(pair, 1):
                    px, py = pt
                    if area[px][py] >= BIGNUMBERPID and not issource:
                        estr = 'conflict, pair '+str(pid)
                        IO.warning.warning(
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
                IO.warning.warning(
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
                IO.warning.warning(
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
            return 'link line fail', 0, pathstr
        if type(cell) != type(None) and type(layer) != type(None):
            length = Interactive._show_path(cell, layer, brush12[1], pathstr)
        else:
            length = 0
        return '', length, pathstr

    @staticmethod
    def autoRoute(cell, layer, size, cellList, brushs, layerList=None, box=None, layermod='not in', order=None):
        brushs = [[b2, b1] for b1, b2 in brushs]
        if type(box) == type(None):
            box = Interactive._box_selected()
        if not box:
            raise RuntimeError('no box set')
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
        paths = []
        for line, brush12 in zip(lines, brushs):
            checkresult, length, pathstr = AutoRoute._linkLine(
                cell, layer, line, brush12, areaxyToXy)
            if checkresult:
                return checkresult, [], []
            lengths.append(length)
            paths.append(pathstr)
        return '', lengths, paths
    
    @staticmethod
    def stackedRoute(cell, layer, size, brushScatter, brushLine, stacks, cellList, layerList=None, box=None, layermod='not in'):
        ''' 
        层叠布线

        输入: 

        1. 端口组1, 散布, 朝向一致

        2. 端口组2, 排在一个直线上, 朝向一致垂直于排布的直线, 端口组1全部在端口组2的同一侧, 两组端口只需要两两连接不要求指定的配对

        3. 切割线组, 从远到近的接近端口组2, 与端口组2平行, 且覆盖全部端口组1

        4. 区域, 覆盖所有端口和切割线

        过程:

        1. 栅格化区域

        2. 沿着切割线组推进

        1. 检测线上的新增端口数

        2. 检测并编号线上可用的空间

        3. 均匀的放置中间端口

        4. 把中间端口和前一组的端口连接

        3. 把最后一组端口和端口组2连接

        '''
        if type(box) == type(None):
            box = Interactive._box_selected()
        if not box:
            raise RuntimeError('no box set')
        outregion, inregion = Collision.getShapesFromCellAndLayer(
            cellList, layerList=layerList, box=box, layermod=layermod)
        region = outregion & inregion
        area, xyToAreaxy, areaxyToXy = AutoRoute._Rasterized(size, box, region)
        # def _getStackedPairs(xyToAreaxy, brushs, area, size):
        #     pass
        # pairs=_getStackedPairs(xyToAreaxy, brushs, area, size)
        pass

    @staticmethod
    def linkTwoBrush(brush1, brush2, size=150000, enlargesize=600000, layerList=None, box=None, layermod='not in', cellList=None):
        if type(box) == type(None):
            ppp = 'r{size},180 r{size2},180 r{size2},180'.format(
                size=enlargesize/2, size2=enlargesize)
            painter = CavityPainter(brush1)
            painter.Run(ppp)
            region = painter.Output_Region()
            painter = CavityPainter(brush2)
            painter.Run(ppp)
            region = region + painter.Output_Region()
            box = region.bbox()
        if cellList == None:
            cellList = [IO.top]
        err, _, paths = AutoRoute.autoRoute(cell=None, layer=None, size=size, cellList=cellList, brushs=[
                                            [brush1, brush2]], layerList=layerList, box=box, layermod='not in', order=None)
        if err:
            raise RuntimeError(err)
        return paths[0]

    @staticmethod
    def getLinkTwoBrushWithPassClass():
        return LinkTwoBrushWithPassClass

    @staticmethod
    def linkTwoBrushWithPass(**args):
        linking = LinkTwoBrushWithPassClass()
        linking.setArgs(**args)
        linking.link(strategy=args['strategy'], length=args["length"])
        return linking.finalPath


class LinkTwoBrushWithPassClass:
    # 类
    cache = {}
    cacheFilename = 'linkCache.json'
    # 可覆盖
    cell = None
    layer = None
    linksize = 150000
    enlargesize = 600000
    layerList = None
    radius = 50000  # contortion的半径
    # 实例
    testMode = False
    printRange = True
    cacheId = ''
    _pass = []
    brush1 = None
    brushs = []  # 中介的刷子对
    brush4 = None
    pre = ''
    pres = []
    post = ''
    manual = ''
    posts = []
    paths1 = []
    paths2 = []  # 1比2多1个
    lengths1 = []
    lengths2 = []  # 1比2多1个
    minlengths = []
    maxlengths = []
    minlength = 0
    maxlength = 0
    finalPath = ''
    manualDict = {}  # 形如 {3:'s1000'}, 索引为3的线手动来布, 也可以在_pass中指定, 在_pass中优先级高
    x0 = 0
    y0 = 0

    @staticmethod
    def loadcache():
        with open(IO.workingDir+'/'+LinkTwoBrushWithPassClass.cacheFilename) as fid:
            LinkTwoBrushWithPassClass.cache = json.load(fid)

    @staticmethod
    def savecache():
        with open(IO.workingDir+'/'+LinkTwoBrushWithPassClass.cacheFilename, 'w') as fid:
            json.dump(LinkTwoBrushWithPassClass.cache, fid)

    def reversePath(self, pstr):
        if not pstr:
            return ''
        return TraceRunner.reversePath(pstr)

    def setArgs(self, **args):
        '''
        args={
            "brush1": paintlib.CavityBrush(pointc=pya.DPoint(0,0), angle=0,widout=20000,widin=10000,bgn_ext=0),
            "brush4": paintlib.CavityBrush(pointc=pya.DPoint(0,500000), angle=0,widout=20000,widin=10000,bgn_ext=0),
            "cacheId":"",
            "testMode":False,

            "x0": 782828,
            "y0": 2181652,
            "pre": "",
            "manual": "",
            "post": "s40000 l30000 s260000 r30000",
            "_pass": [
                {
                    "x": 837544,
                    "y": 3029618,
                    "angle": -45,
                    "height": 0,
                    "width": 300000,
                    "pre": "",
                    "manual": "",
                    "post": "s40000 l30000 s260000 r30000"
                },
                {
                    "x": 867086,
                    "y": 2565715,
                    "angle": -135,
                    "height": 245000,
                    "width": 300000,
                    "manual": "s131153 l40000 s4053"
                }
            ],
            "radius":50000,
            "linksize":150000,
            "enlargesize":600000,
            "layerList":None
        }
        '''
        for k in [
            '_pass',
            'brushs',
            'pres',
            'posts',
            'paths1',
            'paths2',
            'lengths1',
            'lengths2',
            'minlengths',
            'maxlengths',
        ]:
            self.__setattr__(k, [])
        for k in [
            'manualDict',
        ]:
            self.__setattr__(k, {})
        for k, v in args.items():
            self.__setattr__(k, v)
        return self

    def link(self, strategy='max', **args):
        '''
        strategy: max,min,set
        args['length']: target length
        '''
        brush1 = self.brush1
        brush4 = self.brush4
        minlengths = self.minlengths
        maxlengths = self.maxlengths
        cacheId = self.cacheId

        if self.cell == None:
            self.cell = IO.link
        if self.layer == None:
            self.layer = IO.layer

        contortion_args_list = []
        if self.manual:
            self.manualDict[0] = self.manual
        for ii, midv in enumerate(self._pass):
            if 'manual' in midv and midv['manual']:
                self.manualDict[ii+1] = midv['manual']
            self.pres.append('' if 'pre' not in midv else midv['pre'])
            self.posts.append('' if 'post' not in midv else midv['post'])
            contortion_args = dict(x=self.x0+midv['x'], y=self.y0+midv['y'], angle=midv['angle'], width=midv['width'],
                                   height=midv['height'], radius=self.radius, widout=brush1.widout,
                                   widin=brush1.widin, strategy='width')
            contortion_args_list.append(contortion_args)
            _, brush2, brush3, minlength, maxlength = SpecialPainter.contortion(
                infoOnly=True, length=0, **contortion_args)
            self.brushs.append(brush2)
            self.brushs.append(brush3)
            minlengths.append(minlength)
            maxlengths.append(maxlength)
            if strategy != 'set':
                length = maxlength
                if strategy == 'min':
                    length = minlength
                path2, _, _, _, _ = SpecialPainter.contortion(
                    infoOnly=False, length=length, **contortion_args)
                if self.testMode:
                    Interactive._show_path(
                        self.cell, self.layer, brush2.reversed(), path2)
                self.paths2.append(path2)

        if cacheId and cacheId in self.cache:
            cache = self.cache[cacheId]
            self.paths1 = cache['path']
            self.lengths1 = cache['length']
            if self.testMode:
                brushs = [brush1]+self.brushs+[brush4]
                for ii in range(int(len(brushs)/2)):
                    pass
                    Interactive._show_path(
                        self.cell, self.layer, brushs[2*ii], self.paths1[ii])
        else:

            brushs = [brush1]+self.brushs+[brush4]
            posts = [self.post]+self.posts
            pres = self.pres+[self.pre]
            for ii in range(int(len(brushs)/2)):

                painter = CavityPainter(brushs[2*ii])
                if posts[ii]:
                    painter.Run(posts[ii])
                brush_link_s = painter.brush

                painter = CavityPainter(brushs[2*ii+1])
                if pres[ii]:
                    painter.Run(pres[ii])
                brush_link_e = painter.brush

                if ii in self.manualDict:
                    path1 = self.manualDict[ii]
                else:
                    path1 = AutoRoute.linkTwoBrush(
                        brush_link_s, brush_link_e, size=self.linksize, layerList=self.layerList, enlargesize=self.enlargesize)
                path1 = posts[ii]+path1+self.reversePath(pres[ii])
                self.paths1.append(path1)

                painter = CavityPainter(brushs[2*ii])
                length1 = painter.Run(self.paths1[ii])
                if self.testMode:
                    painter.Draw(self.cell, self.layer)
                self.lengths1.append(length1)

                cache = {'path': self.paths1, 'length': self.lengths1}
                self.cache[cacheId] = cache
            if self.printRange:
                print('range', cacheId, sum(self.lengths1) +
                      sum(minlengths), sum(self.lengths1)+sum(maxlengths))
        self.minlength = sum(self.lengths1)+sum(minlengths)
        self.maxlength = sum(self.lengths1)+sum(maxlengths)

        if strategy == 'set':
            if 'length' not in args:
                raise RuntimeError(
                    "put ',length=<a number>' in your function call")
            if self.minlength <= args['length'] <= self.maxlength:
                pass
            else:
                raise RuntimeError(
                    f"{self.minlength}<={args['length']}<={self.maxlength} is not True")
            if self.minlength == self.maxlength:
                k = 0
            else:
                k = (args['length']-self.minlength) / \
                    (self.maxlength-self.minlength)
            for ii in range(len(contortion_args_list)):
                contortion_args = contortion_args_list[ii]
                brush2 = self.brushs[2*ii]
                length = minlengths[ii]+k*(maxlengths[ii]-minlengths[ii])
                path2, _, _, _, _ = SpecialPainter.contortion(
                    infoOnly=False, length=length, **contortion_args)
                if self.testMode:
                    Interactive._show_path(
                        self.cell, self.layer, brush2.reversed(), path2)
                self.paths2.append(path2)

        path = self.paths1[0]
        for p1, p2 in zip(self.paths1[1:], self.paths2):
            path = path+p2+p1
        self.finalPath = path
        return path


"""

class linkBrushToPinWithPassClass:
    armLength = 250000
    linking = paintlib.LinkTwoBrushWithPassClass()
    pinStraghtSimulationMode = False

    def setArgs(self, **args):
        '''
        x0=unit.x0,
        y0=unit.y0,
        _pass=args['pass'],
        pre=args['pre'],
        post=args['post'],
        radius=args2['radius'],
        brush1= self.brushs[ri],
        cacheId=args['cacheId'],

        x
        y
        angle
        '''
        self.linking = paintlib.LinkTwoBrushWithPassClass()
        x = args['x']
        y = args['y']
        angle = args['angle']
        x0 = args['x0']
        y0 = args['y0']
        self.brush4 = args['brush4'] = paintlib.CavityBrush(pointc=pya.DPoint(x0+x+self.armLength*cos(angle*pi/180), y0+y+self.armLength*sin(
            angle*pi/180)), angle=angle, widout=args['brush1'].widout, widin=args['brush1'].widin, bgn_ext=0)
        self.linking.setArgs(**args)
        return self

    def link(self, strategy='max', **args):
        painter = paintlib.CavityPainter(self.brush4)
        if self.pinStraghtSimulationMode:
            painter.Run('s_-1000000')
        else:
            painter.Electrode(reverse=True)
        painter.Draw(self.linking.cell, self.linking.layer)
        pass
        return self.linking.link(strategy=strategy, **args)

    @property
    def finalPath(self):
        return self.linking.finalPath
"""
