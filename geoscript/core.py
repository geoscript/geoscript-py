import java
from org.python.core.adapter import ClassAdapter

class ProxyRenamer(ClassAdapter):

  def __init__(self, cls):
    self.name = cls.__name__
    ClassAdapter.__init__(self, cls)

  def rename(self):
    self.adaptedClass.__name__ = self.name

def register(t):
   ProxyRenamer(t).rename()

_tmap = {}
_tmap[int] = java.lang.Integer
_tmap[java.lang.Integer] = int
_tmap[java.lang.Short] = int
_tmap[java.lang.Float] = int

_tmap[long] = java.lang.Long
_tmap[java.lang.Long] = long

_tmap[str] = java.lang.String
_tmap[unicode] = java.lang.String
_tmap[java.lang.String] = str

_tmap[float] = java.lang.Double
_tmap[java.lang.Double] = float
_tmap[java.lang.Float] = float

"""
Maps a jython type to its associated java type.
"""
def map(o):
  if isinstance(o,type):
    t = o 
  else:
    t = type(o)

  if _tmap.has_key(t):
    mapped = _tmap[t]
    if isinstance(o,type):
      return mapped
    else:
      return mapped(o)

  return o

