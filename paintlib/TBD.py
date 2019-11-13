# -*- coding: utf-8 -*-


class TBD(object):
    '''处理待定数值的静态类'''
    id='not init'
    filename='TBD.txt'
    values=[]
    index=0
    inf=999999
    eps=0.01
    @staticmethod
    def init(id,_str=None):
        if _str==None:
            TBD.id=str(id)
            try:
                with open(TBD.filename) as fid:
                    ss=fid.read()
            except FileNotFoundError as _:
                with open(TBD.filename,'w') as fid:
                    ss=TBD.id
                    fid.write(ss)
            lines=[ln for ln in ss.split('\n') if len(ln.strip())>1 and ln.strip()[0] in '-.0123456789']
            if TBD.id != lines[0]:lines=[TBD.id]
        if _str!=None:
            def _set(value,index=-1):
                pass
            TBD.set=_set
            ss=_str
            lines=[ln for ln in ss.split('\n') if len(ln.strip())>1 and ln.strip()[0] in '-.0123456789']
            lines[0]='not file'
        TBD.id=lines[0]
        TBD.values=[[float(value) for value in line.split(',')] for line in lines[1:]]
        return TBD
    @staticmethod
    def get(index=None):
        if index==None:
            TBD.index+=1
            index=-1
        _index=TBD.index+index if index < 0 else index
        whileBool = len(TBD.values[_index:_index+1])==0
        while whileBool:
            TBD.values.append([0,TBD.inf])
            whileBool = len(TBD.values[_index:_index+1])==0
        return TBD.values[_index][0]
    @staticmethod
    def set(value,index=-1):
        _index=TBD.index+index if index < 0 else index
        TBD.values[_index][1]=value
        TBD.values[_index][0]+=value
        if(value < -TBD.eps):print('Warning : minus value in TBD number '+str(_index))
        return value
    @staticmethod
    def isFinish():
        if TBD.id == 'not init':raise RuntimeError('TBD not init')
        finish=True
        for ii in TBD.values:
            if abs(ii[1]) > TBD.eps:
                finish=False
                break
        if TBD.id == 'not file':return finish
        with open(TBD.filename,'w') as fid:
            ss=TBD.id+'\n'+'\n'.join([','.join([str(jj) for jj in ii]) for ii in TBD.values])
            print('TBD :\n'+ss+'\nTBD END')
            fid.write(ss)
        return finish