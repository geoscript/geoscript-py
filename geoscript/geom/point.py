from org.locationtech.jts.geom import Coordinate
from org.locationtech.jts.geom import Point as _Point
from geoscript import core
import geom

class Point(_Point):
  """
  A Point geometry.

  *coord* is a variable list of x, y, z arguments.

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
      p = geom._factory.createPoint(c)

    _Point.__init__(self, p.coordinateSequence, geom._factory)

geom._enhance(Point)
core.registerTypeMapping(_Point, Point)
