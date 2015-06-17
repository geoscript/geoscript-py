import unittest
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import GeoPackage

class GeoPackageWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.ws = GeoPackage('work/data.gpkg')
    self.remove('widgets')
    self.remove('widgets2')
    self.remove('states2')

  def remove(self, layer):
    try:
      self.ws.remove(layer)
    except:
      pass
