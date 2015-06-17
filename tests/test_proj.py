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

  def testBounds(self):
    p = proj.Projection('epsg:3005')
    b = p.bounds 
    assertClose(self, 34758, int(b.west))
    assertClose(self, 359549, int(b.south))
    assertClose(self, 1883159, int(b.east))
    assertClose(self, 1736633, int(b.north))
    assert p == b.proj

    b = p.geobounds
    assertClose(self, -139, int(b.west))
    assertClose(self, 48, int(b.south))
    assertClose(self, -114, int(b.east))
    assertClose(self, 60, int(b.north))
    assert proj.Projection('epsg:4326') == b.proj
