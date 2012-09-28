from geoscript.style import util
from geoscript.style.color import Color
from geoscript.style.expression import Expression
from geoscript.style.fill import Fill, Stroke
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import PointSymbolizer

class Shape(Symbolizer):
  """
  Symbolizer for point geometries that consists of a ``color`` and  ``size``.

  >>> Shape('#ff0000', 5)
  Shape(color=(255,0,0),size=5,type=circle)

  The ``type`` argument is a well known name describing the shape type:

  >>> shp = Shape(type='triangle')

  The default shape is "circle". Allowable values include "square", "triangle", 
  "star", "cross", and "x".
  """

  def __init__(self, color=None, size=6, type='circle', opacity=1.0, rotation=0):
    Symbolizer.__init__(self)
    self.color = Color(color) if color else None
    self.size = Expression(size)
    self.type = type
    self.opacity = Expression(opacity)
    self.rotation = Expression(rotation)
    self._stroke = None

  def stroke(self, color="#000000", width=1, dash=None, cap=None, join=None):
    self._stroke = Stroke(color, width, dash, cap, join)
    return self

  def _prepare(self, rule):
    syms = util.symbolizers(rule, PointSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    Symbolizer._apply(self, sym)
    g = util.graphic(sym)
    g.setSize(self.size.expr)
    if self.rotation != None and self.rotation.expr != None:
        g.setRotation(self.rotation.expr)
    g.graphicalSymbols().clear()
    g.graphicalSymbols().add(self._mark())

  def _mark(self):
    f = self.factory
    mark = f.createMark()
    if self._stroke != None:
        mark.setStroke(self._stroke._stroke())
    else:
        mark.setStroke(Stroke(self.color)._stroke())
    if self.color != None and self.color.expr != None:
        mark.setFill(Fill(self.color, self.opacity)._fill())
    else:
        mark.setFill(None)
    mark.setWellKnownName(self.type)

    return mark

  def __repr__(self):
    return self._repr('color','size','type')
