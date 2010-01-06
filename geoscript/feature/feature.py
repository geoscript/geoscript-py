import string
from org.geotools.feature.simple import SimpleFeatureBuilder
from geoscript import core

class Feature(object):
  """
  An object composed of a set of named attributes with values.

  A feature is constructed from a ``dict`` of name value pairs and an optional identifier.

  >>> f = Feature({ 'name': 'anvil', 'price': 100.0 }, 'widgets.1')
  >>> str(f.get('name'))
  'anvil'

  A feature can also be constructed optionally with a :class:`Schema`.

  >>> from schema import Schema
  >>> s = Schema('widgets', [('name', str), ('price', float)])
  >>> f = Feature({'name': 'anvil'}, '1', s)
  >>> f
  widgets.1 {name: anvil, price: None}

  When *schema* is specified feature values can be passed a ``list``.

  >>> s = Schema('widgets', [('name', str), ('price', float)])
  >>> f = Feature(['anvil', 100.0], '1', s)
  >>> f
  widgets.1 {name: anvil, price: 100.0}
  """
  def __init__(self, atts=None, id=None, schema=None, f=None):

    if atts:
      # attributes specified directly
      from schema import Schema

      # if list specified assume values in order of schema
      if isinstance(atts, list):
        if not schema:
          raise Exception('Values may be specified as list only when schema is supplied')

        natts = {}  
        for i in range(len(atts)):
          natts[schema.fields[i].name] = atts[i]
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

  id = property(getid, None)
  """
  Identifier of the feature as a ``str``

  >>> f = Feature({'name': 'anvil'}, 'widgets.1')
  >>> f.id
  'widgets.1'
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
    Returns a feature attribute value by name. ``KeyError`` is thrown if the attribute does not exist.

    *name* is the name of the attribute whose value to return.

    >>> f = Feature({'name': 'anvil', 'price': 100.0})
    >>> str(f.get('name'))
    'anvil'
    """
    self.schema.field(name)
    return self.f.getAttribute(name)

  def set(self, name, value):
    """
    Sets a feature attribute value by name. ``KeyError`` is thrown is the attribute does not exist.

    *name* is the name of the attribute whose value to set. 

    *value* is the new attribute value.

    >>> f = Feature({'name': 'anvil', 'price': 100.0})
    >>> str(f.get('name'))
    'anvil'
    >>> f.set('name', 'mallet')
    >>> str(f.get('name'))
    'mallet'
    """

    self.schema.field(name)
    self.f.setAttribute(name, value)

  def getattributes(self):

    atts = {}
    for fld in self.schema.fields:
      atts[fld.name] = core.map(self.f.getAttribute(fld.name))

    return atts

  attributes = property(getattributes, None)
  """
  A ``dict`` of name, value for the attributes of the feature.

  >>> f = Feature({'name': 'anvil', 'price': 100.0})
  >>> atts = f.attributes
  >>> str(atts['name'])
  'anvil'
  >>> atts['price']
  100.0
  """

  def __repr__(self):
    atts = ['%s: %s' % (fld.name, self.get(fld.name)) for fld in self.schema.fields]

    id = self.id if self.id.startswith(self.schema.name) else '%s.%s' % (self.schema.name, self.id)
    return '%s {%s}' % (id, string.join(atts,', '))
