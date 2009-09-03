import unittest
from geoscript import geom, feature
from geoscript.layer import ShapefileLayer

class ShapefileLayerTest(unittest.TestCase):

  def setUp(self):
    self.shp = ShapefileLayer('states.shp')

  def testCount(self):
    self.assertEqual(49, self.shp.count())

  def testBounds(self):
    b = self.shp.bounds()
    self.assertEqual(-124,int(b.getMinX()))
    self.assertEqual(24,int(b.getMinY()))
    self.assertEqual(-66,int(b.getMaxX()))
    self.assertEqual(49,int(b.getMaxY()))

  def testFeatures(self):
    count = 0
    for f in self.shp.features():
      self.assert_(f)
      self.assert_(f.get('STATE_NAME'))
      count += 1

    self.assertEqual(49, count)

  def testFeaturesFilter(self):
     features = [f for f in self.shp.features("STATE_ABBR EQ 'TX'")]
     self.assertEqual(1,len(features))
     self.assertEqual('Texas', features[0].get('STATE_NAME'))
