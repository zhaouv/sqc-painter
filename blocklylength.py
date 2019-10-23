# -*- coding: utf-8 -*-
#KLayout 0.24.8
#python 3.4
from paintlib import *

class _SpecialPainter(Painter):
    @staticmethod
    def contortion(cell,layer,x,y,angle,width,height,length,radius,widout=20000,widin=10000,strategy='width'):
        def minlength(n):
            return (n+1)*2*pi*radius/4+(width-(n+1)*2*radius)
        def maxlength(n):
            return minlength(n)+(height-4*radius)+(n-1)*(height-2*radius)
        if height<4*radius:
            raise RuntimeError('height<4*radius')
        if width<4*radius:
            raise RuntimeError('width<4*radius')
        if length<2*pi*radius+width-4*radius:
            raise RuntimeError('length too small')
        maxn=floor(width/(2*radius))-1
        if length>maxlength(maxn):
            raise RuntimeError('length too big')
        if strategy=='width':
            n=maxn
            while length<minlength(n):
                n-=1
        else:
            n=1
            while length>maxlength(n):
                n+=1
        dl=(length-minlength(n))/(2*n)
        path='s{s1} l{r} s{dl} r{r} n{nm}[r{r} s{dl2} l{r},180 s{dl2} r{r}] '
        if n%2==0:
            path+='r{r} s{dl2} l{r},180 s{dl} r{r} '
        else:
            path+='r{r} s{dl} l{r} '
        path+='s{s1}'
        path=path.format(s1=(width-(n+1)*2*radius)/2,r=radius,dl=dl,dl2=dl*2+radius*2,nm=int(floor((n-1)/2)))
        painter=CavityPainter(pointc=pya.DPoint(x,y),angle=angle+180,widout=widout,widin=widin,bgn_ext=0,end_ext=0)
        painter.Run('s{}'.format(width/2))
        brush1=painter.brush
        painter=CavityPainter(brush1.reversed())
        painter.Run(path)
        painter.Draw(cell,layer)
        brush2=painter.brush
        return painter,brush1,brush2





