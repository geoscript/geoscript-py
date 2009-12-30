import unittest
from tests.layer.layertest import LayerTest
from geoscript.workspace import MySQLWorkspace

class MySQLLayer_Test(LayerTest):

  def setUp(self):
    self.l = MySQLWorkspace('geoscript').get('states')

  def testFormat(self):
    assert 'MySQL' == self.l.format
