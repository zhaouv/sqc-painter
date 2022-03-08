
# %%

import pya
import sys
import os

sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import paintlib
import imp
for moduleName in [
    # 'AutoRoute',
    # 'BasicPainter',
    # 'CavityBrush',
    'CavityPainter',
    # 'Collision',
    # 'Interactive',
    # 'IO',
    # 'Painter',
    # 'PcellPainter',
    # 'SpecialPainter',
    # 'TBD',
    # 'TransfilePainter',
]:
    pass
    asdasfaese = imp.load_source(
        'paintlib.'+moduleName, 'paintlib\\'+moduleName+'.py')
    imp.reload(asdasfaese)
imp.reload(paintlib)

layout, top = paintlib.IO.Start("guinew")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
TBD = paintlib.TBD.init(676987)
# %%[markdown]
# list:

# + [ ] ?几个碰撞检测或基于已有图形的例子和最佳实践
# + [ ] ?碰撞检测的ab, 通过切分来优化速度

# + [x] DrawContinueAirbridgePainter 想要超出腔的说明
# + [x] DrawContinueAirbridgePainter 圆角
# + [x] DrawContinueAirbridgePainter 圆角 textcover/文档
# + [ ] DrawContinueAirbridgePainter recordw3pts droplastw3 textcover/文档

# %%
layer = layout.layer(10, 10)  
layer1 = layout.layer(10, 3)  
layer2 = layout.layer(10, 2)  

cell = layout.create_cell("Cavity1")  
top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))

# %% round
a=pya.DPolygon(paintlib.BasicPainter.rectangle(pya.DPoint(),pya.DPoint(0,50000),1000000)[0])
paintlib.BasicPainter.Draw(cell,layer,a)
b=paintlib.PcellPainter().round(a,300,10000)
paintlib.BasicPainter.Draw(cell,layer,b)
# %%输出
print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#

