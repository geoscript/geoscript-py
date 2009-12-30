"""
workspace.memory module -- Memory implementation of Workspace.
"""

from geoscript.workspace import Workspace
from org.geotools.data.memory import MemoryDataStore

class Memory(Workspace):

  def __init__(self):

    mem = MemoryDataStore()
    Workspace.__init__(self, mem)
