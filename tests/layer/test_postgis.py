import unittest
from tests.layer.layertest import LayerTest
from geoscript.layer import PostgisLayer

class PostgisLayer_Test(LayerTest):

  def setUp(self):
    self.l = PostgisLayer('states', 'geoscript')

