"""
The :mod:`geom` module provides geometry classes and utilities for the construction and manipulation of geometry objects.
"""

from java.awt.geom import AffineTransform
from com.vividsolutions.jts.geom import GeometryFactory
from com.vividsolutions.jts.geom import Geometry as _Geometry
from com.vividsolutions.jts.geom.prep import PreparedGeometryFactory
from com.vividsolutions.jts.simplify import DouglasPeuckerSimplifier as DP
from org.geotools.geometry.jts import JTS
from org.geotools.referencing.operation.transform import AffineTransform2D

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
  

def simplify(g, tol):
  """
  Simplifies a geometry object using the Douglas-Peucker simplfication method.
  
  *g* is the :class:`Geometry <geoscript.geom.Geometry>` to simplify. 

  *tol* is the distance tolernance such that all veriticies in the resulting
  simplified geometry will be within this distance from the original geometry.
  """
  return DP.simplify(g, tol)
   
def transform(g, dx=0, dy=0, sx=1, sy=1, shx=0, shy=0, r=0): 
  """
  Tranforms a geometry with an affine transformation.

  *dx*, *dy* specify the x,y translation.

  *sx*, *sy* specify the x,y scale factors.

  *shx, shy* specify the x,y shear factors.

  *r* specifies the rotation angle in radians
  """
  tx = AffineTransform(sx, shy, shx, sy, dx, dy)
  tx.rotate(r)
  return JTS.transform(g, AffineTransform2D(tx))
