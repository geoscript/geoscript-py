"""
workspace.memory module -- Memory implementation of Workspace.
"""

from geoscript.workspace import Workspace
from geoscript.layer import MemoryLayer
from org.geotools.data.memory import MemoryDataStore

class MemoryWorkspace(Workspace):

  def __init__(self):

    mem = MemoryDataStore()
    Workspace.__init__(self, mem)

  def layer(self, name):
    l = Workspace.layer(self, name)
    if l:
      return MemoryLayer(None, None, l.fs)

