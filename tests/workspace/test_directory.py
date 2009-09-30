import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import DirectoryWorkspace

class DirectoryWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = DirectoryWorkspace('data')

  def testNewLayer(self):
    pass

  def testAddLayer(self):
    pass

