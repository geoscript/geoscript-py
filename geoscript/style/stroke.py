from geoscript.style.symbolizer import Symbolizer
from geoscript.filter import Filter
from geoscript.style import util
from org.geotools.styling import LineSymbolizer

class Stroke(Symbolizer):

  def __init__(self, color, width=1):
    Symbolizer.__init__(self)
    self.color = color
    self.width = width

  def __repr__(self):
    return 'Stroke(color=%s, width=%d)%s' % (self.color, self.width, 
       self.filter if self.filter != Filter.PASS else '')

  def _prepare(self, rule):
    syms = filter(lambda s: isinstance(s,LineSymbolizer), rule.symbolizers()) 
    if len(syms) == 0:
      sym = self.factory.style.createLineSymbolizer()
      rule.symbolizers().add(sym)
      syms.append(sym)
      
    f = self.factory
    for sym in syms:
      sym.setStroke(f.style.createStroke(f.filter.literal(util.color(self.color)), 
        f.filter.literal(self.width)))
    
   
  def _symbolizer(self, geom=None):
    return util.lineSymbolizer(self.color, self.width)
