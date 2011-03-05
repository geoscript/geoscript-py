from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from geoscript.style.stroke import Stroke
from geoscript.style.icon import Icon
from geoscript.style.hatch import Hatch
from geoscript.filter import Filter
from org.geotools.styling import PolygonSymbolizer

class Fill(Symbolizer):
  """
  Symbolizer for area / polygonal geometries that  fill consists of a ``color`` and
  ``opacity``.

  >>> Fill('#ff0000', 0.5)
  Fill(color=#ff0000,opacity=0.5)

  The ``color`` argument may also be specified as either a well known name or as an
  rgb tuple. 

  >>> fill = Fill('red')
  >>> fill = Fill((255,0,0))
  """

  def __init__(self, color=None, opacity=1.0):
    Symbolizer.__init__(self)
    self.color = color
    self.opacity = opacity
    self._icon = None
    self._hatch = None

  def icon(self, url, format):
    """
    Composes this fill as an :class:`Icon <geoscript.style.icon.Icon>`.

    The ``url`` argument is the url/file containing the image. The ``format`` argument
    is the format or mime type of the image.

    >>> fill = Fill().icon('work/colorblocks.png', 'image/png')
    """
    self._icon = Icon(url, format)
    return self

  def hatch(self, name, stroke=None, size=None): 
    """
    Composes this fill with a hatch pattern.

    The ``name`` argument is the well known name of the hatch pattern. See 
    :class:`Hatch <geoscript.style.hatch.Hatch>` for the list of supported names. 

    The ``stroke`` and ``size`` argument specify the :class:`Stroke` and size to 
    use for the hatch pattern respectively.

    >>> fill = Fill().hatch('slash')
    """
    self._hatch = Hatch(name, stroke, size)
    return self

  def _prepare(self, rule):
    syms = util.symbolizers(rule, PolygonSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    sym.setFill(self._fill())
    
    if self._icon:
      self._icon._apply(sym)

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
    return self._repr('color', 'opacity')
