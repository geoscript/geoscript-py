from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from geoscript.style.stroke import Stroke
from geoscript.style.hatch import Hatch
from geoscript.filter import Filter
from org.geotools.styling import PolygonSymbolizer

class Fill(Symbolizer):

  def __init__(self, color=None, opacity=1.0, icon=None):
    Symbolizer.__init__(self)
    self.color = color
    self.opacity = opacity
    self.icon = icon
    self._hatch = None

  """
  name one of "vertline","horline","slash"," backslash","dot", "plus", "times", 
  "oarrow","carrow","cross","circle","triangle","X","star","arrow","hatch","square"
  """
  def hatch(self, name, stroke=None, size=None): 
    self._hatch = Hatch(name, stroke, size)
    return self

  def _prepare(self, rule):
    syms = util.symbolizers(rule, PolygonSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    sym.setFill(self._fill())
    
    if self.icon:
      self.icon._apply(sym)

  def _fill(self):
    f = self.factory
    fill = f.createFill()

    if self.color:
      fill.setColor(f.filter.literal(util.color(self.color)))

    if self._hatch:
      fill.setGraphicFill(self._hatch._hatch())  

    fill.setOpacity(f.filter.literal(self.opacity))

    return fill

  def __repr__(self):
    return self.__repr__(color=self.color,opacity=self.opacity)
