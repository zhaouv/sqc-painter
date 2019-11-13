# -*- coding: utf-8 -*-
import time
import pya
class IO:
    '''处理输入输出的静态类'''
    #IO:字母 Input Output
    path='/'.join(__file__.replace('\\','/').split('/')[:-2])
    warning=True
    layout=None
    main_window=None
    layout_view=None
    top=None
    auxiliary=None
    link=None
    layer=None
    pointdistance=2000
    centerlineratio=1
    @staticmethod
    def Start(mod="guiopen"):
        if mod=="gds":
            IO.layout=pya.Layout()            
        elif mod=="guinew":
            IO.main_window = pya.Application.instance().main_window()
            IO.layout = IO.main_window.create_layout(1).layout()
            IO.layout_view = IO.main_window.current_view()
            IO.layout_view.rename_cellview("pythonout",0)            
        elif mod=="guiopen":
            IO.main_window = pya.Application.instance().main_window()
            IO.layout_view = IO.main_window.current_view()
            try:
                IO.layout=IO.layout_view.cellview(IO.layout_view.active_cellview_index()).layout()
            except AttributeError as _:
                IO.layout,IO.top=IO.Start("guinew")
                return IO.layout,IO.top
        if len(IO.layout.top_cells())>0:
            IO.top=IO.layout.top_cells()[0]
        else:
            IO.top = IO.layout.create_cell("TOP")
        #
        IO.auxiliary = IO.layout.create_cell("auxiliary")
        IO.top.insert(pya.CellInstArray(IO.auxiliary.cell_index(),pya.Trans()))
        #
        IO.link = IO.layout.create_cell("link")
        IO.auxiliary.insert(pya.CellInstArray(IO.link.cell_index(),pya.Trans()))
        #
        IO.layer=IO.layout.layer(0, 0)
        return IO.layout,IO.top    
        ##layout = main_window.load_layout(string filename,int mode)
    @staticmethod
    def Show():
        if IO.layout_view:
            IO.layout_view.select_cell(IO.top.cell_index(), 0)
            IO.layout_view.max_hier()
            IO.layout_view.add_missing_layers()
            IO.layout_view.zoom_fit()
            strtime=time.strftime("%Y%m%d_%H%M%S")
            print(strtime)
    @staticmethod
    def Write(filename=None):
        if filename==None:
            filename="[pythonout%s].gds"%(time.strftime("%Y%m%d_%H%M%S"))
        print(filename)
        IO.layout.write(filename)