"""
The :mod:`geom` module provides geometry classes and utilities for the construction and manipulation of geometry objects.
"""

from java.lang import Double
from com.vividsolutions.jts.io import WKTReader
from com.vividsolutions.jts.geom import Coordinate, GeometryFactory
from com.vividsolutions.jts.geom import Geometry as _Geometry
from com.vividsolutions.jts.geom import Point as _Point
from com.vividsolutions.jts.geom import LineString as _LineString
from com.vividsolutions.jts.geom import LinearRing as _LinearRing
from com.vividsolutions.jts.geom import Polygon as _Polygon
from com.vividsolutions.jts.geom import MultiPoint as _MultiPoint
from com.vividsolutions.jts.geom import MultiLineString as _MultiLineString
from com.vividsolutions.jts.geom import MultiPolygon as _MultiPolygon
from org.geotools.geometry.jts import ReferencedEnvelope

_wktreader = WKTReader()
_gf = GeometryFactory()

Geometry = _Geometry

class Point(_Point):
  """
  A Point geometry.

  *coord* is specified as variable argument x,y,z values:

  >>> Point(1,2)
  POINT (1 2)
  """

  def __init__(self, *coord):

    if len(coord) == 1 and isinstance(coord[0], _Point):
      p = coord[0]
    else:
      c = Coordinate(coord[0], coord[1])
      if len(coord) > 2:
        c.z = coord[2]
      p = _gf.createPoint(c)
       
    _Point.__init__(self, p.coordinateSequence, _gf)

class LineString(_LineString):
  """
  A LineString geometry.

  *coords* is specified as multiple ``list``/``tuple`` arguments:

  >>> LineString([1,2], [3,4])
  LINESTRING (1 2, 3 4)
  """

  def __init__(self, *coords):
  
    if len(coords) == 1 and isinstance(coords[0], _LineString):
      ls = coords[0]
    else:
      l = []
      for c in coords:
        l.append( Coordinate(c[0],c[1]) )
        if len(c) > 2:
          l[-1].z = c[2]
      ls = _gf.createLineString(l)
  
    _LineString.__init__(self, ls.coordinateSequence, _gf)

class LinearRing(_LinearRing):
  """
  A LineString geometry in which the first and last coordinates are identical forming a closed ring. The arguments for contstructing a ``LinearRing`` are identical to those for constructing a ``LineString``. 

  >>> LinearRing([1,2], [3,4], [4,5], [1,2])
  LINEARRING (1 2, 3 4, 4 5, 1 2)
  """

  def __init__(self, *coords):
    if len(coords) == 1 and isinstance(coords[0], _LinearRing):
      _LinearRing.__init__(self, coords[0].coordinateSequence) 
    else:
      l = LineString(*coords)
      _LinearRing.__init__(self, l.coordinateSequence, _gf)

class Polygon(_Polygon):
  """
  A Polygon geometry.

  *rings* is a variable number of lists of ``list``/``tuple`` defining the rings of the polygon. The first argument is the outer ring and remaining arguments are holes. 

  >>> Polygon( [[1,2], [3,4], [5,6], [1,2]])
  POLYGON ((1 2, 3 4, 5 6, 1 2))
 
  >>> Polygon( [[-10,-10],[10,-10],[10,10],[-10,10],[-10,-10]], [[-5,-5],[-1,-5],[-3,-2],[-5,-5]], [[5,5],[9,5],[7,7],[5,5]] )
  POLYGON ((-10 -10, 10 -10, 10 10, -10 10, -10 -10), (-5 -5, -1 -5, -3 -2, -5 -5), (5 5, 9 5, 7 7, 5 5))

  *rings* may also be specified as a variable number of ``LinearRing`` objects:

  >>> Polygon( LinearRing([-10,-10],[10,-10],[10,10],[-10,10],[-10,-10]), LinearRing([-5,-5],[-1,-5],[-3,-2],[-5,-5]), LinearRing([5,5],[9,5],[7,7],[5,5]) )
  POLYGON ((-10 -10, 10 -10, 10 10, -10 10, -10 -10), (-5 -5, -1 -5, -3 -2, -5 -5), (5 5, 9 5, 7 7, 5 5))
  """

  def __init__(self, *rings):
    if isinstance(rings[0], _Polygon):
      p = rings[0]
      _Polygon.__init__(self, p.exteriorRing, [p.getInteriorRingN(i) for i in range(p.numInteriorRing)], _gf)
    else:
      lr = [r if isinstance(r,LinearRing) else LinearRing(*r) for r in rings ]
      _Polygon.__init__(self, lr[0], lr[1:], _gf)

class MultiPoint(_MultiPoint):
  """
  A MultiPoint goemetry.

  *points* is specified as a variable number of ``list``/``tuple`` arguments: 

  >>> MultiPoint([1,2], [3,4])
  MULTIPOINT (1 2, 3 4)

  *points* may also be specified as a variable number of ``Point`` arguments: 

  >>> MultiPoint(Point(1,2), Point(3,4))
  MULTIPOINT (1 2, 3 4)
   
  """

  def __init__(self, *points):
    
    if isinstance(points[0], _MultiPoint):
      mp = points[0]
      points = [mp.getGeometryN(i) for i in range(mp.numGeometries)]
    elif isinstance(points[0], (list,tuple)):
      points = [Point(*p) for p in points]
          
    _MultiPoint.__init__(self, points, _gf)

class MultiLineString(_MultiLineString):
  """
  A MultiLineString geometry.

  *linestrings* is specified as a variable number of lists of ``list``//``tuple`` arugments:

  >>> MultiLineString([[1,2],[3,4]], [[5,6],[7,8]])
  MULTILINESTRING ((1 2, 3 4), (5 6, 7 8))

  *linestrings* may also be specified as multiple ``LineString`` arguments:

  >>> MultiLineString(LineString([1,2],[3,4]), LineString([5,6],[7,8]))
  MULTILINESTRING ((1 2, 3 4), (5 6, 7 8))

  """

  def __init__(self, *linestrings):
  
    if isinstance(linestrings[0], _MultiLineString):
      mls = linestrings[0]  
      linestrings = [mls.getGeometryN(i) for i in range(mls.numGeometries)]
    elif isinstance(linestrings[0], (list,tuple)):
      linestrings = [LineString(*l) for l in linestrings]

    _MultiLineString.__init__(self, linestrings, _gf)

class MultiPolygon(_MultiPolygon):
  """
  A MultiPolygon geometry.

  *polygons* is specified as a variable number of multidimensional lists of ``list``/``tuple``:

  >>> MultiPolygon( [ [[1,2],[3,4],[5,6],[1,2]] ],  [ [[7,8], [9,10], [11,12], [7,8]] ] )
  MULTIPOLYGON (((1 2, 3 4, 5 6, 1 2)), ((7 8, 9 10, 11 12, 7 8)))

  *polygons* may also be specified as a variable number of ``Polygon`` arguments:

  >>> MultiPolygon(Polygon([[1,2], [3,4], [5,6], [1,2]]), Polygon([[7,8], [9,10], [11,12], [7,8]]))
  MULTIPOLYGON (((1 2, 3 4, 5 6, 1 2)), ((7 8, 9 10, 11 12, 7 8)))
  
  """

  def __init__(self, *polygons):
  
    if isinstance(polygons[0], _MultiPolygon):
       mp = polygons[0]
       polygons = [mp.getGeometryN(i) for i in range(mp.numGeometries)]
    elif isinstance(polygons[0], (list,tuple)):
       polygons = [Polygon(*p) for p in polygons]

    _MultiPolygon.__init__(self, polygons, _gf)

class Bounds(ReferencedEnvelope):

  def __init__(self, l, b, r, t, proj=None):
    self.proj = proj
    ReferencedEnvelope.__init__(self, l, r, b, t, self.proj._crs if self.proj else None)

  def getl(self):
    return self.minX()
  l = property(getl)

  def getb(self):
    return self.minY()
  b = property(getb)

  def getr(self):
    return self.maxX()
  r = property(getr)

  def gett(self):
    return self.maxY()
  t = property(gett)

  def __repr__(self):
    s = '(%s, %s, %s, %s' % (self.l, self.b, self.r, self.t)
    if self.proj:
      s = '%s, %s' % (s, self.proj.id)

    return '%s)' % s

def fromWKT(wkt):
  """
  Constructs a geometry from Well Known Text.

  *wkt* is the Well Known Text string representing the geometry as described by http://en.wikipedia.org/wiki/Well-known_text.

  >>> fromWKT('POINT (1 2)')
  POINT (1 2)
  """
  return _wktreader.read(wkt)

def draw(g, size=(500,500)):
  """
  Draws a geometry onto a canvas.

  *size* is a tuple that specifies the dimensions of the canvas the geometry will drawn upon. 
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
    
    def paintComponent(self, gc):
      gc.setColor(awt.Color.WHITE)
      gc.fill(shp)

      gc.setRenderingHint(awt.RenderingHints.KEY_ANTIALIASING, awt.RenderingHints.VALUE_ANTIALIAS_ON)
      gc.setStroke(awt.BasicStroke(2))
      gc.setColor(awt.Color.BLACK)
      gc.draw(shp)


  shp = LiteShape(g,at,False)
  panel = Panel(shp)
  s = tuple([int(size[x]+2*buf) for x in range(2)])
  panel.preferredSize = s
  frame = swing.JFrame()
  frame.contentPane = panel
  frame.size = s
  frame.visible = True

import core
core.register(Point)
core.register(LineString)
core.register(Polygon)
core.register(MultiPoint)
core.register(MultiLineString)
core.register(MultiPolygon)
core.register(Bounds)
