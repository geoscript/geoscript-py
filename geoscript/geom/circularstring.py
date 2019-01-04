from org.locationtech.jts.geom import Coordinate
from org.geotools.geometry.jts import CircularString as _CircularString
from org.geotools.geometry.jts import CurvedGeometryFactory
from java.lang import Double
from geoscript import core
import geom

class CircularString(_CircularString):
    """
    A CircularString geometry.

    *coords* is a variable list of ``list``/``tuple`` arguments.

    >>> CircularString([1,1], [5,5], [2,2])
    CIRCULARSTRING (1.0 1.0, 5.0 5.0, 2.0 2.0)
    """

    def __init__(self, *coords):
        tolerance = Double.MAX_VALUE    
        if len(coords) == 1 and isinstance(coords[0], _CircularString):
          cs = coords[0].coordinateSequence
        else:
          l = []
          for c in coords:
            l.append( Coordinate(c[0],c[1]) )
            if len(c) > 2:
              l[-1].z = c[2]
          cs = geom._factory.coordinateSequenceFactory.create(l)
        
        doubles = []
        for c in cs.toCoordinateArray():
            doubles.append(c.x)
            doubles.append(c.y)

        cgf = CurvedGeometryFactory(tolerance)
        _CircularString.__init__(self, doubles, cgf, tolerance)

geom._enhance(CircularString)
core.registerTypeMapping(_CircularString, CircularString)
