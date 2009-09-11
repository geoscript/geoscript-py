import unittest
from geoscript import geom, proj, feature

class LayerTest(unittest.TestCase):

  def testCount(self):
    self.assertEqual(49, self.l.count())

  def testCRS(self):
    cs = self.l.crs
    self.assert_(cs)
    self.assertEqual('EPSG:4326', proj.srs(cs))

  def testBounds(self):
    b = self.l.bounds()
    self.assertEqual(-124,int(b.getMinX()))
    self.assertEqual(24,int(b.getMinY()))
    self.assertEqual(-66,int(b.getMaxX()))
    self.assertEqual(49,int(b.getMaxY()))

  def testFeatures(self):
    count = 0
    for f in self.l.features():
      self.assert_(f)
      self.assert_(f.get('STATE_NAME'))
      count += 1

    self.assertEqual(49, count)

  def testFeaturesFilter(self):
     features = [f for f in self.l.features("STATE_ABBR EQ 'TX'")]
     self.assertEqual(1,len(features))
     self.assertEqual('Texas', features[0].get('STATE_NAME'))
