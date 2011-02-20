from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from geoscript.filter import Filter
from org.geotools.styling import PolygonSymbolizer

class Fill(Symbolizer):

  def __init__(self, color):
    Symbolizer.__init__(self)
    self.color = color

  def _prepare(self, rule):
    syms = filter(lambda s: isinstance(s,PolygonSymbolizer), rule.symbolizers()) 
    if len(syms) == 0:
      sym = self.factory.style.createPolygonSymbolizer()
      rule.symbolizers().add(sym)
      syms.append(sym)
      
    f = self.factory
    for sym in syms:
      sym.setFill(f.style.createFill(f.filter.literal(util.color(self.color))))
    
  def __repr__(self):
    return 'Fill(color=%s)%s' % (self.color, 
       self.filter if self.filter != Filter.PASS else '')
