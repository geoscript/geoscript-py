import unittest
from tests.layer.layertest import LayerTest
from geoscript import geom
from geoscript.workspace import MemoryWorkspace
from geoscript.layer import MemoryLayer, ShapefileLayer

class MemoryLayer_Test(LayerTest):

  def setUp(self):
    mem = MemoryWorkspace()
    self.l = mem.addLayer(ShapefileLayer('work/states.shp'))

  def testFormat(self):
    assert 'Memory' == self.l.format
