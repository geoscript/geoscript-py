"""
workspace.spatialite module -- SpatiaLite implementation of Workspace.
"""

import os
from geoscript.workspace import Workspace
from org.geotools.data.spatialite import SpatiaLiteDataStoreFactory

class SpatiaLiteWorkspace(Workspace):

  def __init__(self, db, dir=None):

    if dir:
      db = os.path.join(dir, db)

    params = {'database': db, 'dbtype': 'spatialite'}
    slf = SpatiaLiteDataStoreFactory()
    sl = slf.createDataStore(params)

    Workspace.__init__(self, sl)
