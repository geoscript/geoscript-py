"""
workspace.h2 module -- H2 implementation of Workspace.
"""

import os
from geoscript.workspace import Workspace
from geoscript.layer import H2Layer
from org.geotools.data.h2 import H2DataStoreFactory

class H2Workspace(Workspace):

  def __init__(self, db, dir=None):

    if dir:
      db = os.path.join(dir, db)

    params = {'database': db, 'dbtype': 'h2'}
    h2f = H2DataStoreFactory()
    h2 = h2f.createDataStore(params)

    Workspace.__init__(self, h2)

  def get(self, name):
    l = Workspace.get(self, name)
    if l:
      return H2Layer(None, None, l.fs)

  def add(self, layer, name=None):
    l = Workspace.add(self, layer, name)
    if not l.proj:
      l.proj = layer.proj

    return l
