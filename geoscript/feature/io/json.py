from geoscript.feature import Feature
from org.geotools.geojson.feature import FeatureJSON

_fjson = FeatureJSON()

def writeJSON(f):
  return _fjson.toString(f._feature)

def readJSON(json):
  return Feature(f=_fjson.readFeature(json))
