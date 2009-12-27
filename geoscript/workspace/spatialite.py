"""
workspace.spatialite module -- SpatiaLite implementation of Workspace.
"""

import os
from geoscript.workspace import Workspace
from geoscript.layer import SpatiaLiteLayer
from org.geotools.data.spatialite import SpatiaLiteDataStoreFactory

class SpatiaLiteWorkspace(Workspace):

  def __init__(self, db, dir=None):

    if dir:
      db = os.path.join(dir, db)

    params = {'database': db, 'dbtype': 'spatialite'}
    slf = SpatiaLiteDataStoreFactory()
    sl = slf.createDataStore(params)

    Workspace.__init__(self, sl)

  def layer(self, name):
    l = Workspace.get(self, name)
    if l:
      return SpatiaLiteLayer(None, None, l.fs)

  def add(self, layer, name=None):
    l = Workspace.add(self, layer, name)
    if not l.proj:
      l.proj = layer.proj

    return l
