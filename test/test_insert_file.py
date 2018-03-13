import pya

# Simple script to merge three top level gds streams
#usage
# klayout -b -r make_TOP.py

layout = pya.Layout()
layout.dbu = 0.001
TOP = layout.create_cell("TOP")
gdsFiles=["[insert].gds","[pythonout20161223_191406].gds"]
for i in gdsFiles:
  layout.read(i)

  for i in layout.top_cells():
  # we don't want to insert the topcell itself
    if (i.name == "insert"):
      print("Adding "+i.name)
      i.name="newname"
      cell_index=i.cell_index()
      new_instance=pya.CellInstArray(cell_index,pya.Trans(pya.Point(0,0)))
      TOP.insert(new_instance)

import time
strtime=time.strftime("%Y%m%d_%H%M%S")
print (strtime)

layout.write("[pythonout%s].gds"%strtime)

print (time.strftime("%H:%M:%S"))
#