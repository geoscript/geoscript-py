import unittest
from .layertest import LayerTest
from geoscript.layer import ShapefileLayer

class ShapefileLayerTest(LayerTest):

  def setUp(self):
    self.l = ShapefileLayer('states.shp')
