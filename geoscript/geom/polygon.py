from org.locationtech.jts.geom import Polygon as _Polygon
from geoscript import core
from linearring import LinearRing
import geom

class Polygon(_Polygon):
  """
  A Polygon geometry.

  *rings* is a variable number of lists of ``list``/``tuple`` arguments defining the rings of the polygon. The first argument is the outer ring and remaining arguments are holes. 

  >>> Polygon( [[1,2], [3,4], [5,6], [1,2]])
  POLYGON ((1 2, 3 4, 5 6, 1 2))
 
  >>> Polygon( [[-10,-10],[10,-10],[10,10],[-10,10],[-10,-10]], [[-5,-5],[-1,-5],[-3,-2],[-5,-5]], [[5,5],[9,5],[7,7],[5,5]] )
  POLYGON ((-10 -10, 10 -10, 10 10, -10 10, -10 -10), (-5 -5, -1 -5, -3 -2, -5 -5), (5 5, 9 5, 7 7, 5 5))

  *rings* may also be specified as a variable number of :class:`LinearRing` objects.

  >>> Polygon( LinearRing([-10,-10],[10,-10],[10,10],[-10,10],[-10,-10]), LinearRing([-5,-5],[-1,-5],[-3,-2],[-5,-5]), LinearRing([5,5],[9,5],[7,7],[5,5]) )
  POLYGON ((-10 -10, 10 -10, 10 10, -10 10, -10 -10), (-5 -5, -1 -5, -3 -2, -5 -5), (5 5, 9 5, 7 7, 5 5))
  """

  def __init__(self, *rings):
    if isinstance(rings[0], _Polygon):
      p = rings[0]
      _Polygon.__init__(self, p.exteriorRing, [p.getInteriorRingN(i) for i in range(p.numInteriorRing)], geom._factory)
    else:
      lr = [r if isinstance(r,LinearRing) else LinearRing(*r) for r in rings ]
      _Polygon.__init__(self, lr[0], lr[1:], geom._factory)

geom._enhance(Polygon)
core.registerTypeMapping(_Polygon, Polygon)
