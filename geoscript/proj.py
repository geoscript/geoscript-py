"""
The :mod:`proj` module provides support for coordinate reference system transformation and geometry reprojection.
"""
from com.vividsolutions.jts.geom import CoordinateFilter
from org.osgeo.proj4j import CoordinateReferenceSystem as CRS
from org.osgeo.proj4j import ProjCoordinate
from org.osgeo.proj4j import CRSFactory, CoordinateTransformFactory 

_crsFactory = CRSFactory()
_txFactory = CoordinateTransformFactory()

class Projection(object):
  """
  A cartographic projection or coordinate reference system.

  *proj* is a string that identifies the coordinate reference system (eg. an epsg code):

  >>> prj = Projection('epsg:4326')
  >>> prj.id
  'EPSG:4326'

  Alternatively *proj* may be specified as a well known text string:

  >>> wkt = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
  >>> prj = Projection(wkt)
  >>> prj.id
  'EPSG:4326'
  """

  def __init__(self, proj):
    if isinstance(proj, CRS):
      self._crs = proj
    elif isinstance(proj, Projection):
      self._crs = proj._crs
    elif isinstance(proj, (str,unicode)):
      try:
         self._crs = _crsFactory.createFromName(proj)
      except:
         try:
           self._crs = _crsFactory.createFromParams(None, proj)
         except:
           raise Exception('Unable to determine projection from %s' % proj)

  def getid(self):
    return self._crs.getName()

  id = property(getid, None, None, 'The string identifying the projection')

  def transform(self, obj, dest):
    """
    Transforms an object from this projection to a specified destination projection.

    *obj* is a :class:`Geometry <geoscript.geom.Geometry>` object to transform.

    *dest* is the destination :class:`Projection` to transform to.

     >>> proj = Projection('epsg:4326')
     >>> dest = Projection('epsg:3005')
     >>> import geom
     >>> p1 = geom.Point(-125, 50)
     >>> p2 = proj.transform(p1, dest)
     >>> p2
     POINT (1071693.1296328472 554289.9418924153)

    *obj* may also be specified as a single coordinate ``list`` or ``tuple``. *dest* may also be specified as a string identifying the destination projection.

    >>> proj = Projection('epsg:4326')
    >>> p1 = (-125, 50)
    >>> p2 = proj.transform(p1, 'epsg:3005')
    >>> p2
    (1071693.1296328472, 554289.9418924153)
    """
    fromcrs = self._crs
    tocrs = Projection(dest)._crs
    tx = _txFactory.createTransform(fromcrs, tocrs)

    if isinstance(obj, (list,tuple)):
      # tuple or list
      p1 = ProjCoordinate(*obj)      
      p2 = ProjCoordinate()      

      tx.transform(p1, p2)

      l = [p2.x, p2.y]
      if len(obj) > 2:
         l.append(p2.z)

      return l if isinstance(obj, list) else tuple(l)
    else:
      # geometry
      obj.apply(TransformFilter(tx))
      return obj

  def __str__(self):
    return self.id
  
  def __eq__(self, other):
    return other and self.name == other.name

def transform(obj, src, dst):
  """
  Reprojects an object from a source projection to a target projection. 

  >>> import geom 
  >>> p1 = geom.Point(-125, 50)
  >>> p2 = transform(p1, 'epsg:4326', 'epsg:3005')
  >>> p2
  POINT (1071693.1296328472 554289.9418924153)

  .. seealso:: 

     :func:`Projection.transform`
  """
  
  return Projection(src).transform(obj, dst)

def projections():
  """
  Iterator over all defined projections::

    for p in proj.projections():
       ..

  This function returns :class:`Projection` objects.

  """
  for code in crs.getSupportedCodes('epsg'):
     try:
       yield Projection('epsg:%s' % code)
     except:
       # todo: log this
       pass

class TransformFilter(CoordinateFilter):

  def __init__(self, tx):
    self.tx = tx;

  def filter(self, coord):
    p1 = ProjCoordinate(coord.x, coord.y, coord.z)
    p2 = ProjCoordinate()
    self.tx.transform(p1, p2)
    coord.x = p2.x
    coord.y = p2.y
    coord.z = p2.z
    

