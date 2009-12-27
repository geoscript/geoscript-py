import unittest
from geoscript import geom, feature
from geoscript.layer import ShapefileLayer

class WorkspaceTest:

  def testCreate(self):
    l = self.ws.create('widgets',[ ('geom', geom.Point), ('name', str) ])
    assert l

    l.add({'geom': geom.Point(1,1), 'name': 'one'})
    l.add({'geom': geom.Point(2,2), 'name': 'two'})
    l.add({'geom': geom.Point(3,3), 'name': 'three'})

    assert 3 == l.count()

  def testAdd(self):
    shp = ShapefileLayer('work/states.shp') 
    l = self.ws.add(shp, 'states2')
 
    assert l
    assert shp.count() == l.count()
