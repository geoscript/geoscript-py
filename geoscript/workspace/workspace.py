"""
The :mod:`workspace.workspace` module provides layer access and manipulation.
"""

from org.geotools.data import DataStore
from geoscript.layer import Layer
from geoscript.filter import Filter
from geoscript.util.data import readFeatures
from geoscript import core, geom, feature

class Workspace:
  """
  A workspace is a container of layers.
  """

  def __init__(self, factory=None, params=None, ds=None):
    if self.__class__ == Workspace and not factory and not ds:
      import memory
      mem = memory.Memory()
      self._store = mem._store
    else :
      if ds:
        self._store = ds
      elif factory:
        self._store = factory.createDataStore(params)
      else: 
        raise Exception('Workspace requires a data store or a factory')

      self.factory = factory
      self.params = params

  def getformat(self):
    try:
      return self.factory.displayName
    except AttributeError:
      return type(self._store).__name__[:-9]

  format = property(getformat)
  """
  A ``str`` identifying the format of the workspace.
  """

  def layers(self):
    """
    The names of all the layers in the workspace.

    >>> ws = Workspace()
    >>> l1 = ws.create('foo')
    >>> l2 = ws.create('bar')
    >>> ws.layers()
    ['bar', 'foo']
    """

    return [str(tn) for tn in self._store.typeNames]

  def get(self, name):
    """
    Returns a :class:`Layer geoscript.layer.layer.Layer` in the workspace. This method raised ``KeyError`` if the layer does not exist.

    *name* is the name of a layer to return.

    >>> ws = Workspace()
    >>> try:
    ...   ws.get('foo') 
    ...   raise Exception('Should not get here')
    ... except KeyError:
    ...   pass
    >>> x = ws.create('foo')
    >>> l = ws.get('foo') 
    >>> str(l.name)
    'foo'

    """

    if name in self.layers():
       fs = self._store.getFeatureSource(name)
       return Layer(workspace=self, source=fs)
  
    raise KeyError('No such layer "%s"' % name)

  def create(self, name=None, fields=[('geom', geom.Geometry,'epsg:4326')], schema=None):
     """
     Creates a new :class:`Layer geoscript.layer.layer.Layer` in the workspace.
   
     *name* is the optional name to assign to the new layer.

     *fields* is an optional ``list`` of ``str``/``type`` tuples which define th e schema of the new layer.

     *schema* is the optional :class:`Schema <geoscript.feature.Schema>` of the new layer.

     **Note**: When the *schema* argument is specified neither of *name* or *fields* should be specified.

     >>> from geoscript import geom
     >>> ws = Workspace()
     >>> l1 = ws.create('foo', [('geom', geom.Point)])
     >>> ws.layers()
     ['foo']

     >>> from geoscript.feature import Schema
     >>> l2 = ws.create(schema=Schema('bar', [('geom', geom.Point)]))
     >>> ws.layers()
     ['bar', 'foo']
     """
 
     if not name:
       name = schema.name if schema else Layer._newname()

     if schema:
       schema = feature.Schema(name, schema.fields)

     try:
       self.get(name)
       raise Exception('Layer %s already exists.' % (name))
     except KeyError:
       pass

     schema = schema or feature.Schema(name, fields)
     self._store.createSchema(schema._type) 
     return self.get(name)

  def remove(self, name):
    """
    Removes a layer from the workspace.

    *name* is the name of the layer to remove.

    Note: This method is not supported by all geotools stores and may throw an exception.
    """
    self._store.removeSchema(name)

  def add(self, layer, name=None, chunk=1000):
     """
     Adds an existing layer to the workspace.
    
     *layer* is the :class:`Layer <geoscript.layer.layer.Layer>` to add.

     *name* is the optional name as a ``str`` to assign to the layer when copied into the workspace.

     >>> ws = Workspace()
     >>> ws.layers()
     []
     >>> from geoscript.layer import Layer
     >>> l = Layer('foo')
     >>> l = ws.add(l)
     >>> ws.layers()
     ['foo']
     """

     name = name if name else layer.name
     try:
       self.get(name)
       raise Exception('Layer named "%s" already exists.' % name)
     except KeyError:
       if layer.proj:
         flds = []
         for fld in layer.schema.fields:
           flds.append((fld.name, fld.typ, layer.proj) if issubclass(fld.typ, geom.Geometry) else (fld.name, fld.typ))
       else:
         flds = [(fld.name, fld.typ) for fld in layer.schema.fields]

       l = self.create(name, flds)

       # add all the features
       it = layer._source.getFeatures().features()
       try:
         while True:
           features = readFeatures(it, layer._source.getSchema(), chunk)
           if features.isEmpty():
             break

           l._source.addFeatures(features)

         return l
       finally:
         it.close()

  def close(self):
    """
    Closes the workspace disposing of any resources being consumed. Generally
    this method should always be closed when the workspace is no longer needed.
    """
    self._store.dispose()

  def _format(self, layer):
    return self.format

  def __getitem__(self, key):
     return self.get(key)

  def __setitem__(self, key, val):
     try:
       self.get(key) 

       #todo: drop the existing schema and create a new one
       raise Exception('%s already exists' % key) 
     except KeyError:
       if isinstance(val, list):
         self.create(key, fields=val)
       elif isinstance(val, feature.Schema):
         self.create(key, schema=val)
       else: 
         self.add(val)

  def __iter__(self):
    return self.layers().__iter__()

  def iterkeys(self):
    return self.__iter__()

  def iteritems(self):
    for l in self.layers():
       yield (l, self.get(l)) 

  def keys(self):
    return self.layers()

  def values(self):
    return [v for k,v in self.iteritems()]

core.registerTypeMapping(DataStore, Workspace, lambda x: Workspace(ds=x))
core.registerTypeUnmapping(Workspace, DataStore, lambda x: x._store)
