import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import GeoPackage

class GeoPackageWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = GeoPackage('data.gpkg')
