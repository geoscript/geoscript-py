"""
workspace module -- Provides data access and manipulation of collections of 
layers.
"""

from geoscript.layer import Layer
from geoscript import geom, feature

class Workspace:
  """
  A workspace is a collection of layers.
  """

  def __init__(self, ds=None):
    if self.__class__ == Workspace and not ds:
      import memory
      mem = memory.Memory()
      self.ds = mem.ds
    else :
      if not ds:
        raise Exception('Workspace requires a data store.')

      self.ds = ds

  def getformat(self):
    # first see if the datastore has a ref to its factory
    ds = self.ds
    try:
      return str(ds.dataStoreFactory.displayName)
    except AttributeError:
      # no factory, resort to heuristic of using data store type name
      return type(ds).__name__[:-9]

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
    ['foo', 'bar']
    """

    return [str(tn) for tn in self.ds.typeNames]

  def get(self, name):
    """
    Returns a layer in the workspace.

    >>> ws = Workspace()
    >>> l = ws.get('foo')
    >>> str(l)
    'None'
    >>> x = ws.create('foo')
    >>> l = ws.get('foo') 
    >>> str(l.name)
    'foo'

    This method returns None if no such layer is defined.
    """

    if name in self.layers():
       fs = self.ds.getFeatureSource(name)
       return Layer(workspace=self, fs=fs)
  
    return None

  def create(self, name=None, fields=[('geom', geom.Geometry)], schema=None):
     """
     Creates a new layer in the workspace.
   
     >>> from geoscript import geom
     >>> ws = Workspace()
     >>> l = ws.create('foo', [('geom', geom.Point)])
     >>> ws.layers()
     ['foo']
     """
 
     if not name:
       name = schema.name if schema else Layer._newname()

     if self.get(name):
       raise Exception('Layer %s already exists.' % (name))

     schema = schema or feature.Schema(name, fields)
     self.ds.createSchema(schema.ft) 
     return self.get(name)

  def add(self, layer, name=None):
     """
     Adds an existing layer to the workspace.
    
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
     l = self.get(name)
     if not l:
       if layer.proj:
         flds = []
         for fld in layer.schema.fields:
           flds.append((fld.name, fld.typ, layer.proj) if issubclass(fld.typ, geom.Geometry) else (fld.name, fld.typ))
       else:
         flds = [(fld.name, fld.typ) for fld in layer.schema.fields]
       l = self.create(name, flds)
     
     for f in layer.features():
       l.add(f)

     return l

  def _format(self, layer):
    return self.format
