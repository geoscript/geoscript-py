import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import PostgisWorkspace

class PostgisWorkspaceTest(WorkspaceTest):

  def setUp(self):
    self.ws = PostgisWorkspace('skunk')
