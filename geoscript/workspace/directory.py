"""
workspace.directory module -- Directory  implementation of Workspace
"""

import os
from java import io, net
from geoscript import util
from geoscript.workspace import Workspace
from org.geotools.data.directory import DirectoryDataStore

class Directory(Workspace):

  def __init__(self, dir=os.getcwd()):

    ds = DirectoryDataStore(util.toFile(dir), net.URI('http://geoscript.org'))
    Workspace.__init__(self, ds)

  def _format(self, layer):
    f = type(self.ds.getDataStore(layer.name)).__name__[:-9]
    f = 'Shapefile' if f == 'IndexedShapefile' else f
    return f
