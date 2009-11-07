"""
The :mod:`layer.h2` module provides support for H2 table access.
"""

from geoscript import geom, feature
from geoscript.layer import Layer
from org.geotools.data.h2 import H2DataStoreFactory

class H2Layer(Layer):
  """
  A subclass of :class:`geoscript.layer.layer.Layer` for H2.

  A H2 layer is created by specifying a *table* name and a *database* name.
  """

  def __init__(self, table, database):

    params = {'database': database, 'dbtype': 'h2'}
    h2f = H2DataStoreFactory()
    h2 = h2f.createDataStore(params)
    
    fs = h2.getFeatureSource(table)
    Layer.__init__(self, fs)

  def add(self, o):
    # h2 requires crs to be set in geometry user data
    if self.crs: 
      if isinstance(o, feature.Feature):
        o.geom().userData = self.crs
      elif isinstance(o, list):
        for att,val in o:
          if isinstnace(val, geom.Geometry):
            val.userData = self.crs

    Layer.add(self,o)
