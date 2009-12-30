import unittest
from tests.layer.layertest import LayerTest
from geoscript.layer import Shapefile

class ShapefileLayer_Test(LayerTest):

  def setUp(self):
    self.l = Shapefile('work/states.shp')

  def testFormat(self):
    assert 'Shapefile' == self.l.format 
