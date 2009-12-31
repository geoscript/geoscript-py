"""
The :mod:`workspace.spatialite` module a workspace implementation based on the contents of a SpatiaLite database.
"""

import os
from geoscript.workspace import Workspace
from org.geotools.data.spatialite import SpatiaLiteDataStoreFactory

class SpatiaLite(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` for a SpatiaLite database. Layers of the workspace correspond to tables in the database.

  *db* is the name of the database.

  *dir* is the optional path to a directory containing the SpatiaLite database.

  If the underlying SpatiaLite database does not exist it will be created.

  """

  def __init__(self, db, dir=None):

    if dir:
      db = os.path.join(dir, db)

    params = {'database': db, 'dbtype': 'spatialite'}
    slf = SpatiaLiteDataStoreFactory()
    sl = slf.createDataStore(params)

    Workspace.__init__(self, sl)
