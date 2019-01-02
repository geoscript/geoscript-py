from org.locationtech.jts.io import WKTWriter
from org.geotools.geometry.jts import WKTReader2 as WKTReader
from geoscript.util import deprecated

def readWKT(wkt):
  """
  Constructs a geometry from Well Known Text.

  *wkt* is the Well Known Text string representing the geometry as described by http://en.wikipedia.org/wiki/Well-known_text.

  >>> readWKT('POINT (1 2)')
  POINT (1 2)
  """
  return WKTReader().read(wkt)

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

  return WKTWriter().write(g)
