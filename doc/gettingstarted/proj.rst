.. _gettingstarted.proj:

Projections
===========

The :mod:`geoscript.proj` module provides support for representing spatial reference systems and transforming data between spatial projections.

The :class:`Projection <geoscript.proj.Projection>` class is used to represennt spatial reference system. A common way to represent a spatial reference system is with an `epsg <http://en.wikipedia.org/wiki/European_Petroleum_Survey_Group>`_ code::

  >>> from geoscript.proj import Projection
  >>> prj = Projection('epsg:4326')
  prj
  GEOGCS["WGS 84", 
    DATUM["World Geodetic System 1984", 
      SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]], 
      AUTHORITY["EPSG","6326"]], 
    PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]], 
    UNIT["degree", 0.017453292519943295], 
    AXIS["Geodetic longitude", EAST], 
    AXIS["Geodetic latitude", NORTH], 
    AUTHORITY["EPSG","4326"]]

The :attr:`Projection.id <geoscript.proj.Projection.id>` attribute of a Projection returns its epsg code::

  >>> from geoscript.proj import Projection
  >>> prj = Projection('epsg:4326')
  >>> prj.id
  'EPSG:4326'

Often a spatial reference system is defined by `well known text <http://en.wikipedia.org/wiki/Well-known_text#Spatial_reference_systems>`_ rather than an epsg code. A Projection object can be created directly from well known text::

  >>> from geoscript.proj import Projection
  >>> wkt = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
  >>> prj = Projection(wkt)
  >>> prj
  GEOGCS["GCS_WGS_1984", 
    DATUM["D_WGS_1984", 
      SPHEROID["WGS_1984", 6378137.0, 298.257223563]], 
    PRIMEM["Greenwich", 0.0], 
    UNIT["degree", 0.017453292519943295], 
    AXIS["Longitude", EAST], 
    AXIS["Latitude", NORTH]]

The :attr:`Projection.wkt <geoscript.proj.Projection.wkt>` attribute returns the well known text of a Projection:: 

   >>> from geoscript.proj import Projection
   >>> prj = Projection('epsg:26912')
   >>> prj.wkt
   'PROJCS["NAD83 / UTM zone 12N", \n  GEOGCS["NAD83", \n    DATUM["North American Datum 1983", \n      SPHEROID["GRS 1980", 6378137.0, 298.257222101, AUTHORITY["EPSG","7019"]], \n      TOWGS84[1.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0], \n      AUTHORITY["EPSG","6269"]], \n    PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]], \n    UNIT["degree", 0.017453292519943295], \n    AXIS["Geodetic longitude", EAST], \n    AXIS["Geodetic latitude", NORTH], \n    AUTHORITY["EPSG","4269"]], \n  PROJECTION["Transverse Mercator", AUTHORITY["EPSG","9807"]], \n  PARAMETER["central_meridian", -111.0], \n  PARAMETER["latitude_of_origin", 0.0], \n  PARAMETER["scale_factor", 0.9996], \n  PARAMETER["false_easting", 500000.0], \n  PARAMETER["false_northing", 0.0], \n  UNIT["m", 1.0], \n  AXIS["Easting", EAST], \n  AXIS["Northing", NORTH], \n  AUTHORITY["EPSG","26912"]]'

The :meth:`Projection.transform() <geoscript.proj.Projection.transform>` is used to transform data between spatial reference systems::

   >>> from geoscript.proj import Projection
   >>> src = Projection('epsg:4326')
   >>> src.transform((-111, 45.7), 'epsg:26912')
   (499999.42501775385, 5060716.092032814)

   >>> from geoscript.geom import Point
   >>> src.transform(Point(-111, 45.7), 'epsg:26912')
   POINT (499999.42501775385 5060716.092032814)

