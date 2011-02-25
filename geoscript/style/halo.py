from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from geoscript.style.fill import Fill
from org.geotools.styling import TextSymbolizer

class Halo(Symbolizer):

  def __init__(self, fill=None, radius=1):
    Symbolizer.__init__(self)
    self.fill = fill if fill else Fill('#ffffff')
    self.radius = radius

  def _prepare(self, syms):
    syms = util.symbolizers(syms, TextSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    h = self.factory.createHalo(self.fill._fill(), self._literal(self.radius))
    sym.setHalo(h)

