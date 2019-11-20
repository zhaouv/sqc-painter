
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

layout, top = paintlib.IO.Start("guiopen")  # 在当前的图上继续画,如果没有就创建一个新的
layout.dbu = 0.001  # 设置单位长度为1nm
paintlib.IO.pointdistance = 2000  # 设置腔的精度,转弯处相邻两点的距离
TBD = paintlib.TBD.init(676987)
# %%[markdown]
# list:
# + [x] TraceRunner.reverse
# %%
tr=paintlib.TraceRunner()
a='s 123 l 3456 r 345 '
print(tr.reversePath(a))
a='s_ 123 n3[ l 3456 n3[ l 3456 r 345] r 345] r4567 '
print(tr.reversePath(a))

# %%输出
print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#
