import unittest
from geoscript import geom, proj
from .util import assertClose

class ProjTest(unittest.TestCase):

  def testTransform(self):
    p = geom.Point(-125,50)
    rp = proj.transform(p,'epsg:4326','epsg:3005')
    assertClose(self, 1071693,int(rp.x))
    assertClose(self, 554289,int(rp.y))

  def testTransformList(self):
    l = proj.transform([-125,50],'epsg:4326','epsg:3005')
    assertClose(self, 1071693,int(l[0]))
    assertClose(self, 554289,int(l[1]))
