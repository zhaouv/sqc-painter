
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
# + [ ] 相关文档

# + [x] lift-off 层专用字体
# + [ ] 整合
# + [ ] 相关文档

# %%
layer1 = layout.layer(10, 10)  # 创建新层

cell2 = layout.create_cell("Cavity1")  # 创建一个子cell
top.insert(pya.CellInstArray(cell2.cell_index(), pya.Trans()))
''' # 三平行线的腔
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
'''
# painter2 = paintlib.PcellPainter()
# painter2.DrawText(top, layer1, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()-=_+[]{}\\\\|;:'\",.<>/?",
#                   pya.DCplxTrans(1, 0, False, 0, 0))

stringa='''
sqc-painter

0123456789ab 
z          c
y alphabet d
x          e
w for      f
v lift-off g
u          h
tsrqponmlkji

~!@#$%^&*()-=_+[]
{}\\|;:'\",.<>/?`
'''
#%%
reverse=False
cellname='text'
layer=layer1
cell=top
string=stringa


def drawtext(cell,layer,string,cellname,tr=pya.DCplxTrans(1, 0, False, 0, 0)):
    reverse=False
    charset="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ~!@#$%^&*()-=_+[]{}\\|;:'\",.<>/?`"

    filename=paintlib.IO.path+'/paintlib/gds/chars.gds'
    layout = pya.Layout()
    layout.read(filename)
    cellList = [ii for ii in layout.top_cells()]

    layerList = [(10, 10)]
    _layerlist = []
    for ii in layerList:
        _layerlist.append(layout.find_layer(ii[0], ii[1]))
    layers = [index for index in layout.layer_indices() if index in _layerlist]

    fullregion = pya.Region()
    for layer_ in layers:
        fullregion.insert(cellList[0].begin_shapes_rec(layer_))
    fullregion.merge()

    charshapes=[]
    for ii in range(len(charset)):
        subregion=pya.Region(pya.Box(ii*600,0,ii*600+500,700))
        if not reverse:
            subregion=subregion & fullregion
        else:
            subregion=subregion - fullregion
        subregion.merge()
        subregion.transform(pya.ICplxTrans(1, 0, False, -ii*600, 0))
        charshapes.append(subregion)
        # paintlib.BasicPainter.Draw(cell2,layer1,subregion)
        pass


    ncell = paintlib.IO.layout.create_cell(cellname)  
    cell.insert(pya.CellInstArray(ncell.cell_index(), pya.ICplxTrans.from_dtrans(tr)))

    currentx=0
    currenty=0

    for cc in string.upper():
        if cc=='\n':
            currenty+=1
            currentx=0
            continue
        if cc in charset:
            ii=charset.index(cc)
            paintlib.BasicPainter.Draw(ncell,layer,charshapes[ii].transformed(pya.ICplxTrans(1, 0, False, currentx*600, -currenty*800)))
            currentx+=1
            continue
        if cc in '\r\t\b\f':
            continue
        raise RuntimeError(f'"{cc}" is not supported')

drawtext(cell,layer,string,cellname,tr=pya.DCplxTrans(1, 0, False, 0, 0))
# drawtext(cell,layer,string,cellname,tr=pya.DCplxTrans(0.6, 15, True, 9000, -6000))
    
# %% 删小面积区域

tl=layout.layer(10, 2)
def asdasdasdasd(targetLayer,sourceLayerList=[(10,10)]):
    layers = paintlib.Collision.getLayers(layerList=sourceLayerList, layermod='in')

    for layer in layers:
        it=paintlib.IO.top.begin_shapes_rec(layer)
        while not it.at_end():
            shape_=it.shape()
            area_=shape_.area()
            if area_ > 200000:
                shape_.layer=tl
                # shape_.delete() 也可以放弃上一句直接这样删除
            it.next()
asdasdasdasd(targetLayer=tl)

# RecursiveShapeIterator begin_shapes_rec
# #  ObjectInstPath each_object_selected
# for i in paintlib.IO.layout_view.each_object_selected():    
#     # i.shape.transform(pya.CplxTrans(1,90,False,1000*10,1000*0))
#     if not i.shape.is_box():
#         continue
#     b=i.shape.bbox()
#     if b.height()==200 and b.width()==100:
#         i.shape.delete()
#         i.shape.layer=tl
#         # i.shape.transform(pya.CplxTrans(1,0,False,1000*34048,0))
# %%输出
print(TBD.isFinish())
paintlib.IO.Show()  # 输出到屏幕上
# paintlib.IO.Write()#输出到文件中
#

