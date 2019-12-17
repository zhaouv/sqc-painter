
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
    # 'CavityPainter',
    'Collision',
    # 'Interactive',
    # 'IO',
    # 'Painter',
    # 'PcellPainter',
    # 'SpecialPainter',
    # 'TBD',
    'TransfilePainter',
]:
    asdasfaese = imp.load_source(
        'paintlib.'+moduleName, 'paintlib\\'+moduleName+'.py')
    imp.reload(asdasfaese)
imp.reload(paintlib)

layout, top = paintlib.IO.Start("guiopen")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 1000  # 设置腔的精度,转弯处相邻两点的距离
TBD = paintlib.TBD.init(676987)
# %%[markdown]
# list:
# + [x] AB 数量
# + [x] AB 碰撞
# + [ ] 相关文档
# %%

# 画腔_1
painter3 = paintlib.CavityPainter(pya.DPoint(
    0, 24000), angle=180, widout=48000, widin=16000, bgn_ext=48000, end_ext=16000)
# painter3.painterin.Turning=painter3.painterin.TurningInterpolation
# painter3.painterout.Turning=painter3.painterout.TurningInterpolation

path = 'r 40000 s 50000 r 40000'
for i in range(7):
    path += f's{500000+40000*i} l 40000,180 s{500000+40000*i} r 40000,180'
path += 's 28500'

painter3.Run(path)  # Run内填字符串来描述的内径的运动
# s <length> 直行 r <radius[,angle]> 右转 l <radius[,angle]> 左转 n<number>[<content>] 重复number次content,可以嵌套循环

painter3.Draw(cell2, layer1)  # 把画好的腔置入
# 画Crossover
painter4 = paintlib.TransfilePainter(filepath+"crossover.gds")
painter4.airbridgedistance = 100000  # 设置Crossover的间距
painter4.DrawAirbridgeWithCollisionCheck(cell2, painter3.Getcenterlineinfo(), "Crossover1",28000,1000,1000)

# %%输出
print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#
