"""
The :mod:`layer.layer` module provides the classes for data access and manipulation.
"""
import sys
from java import io
from java import net
from cursor import Cursor
from geoscript import geom, proj, feature
from geoscript.filter import Filter
from org.geotools.data import DefaultQuery, Query, Transaction
from org.geotools.feature import FeatureCollections

class Layer(object):
  """
  A source of spatial data.
  """

  _id = -1
  """
  Internal counter for generating layer names
  """

  def __init__(self, name=None, workspace=None, fs=None, schema=None):
    if not workspace:
       from geoscript.workspace import Memory
       workspace = Memory()
 
    name = name or Layer._newname()
       
    if not fs:
       layer = None
       try:
         layer = workspace.get(name)
       except KeyError:
         pass
        
       if not layer:
         if schema:
           layer = workspace.create(schema.name, schema.fields)
         else:
           layer = workspace.create(name)

       fs = layer.fs

    self.workspace = workspace
    self.schema = schema or feature.Schema(ft=fs.schema) 
    self.fs = fs

    # keep a crs local to allow the native crs to be overriden, or to 
    # provide a crs for layers that don't have one specified
    self._proj = None

  def getformat(self):
    return self.workspace._format(self)

  format = property(getformat)
  """
  A ``str`` identifying the format of the layer.
  """

  def getname(self):
    return self.fs.name.localPart

  name = property(getname)
  """
  The name of the layer as a ``str``.
  """

  def getproj(self):
    if self._proj:
      return self._proj
    else:
      crs = self.fs.schema.coordinateReferenceSystem
      if crs:
        return proj.Projection(crs)

  def setproj(self, value):
    self._proj = proj.Projection(value) 

  proj = property(getproj, setproj)
  """
  The :class:`Projection <geoscript.proj.Projection>` of the layer. In cases where the projection of a layer is 
  unknown this attribute has the value ``None``.

  >>> import proj
  >>> l = Layer()
  >>> l.proj
  None
  >>> l.proj = proj.Projection('epsg:4326')
  >>> l.proj.id
  EPSG:4326
  """
  
  def count(self, filter=None):
    """
    The number of features in the layer as an ``int``.

    *filter* is an optional :class:`Filter <geoscript.filter.Filter>` to constrains the counted set of features.

    >>> l = Layer()
    >>> l.count()
    0
    >>> from geoscript import geom
    >>> l.add([geom.Point(1,2)])
    >>> l.add([geom.Point(3,4)])
    >>> l.count() 
    2
    >>> l.count('INTERSECTS(geom,POINT(3 4))')
    1
    """

    f = Filter(filter) if filter else Filter.PASS
    count = self.fs.getCount(DefaultQuery(self.name, f._filter))
    if count == -1:
      count = 0
      # calculate manually 
      for f in self.features(filter):
        count += 1

    return count

  def bounds(self, filter=None):
    """
    The :class:`Bounds <geoscript.geom.Bounds>` of the layer.

    *filter* is an optional :class:`Filter <geoscript.filter.Filter>` to constrains the returned bounds.

    >>> l = Layer()
    >>> from geoscript import geom 
    >>> l.add([geom.Point(1.0, 2.0)])
    >>> l.add([geom.Point(3.0, 4.0)])

    >>> l.bounds()
    (1.0, 2.0, 3.0, 4.0)

    >>> l.bounds('INTERSECTS(geom,POINT(3 4))')
    (3.0, 4.0, 3.0, 4.0)
    """

    f = Filter(filter) if filter else Filter.PASS
    e = self.fs.getBounds(DefaultQuery(self.name, f._filter))
    if e:
      return geom.Bounds(env=e)

  def features(self, filter=None, transform=None):
    """
    Generator over the :class:`Feature <geoscript.feature.Feature>` s of the layer.

    *filter* is a optional :class:`Filter <geoscript.filter.Filter>` to constrain the features iterated over.

    *transform* is an optional function to be executed to transform the features being iterated over. This 
    function takes a single argument which is a :class:`Feature <geoscript.feature.Feature>` and returns a 
    (possibly different) feature.

    >>> l = Layer()
    >>> from geoscript import geom
    >>> l.add([geom.Point(1,2)])
    >>> l.add([geom.Point(3,4)])
    >>> [ str(f.geom) for f in l.features() ]
    ['POINT (1 2)', 'POINT (3 4)']

    >>> [ str(f.geom) for f in l.features('INTERSECTS(geom,POINT(3 4))') ]
    ['POINT (3 4)']

    >>> def tx (f):
    ...    f.geom = geom.Point(2*f.geom.x, 2*f.geom.y)
    >>> [str(f.geom) for f in l.features(transform=tx)]
    ['POINT (2 4)', 'POINT (6 8)']
    """
    c = self.cursor(filter)
    for f in c:
      if transform:
         result  = transform(f)
         if result and isinstance(result, Feature):
           f = result

      yield f

    c.close()

  def cursor(self, filter=None):
    """
    Returns a :class:`Cursor <geoscript.layer.cursor.Cursor>` over the features of the layer.

    *filter* is a optional :class:`Filter <geoscript.filter.Filter>` to constrain the features iterated over.

    >>> l = Layer()
    >>> from geoscript import geom
    >>> l.add([geom.Point(1,2)])
    >>> l.add([geom.Point(3,4)])
    >>> l.add([geom.Point(5,6)])
    >>> l.add([geom.Point(7,8)])
    >>> l.add([geom.Point(9,10)])
    >>> c = l.cursor()
    >>> f = c.next() 
    >>> f.geom
    POINT (1 2)
    >>> f = c.next() 
    >>> f.geom
    POINT (3 4)
    >>> features = c.read(2)
    >>> len(features)
    2
    >>> features[0].geom
    POINT (5 6)
    >>> features[1].geom
    POINT (7 8)
    >>> features = c.read(2)
    >>> len(features)
    1
    >>> features[0].geom
    POINT (9 10)
    >>> c.close()
    """

    f = Filter(filter) if filter else Filter.PASS
    q = DefaultQuery(self.name, f._filter)
    if self.proj:
      q.coordinateSystem = self.proj._crs

    r = self.fs.dataStore.getFeatureReader(q,Transaction.AUTO_COMMIT)
    return Cursor(r, self)

  def delete(self, filter):
    """
    Deletes features from the layer which match the specified constraint.

    *filter* is a :class:`Filter <geoscript.filter.Filter>` that specifies which features are to be deleted.

    >>> l = Layer()
    >>> from geoscript import geom
    >>> l.add([geom.Point(1,2)])
    >>> l.add([geom.Point(3,4)])
    >>> l.count()
    2
    >>> l.delete('INTERSECTS(geom, POINT(3 4))')
    >>> l.count()
    1
    """

    f = Filter(filter) if filter else Filter.FAIL
    self.fs.removeFeatures(f._filter)

  def add(self, o):
    """
    Adds a :class:`Feature <geoscript.feature.Feature>` to the layer.

    *o* is the feature to add. It may be specified directly as a Feature object or alternatively as a ``dict`` 
    or a ``list``.

    >>> from geoscript import geom
    >>> from geoscript import feature
    >>> l = Layer() 
    >>> l.count()
    0
    >>> f = feature.Feature({'geom': geom.Point(1,2)})
    >>> l.add(f)
    >>> l.count()
    1
    >>> l = Layer()
    >>> l.add({'geom': geom.Point(1,2)})
    >>> l.add([geom.Point(1,2)])
    >>> l.count()
    2
    """
    if isinstance(o, feature.Feature):
      f = o
      if not f.schema:
        f.schema = self.schema
    elif isinstance(o, (dict,list)):
      f = self.schema.feature(o)
      
    fc = FeatureCollections.newCollection() 
    fc.add(f.f)
    self.fs.addFeatures(fc)

  def reproject(self, prj, name=None):
    """
    Reprojects a layer.

    *prj* is the destination :class:`Projection <geoscript.proj.Projection>` 

    *name* is the optional name as a ``str`` to assign to the resulting reprojected layer.

    This method returns a newly reprojected layer. The new layer is create within the containing workspace of the original layer.

    >>> from geoscript import geom
    >>> l = Layer()
    >>> l.proj = 'epsg:4326'
    >>> l.add([geom.Point(-111, 45.7)])
    >>> 
    >>> l2 = l.reproject('epsg:26912')
    >>> l2.proj.id
    'EPSG:26912'

    >>> [f.geom for f in l2.features()]
    [POINT (499999.42501775385 5060716.092032814)]
    """

    prj = proj.Projection(prj)
    name = name or Layer._newname()

    # reproject the schema
    rschema = self.schema.reproject(prj, name)

    # create the reprojected layer
    rlayer = self.workspace.create(schema=rschema)

    # create a query specifying that feautres should be reproje`cted
    q = DefaultQuery(self.name, Filter.PASS._filter)
    if self.proj:
      q.coordinateSystem = self.proj._crs
    q.coordinateSystemReproject = prj._crs 

    fc = self.fs.getFeatures(q)
    i = fc.features()

    # loop through features and add to new reprojeced layer
    while i.hasNext():
      f = feature.Feature(schema=rschema, f=i.next())
      rlayer.add(f)
    
    fc.close(i)
    return rlayer

  def toGML(self,out=sys.stdout):
    try:
      from net.opengis.wfs import WfsFactory
      from org.geotools.wfs.v1_1 import WFS, WFSConfiguration
      from org.geotools.xml import Encoder
    except ImportError:
      raise Exception('toGML() not available, GML libraries not on classpath.') 

    features = self.fs.features
    fc = WfsFactory.eINSTANCE.createFeatureCollectionType()
    fc.feature.add(features)

    e = Encoder(WFSConfiguration())        
    uri = self.fs.name.namespaceURI
    prefix = 'gt'
    e.namespaces.declarePrefix(prefix,uri)
    e.indenting = True
    e.encode(fc, WFS.FeatureCollection, out)

  def toJSON(self,out=sys.stdout):
    try:
      from org.geotools.geojson import GeoJSONWriter
    except ImportError:
      raise Exception('toJSON() not available, GeoJSON libraries not on classpath.')
    else:
      features = self.fs.features
      w = GeoJSONWriter() 
      w.write(features,out)

  @staticmethod
  def _newname():
    Layer._id  += 1
    return 'layer_%d' % Layer._id
