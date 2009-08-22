"""
geom module -- Provides utilities for the construction and manipulation of 
geometry objects.

Geometry constructors take lists of lists defining the coordinates which make
up the geometry.

>>> line = LineString([[1,2],[3,4]])
>>> str(line)
'LINESTRING (1 2, 3 4)'

Constructors also take lists of tuples.

>>> line = LineString([(1,2),(3,4)])
>>> str(line)
'LINESTRING (1 2, 3 4)'
"""

from java.lang import Double
from com.vividsolutions.jts.geom import Coordinate, GeometryFactory
from com.vividsolutions.jts.io import WKTReader

_gf = GeometryFactory()
_wktreader = WKTReader()

def Point(x,y=Double.NaN,z=Double.NaN):
  """
  Constructs a point geometry.

  This function accepts a variety of inputs. The first being direct x,y,z
  arguments:

  >>> point = Point(1,2)
  >>> str(point)
  'POINT (1 2)'

  It also accepts a list or tuple of x,y,z:

  >>> point = Point([1,2])
  >>> str(point)
  'POINT (1 2)'

  Or a list of lists or tuples:

  >>> point = Point([[1,2]])
  >>> str(point)
  'POINT (1 2)'
  """

  if type(x) in (tuple,list) and Double.isNaN(y):
    coords = x

    if len(coords) == 1 and type(coords[0]) in (tuple,list):
      coords = coords[0]

    c = Coordinate(coords[0],coords[1])
    if len(coords) > 2:
      c.z = coords[2]

  else:
     c = Coordinate(x,y)
     c.z = z

  return _gf.createPoint(c)

def LineString(coords):
  """
  Constructs a linestring geometry.

  This function takes a list of lists or tuples:

  >>> line = LineString([ [1,2],[3,4] ])
  >>> str(line)
  'LINESTRING (1 2, 3 4)'
  """

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

  """
  Constructs a polygon geometry.

  The first argument of this function is a list of lists defining the outer
  ring of the polygon:
  
  >>> poly = Polygon([ [1,2],[3,4],[5,6],[1,2] ])
  >>> str(poly)
  'POLYGON ((1 2, 3 4, 5 6, 1 2))'
  
  The second argument is optional and defines a list of lists of lists defining
  the inner rings or holes of the polygon 
  >>> exterior = [ [-10,-10],[10,-10],[10,10],[-10,10],[-10,-10] ]
  >>> holes = [ [ [-5,-5],[-1,-5],[-3,-2],[-5,-5] ], [ [5,5],[9,5],[7,7],[5,5] ] ]
  >>> poly = Polygon(exterior,holes)
  >>> str(poly)
  'POLYGON ((-10 -10, 10 -10, 10 10, -10 10, -10 -10), (-5 -5, -1 -5, -3 -2, -5 -5), (5 5, 9 5, 7 7, 5 5))'
  """

  outer = LineString(ring)
  inner = []
  if holes:
    for h in holes:
      inner.append(LineString(h))

  return _gf.createPolygon(outer,inner)

def Geometry(wkt):
  """
  Constructs a geometry from well known text.

  >>> g = Geometry('POINT (1 2)')
  >>> str(g)
  'POINT (1 2)'
  """
  return _wktreader.read(wkt)

def draw(g,size=(500,500),buf=50.0):
  """
  Draws the geometry onto a frame.
  """
  from java import awt
  from java.awt.geom import AffineTransform
  from javax import swing
  from org.geotools.geometry.jts import LiteShape

  e = g.getEnvelopeInternal()
  scx = size[0] / e.getWidth()
  scy = size[1] / e.getHeight()
       
  tx = -1*e.getMinX() + buf/scx
  ty = -1*e.getMinY() + buf/scy
       
  at = AffineTransform()
  at.scale(scx,scy)
  at.translate(tx,ty)
        
  class Panel(swing.JPanel):

    def __init__(self,shp):
      self.shp = shp
    
    def paintComponent(self, g):
      g.draw(shp)

  shp = LiteShape(g,at,False)
  panel = Panel(shp)
  s = (int(size[0]+2*buf),int(size[1]+2*buf))
  panel.preferredSize = s
  frame = swing.JFrame()
  frame.contentPane = panel
  frame.size = s
  frame.visible = True

