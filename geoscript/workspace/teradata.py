import os
from geoscript.workspace import Workspace
from org.geotools.data.teradata import TeradataDataStoreFactory

class Teradata(Workspace):
  def __init__(self, db, host='localhost', port=1025, user=None, passwd=None):

    user = user if user else db
    params = {'host': host, 'port': port, 'database': db, 'user':user, 
              'passwd': passwd, 'estimatedBounds': True, 'dbtype': 'teradata'} 
    
    Workspace.__init__(self, TeradataDataStoreFactory(), params)
