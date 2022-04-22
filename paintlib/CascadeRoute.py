# -*- coding: utf-8 -*-


import pya
from .IO import IO
from .Collision import Collision
from .Interactive import Interactive

class hungarian:
    # modified from https://gist.github.com/KartikTalwar/3158534
    def __init__(self,weights):
        self.w  = self.fixShape(weights)
        n = len(self.w)
        self.U  = self.V = range(n)
        self.lu = [ max([self.w[u][v] for v in self.V]) for u in self.U]  # start with trivial labels
        self.lv = [ 0                         for v in self.V]
        self.Mu = {}                                       # start with empty matching
        self.Mv = {}
    def fixShape(self,weights):
        n = len(weights)
        m = len(weights[0])
        if n==m:
            pass
        if n<m:
            weights.extend([[0]*m for ii in range(m-n)])
        if n>m:
            for ai in weights:
                ai.extend([0]*(n-m))
        return weights
    def improveLabels(self,val):
        """ change the labels, and maintain minSlack. 
        """
        for u in self.S:
            self.lu[u] -= val
        for v in self.V:
            if v in self.T:
                self.lv[v] += val
            else:
                self.minSlack[v][0] -= val

    def improveMatching(self,v):
        """ apply the alternating path from v to the root in the tree. 
        """
        u = self.T[v]
        if u in self.Mu:
            self.improveMatching(self.Mu[u])
        self.Mu[u] = v
        self.Mv[v] = u

    def slack(self,u,v): return self.lu[u]+self.lv[v]-self.w[u][v]

    def augment(self):
        """ augment the matching, possibly improving the lablels on the way.
        """
        while True:
            # select edge (u,v) with u in S, v not in T and min slack
            ((val, u), v) = min([(self.minSlack[v], v) for v in self.V if v not in self.T])
            assert u in self.S
            if val>0:        
                self.improveLabels(val)
            # now we are sure that (u,v) is saturated
            assert self.slack(u,v)==0
            self.T[v] = u                            # add (u,v) to the tree
            if v in self.Mv:
                u1 = self.Mv[v]                      # matched edge, 
                assert not u1 in self.S
                self.S[u1] = True                    # ... add endpoint to tree 
                for v in self.V:                     # maintain minSlack
                    if not v in self.T and self.minSlack[v][0] > self.slack(u1,v):
                        self.minSlack[v] = [self.slack(u1,v), u1]
            else:
                self.improveMatching(v)              # v is a free vertex
                return

    def maxWeightMatching(self):
        """ given w, the weight matrix of a complete bipartite graph,
            returns the mappings Mu : U->V ,Mv : V->U encoding the matching
            as well as the value of it.
        """
        n  = len(self.w)
        while len(self.Mu)<n:
            free = [u for u in self.V if u not in self.Mu]      # choose free vertex u0
            u0 = free[0]
            self.S = {u0: True}                            # grow tree from u0 on
            self.T = {}
            self.minSlack = [[self.slack(u0,v), u0] for v in self.V]
            self.augment()
        #                                    val. of matching is total edge weight
        val = sum(self.lu)+sum(self.lv)
        return (self.Mu, self.Mv, val)

class CascadeRoute:
    
    @staticmethod
    def _potentialPoints(stack,size,potentialRate):
        def getp(ll, p1, p2):
            bl = p1.distance(p2)
            if bl<ll:
                return bl-ll,pya.DPoint()
            dx = p2.x-p1.x
            dy = p2.y-p1.y
            k = 1.0*ll/bl
            return bl-ll,pya.DPoint(p1.x+k*dx, p1.y+k*dy)
        delta = size*potentialRate
        rest = 0.0
        potentialPts=[]
        for pts in stack:
            for pi in range(0,len(pts)-1):
                p1=pts[pi]
                p2=pts[pi+1]
                if rest < 0:
                    rest,pt = getp(delta+rest, p1, p2)
                    if rest>=0.0:
                        p1 = pt
                        potentialPts.append(p1)
                while rest>=0.0:
                    rest,pt = getp(delta, p1, p2)
                    if rest>=0.0:
                        p1 = pt
                        potentialPts.append(p1)
        return potentialPts

    @staticmethod
    def _candidatePoints(potentialPts,region,size):
        candidatePts=[]
        for pt in potentialPts:
            x1=pt.x
            y1=pt.y
            check_box = pya.Box(x1-size/2, y1-size/2, x1+size/2, y1+size/2)
            empty = (pya.Region(check_box) & region).is_empty()
            if empty:
                candidatePts.append(pt)
        return candidatePts

    @staticmethod
    def _selectPoints(lastSelectedStackPts,candidatePts,saveRate):
        # step 1 均匀的选择 saveRate 倍的点
        tosavenum = int(len(lastSelectedStackPts)*saveRate)
        savedCandidatePts = candidatePts
        if tosavenum < len(candidatePts):
            savedCandidatePts = []
            toadd = tosavenum/len(candidatePts)
            tosave=0.5
            for pt in candidatePts:
                tosave+=toadd
                if tosave>=1:
                    tosave-=1
                    savedCandidatePts.append(pt)
        # step 2 用匈牙利算法来执行完美匹配
        cost=[
            [
                -int(p1.distance(p2)) 
                for p2 in savedCandidatePts
            ] 
            for p1 in lastSelectedStackPts
        ]
        h = hungarian(cost).maxWeightMatching()
        pts=[]
        for k in range(len(lastSelectedStackPts)):
            pts.append(savedCandidatePts[h[0][k]])
        return pts

    @staticmethod
    def _pairingPoints(lastSelectedStackPts,ptsOut):
        cost=[
            [
                -int(p1.distance(p2)) 
                for p2 in ptsOut
            ] 
            for p1 in lastSelectedStackPts
        ]
        h = hungarian(cost).maxWeightMatching()
        return h[0]

    @staticmethod
    def CascadeRouteStraightforward(cell, layer, sizes, potentialRates, saveRates, ptsIn, ptsOut, stacks, cellList, layerList=None, box=None, layermod='not in'):

        if type(box) == type(None):
            box = Interactive._box_selected()
        if not box:
            raise RuntimeError('no box set')
        outregion, inregion = Collision.getShapesFromCellAndLayer(
            cellList, layerList=layerList, box=box, layermod=layermod)
        region = outregion & inregion
        
        lastSelectedStackPts = ptsIn
        selectedStackPts = [ptsIn]
        for si,stack in enumerate(stacks):
            potentialRate = potentialRates[si]
            saveRate = saveRates[si]
            size = sizes[si]
            potentialPts = CascadeRoute._potentialPoints(stack,size,potentialRate)
            candidatePts = CascadeRoute._candidatePoints(potentialPts,region,size)
            lastSelectedStackPts = CascadeRoute._selectPoints(lastSelectedStackPts,candidatePts,saveRate)
            selectedStackPts.append(lastSelectedStackPts)
        order={}
        if type(ptsOut)!=type(None):
            order=CascadeRoute._pairingPoints(lastSelectedStackPts,ptsOut)
            pts=[]
            for k in range(len(ptsOut)):
                pts.append(ptsOut[order[k]])
            selectedStackPts.append(pts)
        return selectedStackPts,order

    

