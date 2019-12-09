# -*- coding: utf-8 -*-

# 初始化
import json
import pya
import sys
import os
#
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'sqc-painter'))

if 1:
    import paintlib
    # from imp import reload
    # reload(paintlib)
layout, top = paintlib.IO.Start("guiopen")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
paintlib.IO.SetWoringDir(__file__)

marks = paintlib.Interactive.scanBoxes()
paintlib.IO.Show()

print(json.dumps(marks, indent=4))

# 选中的对象个数
# count=0
# for i in paintlib.IO.layout_view.each_object_selected():    
#     # i.shape.transform(pya.CplxTrans(1,90,False,1000*10,1000*0))
#     count+=1
#     pass
print('count:',list(paintlib.IO.layout_view.each_object_selected()).__len__())