from geoscript.style import util
from geoscript.style.color import Color
from geoscript.style.expression import Expression
from geoscript.style.fill import Fill
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import TextSymbolizer

class Halo(Symbolizer):
  """
  Symbolizer for label background.

  A halo is composed of a :class:`Fill <geoscript.style.fill.Fill>` and a ``radius`` 
  that specifies the extend the of background.

  >>> Halo(Fill('white'), 4)
  Halo(fill=Fill(color=(255,255,255),opacity=1.0),radius=4)
  """
  def __init__(self, fill=None, radius=1):
    Symbolizer.__init__(self)
    if fill:
      if not isinstance(fill, Fill):
        fill = Fill(Color(fill))
    else:
      fill = Fill('#ffffff')
    self.fill = fill
    self.radius = Expression(radius)

  def _prepare(self, syms):
    syms = util.symbolizers(syms, TextSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    Symbolizer._apply(self, sym)
    h = self.factory.createHalo(self.fill._fill(), self.radius.expr)
    sym.setHalo(h)

  def __repr__(self):
    return self._repr('fill','radius')
