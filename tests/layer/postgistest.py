import unittest
from geoscript import geom, feature
from geoscript.layer import PostgisLayer

class PostgisLayerTest(unittest.TestCase):

  def setUp(self):
    self.pg = PostgisLayer('states', db='skunk')

  def testCount(self):
    self.assertEqual(49, self.pg.count())

  def testBounds(self):
    b = self.pg.bounds()
    self.assertEqual(-124,int(b.getMinX()))
    self.assertEqual(24,int(b.getMinY()))
    self.assertEqual(-66,int(b.getMaxX()))
    self.assertEqual(49,int(b.getMaxY()))

  def testFeatures(self):
    count = 0
    for f in self.pg.features():
      self.assert_(f)
      self.assert_(f.get('STATE_NAME'))
      count += 1

    self.assertEqual(49, count)

  def testFeaturesFilter(self):
     features = [f for f in self.pg.features("STATE_ABBR EQ 'TX'")]
     self.assertEqual(1,len(features))
     self.assertEqual('Texas', features[0].get('STATE_NAME'))
