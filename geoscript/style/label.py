from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from geoscript.style.font import Font
from geoscript.style.halo import Halo
from org.geotools.styling import TextSymbolizer

class Label(Symbolizer):

  def __init__(self, property):
    Symbolizer.__init__(self)
    self.property = property
    self._font = None
    self._halo = None
    self._placement = None
    self.options = {}

  def font(self, font):
    self._font = Font(font)
    return self

  def halo(self, fill=None, radius=1):
    self._halo = Halo(fill, radius)
    return self

  def point(self, anchor=(0,0), displace=(0,0), rotate=0):
    f = self.factory
    ap = f.createAnchorPoint(self._literal(anchor[0]), self._literal(anchor[1]))
    dp = f.createDisplacement(self._literal(displace[0]), self._literal(displace[1]))
    self._placement = f.createPointPlacement(ap, dp, self._literal(rotate))
    return self

  def linear(self, offset=0, gap=None, igap=None, align=False, follow=False, 
             displace=None, repeat=None):
    f = self.factory
    lp = f.createLinePlacement(self._literal(offset))
    lp.setAligned(align)
    #lp.setRepeated(repeat)
    if gap:   
      lp.setGap(self._literal(gap))
    if igap:
      lp.setInitialGap(self._literal(gap))
    self._placement = lp

    self.options = {"followLine": follow}
    if displace:
      self.options['maxDisplacement'] = displace
    if repeat:
      self.options['repeat'] = repeat
    return self

  def _prepare(self, rule):
    syms = util.symbolizers(rule, TextSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    sym.setLabel(self.factory.filter.property(self.property))

    if self._font:
      self._font._apply(sym)
    if self._halo:
      self._halo._apply(sym)

    if self._placement:
      sym.setLabelPlacement(self._placement)

    for k,v in self.options.iteritems(): 
	  sym.getOptions()[k] = str(v)

  def __repr__(self):
    return self.__repr__(property=self.property)
