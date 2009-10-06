"""
The :mod:`proj` module provides support for coordinate reference system transformation and geometry reprojection.
"""
from org.geotools.geometry.jts import GeometryCoordinateSequenceTransformer as GeometryTX
from org.geotools.referencing import CRS as _CRS
from org.opengis.referencing.crs import CoordinateReferenceSystem

CRS = CoordinateReferenceSystem
"""
Class defining a Coordinate Reference System.
"""

def _toCRS(o):
  """
  Transforms an object to a crs if possible. This method can take a crs object (no action required), or a string.
  """

  if isinstance(o,CRS):   
     return o
  elif isinstance(o,str):
     return _CRS.decode(o)

def transform(g, src, dst):
  """
  Reprojects a geometry from a source projection to a target projection. 

  *g* is the ``Geometry`` object to be tranformed. *src* and *dst* define the source and target reference systems and are specified as epsg codes strings:

  >>> import geom 
  >>> p1 = geom.point(-125, 50)
  >>> p2 = transform(p1, 'epsg:4326', 'epsg:3005')
  >>> str(p2)
  'POINT (1071693.1296328472 554289.941892416)'

  *g* may also be specified as a *list* or *tuple* of coordinates:

  >>> p1 = [-125, 50]
  >>> p2 = transform(p1, 'epsg:4326', 'epsg:3005')
  >>> str(p2)
  '[1071693.1296328472, 554289.941892416]'

  *src* and *dst* may also be specified as ``CRS`` objects: 

  >>> wkt = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
  >>> src = crs(wkt)
  >>> dst = crs('epsg:3005')
  >>> p = transform((-125, 50), src, dst)
  >>> str(p)
  '(1071693.1296956574, 554289.937440172)'
  """

  fromcrs = _toCRS(src)
  tocrs = _toCRS(dst)
  tx = _CRS.findMathTransform(fromcrs,tocrs)

  if isinstance(g, (list,tuple)):
    import jarray
    transformed = jarray.zeros(len(g),'d')
    tx.transform(g,0,transformed,0,1)
    l = [transformed[x] for x in range(len(g))]
    return l if isinstance(g, list) else tuple(l)
  else:
    #geometry
    gt = GeometryTX()
    gt.mathTransform = tx

    return gt.transform(g)

def crs(s):
  """
  Parses a string into a ``CRS``.

  *s* may be specified as a spatial reference system identifier:

  >>> cs = crs('epsg:4326')
  >>> str(cs.name)
  'EPSG:WGS 84'

  *s* may be also be specified as a Well Known Text string:

  >>> cs = crs('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]') 
  >>> str(cs.name)
  'GCS_WGS_1984'
  """
 
  try:
    return _CRS.decode(s)
  except:
    try :
      return _CRS.parseWKT(s)
    except:
       raise Exception('Unable to parse %s' % (s))

def srs(cs):
  """
  Looks up the epsg code of a ``CRS``. 

  >>> cs = crs('EPSG:4326')
  >>> srs(cs)
  'EPSG:4326'

  This function returns ``None`` if *cs* can not matched to an epsg code.
  """

  id = _CRS.lookupIdentifier(cs, True)
  return str(id) if id else None
