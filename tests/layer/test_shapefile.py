import unittest
from tests.layer.layertest import LayerTest
from geoscript.layer import ShapefileLayer

class ShapefileLayer_Test(LayerTest):

  def setUp(self):
    self.l = ShapefileLayer('data/states.shp')
