"""
feature module -- Feature model classes
"""

from com.vividsolutions.jts.geom import Geometry
from org.opengis.feature.type import GeometryDescriptor
from org.geotools.feature.simple import SimpleFeatureBuilder
from org.geotools.referencing import CRS 

"""
A feature type is the schema for a feature. It specifies the names and
types of a features attributes.
 
>>> atts = []
>>> atts.append({'name':'att1', 'type', int})
>>> atts.append({'name':'att2', 'type', str})
>>> ft = FeatureType(atts=atts)
>>> str(ft)
"{'att1': int, 'att2': str}"
"""
class FeatureType:

  def __init__(self, name=None, ft=None, atts={}, geom={}):
    self.name = name
    self.ft = ft
    self.atts = atts
    self.geom = geom

    #set a name if not supplied directly
    if not self.name and ft:
      self.name = ft.localName
    
    if ft:
      #generate attributes from gt feature type
      for ad in ft.attributeDescriptors:
         att = {}
         att['name'] = ad.localName
         att['type'] = ad.type.binding
         if isinstance(ad,GeometryDescriptor):
            #geom attribute, look for a crs
            crs = ad.type.coordinateReferenceSystem
            if crs:
              att['srs'] = CRS.toSRS(crs)
              att['epsg'] = CRS.lookupEpsgCode(crs,True)

         if isinstance(ad,GeometryDescriptor) and not self.geom:
            #default geom attribute
            self.geom = att
         else:    
            #regular attribute
            self.atts[att['name']] = att

    elif atts:
      #attributes supplied directly, scan for geometry
      for att in atts.values():
        if isinstance(att['type'],Geometry) and not self.geom:
           self.geom = att

      if self.geom:
        atts.remove(self.geom)

class Feature:
  """
  A feature is a set of attributes (key value pairs) and a geometry.

  >>> import geom
  >>> f = Feature(atts={'name':'widget'},geom=geom.Point(1,2))
  >>> str(f)
  "{'name': 'widget'}; POINT (1 2)"

  The attributes of a feature can be get and set:

  >>> f.get('name')
  'widget'
  >>> f.set('name','foobar')
  >>> f.get('name')
  'foobar'

  The geometry of a feature can also be modified:

  >>> f.geom = geom.LineString([ [1,2],[3,4] ])
  >>> str(f.geom)
  'LINESTRING (1 2, 3 4)'

  """
  def __init__(self, id=None, ftype=None, f=None, atts=None, geom=None):
    self.id = id
    self.ftype = ftype
    self.f = f
    self.atts = {}
    self.geom = None
    
    # set a unique identifier
    if not id:
      if f:
        # set from feature
        self.id = f.id
      else:
        # generate a unique id
        import uuid
        self.id = str(uuid.uuid1())

        # qualify with feature type name if possible
        if ftype and ftype.name:
          self.id = '%s.%s' % (ftype.name, self.id)

    if ftype and f:
       for att in ftype.atts.keys():
         if ftype.geom and att == ftype.geom['name']:
            self.geom = f.getAttribute(att)
         else:
            self.atts[att] = f.getAttribute(att)

    if not ftype:
       #generate type from attributes
       if atts:
         tatts = {}
         for att,val in atts.iteritems():
           tatts[att] = {'name':att, 'type':type(val)}

         self.ftype = FeatureType(atts=tatts)

    if atts:
       for att,val in atts.iteritems():
           self.atts[att] = val

    if geom:
       self.geom = geom
       
  def __str__(self):
    return '%s; %s' % (str(self.atts),str(self.geom))

  def set(self,att,value):
     self.atts[att] = value

  def get(self,att):
     if self.atts.has_key(att): 
        return self.atts[att]

  def _sync(self):
     if not self.f:
       b = SimpleFeatureBuilder(self.type.ft) 
       self.f = b.buildFeature(None,[])

     for att, val in self.atts.iteritems(): 
        self.f.setAttribute(att,val)

     self.f.setDefaultGeometry(self.geom)
 
