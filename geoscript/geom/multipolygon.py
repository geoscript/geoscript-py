from org.locationtech.jts.geom import MultiPolygon as _MultiPolygon
from geoscript import core
from polygon import Polygon
import geom

class MultiPolygon(_MultiPolygon):
  """
  A MultiPolygon geometry.

  *polygons* is a variable number of multidimensional lists of ``list``/``tuple``.

  >>> MultiPolygon( [ [[1,2],[3,4],[5,6],[1,2]] ],  [ [[7,8], [9,10], [11,12], [7,8]] ] )
  MULTIPOLYGON (((1 2, 3 4, 5 6, 1 2)), ((7 8, 9 10, 11 12, 7 8)))

  *polygons* may also be specified as a variable number of :class:`Polygon` arguments.

  >>> MultiPolygon(Polygon([[1,2], [3,4], [5,6], [1,2]]), Polygon([[7,8], [9,10], [11,12], [7,8]]))
  MULTIPOLYGON (((1 2, 3 4, 5 6, 1 2)), ((7 8, 9 10, 11 12, 7 8)))
  
  """

  def __init__(self, *polygons):
  
    if isinstance(polygons[0], _MultiPolygon):
       mp = polygons[0]
       polygons = [mp.getGeometryN(i) for i in range(mp.numGeometries)]
    elif isinstance(polygons[0], (list,tuple)):
       polygons = [Polygon(*p) for p in polygons]

    _MultiPolygon.__init__(self, polygons, geom._factory)

geom._enhance(MultiPolygon)
core.registerTypeMapping(_MultiPolygon, MultiPolygon)
