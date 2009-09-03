"""
layer/postgis module -- Postgis implementation of Layer.

A postgis layer is created by specifying a table name and database name:

   pg = PostgisLayer('myTable', 'myDatabase)

The host, port, schema, user, and passwd parameters all have default values but
can be specified with named parameters:

   pg = PostgisLayer('myTable', 'myDatabase', host='192.168.10.1', port=2345, 
                     schema='nonpublic', user='jdoe', passwd='secret') 

"""

import os
from geoscript.layer import Layer
from org.geotools.data.postgis import PostgisDataStoreFactory

class PostgisLayer(Layer):

  def __init__(self, table, db, host='localhost', port=5432, schema='public', 
               user=os.environ['USER'], passwd=None):

    params = {'host': host, 'port': port, 'schema': schema, 'database': db,
              'user':user, 'passwd': passwd, 'dbtype': 'postgis'}
    pgf = PostgisDataStoreFactory()
    pg = pgf.createDataStore(params)
    
    fs = pg.getFeatureSource(table)
    Layer.__init__(self, fs)
