"""
The :mod:`workspace.mysql` module a workspace implementation based on the contents of a MySQL database.
"""

from java.lang.System import getProperty as sysprop
from geoscript.workspace import Workspace
from org.geotools.data.mysql import MySQLDataStoreFactory

class MySQL(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` for a MySQL database. Layers of the workspace correspond to tables in the database.

  *db* is the name of the database.

  *host* is the optional host name. Defaults to 'localhost'.

  *port* is the optional port the database is listening on as an ``int``. Defaults to 3306.

  *user* is the optional username to connect as. Defaults to the current user.

  *passwd* is the optional password to connect with.

  """
  def __init__(self, db, host='localhost', port=3306, user=sysprop('user.name'),
               passwd=None):

    params = {'host': host, 'port': port, 'database': db,
              'user':user, 'passwd': passwd, 'dbtype': 'mysql'}
    Workspace.__init__(self, MySQLDataStoreFactory(), params)

