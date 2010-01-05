from point import Point
from linestring import LineString
from linearring import LinearRing
from polygon import Polygon
from multipoint import MultiPoint
from multilinestring import MultiLineString
from multipolygon import MultiPolygon
from bounds import Bounds
from geom import Geometry
from geom import fromWKT

from geoscript import core
core.register(Point)
core.register(LineString)
core.register(Polygon)
core.register(MultiPoint)
core.register(MultiLineString)
core.register(MultiPolygon)
core.register(Bounds)
