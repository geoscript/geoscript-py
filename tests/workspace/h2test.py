import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import H2Workspace

class H2WorkspaceTest(WorkspaceTest):

  def setUp(self):
    self.ws = H2Workspace('acme', 'work')
