"""
The :mod:`layer.postgis` module provides support for Postgis table access.
"""

import os
from geoscript.layer import Layer
from org.geotools.data.postgis import PostgisNGDataStoreFactory

class PostgisLayer(Layer):
  """
  A subclass of :class:`geoscript.layer.layer.Layer` for Postgis.

  A Postgis layer is created by specifying the *table* name and database connection parameters.
  """

  def __init__(self, table, db, host='localhost', port=5432, schema='public', 
               user=os.environ['USER'], passwd=None):

    params = {'host': host, 'port': port, 'schema': schema, 'database': db,
              'user':user, 'passwd': passwd, 'dbtype': 'postgis'}
    pgf = PostgisNGDataStoreFactory()
    pg = pgf.createDataStore(params)
    
    fs = pg.getFeatureSource(table)
    Layer.__init__(self, fs)
