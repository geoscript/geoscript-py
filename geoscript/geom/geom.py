"""
The :mod:`geom` module provides geometry classes and utilities for the construction and manipulation of geometry objects.
"""

from com.vividsolutions.jts.geom import GeometryFactory
from com.vividsolutions.jts.geom import Geometry as _Geometry
from com.vividsolutions.jts.geom.prep import PreparedGeometryFactory
from com.vividsolutions.jts.io import WKTReader, WKBReader, WKBWriter

_factory = GeometryFactory()
_prepfactory = PreparedGeometryFactory()
_wktreader = WKTReader()
_wkbreader = WKBReader()
_wkbwriter = WKBWriter()

Geometry = _Geometry
"""
Base class for all geometry classes.
"""

def fromWKT(wkt):
  """
  Constructs a geometry from Well Known Text.

  *wkt* is the Well Known Text string representing the geometry as described by http://en.wikipedia.org/wiki/Well-known_text.

  >>> fromWKT('POINT (1 2)')
  POINT (1 2)
  """
  return _wktreader.read(wkt)

def fromWKB(wkb):
  """
  Constructs a geometry from Well Known Binary.
  """
  if isinstance(wkb, (str,unicode)):
    from java.math import BigInteger
    wkb = BigInteger(wkb, 16).toByteArray()

  return _wkbreader.read(wkb)
   
def toWKB(g):
  """
  Encodes a geometry as Well Known Binary.
  """

  return _wkbwriter.write(g)
  
def prepare(g):
  """
  Constructs a prepared geometry. Prepared geometries make repeated spatial 
  operations (such as intersection) more efficient.

  *g* is the :class:`Geometry <geoscript.geom.Geometry>` to prepare.

  >>> prep = prepare(fromWKT('POLYGON ((0 0, 10 0, 10 10, 0 10, 0 0))'))
  >>> prep.intersects(fromWKT('POLYGON ((4 4, 6 4, 6 6, 4 6, 4 4))'))
  True
  """
  return _prepfactory.create(g)
  
