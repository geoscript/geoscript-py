import os
import shutil
from tests.workspace.workspacetest import WorkspaceTest
from geoscript.workspace import FlatGeobuf

class FlatGeobufWorkspace_Test(WorkspaceTest):

  def setUp(self):
    self.path = 'work/flatgeobufs'
    if os.path.isdir(self.path):
        shutil.rmtree(self.path)
    os.mkdir(self.path)
    self.ws = FlatGeobuf(self.path)
