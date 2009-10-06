"""
The :mod:`geom` module provides utilities for the construction and manipulation of 
geometry objects.

In general constructors in this module take lists of ``list`` defining the coordinates that make up the geometry.

>>> linestring([ [1,2], [3,4] ])
LINESTRING (1 2, 3 4)

Or alternatively lists of ``tuple``.

>>> linestring([ (1,2), (3,4) ])
LINESTRING (1 2, 3 4)
"""

from java.lang import Double
from com.vividsolutions.jts.io import WKTReader
from com.vividsolutions.jts import geom 

_wktreader = WKTReader()
_gf = geom.GeometryFactory()

Geometry = geom.Geometry
Point = geom.Point
LineString = geom.LineString
Polygon = geom.Polygon
MultiPoint = geom.MultiPoint
MultiLineString = geom.MultiLineString
MultiPolygon = geom.MultiPolygon

def point(*coord):
  """
  Constructs a ``Point`` geometry.

  *coord* may be specified in a variety of ways. The first is directly as x, y, z values: 

  >>> point(1,2)
  POINT (1 2)

  It can also be specified as a ``list``/``tuple`` of x, y, z:

  >>> point([1,2])
  POINT (1 2)

  Or a list of ``list``/``tuples``:

  >>> point([[1,2]])
  POINT (1 2)
  """

  if len(coord) == 1 and isinstance(coord[0], (tuple,list)):
     # list or tuple case
     coords = coord[0]
     if len(coords) == 1 and isinstance(coords[0], (tuple,list)):
        coords = coords[0]

     c = geom.Coordinate(coords[0],coords[1])
     if len(coords) > 2:
       c.z = coords[2]

  else:
     # x [,y,[z]] case
     c = geom.Coordinate(coord[0], coord[1])
     if len(coord) > 2:
       c.z = coord[2]
     
  return _gf.createPoint(c)

def linestring(*coords):
  """
  Constructs a ``LineString`` geometry.

  *coords* is specified as multiple lists/tuples or a list of lists/tuples:

  >>> linestring([1,2],[3,4])
  LINESTRING (1 2, 3 4)

  >>> linestring([ [1,2],[3,4] ])
  LINESTRING (1 2, 3 4)
  """

  if len(coords) == 1 and isinstance(coords[0], (tuple,list)):
    coords = coords[0]

  l = []
  for c in coords:
    l.append( geom.Coordinate(c[0],c[1]) )
    if len(c) > 2:
      l[-1].z = c[2]

  if l[0] == l[-1]:
    return _gf.createLinearRing(l)
  else:
    return _gf.createLineString(l)

def polygon(ring,holes=None):

  """
  Constructs a Polygon geometry.

  The first argument *ring* is a list of ``list``/``tuple`` defining the outer ring of the polygon:
  
  >>> polygon([ [1,2],[3,4],[5,6],[1,2] ])
  POLYGON ((1 2, 3 4, 5 6, 1 2))
  
  The second argument ``holes`` is optional and defines a list of lists of lists/tuples defining the inner rings or holes of the polygon:

  >>> exterior = [ [-10,-10],[10,-10],[10,10],[-10,10],[-10,-10] ]
  >>> holes = [ [ [-5,-5],[-1,-5],[-3,-2],[-5,-5] ], [ [5,5],[9,5],[7,7],[5,5] ] ]
  >>> polygon(exterior,holes)
  POLYGON ((-10 -10, 10 -10, 10 10, -10 10, -10 -10), (-5 -5, -1 -5, -3 -2, -5 -5), (5 5, 9 5, 7 7, 5 5))
  """

  outer = linestring(ring)
  inner = []
  if holes:
    for h in holes:
      inner.append(linestring(h))

  return _gf.createPolygon(outer,inner)

def multipoint(*points):
  """
  Constructs a MultiPoint goemetry.

  ``points`` may be specified as multiple Point arguments or a list of Point arguments:

  >>> multipoint(point(1,2), point(3,4))
  MULTIPOINT (1 2, 3 4)

  >>> multipoint([point(1,2), point(3,4)])
  MULTIPOINT (1 2, 3 4)
  """
  
  if len(points) == 1 and isinstance(points[0], (tuple,list)):
     points = points[0]

  return _gf.createMultiPoint(points)  

def multilinestring(*linestrings):
  """
  Constructs a MultiLineString geometry.

  ``linestrings`` may be specified as multiple LineString arguments or a list of LineString arguments: 

   >>> multilinestring(linestring([[1,2],[3,4]]), linestring([[5,6],[7,8]]))
   MULTILINESTRING ((1 2, 3 4), (5 6, 7 8))
  """

  if len(linestrings) == 1 and isinstance(linestrings[0], (tuple,list)):
     linestrings = linestrings[0]

  return _gf.createMultiLineString(linestrings)  

def multipolygon(*polygons):
  """
  Constructs a MultiPolygon geometry.

  ``polygons`` may be specified as multiple Polygon arguments or a list of Polygon arguments:

   >>> multipolygon(polygon([[1,2], [3,4], [5,6], [1,2]]), polygon([[7,8], [9,10], [11,12], [7,8]]))
   MULTIPOLYGON (((1 2, 3 4, 5 6, 1 2)), ((7 8, 9 10, 11 12, 7 8)))
  
  """

  if len(polygons) == 1 and isinstance(polygons[0], (tuple,list)):
     polygons = polygons[0]

  return _gf.createMultiPolygon(polygons)

def fromWKT(wkt):
  """
  Constructs a geometry by parsing Well Known Text.

  ``wkt`` is the Well Known Text string representing the geometry as described by http://en.wikipedia.org/wiki/Well-known_text.

  >>> fromWKT('POINT (1 2)')
  POINT (1 2)
  """
  return _wktreader.read(wkt)

def draw(g, size=(500,500)):
  """
  Draws a geometry onto a canvas.

  ``size`` is a tuple that specifies the dimensions of the canvas the geometry will drawn upon. 
  """
  from java import awt
  from java.awt.geom import AffineTransform
  from javax import swing
  from org.geotools.geometry.jts import LiteShape

  buf = 50.0
  e = g.getEnvelopeInternal()
  scx = size[0] / e.width
  scy = size[1] / e.height
       
  tx = -1*e.minX
  ty = -1*e.minY
       
  at = AffineTransform()
  
  # scale to size of canvas (inverting the y axis)
  at.scale(scx,-1*scy)
  
  # translate to the origin
  at.translate(tx,ty)

  # translate to account for invert
  at.translate(0,-1*size[1]/scy)

  # buffer
  at.translate(buf/scx,-1*buf/scy)
        
  class Panel(swing.JPanel):

    def __init__(self,shp):
      self.shp = shp
    
    def paintComponent(self, g):
      g.draw(shp)

  shp = LiteShape(g,at,False)
  panel = Panel(shp)
  s = tuple([int(size[x]+2*buf) for x in range(2)])
  panel.preferredSize = s
  frame = swing.JFrame()
  frame.contentPane = panel
  frame.size = s
  frame.visible = True

