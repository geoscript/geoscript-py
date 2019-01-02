"""
The :mod:`filter` module provides utilities for parsing and encoding filters.
"""

import sys
from java import io, lang
from org.opengis.filter import Filter as _Filter
from org.geotools.filter.text.cql2 import CQL
from org.geotools.filter.text.ecql import ECQL
from org.geotools.xsd import Parser, Encoder
from org.geotools.factory import CommonFactoryFinder
from geoscript import core

_factory = CommonFactoryFinder.getFilterFactory(None)

class Filter(object):
  """
  A predicate or constraint used to match or filter :class:`Feature <geoscript.feature.Feature>` objects.

  *obj* is the CQL ``str`` representation of the filter.

  >>> f = Filter("name = 'foobar'")
  >>> f
  [ name = foobar ]

  *obj* may also be specified as XML.

  >>> f = Filter('<Filter><PropertyIsEqualTo><PropertyName>name</PropertyName><Literal>foobar</Literal></PropertyIsEqualTo></Filter>')
  >>> f
  [ name = foobar ]
  """

  def __init__(self, obj):
    if isinstance(obj, Filter):
      self._filter = obj._filter
    elif isinstance(obj, _Filter):
      self._filter = obj
    elif isinstance(obj, (str, unicode)):
      # first try parsing as CQL
      try:
        self._filter = _fromCQL(obj)
      except:
        # next try as ECQL
        try:
          self._filter = _fromECQL(obj)
        except:
          # next try as XML
          try:
            self._filter = _fromXML(obj)
          except:
            try:
              self._filter = _fromXML(obj, version=1.1)
            except:
              raise Exception('Could not parse "%s" as filter' % (obj))

  def getcql(self):
     return _toCQL(self._filter)    

  cql = property(getcql, None, None, 'The CQL representation of the filter.')

  def xml(self, pretty=True, version=1.0):
    """
    Returns the OGC XML representation of the filter.

    *pretty* controls if the resulting xml is "pretty printed" or not.

    *version* specifies the version of of the OGC filter encoding specification to use for encoding. The default is 1.0. Other possibilites include 1.1.

    >>> f = Filter("name = 'foobar'")
    >>> xml = f.xml(False)
    >>> from xml.dom import minidom
    >>> d = minidom.parseString(xml)
    >>> str(d.documentElement.tagName)
    'ogc:Filter'
    """
    return _toXML(self._filter, pretty, version)
   
  def evaluate(self, f):
    """
    Evaluates the filter against a Feature.

    *f* is the :class:`geoscript.feature.Feature` to evaluate against.

    >>> from geoscript.feature import Feature
    >>> feature = Feature({'name': 'foobar'})
    >>> f = Filter("name = 'foobar'")
    >>> f.evaluate(feature)
    True
    """
    return self._filter.evaluate(f._feature)
 
  def __eq__(self, other):
    return self._filter.equals(other._filter)

  def __hash__(self):
    return self._filter.hashCode()

  def __repr__(self):
    return self._filter.toString()

  def __add__(self, other):
    oth = Filter(other) if other is not None else None

    if oth is None or oth._filter == _Filter.INCLUDE:
       return Filter(self._filter)

    if self._filter == _Filter.INCLUDE:
       return oth

    return Filter(_factory.and(self._filter, oth._filter))

Filter.PASS = Filter(_Filter.INCLUDE)
Filter.FAIL = Filter(_Filter.EXCLUDE)

def _fromCQL(cql):
  """Parses a CQL string into a filter object."""

  return CQL.toFilter(cql)

def _fromECQL(cql):
  """Parses a ECQL string into a filter object."""

  return ECQL.toFilter(cql)

def _toCQL(filter):
  """Encodes a filter object as a CQL string."""

  return CQL.toCQL(filter)

def _fromXML(xml, version=1.0):
  """Parses a XML string into a filter object."""

  ogc, ogcconfig  = _ogc(version)
  parser = Parser(ogcconfig)
  return parser.parse(io.StringReader(xml))

def _toXML(filter, pretty=True, version=1.0):
  """
  Encodes a filter object as XML.

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

core.registerTypeMapping(_Filter, Filter)
core.registerTypeMapping(Filter, _Filter, lambda x: x._filter)
