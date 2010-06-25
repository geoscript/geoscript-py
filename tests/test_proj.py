import unittest
from geoscript import geom, proj

class ProjTest(unittest.TestCase):

  def testTransform(self):
    p = geom.Point(-125,50)
    rp = proj.transform(p,'epsg:4326','epsg:3005')
    self.assertEqual(1071693,int(rp.x))
    self.assertEqual(554290,int(rp.y))

  def testTransformList(self):
    l = proj.transform([-125,50],'epsg:4326','epsg:3005')
    self.assertEqual(1071693,int(l[0]))
    self.assertEqual(554290,int(l[1]))
