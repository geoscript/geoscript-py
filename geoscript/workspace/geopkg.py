"""
The :mod:`workspace.geopkg` module a workspace implementation based on the contents of a GeoPackage database.
"""

import os
from geoscript.workspace import Workspace
from org.geotools.geopkg import GeoPkgDataStoreFactory

class GeoPackage(Workspace):
  def __init__(self, db, dir=None):

    if dir:
      db = os.path.join(dir, db)

    params = {'database': db, 'dbtype': 'geopkg'}
    Workspace.__init__(self, GeoPkgDataStoreFactory(), params)

