"""
The :mod:`proj` module provides support for coordinate reference system transformation and geometry reprojection.
"""
from org.geotools.geometry.jts import GeometryCoordinateSequenceTransformer as GeometryTX
from org.geotools.referencing import CRS as crs
from org.opengis.referencing.crs import CoordinateReferenceSystem
from geoscript import core

CRS = CoordinateReferenceSystem

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
         self._crs = crs.decode(proj)
      except:
         try:
           self._crs = crs.parseWKT(proj)
         except:
           raise Exception('Unable to determine projection from %s' % proj)

  def getid(self):
    return str(crs.lookupIdentifier(self._crs, True))

  id = property(getid, None, None, 'The string identifying the projection')

  def getwkt(self):
    return str(self._crs.toString())

  wkt = property(getwkt, None, None, 
     'The well known text string representing the projection')

  def getbounds(self):
    from geoscript.geom.bounds import Bounds
    #extent = crs.getGeographicBoundingBox(self._crs)  
    env = crs.getEnvelope(self._crs)
    if env:
      return Bounds(env.getMinimum(0), env.getMinimum(1), 
        env.getMaximum(0), env.getMaximum(1), self)
  bounds = property(getbounds, None, None, 
     'The extent for this projection as a :class:`Bounds <geoscript.geom.Bounds>` object. If unknown this method returns ``None``.')

  def getgeobounds(self):
    from geoscript.geom.bounds import Bounds
    box = crs.getGeographicBoundingBox(self._crs)  
    if box:
      return Bounds(box.westBoundLongitude, box.southBoundLatitude, 
        box.eastBoundLongitude, box.northBoundLatitude, 'epsg:4326')
  geobounds = property(getgeobounds, None, None, 
     'The geographic extent for this projection as a :class:`Bounds <geoscript.geom.Bounds>` object. If unknown this method returns ``None``.')

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
     >>> p2.round()
     POINT (1071693 554290)


    *obj* may also be specified as a single coordinate ``list`` or ``tuple``. *dest* may also be specified as a string identifying the destination projection.

    >>> proj = Projection('epsg:4326')
    >>> p1 = (-125, 50)
    >>> p2 = proj.transform(p1, 'epsg:3005')
    >>> [round(x) for x in p2]
    [1071693.0, 554290.0]
    """
    fromcrs = self._crs
    tocrs = Projection(dest)._crs
    tx = crs.findMathTransform(fromcrs,tocrs)

    if isinstance(obj, (list,tuple)):
      # tuple or list
      import jarray
      transformed = jarray.zeros(len(obj), 'd')
      tx.transform(obj, 0, transformed, 0, 1)
      l = [transformed[x] for x in range(len(obj))]
      return l if isinstance(obj, list) else tuple(l)
    else:
      # geometry
      gt = GeometryTX()
      gt.mathTransform = tx

      return core.map(gt.transform(obj))

  def __str__(self):
    return self.id
  
  def __repr__(self):
    return self.wkt

  def __eq__(self, other):
    return crs.equalsIgnoreMetadata(self._crs, other._crs)

def transform(obj, src, dst):
  """
  Reprojects an object from a source projection to a target projection. 

  >>> import geom 
  >>> p1 = geom.Point(-125, 50)
  >>> p2 = transform(p1, 'epsg:4326', 'epsg:3005')
  >>> p2.round()
  POINT (1071693 554290)

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

core.registerTypeMapping(CRS, Projection)
core.registerTypeUnmapping(Projection, CRS, lambda x: x._crs)

