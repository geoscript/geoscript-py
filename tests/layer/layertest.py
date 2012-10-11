import unittest
from java import io
from ..util import skipIfNoDB
from geoscript import geom, proj, feature
from geoscript.layer import writeGML, readGML, readJSON, writeJSON
from org.geotools.factory import CommonFactoryFinder
from org.opengis.filter.sort import SortOrder

class LayerTest:

  def skipIfNoDB(self, id):
    skipIfNoDB(id)
    
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

  def testReadWriteGML(self):
    ostream = io.ByteArrayOutputStream() 
    writeGML(self.l, output=ostream)

    istream = io.ByteArrayInputStream(ostream.toByteArray())
    l = readGML(istream)

    assert self.l.count() == l.count()

    c = self.l.cursor("STATE_ABBR = 'TX'")
    ostream = io.ByteArrayOutputStream()
    writeGML(c, output=ostream)
    c.close()

    istream = io.ByteArrayInputStream(ostream.toByteArray())
    l = readGML(istream) 
    assert 1 == l.count()
    f = [x for x in l.features()][0]

    assert 'Texas' == f['STATE_NAME']

  def testReadWriteJSON(self):
    ostream = io.ByteArrayOutputStream() 
    writeJSON(self.l, output=ostream)

    istream = io.ByteArrayInputStream(ostream.toByteArray())
    l = readJSON(istream)

    assert self.l.count() == l.count()

    c = self.l.cursor("STATE_ABBR = 'TX'")
    ostream = io.ByteArrayOutputStream()
    writeJSON(c, output=ostream)
    c.close()

    istream = io.ByteArrayInputStream(ostream.toByteArray())
    l = readJSON(istream) 
    assert 1 == l.count()
    f = [x for x in l.features()][0]

    assert 'Texas' == f['STATE_NAME']

  def testSort(self):
    # check that the layer supports sorting
    ff = CommonFactoryFinder.getFilterFactory(None)
    sortBy = ff.sort('STATE_NAME', SortOrder.ASCENDING)
    if not self.l._source.getQueryCapabilities().supportsSorting([sortBy]):
      return

    c = self.l.cursor(sort=('STATE_NAME'))
    assert 'Alabama' == c.next()['STATE_NAME']
    assert 'Arizona' == c.next()['STATE_NAME']
    assert 'Arkansas' == c.next()['STATE_NAME']
    c.close()

    c = self.l.cursor(sort=('STATE_NAME', 'DESC'))
    assert 'Wyoming' == c.next()['STATE_NAME']
    assert 'Wisconsin' == c.next()['STATE_NAME']
    assert 'West Virginia' == c.next()['STATE_NAME']
    c.close()

  def testUpdate(self):
    c = self.l.cursor("STATE_NAME = 'New York'")
    f = c.next()
    c.close()

    f['STATE_NAME'] = 'Newer York'
    self.l.update(f)

    assert 0 == self.l.count("STATE_NAME = 'New York'")
    assert 1 == self.l.count("STATE_NAME = 'Newer York'")

    c = self.l.cursor("STATE_NAME = 'Newer York'")
    f = c.next()
    c.close()
    
    assert 'NY' == f['STATE_ABBR']
    f['STATE_NAME'] = 'New York'
    self.l.update(f, ['STATE_NAME'])

    assert 1 == self.l.count("STATE_NAME = 'New York'")
    assert 0 == self.l.count("STATE_NAME = 'Newer York'")

