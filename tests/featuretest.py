import unittest
from geoscript import geom, feature

class FeatureTest(unittest.TestCase):

  def testBasic(self):
    id = 'fid'
    g = geom.Point(-125,50)
    a = {'x':1, 'y': 1.1, 'z': 'one'}
    f = feature.Feature(id='fid', atts=a, geom=g)
    self.assertEqual(id,f.id)
    self.assertEqual(g,f.geom)
    self.assertEqual(a,f.atts)
