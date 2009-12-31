"""
the :mod:`workspace.directory` module provides a workspace implemntation based on the contents of a directory on a file system.
"""

import os
from java import io, net
from geoscript import util
from geoscript.workspace import Workspace
from org.geotools.data.directory import DirectoryDataStore

class Directory(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` that provides layers that correspond to the files in a directory.

  *dir* is the optional path as a ``str`` to a directory. If not specified it defaults to ``os.getcwd()``.
  """

  def __init__(self, dir=None):
    dir = dir or os.getcwd()
    ds = DirectoryDataStore(util.toFile(dir), net.URI('http://geoscript.org'))
    Workspace.__init__(self, ds)

  def _format(self, layer):
    f = type(self.ds.getDataStore(layer.name)).__name__[:-9]
    f = 'Shapefile' if f == 'IndexedShapefile' else f
    return f

  def __repr__(self):
    return 'Directory[%s]' % str(self.ds.info.source.path)
