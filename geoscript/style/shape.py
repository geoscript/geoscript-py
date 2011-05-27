from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from geoscript.style.fill import Fill
from org.geotools.styling import PointSymbolizer

class Shape(Symbolizer):
  """
  Symbolizer for point geometries that consists of a ``color`` and  ``size``.

  >>> Shape('#ff0000', 5)
  Shape(color=#ff0000,size=5,type=circle)

  The ``type`` argument is a well known name describing the shape type:

  >>> shp = Shape(type='triangle')

  The default shape is "circle". Allowable values include "square", "triangle", 
  "star", "cross", and "x".
  """

  def __init__(self, color=None, size=6, type='circle'):
    Symbolizer.__init__(self)
    self.color = color
    self.size = size
    self.type = type

  def _prepare(self, rule):
    syms = util.symbolizers(rule, PointSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    Symbolizer._apply(self, sym)
    g = util.graphic(sym)
    g.setSize(self._literal(self.size))
    g.graphicalSymbols().clear()
    g.graphicalSymbols().add(self._mark())

  def _mark(self):
    f = self.factory
    mark = f.createMark()

    mark.setFill(Fill(self.color)._fill())
    mark.setWellKnownName(self.type)

    return mark

  def __repr__(self):
    return self._repr('color','size','type')
