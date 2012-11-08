from geoscript.style.symbolizer import Symbolizer
from geoscript.filter import Filter

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
      part.zindex(z)
    return self

  def __repr__(self):
    return '(%s)%s' % (','.join([str(part) for part in self.parts]), 
      self.filter if self.filter != Filter.PASS else '')

