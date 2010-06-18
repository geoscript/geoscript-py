import java
from org.geotools.geojson.geom import GeometryJSON 

_geojson = GeometryJSON()

def writeJSON(g):
  """
  Writes a geometry object as GeoJSON.

  >>> from geoscript.geom import Point 
  >>> str(writeJSON(Point(1,2)))
  '{"type":"Point","coordinates":[1,2]}'
  """
  return _geojson.toString(g)

def readJSON(json):
  """
  Reads a geometry a from GeoJSON.

  >>> readJSON('{"type":"Point","coordinates":[1,2]}')
  POINT (1 2)
  """
  return _geojson.read(java.lang.String(json))
