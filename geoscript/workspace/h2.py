"""
The :mod:`workspace.h2` module a workspace implementation based on the contents of a H2 database.
"""

import os
from geoscript.workspace import Workspace
from org.geotools.data.h2 import H2DataStoreFactory
from org.h2.tools import Server

class H2(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` for an H2 database. 

  *db* is the name of the database.

  *dir* is the optional path to a directory containing the H2 database.

  If the underlying H2 database does not exist it will be created.
  """

  def __init__(self, db, dir=None):

    if dir:
      db = os.path.join(dir, db)

    params = {'database': db, 'dbtype': 'h2'}
    Workspace.__init__(self, H2DataStoreFactory(), params)

  def server(self):
    s = Server()
    s.run([])
    return s
