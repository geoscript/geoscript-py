import unittest
from tests.layer.layertest import LayerTest
from geoscript.workspace import PostgisWorkspace

class PostgisLayer_Test(LayerTest):

  def setUp(self):
    self.l = PostgisWorkspace('geoscript').get('states')

  def testFormat(self):
    assert 'PostGIS' == self.l.format
