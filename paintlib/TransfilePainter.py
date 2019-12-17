# -*- coding: utf-8 -*-

from math import pi, atan2
import pya
from .IO import IO
from .Painter import Painter
from .Collision import Collision


class TransfilePainter(Painter):
    def __init__(self, filename="[insert].gds"):
        self.outputlist = []
        self.filename = filename
        layout = pya.Layout()
        layout.read(filename)
        names = [i.name for i in layout.top_cells()]
        if(len(names) != 1):
            raise RuntimeError('insert file must have only one top cell')
        if(names[0] == 'TOP'):
            raise RuntimeError("the name of insert file's cell can not be TOP")
        self.insertcellname = names[0]
        self.airbridgedistance = 100000

    @staticmethod
    def airbridgeDistanceFunc(distance, inputList=None, staticList=[0, 0, 0, [0]]):
        ''' 
        设置间距及使用
        paintera=paintlib.TransfilePainter("[Crossover48].gds")
        paintera.airbridgeDistanceFunc(0,[50000,20000,50000,20000,50000,20000,50000,20000,50000,20000,50000,20000,50000,20000,50000,20000,123456])
        paintera.airbridgedistance=paintera.airbridgeDistanceFunc
        paintera.DrawAirbridge(cellairbridge,centerlinelist,"Crossover48")

        staticList [0]是上一个airbridge的距离,[1]是当前是第几个点,[2]是下一次的间隔,[3]是输入的列表
        这里利用了默认参数只初始化一次 
        '''
        if inputList != None:
            staticList[3] = inputList
            staticList[3].append(0)
            return 0
        if (distance < staticList[0]):
            staticList[0] = 0
            staticList[1] = 0
            staticList[2] = 0
        if (staticList[2] == 0):
            staticList[2] = staticList[3][0]
        dd = distance-staticList[0]
        if(dd > staticList[2]):
            staticList[0] += staticList[2]
            staticList[1] += 1
            if staticList[1] < len(staticList[3]):
                staticList[2] = staticList[3][staticList[1]]
            else:
                staticList[1] -= 1
        return staticList[1]

    def DrawAirbridge(self, cell, centerlinelist, newcellname="Airbige", collision={}):
        '''
        collision = {} 表示不做检查
        或者是 {
            'region': pya.Region, 
            'regionInsert': pya.Region, 
            'push': int
        } 进行碰撞检测
        push需要小于airbridge间距, 否侧可能会有奇怪的行为
        '''
        IO.layout.read(self.filename)
        for icell in IO.layout.top_cells():
            if (icell.name == self.insertcellname):
                icell.name = newcellname
                break
        counts = []
        for cpts, brush in centerlinelist:
            distance = 0
            if not hasattr(self.airbridgedistance, '__call__'):
                distance = self.airbridgedistance*0.25
            dt_int = 0
            for i, pt in enumerate(cpts[1:-1], 1):
                distance = distance+pt.distance(cpts[i-1])
                if hasattr(self.airbridgedistance, '__call__'):
                    calt_int = self.airbridgedistance(distance)
                else:
                    calt_int = distance//self.airbridgedistance
                if calt_int != dt_int:
                    dx = cpts[i+1].x-cpts[i-1].x
                    dy = cpts[i+1].y-cpts[i-1].y
                    tr = pya.CplxTrans(
                        1, atan2(dy, dx)/pi*180, False, pt.x, pt.y)
                    draw_=True
                    if collision:
                        region_=collision['regionInsert'].transformed(pya.ICplxTrans.from_trans(tr))
                        if (region_ & collision['region']).is_empty():
                            collision['region']=collision['region']+region_
                        else:
                            draw_=False
                            distance-=collision['push']
                    if draw_:
                        new_instance = pya.CellInstArray(
                            icell.cell_index(), tr)
                        cell.insert(new_instance)
                        dt_int = dt_int+1
            counts.append(dt_int)
        for icell in IO.layout.top_cells():
            if (icell.name == self.insertcellname):
                icell.flatten(True)
                icell.delete()
        return counts

    def DrawAirbridgeWithCollisionCheck(self, cell, centerlinelist, newcellname, boxY, boxWidth, boxHeight):
        # get all shapes
        region = Collision.getRegionFromLayers(layerList=[], layermod='not in')
        # insert
        regionInsert = pya.Region()
        regionInsert.insert(
            pya.Box(-boxWidth/2, boxY-boxHeight/2, boxWidth/2, boxY+boxHeight/2))
        regionInsert.insert(
            pya.Box(-boxWidth/2, -boxY-boxHeight/2, boxWidth/2, -boxY+boxHeight/2))
        return self.DrawAirbridge(cell, centerlinelist, newcellname, collision={'region': region, 'regionInsert': regionInsert, 'push': 10000})

    def DrawMark(self, cell, pts, newcellname="Mark"):
        IO.layout.read(self.filename)
        for icell in IO.layout.top_cells():
            if (icell.name == self.insertcellname):
                icell.name = newcellname
                break
        for pt in pts:
            tr = pya.Trans(int(pt.x), int(pt.y))
            new_instance = pya.CellInstArray(icell.cell_index(), tr)
            cell.insert(new_instance)
        for icell in IO.layout.top_cells():
            if (icell.name == self.insertcellname):
                icell.flatten(True)
                icell.delete()

    def DrawGds(self, cell, newcellname, DCplxTrans1):
        '''
        tr=pya.DCplxTrans(1,0,False,0,0)
        倍数,逆时针度数,是否绕x翻转,平移x,平移y
        '''
        tr = pya.CplxTrans.from_dtrans(DCplxTrans1)
        resultcell = None
        IO.layout.read(self.filename)
        for icell in IO.layout.top_cells():
            if (icell.name == self.insertcellname):
                icell.name = newcellname
                resultcell = icell
                break
        new_instance = pya.CellInstArray(icell.cell_index(), tr)
        cell.insert(new_instance)
        for icell in IO.layout.top_cells():
            if (icell.name == self.insertcellname):
                icell.flatten(True)
                icell.delete()
        return resultcell
