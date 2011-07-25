import sys
from java import awt
from geoscript.style.factory import StyleFactory
from geoscript.style import io
from geoscript.filter import Filter
from geoscript.util import seqdict

class Symbolizer(object):
  """
  Base class for all symbolizers.
  """

  def __init__(self):
    self.filter = Filter.PASS
    self.scale = (-1,-1)
    self.z = 0
    self.options = {}
    self.factory = StyleFactory()

  def where(self, filter):
    """
    Appies a filter to the symbolizer. The ``filter`` argument can be a CQL string or
    an instance of :class:`Filter <geoscript.filter.Filter>`.
    """
    self.filter = self.filter + filter
    return self

  def range(self, min=-1, max=-1):
    """
    Applies a min/max scale denominator to the symbolizer.
    """
    self.scale = (min, max) 
    return self

  def zindex(self, z):
    """
    Applies a z-index to the symbolizer. Symbolizers with a higher z-index are drawn on
    top of those with a smaller z-index.
    """
    self.z = z
    return self

  def asSLD(self, out=sys.stdout):
    """
    Serializes the symbolizer to SLD. The ``out`` argument is the file/output stream to
    write to.
    """
    io.writeSLD(self, out)
     
  def _apply(self, sym):
    for k,v in self.options.iteritems(): 
	  sym.getOptions()[k] = str(v)

  def __add__(self, other):
    from geoscript.style.composite import Composite
    return Composite(self, other)

  def _style(self):
    from geoscript.style.composite import Composite
    # first level table groups by zindex
    ztbl = seqdict()
    q = [self]
 
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
          
 
    style = self.factory.createStyle()
    for stbl in ztbl.values():
      fts = self.factory.createFeatureTypeStyle()
      style.addFeatureTypeStyle(fts)
 
      for scale in stbl.keys():
        ftbl = stbl[scale]
        for fil in ftbl.keys():
          syms = ftbl[fil]
          rule = self.factory.createRule() 
          fts.addRule(rule)
          if scale[0] > -1:
            rule.setMinScaleDenominator(scale[0])
          if scale[1] > -1:
            rule.setMaxScaleDenominator(scale[1])
 
          rule.setFilter(fil._filter)

          for sym in syms:  
            sym._prepare(rule)
             
    return style

  def _repr(self, *props):
    return '%s(' % (self.__class__.__name__) + ','.join(
      ['%s=%s' % (p, getattr(self, p)) for p in props]) + ')%s' % (   
      self.filter if self.filter != Filter.PASS else '')
