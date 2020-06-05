import os
import shutil
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import Geobuf

class GeobufWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.path = 'work/geobufs'
    if os.path.isdir(self.path):
        shutil.rmtree(self.path)
    os.mkdir(self.path)
    self.ws = Geobuf(self.path)
