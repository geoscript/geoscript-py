"""
workspace.postgis module -- Postgis implementation of Workspace
"""

import os
from geoscript.workspace import Workspace
from org.geotools.data.postgis import PostgisNGDataStoreFactory

class PostGIS(Workspace):

  def __init__(self, db, host='localhost', port=5432, schema='public', 
               user=os.environ['USER'], passwd=None):

    params = {'host': host, 'port': port, 'schema': schema, 'database': db,
              'user':user, 'passwd': passwd, 'dbtype': 'postgis'}
    pgf = PostgisNGDataStoreFactory()
    pg = pgf.createDataStore(params)
    
    Workspace.__init__(self, pg)
