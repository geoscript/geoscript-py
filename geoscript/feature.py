"""
feature module -- Classes for simple feature access.
"""

import java
import string
from geoscript import geom, proj
from org.opengis.feature.type import GeometryDescriptor
from org.geotools.feature import NameImpl
from org.geotools.feature.simple import SimpleFeatureBuilder, SimpleFeatureTypeBuilder

_tmap = {}
_tmap[int] = java.lang.Integer
_tmap[java.lang.Integer] = int
_tmap[java.lang.Short] = int
_tmap[java.lang.Float] = int

_tmap[long] = java.lang.Long
_tmap[java.lang.Long] = long

_tmap[str] = java.lang.String
_tmap[unicode] = java.lang.String
_tmap[java.lang.String] = str

_tmap[float] = java.lang.Double
_tmap[java.lang.Double] = float
_tmap[java.lang.Float] = float

"""
Maps a jython type to its associated java type.
"""
def _map(o):
  if isinstance(o,type):
    t = o 
  else:
    t = type(o)

  if _tmap.has_key(t):
    mapped = _tmap[t]
    if isinstance(o,type):
      return mapped
    else:
      return mapped(o)

  return o

class Schema(object):
  """
  Describes the structure of a feature. A schema is composed of a name, and a set of attributes each containing a name and a type.

  *atts* is specicied as a ``list`` of (``str``, ``type``) tuples:

  >>> import geom
  >>> schema = Schema('widgets', [ ('geom', geom.Point), ('name', str), ('price', float) ])
  >>> str(schema)
  'widgets [geom: Point, name: str, price: float]'

  """

  def __init__(self, name=None, atts=[], ft=None):
    self.ft = ft

    if name and atts:
      # name and attributes specified directly, generate gt feature type 
      # from list
      tb = SimpleFeatureTypeBuilder()
      tb.setName(NameImpl(name))
      for att in atts:
        name, typ = att[0], att[1]
        if issubclass(typ, geom.Geometry):
          # look for srs/crs info
          if len(att) > 2:
            xrs = att[2]
            if isinstance(xrs,str):
              tb.srs(xrs)
            elif isinstance(xrs,proj.CRS):
              tb.crs(xrs)
          
        # we call _map() here to avoid setting the type binding to a Python
        # (eg: PyInteger) type, but rather a native java type (Integer)
        tb.add(name, _map(typ))

      self.ft = tb.buildFeatureType()
        
    elif ft:
      # gt feature type specified directly
      self.ft = ft
    else:
      raise Exception('No attributes specified for feature type.')

  def getname(self):
    return self.ft.name.localPart

  name = property(getname)
  """
  The name of the schema. A schema name is usually descriptive of the type of feature being descripted, for example 'roads', 'streams', 'persons', etc...

  >>> s = Schema('widgets')
  >>> s.name
  'widgets'
  """

  def getgeom(self):
    gd = self.ft.geometryDescriptor
    if gd:
      return self.attribute(gd.localName)

  geom = property(getgeom)
  """
  The geometry :class:`Attribute` of the schema. Returns ``None`` in the event the schema does not contain any geometric attributes.

  >>> s = Schema('widgets', [ ('geom',geom.Point) ])
  >>> s.geom
  (geom, Point)
  """

  def attribute(self, name):
    """
    Returns the :class:`Attribute` named *name*, or ``None`` if no such attribute exists in the schema.

    >>> s = Schema('widgets', [('name', str), ('price', float)])
    >>> s.attribute('price')
    price: float
    """

    ad = self.ft.getDescriptor(name)
    if ad:
      att = Attribute(ad.localName, _map(ad.type.binding))
      if isinstance(ad, GeometryDescriptor) and ad.coordinateReferenceSystem:
        att.proj = proj.Projection(ad.coordinateReferenceSystem)

      return att

  def getattributes(self):
    return [self.attribute(ad.localName) for ad in self.ft.attributeDescriptors]

  attributes = property(getattributes)
  """
  Returns a ``list`` of all schema :class:`Attribute`.

  >>> s = Schema('widgets', [ ('name', str), ('price', float) ])
  >>> s.attributes
  [name: str, price: float]
  """

  def feature(self, vals, id=None):
    """
    Creates a feature of the schema from a ``dict`` of values values.

    >>> s = Schema('widgets', [('name', str), ('price', float) ])
    >>> f = s.feature({'name': 'anvil', 'price': 100.0}, '1')
    >>> str(f) 
    'widgets.1 {name: anvil, price: 100.0}'
    """
    return Feature(vals, id, self)
     
  def __str__(self):
    atts = ['%s' % str(att) for att in self.attributes]
    return '%s [%s]' % (self.name, string.join(atts,', '))

class Attribute(object):
  """
  A schema attribute composed of a name and a type. A geometric attribute also contains a :class:`geoscript.proj.Projection`.
  """

  def __init__(self, name, typ, proj=None):
    self.name = name
    self.typ = typ
    self.proj = proj

  def __repr__(self):
    return '%s: %s' % (self.name, self.typ.__name__)

class Feature(object):
  """
  An object composed of a set of named attributes with values.

  A feature is constructed from a ``dict`` of name value pairs and an optional identifier:

  >>> f = Feature({ 'name': 'anvil', 'price': 100.0 }, 'widgets.1')
  >>> str(f.get('name'))
  'anvil'

  A feature can also be constructed optionally with a :class:`Schema`:

  >>> s = Schema('widgets', [('name', str), ('price', float)])
  >>> f = Feature({'name': 'anvil'}, '1', s)
  >>> str(f)
  'widgets.1 {name: anvil, price: None}'

  When *schema* is specified feature values can be passed a ``list``:

  >>> s = Schema('widgets', [('name', str), ('price', float)])
  >>> f = Feature(['anvil', 100.0], '1', s)
  >>> str(f)
  'widgets.1 {name: anvil, price: 100.0}'

  """
  def __init__(self, atts=None, id=None, schema=None, f=None):

    if atts:
      # attributes specified directly

      # if list specified assume values in order of schema
      if isinstance(atts, list):
        if not schema:
          raise Exception('Values may be specified as list only when schema is supplied')

        natts = {}  
        for i in range(len(atts)):
          natts[schema.attributes[i].name] = atts[i]
        atts = natts

      # generate feature type if necessary
      self.schema = schema 
      if not self.schema: 
        self.schema = Schema('feature', [(att, type(val)) for att,val in atts.iteritems()])
      
      # generate feature
      b = SimpleFeatureBuilder(self.schema.ft)
      for att, val in atts.iteritems(): 
        b.set(att, val)

      self.f = b.buildFeature(id)

    elif f:
      # feature specififed directly
      self.f = f
      self.schema = schema if schema else Schema(ft=f.type)

    else:
      raise Exception('No attributes specified for feature')

  def getid(self):
    return self.f.identifier.toString()

  id = property(getid)
  """
  Id of the feature.

  >>> f = Feature({'name': 'anvil'}, 'widgets.1')
  >>> f.id
  widgets.1
  """

  def getgeom(self):
    return self.f.defaultGeometry

  def setgeom(self, g):
    self.f.defaultGeometry = g

  geom = property(getgeom, setgeom)
  """
  The geometry of the feature.

  >>> import geom
  >>> f = Feature({'geom': geom.Point(1,1)})
  >>> f.geom
  POINT (1 1)
  >>> f.geom = geom.Point(2,2)
  >>> f.geom
  POINT (2 2)
  """

  def get(self, name):
    """
    Returns a feature attribute value. *name* is the name of the attribute whose value to return.

    >>> f = Feature({'name': 'anvil', 'price': 100.0})
    >>> str(f.get('name'))
    'anvil'
    """
    return self.f.getAttribute(name)

  def set(self, name, value):
    """
    Sets a feature attribute value. *name* is the name of the attribute whose value to set, and *value* is the new attribute value.

    >>> f = Feature({'name': 'anvil', 'price': 100.0})
    >>> str(f.get('name'))
    'anvil'
    >>> f.set('name', 'mallet')
    >>> str(f.get('name'))
    'mallet'
    """

    self.f.setAttribute(name, value)

  def getattributes(self):

    atts = {}
    for att in self.schema.attributes:
      atts[att.name] = _map(self.f.getAttribute(att.name))

    return atts

  attributes = property(getattributes)
  """
  Returns a ``dict`` of name, value for the attributes of the feature.

  >>> f = Feature({'name': 'anvil', 'price': 100.0})
  >>> atts = f.attributes
  >>> str(atts['name'])
  'anvil'
  >>> atts['price']
  100.0
  """
  def __str__(self):
    atts = ['%s: %s' % (att.name, self.get(att.name)) for att in self.schema.attributes]

    id = self.id if self.id.startswith(self.schema.name) else '%s.%s' % (self.schema.name, self.id)
    return '%s {%s}' % (id, string.join(atts,', '))
