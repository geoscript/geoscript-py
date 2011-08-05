from geoscript.feature import Feature
from org.geotools.geojson.feature import FeatureJSON

_fjson = FeatureJSON()

def writeJSON(f):
  """
  Writes a :class:`Feature <geoscript.feature.Feature>` object as GeoJSON.

  >>> from geoscript.geom import Point
  >>> writeJSON(Feature({'geom':Point(1,1),'name':'one'},'1'))
  u'{"type":"Feature","geometry":{"type":"Point","coordinates":[1,1]},"properties":{"name":"one"},"id":"1"}'
  """
  return _fjson.toString(f._feature)

def readJSON(json):
  """
  Reads a :class:`Feature <geoscript.feature.Feature>` object from GeoJSON.

  >>> readJSON('{"type":"Feature","geometry":{"type":"Point","coordinates":[1,1]},"properties":{"name":"one"},"id":"1"}')
  feature.1 {name: one, geometry: POINT (1 1)}
  """ 
  return Feature(f=_fjson.readFeature(json))
