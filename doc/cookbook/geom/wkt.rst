.. _cookbook.geom.wkt:

Reading Geometries from Well Known Text
=======================================

The :meth:`geom.fromWKT() <geoscript.geom.fromWKT>` function is used to parse well known text strings::

  >>> from geoscript import geom
  >>> pt = geom.fromWKT('POINT(6 10)')
  >>> pt
  POINT (6 10)
  >>> mpoly = from.fromWKT('MULTIPOLYGON(((1 1,5 1,5 5,1 5,1 1),(2 2, 3 2, 3 3, 2 3,2 2)),((3 3,6 2,6 4,3 3)))')
  >>> mpoly
  MULTIPOLYGON (((1 1,5 1,5 5,1 5,1 1),(2 2, 3 2, 3 3, 2 3,2 2)),((3 3,6 2,6 4,3 3)))
  
Writing Geometries to Well Known Text
=====================================

The string representation of a geometry object is its well known text representation::

  >>> from geoscript import geom
  >>> pt = geom.fromWKT('POINT(6 10)')
  >>> wkt = str(pt)
  >>> wkt
  'POINT (6 10)'
