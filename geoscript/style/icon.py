from geoscript.util import toURL
from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from geoscript.filter import Filter
from org.geotools.styling import PointSymbolizer, PolygonSymbolizer

class Icon(Symbolizer):

  def __init__(self, url, format):
    Symbolizer.__init__(self)
    self.url = toURL(url)
    self.format = format

  def _prepare(self, rule):
    syms = util.symbolizers(rule, PointSymbolizer)
    for sym in syms:
      self._apply(sym)
    
  def _apply(self, sym):
    eg = self.factory.createExternalGraphic(self.url, self.format)
    g = util.graphic(sym)
    if g:
      g.graphicalSymbols().add(eg)

  def __repr__(self):
    return 'Icon(url=%s,format=%s)%s' % (self.url, self.format,
       self.filter if self.filter != Filter.PASS else '')
