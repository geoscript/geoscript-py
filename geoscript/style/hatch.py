from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import LineSymbolizer, PolygonSymbolizer

class Hatch(Symbolizer):

  def __init__(self, name, stroke=None, size=None):
    Symbolizer.__init__(self)
    self.name = name
    if not stroke:
      from geoscript.style.stroke import Stroke
      stroke = Stroke()

    self.stroke = stroke 
    self.size = size if size else 8

  def _prepare(self, syms):
    raise Exception('not implemnted')

  def _apply(self, sym):
    raise Exception('not implemnted')

  def _hatch(self):
    f = self.factory
    mark = f.createMark()
    mark.setWellKnownName('shape://%s' % self.name)
    mark.setStroke(self.stroke._stroke())

    graphic = self.factory.createGraphic()    
    graphic.graphicalSymbols().clear()
    graphic.graphicalSymbols().add(mark)
    graphic.setSize(self.size)

    return graphic
