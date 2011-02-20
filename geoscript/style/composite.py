from geoscript.style.symbolizer import Symbolizer
from geoscript.filter import Filter
from geoscript.util import seqdict

class Composite(Symbolizer):

  def __init__(self, *parts):
    Symbolizer.__init__(self)
    self.parts = parts

  def where(self, filter):
    for part in self.parts:
      part.where(filter)
    return self
 
  def range(self, min=-1, max=-1):
    for part in self.parts:
      part.range(min, max)
    return self
  
  def zindex(self, z):
    for part in self.parts:
      part.z = z
    return self

  def __repr__(self):
    return '(%s)%s' % (','.join([str(part) for part in self.parts]), 
      self.filter if self.filter != Filter.PASS else '')

  def _style(self):
    # first level table groups by zindex
    ztbl = seqdict()
    q = []
    q.extend(self.parts)
 
    while len(q) > 0:
      sym = q[0]; del q[0]
      if isinstance(sym, Composite):
        [q.insert(0, x) for x in reversed(sym.parts)]
        #q.extend(sym.parts)
      else:
        if not ztbl.has_key(sym.z):
          ztbl[sym.z] = seqdict()
 
        # second level table is scale
        stbl = ztbl[sym.z]
        if not stbl.has_key(sym.scale):
          stbl[sym.scale] = seqdict() 
 
        # third level table is filter
        ftbl = stbl[sym.scale]
        if not ftbl.has_key(sym.filter):
          ftbl[sym.filter] = []
 
        ftbl[sym.filter].append(sym)
          
 
    #import pdb; pdb.set_trace()
    factory = self.factory.style
    style = factory.createStyle()
    for stbl in ztbl.values():
      fts = factory.createFeatureTypeStyle()
      style.addFeatureTypeStyle(fts)
 
      for scale in stbl.keys():
        ftbl = stbl[scale]
        for fil in ftbl.keys():
          syms = ftbl[fil]
          rule = factory.createRule() 
          fts.addRule(rule)
          if scale[0] > -1:
            rule.setMinScaleDenominator(scale[0])
          if scale[1] > -1:
            rule.setMaxScaleDenominator(scale[1])
 
          rule.setFilter(fil._filter)

          for sym in syms:  
            sym._prepare(rule)
             
    return style
