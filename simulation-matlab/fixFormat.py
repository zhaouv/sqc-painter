# -*- coding: utf-8 -*-
import re
import json


def fixOneLayerFile(ss):
    ss=re.sub(r'VER.*', 'VER 14.52', ss, 1)
    ss=re.sub(r'\n(BOX.*)\n.*\n.*\n', '''
MET "Al" 1 NOR INF 0 0.1 \\1
      2000 1 1 0 0 0 0 "Air"
      500 9.3 1 3e-006 0 0 0 "Sapphire" A 11.5 1 3e-006 0 0 
TECHLAY METAL Al <UNSPECIFIED> 10 0 
0 0 0 N 0 1 1 100 100 0 0 0 Y
END
END
LORGN 0 1000 U 
''', ss, 1)
    ss=re.sub(r'(\n\d.*Y\n)','\\1TLAYNAM Al INH\n',ss)
    ss=re.sub(r'\r','',ss)
    return ss


def fixThreeLayerFile(ss):
    ss=re.sub(r'VER.*', 'VER 14.52', ss, 1)
    ss=re.sub(r'\n(BOX.*)\n'+3*r'.*\n', '''
MET "Al" 1 NOR INF 0 0.1 
MET "Unknown_metal" 1 VOL INF 0
\\1
      2000 1 1 0 0 0 0 "Air"
      2 1 1 0 0 0 0 "Air"
      500 9.3 1 3e-006 0 0 0 "Sapphire" A 11.5 1 3e-006 0 0 
TECHLAY METAL Stream2:2 <UNSPECIFIED> 2 2
0 0 -1 N 0 1 1 100 100 0 0 0 Y
END
END
TECHLAY VIA Stream3:0 <UNSPECIFIED> 3 0
VIA POLYGON
0 0 -1 N 0 1 1 100 100 0 0 0 Y
TOLEVEL 1 RING NOCOVERS
END
END
TECHLAY METAL Stream10:0 <UNSPECIFIED> 10 0
1 0 0 N 0 1 1 100 100 0 0 0 Y
END
END
LORGN 0 1000 U 
''', ss, 1)
    ss=re.sub(r'(\n0.*Y\n)','\\1TLAYNAM Stream2:2 NOH\n',ss)
    ss=re.sub(r'(\n1.*Y\n)','\\1TLAYNAM Stream10:0 NOH\n',ss)
    ss=re.sub(r'\r','',ss)
    return ss

if __name__=='__main__':
    with open(r'E:\workspace\GitHub\sqc-painter\[mail-simulation]\diff\TBD_projectname_raw.son',encoding='utf-8') as fid:
        ss=fid.read()
    print(fixOneLayerFile(ss))
    print('\n====\n'*3)
    with open(r'E:\workspace\GitHub\sqc-painter\[mail-simulation]\diff\projectname_mm_raw.son',encoding='utf-8') as fid:
        ss=fid.read()
    print(fixThreeLayerFile(ss))