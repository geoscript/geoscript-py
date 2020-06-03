"""
the :mod:`workspace.property` module provides a workspace implemntation based on a directory of java style property files. 
"""

import os
from java import io, net
from geoscript import util
from geoscript.workspace import Workspace
from org.geotools.data.geobuf import GeobufDataStoreFactory

class Geobuf(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` that provides layers that correspond to geobuf files in a directory.

  *dir* is the optional path as a ``str`` to a directory. If not specified it defaults to ``os.getcwd()``.
  """

  def __init__(self, dir=None, precision=6, dimension=2):
    dir = dir or os.getcwd()
    params = {'file': util.toFile(dir), 'precision': precision, 'dimension': dimension}
    Workspace.__init__(self, GeobufDataStoreFactory(), params)

  def __repr__(self):
    return 'Geobuf[%s]' % str(self._store.info.source.path)
