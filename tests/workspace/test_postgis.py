import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import PostGIS

class PostgisWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.skipIfNoDB('postgis')
    self.ws = PostGIS('geoscript')
