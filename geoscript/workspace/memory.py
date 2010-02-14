"""
The :mod:`workspace.memory` module provides a workspace implementation based on layers created strictly in memory and not persisted on disk.
"""

from geoscript.workspace import Workspace
from org.geotools.data.memory import MemoryDataStore

class Memory(Workspace):
  """
  A subclass of :class:`Workspace <geoscript.workspace.workspace.Workspace>` for which layers are created and stored in memory.
  """

  def __init__(self):

    Workspace.__init__(self, MemoryDataStoreFactory())

class MemoryDataStoreFactory(object):

  def __init__(self):
    pass

  def createDataStore(self, params):
    return MemoryDataStore()
