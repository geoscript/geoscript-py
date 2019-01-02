from org.locationtech.jts.geom import MultiPoint as _MultiPoint
from geoscript import core
from point import Point
import geom

class MultiPoint(_MultiPoint):
  """
  A MultiPoint goemetry.

  *points* is a variable number of ``list``/``tuple`` arguments. 

  >>> MultiPoint([1,2], [3,4])
  MULTIPOINT ((1 2), (3 4))

  *points* may also be specified as a variable number of :class:`Point` arguments. 

  >>> MultiPoint(Point(1,2), Point(3,4))
  MULTIPOINT ((1 2), (3 4))
   
  """

  def __init__(self, *points):
    
    if isinstance(points[0], _MultiPoint):
      mp = points[0]
      points = [mp.getGeometryN(i) for i in range(mp.numGeometries)]
    elif isinstance(points[0], (list,tuple)):
      points = [Point(*p) for p in points]
          
    _MultiPoint.__init__(self, points, geom._factory)

geom._enhance(MultiPoint)
core.registerTypeMapping(_MultiPoint, MultiPoint)
