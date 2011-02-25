from geoscript.style.symbolizer import Symbolizer
from geoscript.style.hatch import Hatch
from geoscript.filter import Filter
from geoscript.style import util
from org.geotools.styling import LineSymbolizer

class Stroke(Symbolizer):

  def __init__(self, color='#000000', width=1, dash=None, cap=None, join=None):
    Symbolizer.__init__(self)
    self.color = color
    self.width = width
    self.dash = dash
    self.cap = cap
    self.join = join
    self._hatch = None

  def hatch(self, name, stroke=None, size=None):
    self._hatch = Hatch(name, stroke, size)
    return self

  def _prepare(self, rule):
    syms = util.symbolizers(rule, LineSymbolizer)
    for sym in syms:
      self._apply(sym)
    
  def _apply(self, sym):
    sym.setStroke(self._stroke())

  def _stroke(self):
    f = self.factory
    stroke = f.createStroke(f.filter.literal(util.color(self.color)), 
      f.filter.literal(self.width))

    if self.dash:
      if isinstance(self.dash, tuple): 
        stroke.setDashArray(self.dash[0])
        stroke.setDashOffset(f.filter.literal(self.dash[1]))
      else:
        stroke.setDashArray(self.dash)

    if self.cap:
      stroke.setLineCap(f.filter.literal(self.cap))
    if self.join:
      stroke.setLineJoin(f.filter.literal(self.join))
   
    if self._hatch:
      stroke.setGraphicStroke(self._hatch._hatch())

    return stroke

  def __repr__(self):
    return self.__repr__(color=self.color, width=self.width)

