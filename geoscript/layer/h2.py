"""
layer.h2 module -- H2 implementation of Layer.
"""

from geoscript.layer import Layer
from org.geotools.data.h2 import H2DataStoreFactory

class H2Layer(Layer):

  def __init__(self, table, db):

    params = {'database': db, 'dbtype': 'h2'}
    h2f = H2DataStoreFactory()
    h2 = h2f.createDataStore(params)
    
    fs = h2.getFeatureSource(table)
    Layer.__init__(self, fs)
