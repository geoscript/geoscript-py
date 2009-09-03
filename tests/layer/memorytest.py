import unittest
from geoscript import geom, feature
from geoscript.layer import MemoryLayer

class MemoryLayerTest(unittest.TestCase):

  def setUp(self):
    self.mem = MemoryLayer('widgets',[('geom',geom.Point),('name',str)])

  def testAdd(self):
      self.assertEqual(0, self.mem.count())

      f = feature.Feature(atts={'name':'foo', 'geom': geom.point(1,2)})
      self.mem.add(f)
      self.assertEqual(1,self.mem.count())

      f = [x for x in self.mem.features()][0]

      self.assert_(f)
      self.assertEqual((1,2),(f.geom().x,f.geom().y))
      self.assertEqual('foo',f.get('name'))

