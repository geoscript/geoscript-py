import string
from org.opengis.feature.type import FeatureType, GeometryDescriptor
from org.geotools.feature import NameImpl
from org.geotools.feature.simple import SimpleFeatureTypeBuilder
from geoscript import core, geom, proj
from geoscript.util import deprecated
from field import Field
from feature import Feature

class Schema(object):
  """
  Describes the structure of a feature. A schema is composed of a name, and a set of fields each containing a name and a type.

  *name* is a ``str``.

  *fields* is a ``list`` of (``str``, ``type``) tuples.

  >>> from geoscript import geom
  >>> schema = Schema('widgets', [ ('geom', geom.Point), ('name', str), ('price', float) ])
  >>> schema
  widgets [geom: Point, name: str, price: float]

  """

  def __init__(self, name=None, fields=[], ft=None, 
               uri='http://geoscript.org/feature'):
    self._type = ft

    if name and fields:
      # name and fields specified directly, generate gt feature type 
      # from list
      tb = SimpleFeatureTypeBuilder()
      tb.setName(NameImpl(name))
      tb.setNamespaceURI(uri)
      for fld in fields:
        if isinstance(fld, Field):
          name, typ, prj = fld.name, fld.typ, fld.proj
        else:
          name, typ = fld[0], fld[1]
          prj = None
          if issubclass(typ, geom.Geometry):
            # look for srs/crs info
            if len(fld) > 2:
              prj = proj.Projection(fld[2])
        prj = prj if prj else proj.Projection('EPSG:4326')
        if prj:
          tb.crs(prj._crs)
          
        # we call unmap() here to avoid setting the type binding to a Python
        # (eg: PyInteger) type, but rather a native java type (Integer)
        tb.add(name, core.unmap(typ))

      self._type = tb.buildFeatureType()
        
    elif ft:
      # gt feature type specified directly
      self._type = ft
    else:
      raise Exception('No fields specified for feature type.')

  def getname(self):
    return self._type.name.localPart

  name = property(getname, None, None, 'The name of the schema. A schema name is usually descriptive of the type of feature being described, for example "roads", "streams", "persons", etc...')

  def geturi(self):
    return self._type.name.namespaceURI
  uri = property(geturi, None, None, 'The namespace uri of the schema. A schema namespace uri qualifies the schema name, usually used for purposes of encoding GML.') 

  def getgeom(self):
    gd = self._type.geometryDescriptor
    if gd:
      return self.get(gd.localName)

  geom = property(getgeom, None, None, 'The geometry :class:`Field` of the schema. Returns ``None`` in the event the schema does not contain any geometric attributes')

  def getproj(self):
    crs = self._type.coordinateReferenceSystem
    if crs:
       return proj.Projection(crs)

  proj = property(getproj, None, None, 'The :class:`Projection <geoscript.proj.Projection>` of the schema. Returns ``None`` if the schema does not contain any geometric attributes or if the information is not available.')

  @deprecated
  def field(self, name):
    """
    Use :func:`get`.
    """
    return self.get(name)

  def get(self, name):
    """
    Returns the :class:`Field` of a specific name or ``None`` if no such attribute exists in the schema.
 
    *name* is the name of the field as a ``str``.

    >>> s = Schema('widgets', [('name', str), ('price', float)])
    >>> s.get('price')
    price: float
    """

    ad = self._type.getDescriptor(name)
    if ad:
      att = Field(ad.localName, core.map(ad.type.binding))
      if isinstance(ad, GeometryDescriptor) and ad.coordinateReferenceSystem:
        att.proj = proj.Projection(ad.coordinateReferenceSystem)

      return att

    raise KeyError('No such field "%s"' % name)

  def getfields(self):
    return [self.get(ad.localName) for ad in self._type.attributeDescriptors]

  fields = property(getfields)
  """
  A ``list`` of all schema :class:`fields <geoscript.feature.Field>`.

  >>> s = Schema('widgets', [ ('name', str), ('price', float) ])
  >>> s.fields
  [name: str, price: float]
  """

  def feature(self, vals, id=None):
    """
    Creates a feature of the schema from a ``dict`` of values values.
 
    *vals* is a ``dict`` in which keys are attribute names, and values are attribute values.

    *id* is an optional feature identifier as a ``str``.

    >>> s = Schema('widgets', [('name', str), ('price', float) ])
    >>> f = s.feature({'name': 'anvil', 'price': 100.0}, '1')
    >>> f 
    widgets.1 {name: anvil, price: 100.0}
    """
    return Feature(vals, id, self)
     
  def reproject(self, prj, name=None):
    """ 
    Transforms all the geometric attributes of a schema to a specified projection returning the result as a new schema.

    *prj* is a the target :class:`Projection <geoscript.proj.Projection>`.

    *name* is the optional name of the resulting schema.
    
    """ 

    prj = proj.Projection(prj)

    # copy the original schema fields and override the projection
    # on any geometric fields
    flds = self.fields
    for fld in flds: 
      if issubclass(fld.typ, geom.Geometry):
        fld.proj = prj

    if not name: 
      name = self.name

    return Schema(name, flds)

  def __getitem__(self, key):
    return self.get(key)

  def __iter__(self):
    for f in self.fields:
      yield f.name

  def iterkeys(self):
    return self.__iter__()

  def iteritems(self):
    for f in self.fields:
      yield f.name, f

  def keys(self):
    return [f.name for f in self.fields] 

  def values(self):
    return self.fields

  def __repr__(self):
    flds = ['%s' % str(fld) for fld in self.fields]
    return '%s [%s]' % (self.name, string.join(flds,', '))

  def __eq__(self, other):
    return other and self._type == other._type

core.registerTypeMapping(FeatureType, Schema, lambda x: Schema(ft=x))
core.registerTypeUnmapping(Schema, FeatureType, lambda x: x._type)
