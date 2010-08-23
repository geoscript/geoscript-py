import unittest
from geoscript import geom
from com.vividsolutions.jts.geom import Coordinate, GeometryFactory

class GeomTest(unittest.TestCase):

  def setUp(self):
    self.gf = GeometryFactory()

  def testPoint(self):
    p = geom.Point(1,2)
    self.assertEqual('POINT (1 2)', str(p))

  def testPointFromJTS(self):
    p = geom.Point(self.gf.createPoint(Coordinate(1,2)))
    self.assertEqual('POINT (1 2)', str(p))

  def testLineString(self):
    l = geom.LineString((1,2),(3,4))
    self.assertEqual('LINESTRING (1 2, 3 4)', str(l)) 

  def testLineStringFromJTS(self):
    ls = self.gf.createLineString([Coordinate(1,2), Coordinate(3,4)])
    l = geom.LineString(ls)
    self.assertEqual('LINESTRING (1 2, 3 4)', str(l)) 
  
  def testPolygon(self):
    p = geom.Polygon([[1,2],[3,4],[5,6],[1,2]])
    self.assertEqual('POLYGON ((1 2, 3 4, 5 6, 1 2))', str(p)) 

  def testPolygonFromJTS(self):
    poly = self.gf.createPolygon(self.gf.createLinearRing([Coordinate(1,2),Coordinate(3,4), Coordinate(5,6), Coordinate(1,2)]), [])
    p = geom.Polygon(poly)
    self.assertEqual('POLYGON ((1 2, 3 4, 5 6, 1 2))', str(p)) 

  def testMultiPoint(self):
    mp = geom.MultiPoint([1,2], [3,4])
    self.assertEqual('MULTIPOINT ((1 2), (3 4))', str(mp))

  def testMultiPointFromJTS(self):
    mp = geom.MultiPoint(self.gf.createMultiPoint([self.gf.createPoint(Coordinate(1,2)), self.gf.createPoint(Coordinate(3,4))]))
    self.assertEqual('MULTIPOINT ((1 2), (3 4))', str(mp))

  def testMultiLineString(self):
    ml = geom.MultiLineString([[1,2],[3,4]], [[5,6],[7,8]])
    self.assertEqual('MULTILINESTRING ((1 2, 3 4), (5 6, 7 8))', str(ml))

  def testMultiLineStringFromJTS(self):
    mls = self.gf.createMultiLineString([self.gf.createLineString([Coordinate(1,2),Coordinate(3,4)]), self.gf.createLineString([Coordinate(5,6),Coordinate(7,8)])])
    ml = geom.MultiLineString(mls)
    self.assertEqual('MULTILINESTRING ((1 2, 3 4), (5 6, 7 8))', str(ml))

  def testMultiPolygon(self):
    mp = geom.MultiPolygon([ [[1,2],[3,4],[5,6],[1,2]] ])
    self.assertEqual('MULTIPOLYGON (((1 2, 3 4, 5 6, 1 2)))', str(mp))

  def testBounds(self):
    b = geom.Bounds(1.0, 2.0, 3.0, 4.0)
    self.assertEqual('(1.0, 2.0, 3.0, 4.0)', str(b))
 
    b = geom.Bounds(1.0, 2.0, 3.0, 4.0, 'epsg:4326')
    self.assertEqual('(1.0, 2.0, 3.0, 4.0, EPSG:4326)', str(b))
    
  def testBoundsReproject(self):
    b = geom.Bounds(-111, 44.7, -110, 44.9, 'epsg:4326')
    b1 = b.reproject('epsg:26912')
    self.assertEqual(499999, int(b1.west))
    self.assertEqual(4949624, int(b1.south))
    self.assertEqual(579224, int(b1.east))
    self.assertEqual(4972327, int(b1.north))
    
  def testBoundsScale(self):
    b = geom.Bounds(5,5,10,10)

    b1 = b.scale(2)
    assert 2.5 == b1.west
    assert 2.5 == b1.south
    assert 12.5 == b1.east
    assert 12.5 == b1.north
  
    b1 = b.scale(0.5)
    assert 6.25 == b1.west
    assert 6.25 == b1.south
    assert 8.75 == b1.east
    assert 8.75 == b1.north

  def testBoundsExpand(self):
    b1 = geom.Bounds(0,0,5,5)
    b2 = geom.Bounds(5,5,10,10)
    b1.expand(b2)

    assert 0 == b1.west and 0 == b1.south
    assert 10 == b1.east and 10 == b1.north
  
  def testMultiPolygonFromJTS(self):
    mp = geom.MultiPolygon(self.gf.createMultiPolygon([self.gf.createPolygon(self.gf.createLinearRing([Coordinate(1,2),Coordinate(3,4),Coordinate(5,6),Coordinate(1,2)]),[])]))
    self.assertEqual('MULTIPOLYGON (((1 2, 3 4, 5 6, 1 2)))', str(mp))

  def testFromWKT(self):
    g = geom.fromWKT('POINT(1 2)') 
    self.assertEqual('Point',g.geometryType)
    self.assertEqual(1,g.x)
    self.assertEqual(2,g.y)
