import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import DirectoryWorkspace

class DirectoryWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = DirectoryWorkspace('data')

  def testCreate(self):
    pass

  def testAdd(self):
    pass

