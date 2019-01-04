from org.locationtech.jts.geom import Coordinate
from org.geotools.geometry.jts import CompoundRing as _CompoundRing
from org.geotools.geometry.jts import CurvedGeometryFactory
from linestring import LineString
from circularstring import CircularString
from java.lang import Double
from geoscript import core
import geom

class CompoundRing(_CompoundRing):
    """
    A CompoundRing geometry.

    *linestrings* is a variable list of ``LineStrings`` or ``CircularStrings`` arguments.

    >>> CompoundRing(CircularString([10.0, 10.0], [0.0, 20.0], [-10.0, 10.0]),LineString([-10.0, 10.0], [-10.0, 0.0], [10.0, 0.0], [10.0, 10.0]))
    COMPOUNDCURVE (CIRCULARSTRING (10.0 10.0, 0.0 20.0, -10.0 10.0), (-10.0 10.0, -10.0 0.0, 10.0 0.0, 10.0 10.0))
    """

    def __init__(self, *linestrings):
        tolerance = Double.MAX_VALUE    
        if len(linestrings) == 1 and isinstance(linestrings[0], _CompoundRing):
            cc = linestrings[0]
            linestrings = cc.components

        cgf = CurvedGeometryFactory(tolerance)
        _CompoundRing.__init__(self, linestrings, cgf, tolerance)

geom._enhance(CompoundRing)
core.registerTypeMapping(_CompoundRing, CompoundRing)


