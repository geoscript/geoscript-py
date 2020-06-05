"""
the :mod:`workspace.property` module provides a workspace implemntation based on a directory of java style property files. 
"""

import os
from java import io, net
from geoscript import util
from geoscript.workspace import Workspace
from org.geotools.data.flatgeobuf import FlatgeobufDataStoreFactory

class FlatGeobuf(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` that provides layers that correspond to flatgeobuf files in a directory.

  *dir* is the optional path as a ``str`` to a directory. If not specified it defaults to ``os.getcwd()``.
  """

  def __init__(self, dir=None):
    dir = dir or os.getcwd()
    params = {'flatgeobuf-file': util.toFile(dir)}
    Workspace.__init__(self, FlatgeobufDataStoreFactory(), params)

  def __repr__(self):
    return 'FlatGeobuf[%s]' % str(self._store.info.source.path)
