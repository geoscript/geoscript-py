"""
The :mod:`workspace.workspace` module provides layer access and manipulation.
"""

from geoscript.layer import Layer
from geoscript import geom, feature

class Workspace:
  """
  A workspace is a container of layers.
  """

  def __init__(self, factory=None, params=None):
    if self.__class__ == Workspace and not factory:
      import memory
      mem = memory.Memory()
      self.ds = mem.ds
    else :
      if not factory:
        raise Exception('Workspace requires a data store factory.')

      self.factory = factory
      self.params = params
      self.ds = factory.createDataStore(params)

  def getformat(self):
    try:
      return self.factory.displayName
    except AttributeError:
      return type(self.ds).__name__[:-9]

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
       fs = self.ds.getFeatureSource(name)
       return Layer(workspace=self, fs=fs)
  
    raise KeyError('No such layer "%s"' % name)

  def create(self, name=None, fields=[('geom', geom.Geometry)], schema=None):
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
     ['foo', 'bar']
     """
 
     if not name:
       name = schema.name if schema else Layer._newname()

     try:
       self.get(name)
       raise Exception('Layer %s already exists.' % (name))
     except KeyError:
       pass

     schema = schema or feature.Schema(name, fields)
     self.ds.createSchema(schema.ft) 
     return self.get(name)

  def add(self, layer, name=None):
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
       for f in layer.features():
         l.add(f)

       return l

  def _format(self, layer):
    return self.format
