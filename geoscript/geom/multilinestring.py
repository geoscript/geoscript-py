from org.locationtech.jts.geom import MultiLineString as _MultiLineString
from linestring import LineString
from geoscript import core
import geom

class MultiLineString(_MultiLineString):
  """
  A MultiLineString geometry.

  *linestrings* is a variable number of lists of ``list``/``tuple`` arugments.

  >>> MultiLineString([[1,2],[3,4]], [[5,6],[7,8]])
  MULTILINESTRING ((1 2, 3 4), (5 6, 7 8))

  *linestrings* may also be specified as multiple :class:`LineString` arguments.

  >>> MultiLineString(LineString([1,2],[3,4]), LineString([5,6],[7,8]))
  MULTILINESTRING ((1 2, 3 4), (5 6, 7 8))

  """

  def __init__(self, *linestrings):
  
    if isinstance(linestrings[0], _MultiLineString):
      mls = linestrings[0]  
      linestrings = [mls.getGeometryN(i) for i in range(mls.numGeometries)]
    elif isinstance(linestrings[0], (list,tuple)):
      linestrings = [LineString(*l) for l in linestrings]

    _MultiLineString.__init__(self, linestrings, geom._factory)

geom._enhance(MultiLineString)
core.registerTypeMapping(_MultiLineString, MultiLineString)
