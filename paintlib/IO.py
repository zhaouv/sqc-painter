# -*- coding: utf-8 -*-
import time
import pya


class warningClass:
    #
    minus_stright = True
    big_angle_turning = True
    #
    level = 0

    def warning(self, *a, **k):
        if self.level == 0:
            self.error(*a, **k)
            return
        if self.level == 1:
            if len(a) == 3:
                pya.MessageBox.warning(*a)
            else:
                print(*a, **k)
            return
        if self.level == 2:
            print(*a, **k)
            return
        if self.level == 3:
            pass
            return

    def error(self, *a, **k):
        raise RuntimeError(a, k)


class IO:
    '''处理输入输出的静态类'''
    # IO:字母 Input Output
    path = '/'.join(__file__.replace('\\', '/').split('/')[:-2])
    workingDir = '/'.join(__file__.replace('\\', '/').split('/')[:-2])
    #
    warning = warningClass()
    #
    layout = None
    main_window = None
    layout_view = None
    top = None
    auxiliary = None
    link = None
    layer = None
    pointdistance = 2000
    centerlineratio = 1
    @staticmethod
    def Start(mod="guiopen"):
        if mod == "gds":
            IO.layout = pya.Layout()
        elif mod == "guinew":
            IO.main_window = pya.Application.instance().main_window()
            IO.layout = IO.main_window.create_layout(1).layout()
            IO.layout_view = IO.main_window.current_view()
            IO.layout_view.rename_cellview("pythonout", 0)
        elif mod == "guiopen":
            IO.main_window = pya.Application.instance().main_window()
            IO.layout_view = IO.main_window.current_view()
            try:
                IO.layout = IO.layout_view.cellview(
                    IO.layout_view.active_cellview_index()).layout()
            except AttributeError as _:
                return IO.Start("guinew")
        if len(IO.layout.top_cells()) > 0:
            IO.top = IO.layout.top_cells()[0]
        else:
            IO.top = IO.layout.create_cell("TOP")
        #
        IO.auxiliary = IO.layout.create_cell("auxiliary")
        IO.top.insert(pya.CellInstArray(
            IO.auxiliary.cell_index(), pya.Trans()))
        #
        IO.link = IO.layout.create_cell("link")
        IO.auxiliary.insert(pya.CellInstArray(
            IO.link.cell_index(), pya.Trans()))
        #
        IO.layer = IO.layout.layer(0, 0)
        for li1, li2 in [(0, 1), (0, 2)]:
            IO.layout.layer(li1, li2)
        return IO.layout, IO.top
        # layout = main_window.load_layout(string filename,int mode)

    @staticmethod
    def SetWoringDir(filename):
        '''
        paintlib.IO.SetWoringDir(__file__)
        '''
        IO.workingDir = '/'.join(filename.replace('\\', '/').split('/')[:-1])

    @staticmethod
    def Show():
        if IO.layout_view:
            IO.layout_view.select_cell(IO.top.cell_index(), 0)
            IO.layout_view.max_hier()
            IO.layout_view.add_missing_layers()
            IO.layout_view.zoom_fit()
            strtime = time.strftime("%Y%m%d_%H%M%S")
            print(strtime)

    @staticmethod
    def Write(filename=None):
        if filename == None:
            filename = IO.workingDir + \
                "/[pythonout%s].gds" % (time.strftime("%Y%m%d_%H%M%S"))
        print(filename)
        IO.layout.write(filename)
    
    @staticmethod
    def Flatten(newcellname=''):
        IO.top.flatten(True)
        if newcellname:
            IO.top.name=str(newcellname)

    @staticmethod
    def RemoveAuxiliary():
        IO.auxiliary.flatten(True)
        IO.auxiliary.delete()