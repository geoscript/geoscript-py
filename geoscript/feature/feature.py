import string
from org.geotools.feature.simple import SimpleFeatureBuilder
from org.opengis.feature import Feature as _Feature
from geoscript import core, geom

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

    from schema import Schema
    if atts:
      # attributes specified directly

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
      b = SimpleFeatureBuilder(self.schema._type)
      for att, val in atts.iteritems(): 
        b.set(att, val)

      self._feature = b.buildFeature(str(id) if id else None)

    elif f:
      # feature specififed directly
      self._feature = f
      self.schema = schema if schema else Schema(ft=f.type)

    else:
      raise Exception('No attributes specified for feature')

  def getid(self):
    return self._feature.identifier.toString()

  id = property(getid, None)
  """
  Identifier of the feature as a ``str``

  >>> f = Feature({'name': 'anvil'}, 'widgets.1')
  >>> f.id
  'widgets.1'
  """

  def getgeom(self):
    return core.map(self._feature.defaultGeometry)

  def setgeom(self, g):
    self._feature.defaultGeometry = g

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

  def getbounds(self):
    env = self._feature.getBounds()
    if env is not None and not env.isNull():
      return geom.Bounds(env=env)

  bounds = property(getbounds)
  """
  The :class:`Bounds <geoscript.geom.bounds.Bounds>` of the feature geometry. 
  Will return ``None`` if the feature does not contain any geometric attributes.
  """

  def get(self, name):
    """
    Returns a feature attribute value by name. ``KeyError`` is thrown if the attribute does not exist.

    *name* is the name of the attribute whose value to return.

    >>> f = Feature({'name': 'anvil', 'price': 100.0})
    >>> str(f.get('name'))
    'anvil'
    """
    self.schema.get(name)
    return self._feature.getAttribute(name)

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

    self.schema.get(name)
    self._feature.setAttribute(name, value)

  def getattributes(self):
    atts = {}
    for fld in self.schema.fields:
      atts[fld.name] = core.map(self._feature.getAttribute(fld.name))

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

  def __getitem__(self, key):
    return self.get(key)

  def __setitem__(self, key, value):
    self.set(key, value)

  def __iter__(self):
    return self.schema.__iter__()

  def iterkeys(self):
    return self.__iter__()

  def iteritems(self):
    return self.attributes.iteritems()

  def keys(self):
    return [f.name for f in self.schema.fields]

  def values(self):
    return [core.map(val) for val in self._feature.getAttributes()]

  def __repr__(self):
    atts = ['%s: %s' % (fld.name, self.get(fld.name)) for fld in self.schema.fields]

    id = self.id if self.id.startswith(self.schema.name) else '%s.%s' % (self.schema.name, self.id)
    return '%s {%s}' % (id, string.join(atts,', '))

  def __eq__(self, other):
    return other and self._feature == other._feature

core.registerTypeMapping(_Feature, Feature, lambda x: Feature(f=x))
core.registerTypeUnmapping(Feature, _Feature, lambda x: x._feature)
