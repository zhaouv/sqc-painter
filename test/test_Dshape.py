# -*- coding: utf-8 -*-
#测试pcell
import pya
from math import *

#.insert(pya.Polygon.from_dpoly(x))
layout = pya.Layout()
top = layout.create_cell("TOP")
l1 = layout.layer(1, 0)
#Basic.CIRCLE DONUT ELLIESP ROUND_POLYGON
#Basic.STROKED_BOX STROKED_POLYGON
#ARC CIRCLE DONUT ELLIPSE PIE ROUND_PATH
#ROUND_POLYGON STROKED_BOX STROKED_POLYGON TEXT

#Box
box1=pya.Box(70, 70, 200, 200)
top.shapes(l1).insert(box1)
#Polygon
pts=[pya.Point(0,0),pya.Point(50,0),pya.Point(50,50),pya.Point(40,60),pya.Point(0,50)]
polygon1=pya.Polygon(pts)
top.shapes(l1).insert(polygon1)
#DPath
dpts=[pya.DPoint(0.4,0),pya.DPoint(50,0),pya.DPoint(50,50),pya.DPoint(40.5,60.6),pya.DPoint(0,50)]
dpath1=pya.DPath(dpts,4,5,0,True)
top.shapes(l1).insert(pya.Path.from_dpath(dpath1))
#DCplxTrans
#倍数,逆时针度数,是否绕x翻转,平移x,平移y
tr=pya.DCplxTrans(10,45,False,1000,1000)
#xxx.transform(tr)#本身改变
#xxx.transformed(tr)本身不变返回新的
#对一个点pt做变换的方法
#pya.DEdge(pya.DPoint(),pt).transformed(DCplxTrans).p2

#DText
text1=pya.DText("TEST_Text",pya.DTrans(-10,-10),100,1)
top.shapes(l1).insert(pya.Text.from_dtext(text1))
#a text can be printed @ruby  
#it dose not work in python
#lib.layout.pcell_declaration can't be found
'''
begin
ly = RBA::Layout.new
 top = ly.add_cell("TOP")

 # find the lib
 lib = RBA::Library.library_by_name("Basic")
 lib || raise("Unknown lib 'Basic'")

 # find the pcell
 pcell_decl = lib.layout.pcell_declaration("TEXT")
 pcell_decl || raise("Unknown PCell 'TEXT'")

 # set the parameters
 param = { "text" => "KLAYOUT RULES", "layer" => 
RBA::LayerInfo::new(10, 0), "mag" => 2.5 }

 # build a param array using the param hash as a source
 pv = pcell_decl.get_parameters.collect do |p|
 param[p.name] || p.default
 end

 # create a PCell variant cell
 pcell_var = ly.add_pcell_variant(lib, pcell_decl.id, pv)

 # instantiate that cell
 t = RBA::Trans::new(RBA::Trans::r90, 0, 0)
 pcell_inst = ly.cell(top).insert(RBA::CellInstArray::new(pcell_var, t))

 # write the output
 ly.write("pcells.gds")

ensure
 # if KLayout is started with "-r script.rb" this line ensures that 
the GC has been run
 # before KLayout exists. In particular this removes the link to the 
library which otherwise
 # causes a crash. This will be fixed in version 0.22.2.
 lib = nil
 GC.start

end
'''
#
import time
strtime=time.strftime("%Y%m%d_%H%M%S")
print (strtime)
layout.write("[pythonout%s].gds"%strtime)
print (time.strftime("%H:%M:%S"))
#