"""
The :mod:`layer.memory` module provides support for in memory data access.
"""

from geoscript.layer import Layer
from geoscript import geom, feature
from org.geotools.data.memory import MemoryDataStore

class MemoryLayer(Layer):
  """
  A subclass of :class:`geoscript.layer.layer.Layer` for in memory data access.

  A memory layer is created by specifying a :class:`geoscript.feature.Schema`. If the *schema* is omitted the layer is created with the schema::

     layer [geom: Geometry]

  Or alternatively just a *name* may be specified.
  """

  def __init__(self, schema=None, name=None):
    if not schema:
      if not name:
        name = 'layer'
      schema = feature.Schema(name, [('geom', geom.Geometry)])

    ds = MemoryDataStore(schema.ft)
    Layer.__init__(self,ds.getFeatureSource(name))
