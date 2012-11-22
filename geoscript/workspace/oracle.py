"""
The :mod:`workspace.oracle` module a workspace implementation based on the contents of a Oracle database.
"""
from java.lang.System import getProperty as sysprop
from geoscript.workspace import Workspace
from org.geotools.data.oracle import OracleNGDataStoreFactory

class Oracle(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` for a Oracle database. Layers of the workspace correspond to tables in the database.

  *db* is the name of the database.

  *host* is the optional host name. Defaults to 'localhost'.

  *port* is the optional port the database is listening on as an ``int``. Defaults to 1521.

  *schema* is the optional database schema to connect to. If not specified 
  defaults to the same value as *value*

  *user* is the optional username to connect as. Defaults to the current user.

  *passwd* is the optional password to connect with.

  *estimated_extent* is an optional flag that controls whether to use the PostGIS 
  ``estimated_extent`` function when calculating bounds.

  """

  def __init__(self, db, host='localhost', port=1521, schema=None,
               user=sysprop('user.name'), passwd=None, estimated_extent=False):

    if schema is None:
      schema = user

    params = {'host': host, 'port': port, 'schema': schema, 'database': db,
              'user':user, 'passwd': passwd, 'dbtype': 'oracle', 
              'Estimated extends': estimated_extent}
    
    Workspace.__init__(self, OracleNGDataStoreFactory(), params)
