.. _gettingstarted.geom:

Geometries
==========

The :mod:`geoscript.geom` module provides classes for representing two dimensional spatial objects, or geometries. Geometry objects are created by specifying sets of coordinates::

  >>> from geoscrpt import geom 

  >>> point = geom.Point(10, 10)
  >>> point
  POINT (10 10)

  >>> line = geom.LineString([10, 10], [20, 20], [30, 40])
  >>> line
  LINESTRING (10 10, 20 20, 30 40)

The api reference details how to construct the various Geometry types:

  * :class:`geoscript.geom.Point`
  * :class:`geoscript.geom.LineString`
  * :class:`geoscript.geom.Polygon`
  * :class:`geoscript.geom.MultiPoint`
  * :class:`geoscript.geom.MultiLineString`
  * :class:`geoscript.geom.MultiPolygon`
  
Geometries can also be created from `well known text <http://en.wikipedia.org/wiki/Well-known_text>`_ representation::

  >>> from geoscript import geom

  >>> poly = geom.fromWKT('POLYGON ((10 10, 10 20, 20 20, 20 15, 10 10))')
  >>> poly
  POLYGON ((10 10, 10 20, 20 20, 20 15, 10 10))

Geometry objects provide a number of methods for calculating properties of a geometry. For example methods for obtaining area and length::

  >>> from geoscript import geom

  >>> poly = geom.fromWKT('POLYGON ((10 10, 10 20, 20 20, 20 15, 10 10))')
  >>> poly.area
  75.0 
  >>> poly.length
  36.180339887498945

There are also methods for calculating properties which are themselves geometries such as buffer and centroid::

  >>> from geoscript import geom

  >>> line = geom.LineString([10, 10], [20, 20], [30, 40])
  >>> poly = line.buffer(10)
  >>> poly.area
  1041.9912814842407

  >>> line.centroid
  POINT (21.12574113277207 24.188611699158105)

The Geometry class also contains operations and predicates for determining spatial relationships such as intersection and containment::

  >>> from geoscript import geom

  >>> poly = geom.Polygon([[10, 10], [10, 20], [20, 20], [20, 15], [10, 10]])
  >>> line = geom.LineString([10, 10], [20, 20], [30, 40])
  >>> poly.intersects(line)
  True
  >>> poly.intersection(line)
  LINESTRING (10 10, 20 20) 

The geoscript geometry module is based on the `JTS <http://tsusiatsoftware.net/jts/main.html>`_ library. Classes in the :mod:`geoscript.geom` module are extensions of their counterparts from JTS which means any JTS geometry methods can be called on a geoscript geometry instance. See the JTS `javadocs <http://tsusiatsoftware.net/jts/javadoc/com/vividsolutions/jts/geom/Geometry.html>`_ for more information.
