import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import PostGIS

class PostgisWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.skipIfNoDB('postgresql')
    self.ws = PostGIS('geoscript')
