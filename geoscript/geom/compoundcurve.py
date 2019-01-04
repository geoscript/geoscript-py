from org.locationtech.jts.geom import Coordinate
from org.geotools.geometry.jts import CompoundCurve as _CompoundCurve
from org.geotools.geometry.jts import CurvedGeometryFactory
from linestring import LineString
from circularstring import CircularString
from java.lang import Double
from geoscript import core
import geom

class CompoundCurve(_CompoundCurve):
    """
    A CompoundCurve geometry.

    *linestrings* is a variable list of ``LineStrings`` or ``CircularStrings`` arguments.

    >>> CompoundCurve(CircularString([10.0, 10.0], [0.0, 20.0], [-10.0, 10.0]), LineString([-10.0, 10.0], [-10.0, 0.0], [10.0, 0.0], [5.0, 5.0]))
    COMPOUNDCURVE (CIRCULARSTRING (10.0 10.0, 0.0 20.0, -10.0 10.0), (-10.0 10.0, -10.0 0.0, 10.0 0.0, 5.0 5.0))
    """

    def __init__(self, *linestrings):
        tolerance = Double.MAX_VALUE    
        if len(linestrings) == 1 and isinstance(linestrings[0], _CompoundCurve):
            cc = linestrings[0]
            linestrings = cc.components

        cgf = CurvedGeometryFactory(tolerance)
        _CompoundCurve.__init__(self, linestrings, cgf, tolerance)

geom._enhance(CompoundCurve)
core.registerTypeMapping(_CompoundCurve, CompoundCurve)

