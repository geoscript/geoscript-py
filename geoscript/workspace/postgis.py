"""
The :mod:`workspace.postgis` module a workspace implementation based on the contents of a PostGIS database.
"""
from java.lang.System import getProperty as sysprop
from geoscript.workspace import Workspace
from org.geotools.data.postgis import PostgisNGDataStoreFactory

class PostGIS(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` for a PostGIS database. Layers of the workspace correspond to tables in the database.

  *db* is the name of the database.

  *host* is the optional host name. Defaults to 'localhost'.

  *port* is the optional port the database is listening on as an ``int``. Defaults to 5432.

  *schema* is the optional database schema to connect to. Defaults to 'public'.

  *user* is the optional username to connect as. Defaults to the current user.

  *passwd* is the optional password to connect with.

  *estimated_extent* is an optional flag that controls whether to use the PostGIS 
  ``estimated_extent`` function when calculating bounds.

  *fetch_size* is the optional size of cursor result sets fetched from the 
  server. The default value is 2000.
  """

  def __init__(self, db, host='localhost', port=5432, schema='public', 
               user=sysprop('user.name'), passwd=None, estimated_extent=False,
               fetch_size=2000):

    params = {'host': host, 'port': port, 'schema': schema, 'database': db,
              'user':user, 'passwd': passwd, 'dbtype': 'postgis', 
              'Estimated extends': estimated_extent, 'fetch size': fetch_size}
    
    Workspace.__init__(self, PostgisNGDataStoreFactory(), params)
