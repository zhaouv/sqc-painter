import pya


class Generator:

  def __init__(self):

    self.layout = pya.Layout()
    self.layout.dbu = 0.001

    self.top = self.layout.create_cell("TOP")
    self.layer_index = self.layout.insert_layer(pya.LayerInfo(15,99))

    self.lib = pya.Library.library_by_name("Basic")
    if self.lib == None:
      raise Exception("Unknown lib 'Basic'")

    self.pcell_decl = self.lib.layout().pcell_declaration("TEXT");
    if self.pcell_decl == None:
      raise Exception("Unknown PCell 'TEXT'")

  def make_pattern(self, l, w, xpos, ypos, num):

    a1 = [ 
      pya.Point(0, 0), 
      pya.Point(100, 0), 
      pya.Point(100, l + w), 
      pya.Point(200, l + w), 
      pya.Point(200, 0), 
      pya.Point(300, 0) 
    ]

    y1 = l + w / 2 - 20
    x1 = 150
    d1 = [ pya.Point(x1, y1), pya.Point(x1, -w / 2) ]

    y2 = w / 2 + 20
    x2 = 50
    e1 = [ pya.Point(x2, y2), pya.Point(x2, l + w + w / 2) ]


    unit_cell = self.layout.create_cell("1")
    unit_cell.shapes(self.layer_index).insert(pya.Path(a1, w))
    unit_cell.shapes(self.layer_index).insert(pya.Path(d1, w))
    unit_cell.shapes(self.layer_index).insert(pya.Path(e1, w))
    unit_cell.shapes(self.layer_index).insert(pya.Box(x1 - w / 2 - 2, y1 - 2, x1 - w / 2 + 2, y1 + 2))
    unit_cell.shapes(self.layer_index).insert(pya.Box(x1 + w / 2 + 2, y1 - 2, x1 + w / 2 + 2, y1 + 2))
    unit_cell.shapes(self.layer_index).insert(pya.Box(x2 - w / 2 - 2, y2 - 2, x2 - w / 2 + 2, y2 + 2))
    unit_cell.shapes(self.layer_index).insert(pya.Box(x2 + w / 2 + 2, y2 - 2, x2 + w / 2 + 2, y2 + 2))

    nx = 45
    dx = 200
    ny = 28
    dy = 320
    ox = xpos
    oy = ypos

    trans = pya.Trans(pya.Point(ox, oy))
    ax = pya.Point(dx, 0)
    ay = pya.Point(0, dy)
    self.top.insert(pya.CellInstArray(unit_cell.cell_index(), trans, ax, ay, nx, ny))

    # Note: this is the translation of named parameters to the PCell specific parameter vector
    # pv. Since the parameter vector is built the same way always, we could simply exchange the 
    # text parameter, given we have the index.

    param = { 
      "text": "%02d-%06d" % ( l, num ), 
      "layer": pya.LayerInfo(15,99), 
      "mag": 1 
    }

    pv = []
    for p in self.pcell_decl.get_parameters():
      if p.name in param:
        pv.append(param[p.name])
      else:
        pv.append(p.default)

    # "fake PCell code" - see other thread ("Creating letters")
    text_cell = self.layout.create_cell("1T")
    self.pcell_decl.produce(self.layout, [ self.layer_index ], pv, text_cell)

    t = pya.Trans(pya.Trans.R0, -1000 + xpos, -1000 + ypos)
    self.top.insert(pya.CellInstArray(text_cell.cell_index(), t))

  def done(self, filename):
    self.layout.write(filename)
    print("Output file written: " + filename)

# =================================================================

g = Generator()

ncolumns = 3
nrows = 2
num = 1

for i in range(0, ncolumns):
  print("Column " + str(i+1) + "/" + str(ncolumns) + " ..")
  for j in range(0, nrows):
    g.make_pattern(50 + (i + j) % 73, 30, 15000 * i, 15000 * j, num)
    num = num + 1

g.done("test.gds")
