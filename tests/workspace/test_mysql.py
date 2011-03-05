import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import MySQL

class MySQLWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = MySQL('geoscript')
