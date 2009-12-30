import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import Memory

class MemoryWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = Memory()
