"""
feature module -- Provides classes for simple feature access.
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

class FeatureType:
  """
  A feature type is the schema for a feature. It specifies the names and 
  types of a features attributes. A feature type can be constructed from a 
  list of name, type tuples
   
  >>> import geom
  >>> ft = FeatureType('myFeatureType', [ ('geom',geom.Point), ('att1',int), ('att2',str) ])
  >>> str(ft)
  'myFeatureType {geom: Point, att1: int, att2: str}'

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

  def name(self):
    """
    The name of the feature type.

    >>> ft = FeatureType('myFeatureType', [ ('geom',geom.Point), ('att1',int), ('att2',str) ])
    >>> str(ft.name())
    'myFeatureType'
    """

    return self.ft.name.localPart

  def geom(self):
    """
    The geometry attribute of the feature type. The attribute is represented by
    a tuple of the form (<name>,<type> [,<crs>])

    >>> ft = FeatureType('myFeatureType', [ ('geom',geom.Point), ('att1',int), ('att2',str) ])
    >>> g = ft.geom()
    >>> str(g[0])
    'geom'
    >>> g[1].__name__
    'Point'
    """

    gd = self.ft.geometryDescriptor
    if gd:
      geom = (gd.localName,gd.type.binding)
      if gd.coordinateReferenceSystem:
        geom = (geom[0],geom[1],gd.coordinateReferenceSystem)

      return geom

  def atts(self):
    """
    Iterates over attributes.

    >>> ft = FeatureType('myFeatureType', [ ('geom',geom.Point), ('att1',int), ('att2',str) ])
    >>> str(', '.join(['%s: %s' % (att,typ.__name__) for att,typ in ft.atts()]))
    'geom: Point, att1: int, att2: str'
    """

    for ad in self.ft.attributeDescriptors:
      yield (ad.localName, _map(ad.type.binding))

  def attnames(self):
    """ 
    Iterates over attribute names.
    >>> ft = FeatureType('myFeatureType', [ ('geom',geom.Point), ('att1',int), ('att2',str) ])
    >>> str(', '.join(['%s' % (att) for att in ft.attnames()]))
    'geom, att1, att2'
    """

    for ad in self.ft.attributeDescriptors:
      yield ad.localName

  def feature(self, vals, id=None):
    """
    Creates a feature of the type from a list of attribute values.

    >>> ft = FeatureType('myFeatureType', [ ('geom',geom.Point), ('att1',int), ('att2',str) ])
    >>> f = ft.feature([geom.point(1,1), 1, 'one'], 'fid1')
    >>> str(f) 
    'fid1 {geom: POINT (1 1), att1: 1, att2: one}'
    """
    return Feature(zip([att for att in self.attnames()],vals), id, self)
     
  def __str__(self):
    atts = ['%s: %s' % (att,typ.__name__) for att,typ in self.atts()]
    return '%s {%s}' % (self.name(), string.join(atts,', '))

class Feature:
  """
  A feature is a set of attributes (key value pairs) and a geometry.

  >>> import geom
  >>> f = Feature([ ('name','widget'), ('geom', geom.point(1,2)) ], 'fid1') 
  >>> str(f)
  'fid1 {name: widget, geom: POINT (1 2)}'

  The attributes of a feature can be get and set:

  >>> str(f.get('name'))
  'widget'
  >>> f.set('name','foobar')
  >>> str(f.get('name'))
  'foobar'

  The geometry of a feature can also be modified:

  >>> f.geom()
  POINT (1 2)
  >>> f.geom(geom.point(3,4))
  POINT (3 4)

  """
  def __init__(self, atts=None, id=None, ftype=None, f=None):

    if atts:
      # attributes specified directly

      # turn into list of tuples if necessary
      if isinstance(atts, dict):
        l = [(x,y) for x,y in atts.iteritems()]
        atts = l

      # generate feature type if necessary
      self.ftype = ftype 
      if not self.ftype: 
        self.ftype = FeatureType('feature', [(x[0],type(x[1])) for x in atts])
      
      # generate feature
      b = SimpleFeatureBuilder(self.ftype.ft)
      for att in atts: 
        b.set(att[0],att[1])

      self.f = b.buildFeature(id)

    elif f:
      # feature specififed directly
      self.f = f
      self.ftype = ftype if ftype else FeatureType(f.type)

    else:
      raise Exception('No attributes specified for feature')

  def id(self):
    """
    Id of the feature.

    >>> import geom
    >>> f = Feature({'geom': geom.point(1,1)}, 'fid.one')
    >>> str(f.id())
    'fid.one'
    """

    return self.f.identifier.toString()

  def geom(self, g=None):
    """
    Gets and sets the geometry of the feature.
    >>> import geom
    >>> f = Feature({'geom': geom.point(1,1)}, 'fid.one')
    >>> f.geom()
    POINT (1 1)
    >>> f.geom(geom.point(2,2))
    POINT (2 2)
    """

    if g:
      self.f.defaultGeometry = g

    return self.f.defaultGeometry

  def get(self,att):
    """
    Gets an attribute of a feature.
    >>> import geom
    >>> f = Feature({'geom': geom.point(1,1), 'name': 'one'}, 'fid.one')
    >>> str(f.get('name'))
    'one'
    """
    return self.f.getAttribute(att)

  def set(self,att,value):
    """
    Sets an attribute of a feature.
    >>> import geom
    >>> f = Feature({'geom': geom.point(1,1), 'name': 'one'}, 'fid.one')
    >>> str(f.get('name'))
    'one'
    >>> f.set('name', 'two')
    >>> str(f.get('name'))
    'two'
    """

    self.f.setAttribute(att,value)

  def atts(self):
    """
    Iterates over attributes.
    >>> import geom
    >>> f = Feature({'geom': geom.point(1,1), 'name': 'one'}, 'fid.one')
    >>> str(', '.join(['%s: %s' % (att,val) for att,val in f.atts()]))
    'geom: POINT (1 1), name: one'
    """

    for att in self.ftype.attnames():
      yield (att, _map(self.f.getAttribute(att)))

  def __str__(self):
    atts = ['%s: %s' % (att,val) for att,val in self.atts()]
    return '%s {%s}' % (self.id(), string.join(atts,', '))
