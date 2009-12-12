"""
The :mod:`layer.spatialite` module provides support for SpatiaLite table access.
"""

from geoscript import geom, feature
from geoscript.layer import Layer
from org.geotools.data.spatialite import SpatiaLiteDataStoreFactory

class SpatiaLiteLayer(Layer):
  """
  A subclass of :class:`geoscript.layer.layer.Layer` for SpatiaLite.

  A SpatiaLite layer is created by specifying a *table* name and a *database* name.
  """

  def __init__(self, table, database, fs=None):

    if not fs:
      params = {'database': database, 'dbtype': 'spatialite'}
      slf = SpatiaLiteDataStoreFactory()
      sl = slf.createDataStore(params)
    
      fs = sl.getFeatureSource(table)
    
    Layer.__init__(self, fs)

  def _newLayer(self, schema, **options):

    sl = self.fs.dataStore
    sl.createSchema(schema.ft) 
    return SpatiaLiteLayer(None, None, sl.getFeatureSource(schema.name)) 
