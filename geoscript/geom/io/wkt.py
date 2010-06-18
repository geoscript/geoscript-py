from com.vividsolutions.jts.io import WKTReader, WKTWriter, WKBReader, WKBWriter
from geoscript.util import deprecated

_wktreader = WKTReader()
_wktwriter = WKTWriter()
_wkbreader = WKBReader()
_wkbwriter = WKBWriter()

def readWKT(wkt):
  """
  Constructs a geometry from Well Known Text.

  *wkt* is the Well Known Text string representing the geometry as described by http://en.wikipedia.org/wiki/Well-known_text.

  >>> readWKT('POINT (1 2)')
  POINT (1 2)
  """
  return _wktreader.read(wkt)

@deprecated
def fromWKT(wkt):
  """Use :func:`readWKT`"""

  return readWKT(wkt)

def writeWKT(g):
  """
  Writes a geometry as Well Known Text.

  *g* is the geometry to serialize.

  >>> from geoscript.geom import Point
  >>> str(writeWKT(Point(1,2)))
  'POINT (1 2)'
  """

  return _wktwriter.write(g)

def readWKB(wkb):
  """
  Constructs a geometry from Well Known Binary.

  >>> 
  """
  if isinstance(wkb, (str,unicode)):
    from java.math import BigInteger
    wkb = BigInteger(wkb, 16).toByteArray()

  return _wkbreader.read(wkb)

@deprecated
def fromWKB(wkb):
  """Use :func:`readWKB`"""
  return readWKB(wkb)
   
def writeWKB(g):
  """
  Encodes a geometry as Well Known Binary.
  """

  return _wkbwriter.write(g)

@deprecated
def toWKB(g):
  """Use :func:`writeWKB`"""
  return writeWKB(g)

