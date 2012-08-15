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
  if not _fmap.has_key(fromType):
    _fmap[fromType] = []
  _fmap[fromType].append(TypeMapper(fromType, toType, conv))

def registerTypeUnmapping(fromType, toType, conv=None):
  """
  Registers a reverse mapping (called by :func:`unmap`) from a jython/geoscript
  type to a java/geotools type.
  """
  if not _rmap.has_key(fromType):
     _rmap[fromType] = []
  _rmap[fromType].append(TypeMapper(fromType, toType, conv))

# register some core type mappers
registerTypeMapping(java.lang.Integer, int)
registerTypeMapping(java.lang.Short, int)
registerTypeMapping(java.lang.Byte, int)
registerTypeUnmapping(int, java.lang.Integer)

registerTypeMapping(java.lang.Long, long)
registerTypeUnmapping(long, java.lang.Long)

registerTypeMapping(java.lang.String, str)
registerTypeUnmapping(str, java.lang.String)
registerTypeUnmapping(unicode, java.lang.String)

registerTypeMapping(java.lang.Double, float)
registerTypeMapping(java.lang.Float, float)
registerTypeUnmapping(float, java.lang.Double)

def map(o, to=None):
  """
  Maps a java/geotools type to its associated jython/geoscript type.
  """
  return _doMap(o, _fmap, to)

def unmap(o, to=None):
  """
  Reverse maps a jython/geoscript type to its associated java/geotools type.
  """
  return _doMap(o, _rmap, to)

def _doMap(o, maps, to):
  if isinstance(o,type):
    t = o 
  else:
    t = type(o)

  def f(o, tms, to):
    tm = None
    if to and len(tms) > 1:
      for x in tms:
        if issubclass(to, x.toType):
          tm = x
          break
    if not tm:
      tm = tms[0]

    return tm.map(o)

  if maps.has_key(t):
    return f(o, maps[t], to)

  # could not find direct match, look for subclasses
  matches = [x for x in maps.keys() if issubclass(t,x)]
  if len(matches) == 1:
    # single match, go with it
    return f(o, maps[matches[0]], to)

  return o


