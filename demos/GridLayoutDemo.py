
# %%

import pya
import sys
import os

# sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import paintlib

layout, top = paintlib.IO.Start("guinew")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
# TBD = paintlib.TBD.init(676987)

# %%
layer = layout.layer(10, 10)  
layer1 = layout.layer(10, 3)  
layer2 = layout.layer(10, 2)  

cell = layout.create_cell("C1")  
top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))

false=False
true=True
typea={
    "type": "combiner",
    "statement": [
        {
            "type": "variableDefine",
            "id": "a",
            "value": 50000,
            "description": ""
        },
        {
            "type": "dispatch",
            "keytype": "variable",
            "id": "a,a",
            "value": "c1@xx,c1@yy"
        },
        {
            "type": "brushDefine",
            "id": "brush1",
            "x": 0,
            "y": 0,
            "angle": 0,
            "widout": 8000,
            "widin": 4000,
            "description": ""
        },
        {
            "type": "structureAt",
            "id": "c1",
            "brushid": "brush1",
            "reverse": false,
            "content": {
                "type": "attachmentTree",
                "id": "cycle"
            }
        },
        {
            "type": "dispatch",
            "keytype": "collection",
            "id": "c1@0,c1@1",
            "value": "0,1"
        }
    ]
}

g1=paintlib.GridLayout(
    '''
    # aaa
    as d
       a
       s
       d
       f
     a sddd
    as dd #sdf
    ''',
    {
    'a':{"width":100000,"height":200000,"id":'typea'},
    's':{"width":100000,"height":200000,"id":'types'},
    'd':{"width":100000,"height":200000,"id":'typed'},
    'f':{"width":100000,"height":50000,"id":'typef'},
    },
    [
        {
            "condition":"1",
            "export":[["collection.merge","0,1","0_0,10_0"]],
        },
        {
            "condition":"'{mark}'=='s'",
            "vars":{"a":80000}
        },
        {
            "condition":"'{mark}'=='d'",
            "vars":{"a":60000}
        },
        {
            "condition":"{xindex}==0 and {yindex}==0",
            "vars":{"a":25000}
        },
    ]
).load( {"type": "combiner","statement": []}, metal={
    "cycle":{
            "type": "attachmentTree",
            "define": [
                {
                    "type": "variable",
                    "id": "xx",
                    "value": 50000,
                    "description": ""
                },
                {
                    "type": "variable",
                    "id": "yy",
                    "value": 50000,
                    "description": ""
                }
            ],
            "structure": [
                {
                    "type": "structure",
                    "side": "ul",
                    "collection": "0",
                    "width": "xx",
                    "height": "yy",
                    "shape": {
                        "type": "arc",
                        "side": "dr"
                    },
                    "attachment": [
                        {
                            "type": "attachmentnone"
                        }
                    ]
                },
                {
                    "type": "structure",
                    "side": "ur",
                    "collection": "1",
                    "width": "xx",
                    "height": "yy",
                    "shape": {
                        "type": "arc",
                        "side": "dl"
                    },
                    "attachment": [
                        {
                            "type": "attachmentnone"
                        }
                    ]
                },
                {
                    "type": "structure",
                    "side": "dr",
                    "collection": "1",
                    "width": "xx",
                    "height": "yy",
                    "shape": {
                        "type": "arc",
                        "side": "ul"
                    },
                    "attachment": [
                        {
                            "type": "attachmentnone"
                        }
                    ]
                },
                {
                    "type": "structure",
                    "side": "dl",
                    "collection": "1",
                    "width": "xx",
                    "height": "yy",
                    "shape": {
                        "type": "arc",
                        "side": "ur"
                    },
                    "attachment": [
                        {
                            "type": "attachmentnone"
                        }
                    ]
                }
            ]
        },
    "typea":typea,
    "types":typea,
    "typed":typea,
    "typef":typea,
})
painter=paintlib.ComponentPainter().update(g1).Draw({
    "type": "componentPainter",
    "statement": [
        {
            "type": "drawCollection",
            "op": "regex",
            "collection": "(\\d+)_(\\d+)",
            "cell": "TOP",
            "l1": "$1",
            "l2": "$2"
        }
    ]
})

# %%输出
# print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#

