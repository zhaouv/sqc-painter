
# %%

import pya
import sys
import os

sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import paintlib
import imp
for moduleName in [
    'AttachmentTree',
    # 'AutoRoute',
    # 'BasicPainter',
    # 'CascadeRoute',
    # 'CavityBrush',
    # 'CavityPainter',
    # 'Collision',
    # 'GridLayout',
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

class g:
    pass

def main():
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


    # %%输出
    # print(TBD.isFinish())
    paintlib.IO.Show()  # 输出到屏幕上
    # paintlib.IO.Write()#输出到文件中
    #

