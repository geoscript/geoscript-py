from java.lang import Double
from com.vividsolutions.jts.geom import Coordinate, GeometryFactory
from com.vividsolutions.jts.io import WKTReader

_gf = GeometryFactory()
_wktreader = WKTReader()

def Point(x,y,z=Double.NaN):
  return _gf.createPoint(Coordinate(x,y,z))

def LineString(coords):
  l = []
  for c in coords:
    l.append( Coordinate(c[0],c[1]) )
    if len(c) > 2:
      l[-1].z = c[2]

  if l[0] == l[-1]:
    return _gf.createLinearRing(l)
  else:
    return _gf.createLineString(l)

def Polygon(ring,holes=None):
  outer = LineString(ring)
  inner = []
  if holes:
    for h in holes:
      inner.append(_gf.linestring(h))

  return _gf.createPolygon(outer,inner)

def Geometry(wkt):
  return _wktreader.read(wkt)
