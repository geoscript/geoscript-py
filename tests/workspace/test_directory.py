import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import Directory

class DirectoryWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = Directory('work')

  def testCreate(self):
    pass

  def testAdd(self):
    pass

