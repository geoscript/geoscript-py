from org.locationtech.jts.io import WKBReader, WKBWriter
from geoscript.util import bytes, deprecated

def readWKB(wkb, base=16):
  """
  Constructs a geometry from Well Known Binary.

  *wkb* may be specified as a `list` or an `array`. It may also be supplied
  as a `str` in which the *base* argument is used to specify the base/radix
  with which to interpret the string.

  >>> readWKB([0,0,0,0,1,63,-16,0,0,0,0,0,0,64,0,0,0,0,0,0,0])
  POINT (1 2)

  >>> readWKB('00000000013ff00000000000004000000000000000', 16)
  POINT (1 2)
  """
  if isinstance(wkb, (str,unicode)):
    wkb = bytes.decode(wkb, base)

  return WKBReader().read(wkb)

@deprecated
def fromWKB(wkb):
  """Use :func:`readWKB`"""
  return readWKB(wkb)
   
def writeWKB(g, base=None):
  """
  Encodes a geometry as Well Known Binary.

  By default this function returns the raw bytes composing the WKB. However if 
  the *base* parameter is specified it will return the wkb encoded in that base.

  >>> from geoscript.geom import Point
  >>> writeWKB(Point(1,2), 16)
  '00000000013ff00000000000004000000000000000'
  """
  wkb = WKBWriter().write(g)
  return bytes.encode(wkb, base) if base else wkb

@deprecated
def toWKB(g):
  """Use :func:`writeWKB`"""
  return writeWKB(g)

