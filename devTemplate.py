
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
# + [x] AB 数量
# + [x] AB 碰撞
# + [ ] test cover
# + [ ] 相关文档

# + [x] 三平行线的腔
# + [ ] 三平行线的腔
# %%
layer1 = layout.layer(10, 10)  # 创建新层

cell2 = layout.create_cell("Cavity1")  # 创建一个子cell
top.insert(pya.CellInstArray(cell2.cell_index(), pya.Trans()))
painter3 = paintlib.TriCavityPainter(pya.DPoint(
    0, 24000), angle=180, widout=48000, widin=36000, bgn_ext=0, end_ext=0)

path = 'r 40000 s 50000 r 40000'
for i in range(7):
    path += f's{500000+40000*i} l 40000,180 s{500000+40000*i} r 40000,180'
path += 's 28500'

painter5=paintlib.CavityPainter(painter3.brushr.reversed())
painter5.Run('s80000 r45000')
painter5.Electrode()
painter5.Draw(cell2, layer1)  # 把画好的腔置入


painter3.Run(path)

painter3.Draw(cell2, layer1)  # 把画好的腔置入

painter4=paintlib.CavityPainter(painter3.brushl)
painter4.Run('s20000 l45000')
painter4.Electrode()
painter4.Draw(cell2, layer1)  # 把画好的腔置入


# %%输出
print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#

