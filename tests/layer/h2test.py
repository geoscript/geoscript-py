import unittest
from tests.layer.layertest import LayerTest
from geoscript.layer import H2Layer

class H2LayerTest(LayerTest):

  def setUp(self):
    self.l = H2Layer('states', 'data/states')

