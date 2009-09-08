import unittest
from geoscript import geom, feature
from geoscript.layer import ShapefileLayer

class WorkspaceTest(unittest.TestCase):

  def testNewLayer(self):
    l = self.ws.newLayer('widgets',[ ('geom', geom.Point), ('name', str) ])
    self.assert_(l)

    l.add([geom.point(1,1), 'one'])
    l.add([geom.point(2,2), 'two'])
    l.add([geom.point(3,3), 'three'])

    self.assertEqual(3, l.count())

  def testAddLayer(self):
    shp = ShapefileLayer('data/states.shp') 
    l = self.ws.addLayer(shp, 'states2')
 
    self.assert_(l)
    self.assertEqual(shp.count(), l.count())
