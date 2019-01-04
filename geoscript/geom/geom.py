"""
The :mod:`geom` module provides geometry classes and utilities for the construction and manipulation of geometry objects.
"""

from java.awt.geom import AffineTransform
from org.locationtech.jts.geom import GeometryFactory, CoordinateFilter
from org.locationtech.jts.geom import Geometry as _Geometry
from org.locationtech.jts.geom.prep import PreparedGeometryFactory
from org.locationtech.jts.simplify import DouglasPeuckerSimplifier as DP
from org.locationtech.jts.simplify import TopologyPreservingSimplifier as TP
from org.locationtech.jts.densify import Densifier
from org.locationtech.jts.triangulate import DelaunayTriangulationBuilder
from org.locationtech.jts.triangulate import VoronoiDiagramBuilder
from org.locationtech.jts.operation.buffer import BufferOp, BufferParameters
from org.geotools.geometry.jts import JTS
from org.geotools.referencing.operation.transform import AffineTransform2D
from geoscript.geom.bounds import Bounds

_factory = GeometryFactory()
_prepfactory = PreparedGeometryFactory()

Geometry = _Geometry
"""
Base class for all geometry classes.
"""
  
def prepare(g):
  """
  Constructs a prepared geometry. Prepared geometries make repeated spatial 
  operations (such as intersection) more efficient.

  *g* is the :class:`Geometry <geoscript.geom.Geometry>` to prepare.

  >>> from geoscript.geom import readWKT
  >>> prep = prepare(readWKT('POLYGON ((0 0, 10 0, 10 10, 0 10, 0 0))'))
  >>> prep.intersects(readWKT('POLYGON ((4 4, 6 4, 6 6, 4 6, 4 4))'))
  True
  """
  return _prepfactory.create(g)
  
def simplify(g, tol, topology=False):
  """
  Simplifies a geometry object using the Douglas-Peucker simplfication method.
  
  *g* is the :class:`Geometry <geoscript.geom.Geometry>` to simplify. 

  *tol* is the distance tolernance such that all veriticies in the resulting
  simplified geometry will be within this distance from the original geometry.

  *topology* is a flag controlling whether topology should be preserved. The 
  default is 
  """
  simplifier = TP if topology is True else DP
  return simplifier.simplify(g, tol)

def densify(g, tol):
  """
  Densifies a geometry object adding verticies along the line segments of the 
  geometry.

  *g* is the :class:`Geometry <geoscript.geom.Geometry>` to densifiy. 

  *tol* is the distance tolerance such that all ine segments in the densified 
  geometry will be no longer than the distance tolereance
  """
  return Densifier.densify(g, tol)

def transform(g, dx=0, dy=0, sx=1, sy=1, shx=0, shy=0, r=0): 
  """
  Tranforms a geometry with an affine transformation.

  *g* is the :class:`Geometry <geoscript.geom.Geometry>` to transform. 

  *dx*, *dy* specify the x,y translation.

  *sx*, *sy* specify the x,y scale factors.

  *shx, shy* specify the x,y shear factors.

  *r* specifies the rotation angle in radians.
  """
  tx = AffineTransform(sx, shy, shx, sy, dx, dy)
  tx.rotate(r)
  return JTS.transform(g, AffineTransform2D(tx))

def delaunay(obj, tol=0.0):
  """
  Computes a Delaunay Triangulation.

  *obj* is a :class:`Geometry <geoscript.geom.Geometry>` or a ``list`` of
  geometries. 

  *tol* is the snapping tolerance used to improved the robustness of the 
  triangulation computation.

  This function returns a tuple containing two geometry collections. The first
  contains the resulting triangles, the second contains the edges of the 
  resulting triangles.
  """
  dtb = DelaunayTriangulationBuilder()
  dtb.setTolerance(tol)
  dtb.setSites(_sites(obj))
  return (dtb.getTriangles(_factory), dtb.getEdges(_factory))

def voronoi(obj, tol=0.0, bounds=None):
  """
  Computes a Voronoi diagram.

  *obj* is a :class:`Geometry <geoscript.geom.Geometry>` or a ``list`` of
  geometries. 

  *tol* is the snapping tolerance used to improved the robustness of the 

  *bounds* is an optional :class:`Bounds <geoscript.geom.Bounds>` used to 
  clip the resulting diagram. 

  This function returns a geometry collection containing the polygons composing
  the diagram.
  """
  vdb = VoronoiDiagramBuilder()
  vdb.setTolerance(tol)
  vdb.setSites(_sites(obj))
  if bounds:
    vdb.setClipEnvelope(bounds)
  return vdb.getDiagram(_factory)
  
def _sites(obj):
  if isinstance(obj, Geometry):
    return obj

  if isinstance(obj, list):
    # collapse to one list of coordinates
    extract = DelaunayTriangulationBuilder.extractUniqueCoordinates
    def f(x,y):
      x.extend(extract(y))
      return x
    return reduce(f, obj, [])

  return obj

def buffer(g, distance, singleSided=False):
  """
  Computes the buffer (optionally single sides) of a geometry.

  *g* is the :class:`Geometry <geoscript.geom.Geometry>` to buffer.

  *distance* is the buffer distance.
  
  *singleSided* specifies whether to compute a single sided buffer.
  """
  bp = BufferParameters()
  bp.setSingleSided(singleSided)
  
  return BufferOp.bufferOp(g, distance, bp) 

def _bounds(g):
  return Bounds(env=g.getEnvelopeInternal())

class RoundFilter(CoordinateFilter):
   def __init__(self, n):
     self.n = n

   def filter(self, c):
     c.x = round(c.x, self.n)
     c.y = round(c.y, self.n)
     c.z = round(c.z, self.n)

def _round(g, n=0):
  g.apply(RoundFilter(n))
  return g

def _enhance(cls):
  cls.bounds = _bounds
  cls.round = _round

