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
  """

  def __init__(self, schema=None):
    if not schema:
      schema = feature.Schema('layer', [('geom', geom.Geometry)])

    ds = MemoryDataStore(schema.ft)
    Layer.__init__(self,ds.getFeatureSource(name))
