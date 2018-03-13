import pya

# Simple script to merge three top level gds streams
#usage
# klayout -b -r make_TOP.py

layout = pya.Layout()
layout.dbu = 0.001
TOP = layout.create_cell("TOP")
gdsFiles=["[pythonout20161223_154428].gds","[pythonout20161223_191406].gds"]
for i in gdsFiles:
  layout.read(i)

  for i in layout.top_cells():
  # we don't want to insert the topcell itself
    if (i.name != "TOP"):
      print("Adding "+i.name)
      cell_index=i.cell_index()
      new_instance=pya.CellInstArray(cell_index,pya.Trans(pya.Point(0,0)))
      TOP.insert(new_instance)

layout.write("TOP.gds")
