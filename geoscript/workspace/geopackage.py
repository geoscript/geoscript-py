"""
The :mod:`workspace.geopackage` module a workspace implementation based on the contents of a GeoPackage database.
"""
from geoscript import util
from java.lang.System import getProperty as sysprop
from geoscript.workspace import Workspace
from org.geotools.geopkg import GeoPkgDataStoreFactory

class GeoPackage(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` for a GeoPackage database. Layers of the workspace correspond to tables in the database.

  *db* is the database file.

  *user* is the optional username to connect as.

  *passwd* is the optional password to connect with.

  """

  def __init__(self, db, user=None, passwd=None):

    params = {'database': db, 'user':user, 'passwd': passwd, 'dbtype': 'geopkg'}
    
    Workspace.__init__(self, GeoPkgDataStoreFactory(), params)

