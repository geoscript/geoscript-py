import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import PostgisWorkspace

class PostgisWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = PostgisWorkspace('geoscript')
