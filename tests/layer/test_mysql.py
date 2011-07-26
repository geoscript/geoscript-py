import unittest
from tests.layer.layertest import LayerTest
from geoscript.workspace import MySQL

class MySQLLayer_Test(LayerTest):

  def setUp(self):
    self.skipIfNoDB('mysql')
    self.l = MySQL('geoscript').get('states')

  def testFormat(self):
    assert 'MySQL' == self.l.format
