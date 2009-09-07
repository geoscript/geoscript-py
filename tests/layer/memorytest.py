import unittest
from .layertest import LayerTest
from geoscript import geom
from geoscript.workspace import MemoryWorkspace
from geoscript.layer import MemoryLayer, ShapefileLayer

class MemoryLayerTest(LayerTest):

  def setUp(self):
    mem = MemoryWorkspace()
    self.l = mem.addLayer(ShapefileLayer('states.shp'))

