import unittest
from geoscript import geom, feature
from geoscript.layer import ShapefileLayer

class WorkspaceTest:

  def testNewLayer(self):
    l = self.ws.newLayer('widgets',[ ('geom', geom.Point), ('name', str) ])
    assert l

    l.add({'geom': geom.Point(1,1), 'name': 'one'})
    l.add({'geom': geom.Point(2,2), 'name': 'two'})
    l.add({'geom': geom.Point(3,3), 'name': 'three'})

    assert 3 == l.count()

  def testAddLayer(self):
    shp = ShapefileLayer('data/states.shp') 
    l = self.ws.addLayer(shp, 'states2')
 
    assert l
    assert shp.count() == l.count()
