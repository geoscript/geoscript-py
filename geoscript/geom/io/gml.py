from geoscript.util import xml

def writeGML(g, ver=2, format=True, xmldecl=False):
  """
  Writes a geometry object as GML.

  *ver* specifies the gml version to encode. Supported versions include 2, 3, 
  and 3.2.

  *format* specifies whether to format or pretty print the result.

  *xmldecl* specifies whether to include the XML declaration in the result. 

  >>> from geoscript.geom import Point 
  >>> writeGML(Point(1,2), format=False)
  u'<gml:Point xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink"><gml:coord><gml:X>1.0</gml:X><gml:Y>2.0</gml:Y></gml:coord></gml:Point>'
  """
  el = g.getGeometryType()
  
  # in gml 3.2 MultiPolygon and MultiLineString do not exist
  if "MultiPolygon" == el:
    el = "MultiSurface"
  elif "MultiLineString" == el:
    el = "MultiCurve"

  return xml.gml.encode(g, el, ver, format, False, xmldecl)

def readGML(input, ver=2):
  """
  Reads a geometry from GML. 

  *input* is the GML to read specified as a str, file, or some other input 
  stream.

  *ver* specifies the gml version to encode. Supported versions include 2, 3, 
  and 3.2.

  >>> readGML('<gml:Point xmlns:gml="http://www.opengis.net/gml"><gml:coord><gml:X>1.0</gml:X><gml:Y>2.0</gml:Y></gml:coord></gml:Point>')
  POINT (1 2)
  """
  return xml.gml.parse(input, ver)

