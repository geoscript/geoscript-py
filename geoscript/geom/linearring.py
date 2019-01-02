from org.locationtech.jts.geom import Coordinate
from org.locationtech.jts.geom import LinearRing as _LinearRing
from linestring import LineString
from geoscript import core
import geom

class LinearRing(_LinearRing):
  """
  A LineString geometry in which the first and last coordinates are identical forming a closed ring. The arguments for contstructing a ``LinearRing`` are identical to those for constructing a :class:`LineString`. 

  >>> LinearRing([1,2], [3,4], [4,5], [1,2])
  LINEARRING (1 2, 3 4, 4 5, 1 2)
  """

  def __init__(self, *coords):
    if len(coords) == 1 and isinstance(coords[0], _LinearRing):
      _LinearRing.__init__(self, coords[0].coordinateSequence) 
    else:
      l = LineString(*coords)
      _LinearRing.__init__(self, l.coordinateSequence, geom._factory)

geom._enhance(LinearRing)
core.registerTypeMapping(_LinearRing, LinearRing)
