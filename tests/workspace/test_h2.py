import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import H2

class H2Workspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = H2('acme', 'work')
