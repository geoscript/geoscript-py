import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import MemoryWorkspace

class MemoryWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = MemoryWorkspace()
