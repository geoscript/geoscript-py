from org.locationtech.jts.geom import Coordinate
from org.locationtech.jts.geom import LineString as _LineString
from org.locationtech.jts.linearref import LengthIndexedLine
from geoscript import core
from geoscript.geom import Point
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

  def interpolatePoint(self, position):
      """
      Interpolate a :class:`Point <geoscript.geom.Point>` on the :class:`LineString <geoscript.geom.LineString>` at the given position from 0 to 1.
      
      *position* is number between 0 and 1

      """
      indexedLine = LengthIndexedLine(self) 
      length = self.getLength()
      coordinate = indexedLine.extractPoint(position * length)
      return Point(coordinate.x, coordinate.y)

  def locatePoint(self, *coord):
      """
      Locate the position of the :class:`point <geoscript.geom.Point>` along this :class:`LineString <geoscript.geom.LineString>`. The position returned is a number between 0 and 1.

      *coord* A :class:`Point <geoscript.geom.Point>` or a variable list of x,y,z arguments.
      
      """
      point = coord[0] if isinstance(coord[0], Point) else Point(*coord)
      indexedLine = LengthIndexedLine(self)
      position = indexedLine.indexOf(point.coordinate)
      percentAlong = position / self.getLength()
      return percentAlong
  
  def placePoint(self, *coord):
      """
      Place or snap the :class:`point <geoscript.geom.Point>` to the `LineString <geoscript.geom.LineString>`. This method returns a new placed `Point <geoscript.geom.Point>`.

      *coord* A :class:`Point <geoscript.geom.Point>` or a variable list of x,y,z arguments.

      """
      point = coord[0] if isinstance(coord[0], Point) else Point(*coord)
      indexedLine = LengthIndexedLine(self)
      position = indexedLine.indexOf(point.coordinate)
      coord = indexedLine.extractPoint(position)
      return Point(coord.x, coord.y)
  
  def subLine(self, start, end):
      """
      Extract a sub :class:`LineString <geoscript.geom.LineString>` using a start and end position.  Both positions are numbers between 0 and 1.  A new :class:`LineString <geoscript.geom.LineString>` is returned.

      *start* The start position between 0 and 1
      
      *end* The end position between 0 and 1

      """
      indexedLine = LengthIndexedLine(self)
      length = self.getLength()
      return LineString(indexedLine.extractLine(start * length, end * length))

geom._enhance(LineString)
core.registerTypeMapping(_LineString, LineString)
