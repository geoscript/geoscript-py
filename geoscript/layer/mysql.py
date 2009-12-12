"""
The :mod:`layer.mysql` module provides support for MySQL table access.
"""

import os
from geoscript.layer import Layer
from org.geotools.data.mysql import MySQLDataStoreFactory

class MySQLLayer(Layer):
  """
  A subclass of :class:`geoscript.layer.layer.Layer` for MySQL.

  A MySQL layer is created by specifying the *table* name and database connection parameters.
  """

  def __init__(self, table, db, host='localhost', port=3306,  
               user=os.environ['USER'], passwd=None, fs=None):

    if not fs:
      params = {'host': host, 'port': port, 'database': db,
              'user':user, 'passwd': passwd, 'dbtype': 'mysql'}
      fac = MySQLDataStoreFactory()
      ds = fac.createDataStore(params)
    
      fs = ds.getFeatureSource(table)

    Layer.__init__(self, fs)

  def _newLayer(self, schema, **options):

    pg = self.fs.dataStore
    pg.createSchema(schema.ft) 
    return MySQLLayer(None, None, fs=pg.getFeatureSource(schema.name)) 
