"""
proj module -- Provides coordinate reference system and reprojection support.
"""
from org.geotools.geometry.jts import GeometryCoordinateSequenceTransformer as GeometryTX
from org.geotools.referencing import CRS as XCRS
from org.opengis.referencing.crs import CoordinateReferenceSystem

"""
crs utility object 
"""
crs = XCRS

"""
shorthand for crs class
"""
CRS = CoordinateReferenceSystem

def transform(g, fromsrs, tosrs):
  """
  Reprojects a geometry from a source project to a target projection. 

  The arguments 'fromsrs' and 'tosrs' are specified as epsg codes.

  >>> import geom 
  >>> p1 = geom.point(-125,50)
  >>> p2 = transform(p1,'epsg:4326','epsg:3005')
  >>> str(p2)
  'POINT (1071693.1296328472 554289.941892416)'

  This function can also take arrays or tuples of coordinates

  >>> p1 = [-125,50]
  >>> p2 = transform(p1,'epsg:4326','epsg:3005')
  >>> str(p2)
  '[1071693.1296328472, 554289.941892416]'
  """

  fromcrs = crs.decode(fromsrs)
  tocrs = crs.decode(tosrs)
  tx = crs.findMathTransform(fromcrs,tocrs)

  if type(g) in (list,tuple):
    import jarray
    transformed = jarray.zeros(len(g),'d')
    tx.transform(g,0,transformed,0,1)
    return [transformed[x] for x in range(len(g))]
  else:
    #geometry
    gt = GeometryTX()
    gt.mathTransform = tx

    return gt.transform(g)

