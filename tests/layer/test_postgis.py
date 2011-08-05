import unittest
from tests.layer.layertest import LayerTest
from geoscript.workspace import PostGIS

class PostgisLayer_Test(LayerTest):

  def setUp(self):
    self.skipIfNoDB('postgresql')
    self.l = PostGIS('geoscript').get('states')

  def testFormat(self):
    assert 'PostGIS' == self.l.format
