"""
the :mod:`workspace.directory` module provides a workspace implemntation based on the contents of a directory on a file system.
"""

import os
from java import io, net
from geoscript import util
from geoscript.workspace import Workspace
from org.geotools.data.shapefile import ShapefileDataStoreFactory

class Directory(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` that provides layers that correspond to the files in a directory.

  *dir* is the optional path as a ``str`` to a directory. If not specified it defaults to ``os.getcwd()``.
  """

  def __init__(self, dir=None):
    dir = dir or os.getcwd()
    params = {'url': util.toURL(dir)}
    Workspace.__init__(self, ShapefileDataStoreFactory(), params)

  def _format(self, layer):
    f = type(self._store.getDataStore(layer.name)).__name__[:-9]
    f = 'Shapefile' if f == 'IndexedShapefile' else f
    return f

  def __repr__(self):
    return 'Directory[%s]' % str(self._store.info.source.path)
