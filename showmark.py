# -*- coding: utf-8 -*-

# %% 初始化
if 1:
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

# %% 格式化所有(0,1)层位置
if 1:
    marks = paintlib.Interactive.scanBoxes()
    # marks = paintlib.Interactive.scanBoxes(position='center')
    paintlib.IO.Show()

    print(json.dumps(marks, indent=4))

# %% 选中的对象个数
print('count:', list(paintlib.IO.layout_view.each_object_selected()).__len__())

# %% shape相关

# shape to region
# b=pya.Shapes();b.insert(shape_);c=pya.Region(b);

# count=0
# tl=layout.layer(10, 2)
# for i in paintlib.IO.layout_view.each_object_selected():
#     # i.shape.transform(pya.CplxTrans(1,90,False,1000*10,1000*0))
#     # i.shape.delete()
#     # i.shape.layer=tl
#     count+=1
#     pass

# def asdasdasdasd(sourceLayerList=[(10,10)]):
#     layers = paintlib.Collision.getLayers(layerList=sourceLayerList, layermod='in')
#     for layer in layers:
#         it=paintlib.IO.top.begin_shapes_rec(layer)
#         while not it.at_end():
#             shape_=it.shape()
#             area_=shape_.area()
#             if area_ > 200000:
#                 shape_.delete()
#             it.next()
# asdasdasdasd()


# # RecursiveShapeIterator begin_shapes_rec
# # ObjectInstPath each_object_selected
# for i in paintlib.IO.layout_view.each_object_selected():    
#     # i.shape.transform(pya.CplxTrans(1,90,False,1000*10,1000*0))
#     if not i.shape.is_box():
#         continue
#     b=i.shape.bbox()
#     if b.height()==200 and b.width()==100:
#         i.shape.delete()