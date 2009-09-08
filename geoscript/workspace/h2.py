"""
workspace.h2 module -- H2 implementation of Workspace.
"""

import os
from geoscript.workspace import Workspace
from org.geotools.data.h2 import H2DataStoreFactory

class H2Workspace(Workspace):

  def __init__(self, db, dir=None):

    if dir:
      db = os.path.join(dir, db)

    params = {'database': db, 'dbtype': 'h2'}
    h2f = H2DataStoreFactory()
    h2 = h2f.createDataStore(params)

    Workspace.__init__(self, h2)
