import unittest
from tests.layer.layertest import LayerTest
from geoscript.layer import PostgisLayer

class PostgisLayerTest(LayerTest):

  def setUp(self):
    self.l = PostgisLayer('states', db='skunk')

