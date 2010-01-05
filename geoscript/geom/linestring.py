from com.vividsolutions.jts.geom import Coordinate
from com.vividsolutions.jts.geom import LineString as _LineString
import geom

class LineString(_LineString):
  """
  A LineString geometry.

  *coords* is a variable list of ``list``/``tuple`` arguments.

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
      ls = geom._factory.createLineString(l)
  
    _LineString.__init__(self, ls.coordinateSequence, geom._factory)
