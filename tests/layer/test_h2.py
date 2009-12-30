import unittest
from tests.layer.layertest import LayerTest
from geoscript import proj
from geoscript.workspace import H2

class H2Layer_Test(LayerTest):

  def setUp(self):
    ws = H2('work/states')
    self.l = ws.get('states')
    self.l.proj = proj.Projection('epsg:4326')
    
  def testReproject(self):
    #TODO fix this, currently h2 won't reproject
    pass

  def testFormat(self):
    assert 'H2' == self.l.format
