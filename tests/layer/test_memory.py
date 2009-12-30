import unittest
from tests.layer.layertest import LayerTest
from geoscript import geom
from geoscript.layer import Shapefile
from geoscript.workspace import Memory

class MemoryLayer_Test(LayerTest):

  def setUp(self):
    mem = Memory()
    self.l = mem.add(Shapefile('work/states.shp'))

  def testFormat(self):
    assert 'Memory' == self.l.format
