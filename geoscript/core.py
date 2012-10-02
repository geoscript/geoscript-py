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

class TypeMapper(object):
  """
  Maps a jython/geoscript type to java/geotools type, and back.
  """

  def __init__(self, fromType, toType, conv=None):
    self.fromType = fromType
    self.toType = toType
    self.conv = conv

  def map(self, obj):
    if isinstance(obj,type):
      return self.toType

    if self.conv:
      return self.conv(obj)
    
    # default is to try and just invoke the constructor
    return self.toType(obj)
  
# forward type map
_fmap = {}

# reverse type map
_rmap = {}

def registerTypeMapping(fromType, toType, conv=None):
  """
  Registers a forward mapping (called by :func:`map`) from a java/geotools
  type to a jython/geoscript type.
  """
  _fmap[fromType] = TypeMapper(fromType, toType, conv)

def registerTypeUnmapping(fromType, toType, conv=None):
  """
  Registers a reverse mapping (called by :func:`unmap`) from a jython/geoscript
  type to a java/geotools type.
  """
  _rmap[fromType] = TypeMapper(fromType, toType, conv)

# register some core type mappers
registerTypeMapping(java.lang.Integer, int)
registerTypeMapping(java.lang.Short, int)
registerTypeMapping(java.lang.Byte, int)
registerTypeUnmapping(int, java.lang.Integer)

registerTypeMapping(java.lang.Long, long)
registerTypeUnmapping(long, java.lang.Long)

registerTypeMapping(java.lang.Boolean, bool)
registerTypeUnmapping(bool, java.lang.Boolean)

registerTypeMapping(java.lang.String, str)
registerTypeUnmapping(str, java.lang.String)
registerTypeUnmapping(unicode, java.lang.String)

registerTypeMapping(java.lang.Double, float)
registerTypeMapping(java.lang.Float, float)
registerTypeUnmapping(float, java.lang.Double)

def map(o):
  """
  Maps a java/geotools type to its associated jython/geoscript type.
  """
  return _doMap(o, _fmap)

def unmap(o):
  """
  Reverse maps a jython/geoscript type to its associated java/geotools type.
  """
  return _doMap(o, _rmap)

def _doMap(o, maps):
  if isinstance(o,type):
    t = o 
  else:
    t = type(o)

  if maps.has_key(t):
    return maps[t].map(o)

  # could not find direct match, look for subclasses
  matches = [x for x in maps.keys() if issubclass(t,x)]
  if len(matches) == 1:
    # single match, go with it
    return maps[matches[0]].map(o)

  return o


