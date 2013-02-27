from geoscript.style import util
from geoscript.style.expression import Expression
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import RasterSymbolizer

class Opacity(Symbolizer):

  def __init__(self, value=1.0):
    Symbolizer.__init__(self)
    self.value = Expression(value)

  def _prepare(self, rule):
    syms = util.symbolizers(rule, RasterSymbolizer)
    for sym in syms:
      self._apply(sym)
    
  def _apply(self, sym):
    Symbolizer._apply(self, sym)
    sym.setOpacity(self.value.expr)

  def __repr__(self):
    return self._repr('value')

