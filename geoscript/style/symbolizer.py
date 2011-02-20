from java import awt
from geoscript.style.factory import Factory
from geoscript.filter import Filter

class Symbolizer(object):

  def __init__(self):
    self.filter = Filter.PASS
    self.scale = (-1,-1)
    self.z = 0
    self.factory = Factory()

  def where(self, filter):
    self.filter = self.filter + filter
    return self

  def range(self, min=-1, max=-1):
    self.scale = (min, max) 
    return self

  def zindex(self, z):
    self.z = z
    return self

  def __add__(self, other):
    from geoscript.style.composite import Composite
    return Composite(self, other)

