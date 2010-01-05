import unittest
from geoscript import geom, proj, feature

class LayerTest:

  def testCount(self):
    assert 49 == self.l.count()

  def testProj(self):
    prj = self.l.proj
    assert prj 
    assert 'EPSG:4326' == prj.id

  def testBounds(self):
    b = self.l.bounds()
    assert -124 == int(b.getMinX())
    assert 24 == int(b.getMinY())
    assert -66 == int(b.getMaxX())
    assert 49 == int(b.getMaxY())

  def testFeatures(self):
    count = 0
    for f in self.l.features():
      assert f
      assert f.get('STATE_NAME')
      count += 1

    assert 49 == count

  def testFeaturesFilter(self):
     features = [f for f in self.l.features("STATE_ABBR EQ 'TX'")]
     assert 1 == len(features)
     assert 'Texas' == features[0].get('STATE_NAME')

  def testReproject(self):
     rgeoms = [self.l.proj.transform(f.geom, 'epsg:3005') for f in self.l.features()]
     rl = self.l.reproject('epsg:3005', 'reprojected')
     i = 0
     for f in rl.features():
        assert int(rgeoms[i].coordinate.x) == int(f.geom.coordinate.x)
        assert int(rgeoms[i].coordinate.y) == int(f.geom.coordinate.y)
        i += 1

  def testCursor(self):
     c = self.l.cursor()
     f = c.next()
     assert f
     assert f.get('STATE_NAME')
     
     f = c.read(30)
     assert f
     assert len(f) == 30
     assert f[0].get('STATE_NAME')
  
     f = c.read(30)
     assert f
     assert len(f) == 18
     c.close()
