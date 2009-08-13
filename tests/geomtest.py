import unittest
from geoscript import geom

class GeomTest(unittest.TestCase):

  def testPoint(self):
    p = geom.Point(1,2)
    self.assertEqual(1,p.x)
    self.assertEqual(2,p.y)

  def testLineString(self):
    l = geom.LineString([(1,2),(3,4)])
    c = l.coordinates
    self.assertEqual((1,2),(c[0].x,c[0].y))
    self.assertEqual((3,4),(c[1].x,c[1].y))

  def testPolygon(self):
    p = geom.Polygon([[1,2],[3,4],[5,6],[1,2]])
    c = p.exteriorRing.coordinates
    self.assertEqual((1,2),(c[0].x,c[0].y))
    self.assertEqual((3,4),(c[1].x,c[1].y))
    self.assertEqual((5,6),(c[2].x,c[2].y))
    self.assertEqual((1,2),(c[3].x,c[3].y))

  def testWKT(self):
    g = geom.Geometry('POINT(1 2)') 
    self.assertEqual('Point',g.geometryType)
    self.assertEqual(1,g.x)
    self.assertEqual(2,g.y)

  def testReproject(self):
    p = geom.Point(-125,50)
    rp = geom.reproject(p,'epsg:4326','epsg:3005') 
    self.assertEqual(1071693,int(rp.x))
    self.assertEqual(554289,int(rp.y))
