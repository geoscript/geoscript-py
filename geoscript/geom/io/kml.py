from geoscript.util import xml
from org.locationtech.jts.geom import GeometryCollection

def writeKML(g, format=True, xmldecl=False, namespaces=True):
  """
  Writes a geometry object as KML.

  *format* specifies whether to format or pretty print the result.

  *xmldecl* specifies whether to include the XML declaration in the result. 

  >>> from geoscript.geom import Point 
  >>> writeKML(Point(1,2), format=False, namespaces=False)
  u'<Point><coordinates>1.0,2.0</coordinates></Point>'
  """
  el = g.getGeometryType()
  
  # in kml there is only multi geometry
  if isinstance(g, GeometryCollection):
    el = "MultiGeometry"

  return xml.kml.encode(g, el, format, xmldecl, namespaces)

def readKML(input):
  """
  Reads a geometry from KML. 

  *input* is the KML to read specified as a str, file, or some other input 
  stream.

  >>> readKML('<Point><coordinates>1.0,2.0</coordinates></Point>')
  POINT (1 2)
  """
  return xml.kml.parse(input)

