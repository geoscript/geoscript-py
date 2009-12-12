import unittest
from tests.layer.layertest import LayerTest
from geoscript.layer import MySQLLayer

class MySQLLayer_Test(LayerTest):

  def setUp(self):
    self.l = MySQLLayer('states', 'geoscript')

  def testFormat(self):
    assert 'MySQL' == self.l.format
