"""
The :mod:`geom` module provides geometry classes and utilities for the construction and manipulation of geometry objects.
"""

from com.vividsolutions.jts.geom import GeometryFactory
from com.vividsolutions.jts.geom import Geometry as _Geometry
from com.vividsolutions.jts.io import WKTReader

_factory = GeometryFactory()
_wktreader = WKTReader()

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

