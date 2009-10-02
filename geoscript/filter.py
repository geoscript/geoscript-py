"""
filter module -- Provides utilities for parsing and encoding filters.
"""

import sys
from java import io, lang
from org.opengis.filter import Filter as _Filter
from org.geotools.filter.text.cql2 import CQL
from org.geotools.xml import Parser, Encoder

Filter = _Filter

def toFilter(obj):
  """
  Converts an object to a filter. If obj is already a filter object it is 
  returned untouched. If obj is a string an attempt to parse the string as CQL
  is made. Upon failure an attempt to parse the string as XML is made. Upon a
  second failure an Exception is thrown.
  """

  if not obj:
    return None

  if isinstance(obj, Filter):
    return obj
  elif isinstance(obj, str):
    try:
      # parse as CQL
      return fromCQL(obj)
    except:
      try:
        # parse as XML
        return fromXML(obj)
      except:
        raise Exception('Could not convert %s to filter.' % obj)

def fromCQL(cql):
  """
  Parses a CQL string into a filter object.
  
  >>> f = fromCQL("name = 'foobar'")
  >>> str(f)
  '[ name = foobar ]'
  """

  return CQL.toFilter(cql)

def toCQL(filter):
  """
  Encodes a filter object as a CQL string.

  >>> f = fromXML('<filter><PropertyIsEqualTo><PropertyName>name</PropertyName><Literal>foobar</Literal></PropertyIsEqualTo></filter>')
  >>> str(toCQL(f))
  "name = 'foobar'"
  """
  return CQL.toCQL(filter)

def fromXML(xml, version=1.0):
  """
  Parses a XML string into a filter object.
  
  >>> f = fromXML('<Filter><PropertyIsEqualTo><PropertyName>name</PropertyName><Literal>foobar</Literal></PropertyIsEqualTo></Filter>')
  >>> str(f)
  '[ name = foobar ]'
  """

  ogc, ogcconfig  = _ogc(version)
  parser = Parser(ogcconfig)
  return parser.parse(io.StringReader(xml))

def toXML(filter, pretty=True, version=1.0):
  """
  Encodes a filter object as XML.

  >>> f = fromCQL("name = 'foobar'")
  >>> xml = toXML(f, False)
  >>> from xml.dom import minidom
  >>> d = minidom.parseString(xml)
  >>> str(d.documentElement.tagName)
  'ogc:Filter'
  """

  ogc, ogcconfig = _ogc(version)
  e = Encoder(ogcconfig)
  e.indenting = pretty
  e.omitXMLDeclaration = True
  out = io.ByteArrayOutputStream()
  e.encode(filter, ogc.Filter, out)
  return str(lang.String(out.toByteArray()))
 
def _ogc(version):
  try: 
    from org.geotools.filter.v1_0 import OGCConfiguration as OGCConfiguration10, OGC as OGC10
    from org.geotools.filter.v1_1 import OGCConfiguration as OGCConfiguration11, OGC as OGC11

  except ImportError:
    raise Exception('fromXML() not available, filter libs not on classpath')

  return (OGC11.getInstance(),OGCConfiguration11()) if version == 1.1 else (OGC10.getInstance(), OGCConfiguration10())
