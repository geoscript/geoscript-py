import unittest
from geoscript import geom
from com.vividsolutions.jts.geom import Coordinate

class GeomTest(unittest.TestCase):

  def testPoint(self):
    p = geom.Point(1,2)
    self.assertEqual('POINT (1 2)', str(p))

  def testPointFromJTS(self):
    p = geom.Point(geom._gf.createPoint(Coordinate(1,2)))
    self.assertEqual('POINT (1 2)', str(p))

  def testLineString(self):
    l = geom.LineString((1,2),(3,4))
    self.assertEqual('LINESTRING (1 2, 3 4)', str(l)) 

  def testLineStringFromJTS(self):
    ls = geom._gf.createLineString([Coordinate(1,2), Coordinate(3,4)])
    l = geom.LineString(ls)
    self.assertEqual('LINESTRING (1 2, 3 4)', str(l)) 
  
  def testPolygon(self):
    p = geom.Polygon([[1,2],[3,4],[5,6],[1,2]])
    self.assertEqual('POLYGON ((1 2, 3 4, 5 6, 1 2))', str(p)) 

  def testPolygonFromJTS(self):
    poly = geom._gf.createPolygon(geom._gf.createLinearRing([Coordinate(1,2),Coordinate(3,4), Coordinate(5,6), Coordinate(1,2)]), [])
    p = geom.Polygon(poly)
    self.assertEqual('POLYGON ((1 2, 3 4, 5 6, 1 2))', str(p)) 

  def testMultiPoint(self):
    mp = geom.MultiPoint([1,2], [3,4])
    self.assertEqual('MULTIPOINT (1 2, 3 4)', str(mp))

  def testMultiPointFromJTS(self):
    mp = geom.MultiPoint(geom._gf.createMultiPoint([geom._gf.createPoint(Coordinate(1,2)), geom._gf.createPoint(Coordinate(3,4))]))
    self.assertEqual('MULTIPOINT (1 2, 3 4)', str(mp))

  def testMultiLineString(self):
    ml = geom.MultiLineString([[1,2],[3,4]], [[5,6],[7,8]])
    self.assertEqual('MULTILINESTRING ((1 2, 3 4), (5 6, 7 8))', str(ml))

  def testMultiLineStringFromJTS(self):
    mls = geom._gf.createMultiLineString([geom._gf.createLineString([Coordinate(1,2),Coordinate(3,4)]), geom._gf.createLineString([Coordinate(5,6),Coordinate(7,8)])])
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
    
  def testMultiPolygonFromJTS(self):
    mp = geom.MultiPolygon(geom._gf.createMultiPolygon([geom._gf.createPolygon(geom._gf.createLinearRing([Coordinate(1,2),Coordinate(3,4),Coordinate(5,6),Coordinate(1,2)]),[])]))
    self.assertEqual('MULTIPOLYGON (((1 2, 3 4, 5 6, 1 2)))', str(mp))

  def testFromWKT(self):
    g = geom.fromWKT('POINT(1 2)') 
    self.assertEqual('Point',g.geometryType)
    self.assertEqual(1,g.x)
    self.assertEqual(2,g.y)
