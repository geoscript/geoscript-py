"""
The :mod:`workspace.db` module provides a base class for database workspaces.
"""

from geoscript.workspace import Workspace
from  org.geotools.jdbc import VirtualTable, VirtualTableParameter

class DB(Workspace):
  """
  A DB workspace is a workspace backed by a relational database.
  """

  def __init__(self, factory=None, params=None, ds=None):
    Workspace.__init__(self, factory, params, ds);

  def createView(self, name, sql, params=[]):
    """
    Creates a new layer from an SQL query. 

    *name* is the name to assign to the new layer.

    *sql* is the SQL defining the layer. The sql can contain placeholders that 
    are dynamically substituted when a query is preformed on the layer. The 
    syntax is "%<p>%" where ``p`` is the name of the parameter. Each parameter 
    must also be defined in the *params* argument.

    *params* is a ``list`` of all substitutable parameters in the *sql* argument. 
    List values can be either:

      1. A ``str`` - the name of the parameter
      2. A ``tuple`` of two strings, the first being the name of the parameter 
         and the second being the default value of the parameter.
    
    Example::

        l = db.createView("state", 
            "SELECT * FROM states WHERE state_abbr = '%abbr%'", 
            [('abbr', 'TX')])
        l.features(params={'abbr': 'NY'})

    See http://docs.geoserver.org/stable/en/user/data/database/sqlview.html
    """
    vt = VirtualTable(name, sql)
    for p in params:
      if isinstance(p, (str,unicode)):
        vt.addParameter(VirtualTableParameter(p, None))
      elif isinstance(p, (list,tuple)):
        vt.addParameter(VirtualTableParameter(*p))

    self._store.addVirtualTable(vt)
    return self.get(name)

  def deleteView(self, name):
    """
    Deletes a layer previously created with ``createView``. 

    *name* is the name of the view/layer.
    """
    self._store.removeVirtualTable(name)
