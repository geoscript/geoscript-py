"""
workspace.mysql module -- MySQL implementation of Workspace
"""

import os
from geoscript.workspace import Workspace
from org.geotools.data.mysql import MySQLDataStoreFactory

class MySQLWorkspace(Workspace):

  def __init__(self, db, host='localhost', port=3306, user=os.environ['USER'], 
               passwd=None):

    params = {'host': host, 'port': port, 'database': db,
              'user':user, 'passwd': passwd, 'dbtype': 'mysql'}
    fac = MySQLDataStoreFactory()
    ds = fac.createDataStore(params)
    
    Workspace.__init__(self, ds)

