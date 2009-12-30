import unittest
from tests.layer.layertest import LayerTest
from geoscript import geom
from geoscript.layer import ShapefileLayer
from geoscript.workspace import MemoryWorkspace

class MemoryLayer_Test(LayerTest):

  def setUp(self):
    mem = MemoryWorkspace()
    self.l = mem.add(ShapefileLayer('work/states.shp'))

  def testFormat(self):
    assert 'Memory' == self.l.format
