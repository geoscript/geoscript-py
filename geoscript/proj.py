"""
proj module -- Provides coordinate reference system and reprojection support.
"""
from org.geotools.geometry.jts import GeometryCoordinateSequenceTransformer as GeometryTX
from org.geotools.referencing import CRS

def transform(g, fromsrs, tosrs):
  """
  Reprojects a geometry from a source project to a target projection. 

  The arguments 'fromsrs' and 'tosrs' are specified as epsg codes.

  >>> import geom 
  >>> p1 = geom.Point(-125,50)
  >>> p2 = transform(p1,'epsg:4326','epsg:3005')
  >>> str(p2)
  'POINT (1071693.1296328472 554289.941892416)'
  """

  fromcrs = CRS.decode(fromsrs)
  tocrs = CRS.decode(tosrs)
  tx = CRS.findMathTransform(fromcrs,tocrs)

  if type(g) in (list,tuple):
    transformed = [0 for x in range(len(g))]
    tx.transform(g,0,transformed,0,1)
    return transformed
  else:
    #geometry
    gt = GeometryTX()
    gt.mathTransform = tx

    return gt.transform(g)

