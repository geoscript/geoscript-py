import unittest
from geoscript import geom, feature
from geoscript.layer import Layer, Shapefile

class WorkspaceTest:

  def testCreate(self):
    l = self.ws.create('widgets',[ ('geom', geom.Point), ('name', str) ])
    assert l

    l.add({'geom': geom.Point(1,1), 'name': 'one'})
    l.add({'geom': geom.Point(2,2), 'name': 'two'})
    l.add({'geom': geom.Point(3,3), 'name': 'three'})

    assert 3 == l.count()

  def testGetSet(self):
    self.ws['widgets2'] = [ ('geom', geom.Point), ('name', str) ] 
    l = self.ws['widgets2']
    assert l 

    l.add([geom.Point(1,1), 'one'])
    l.add([geom.Point(2,2), 'two'])
    l.add([geom.Point(3,3), 'three'])

    assert 3 == l.count()

  def testIterator(self):
    expected = [name for name in self.ws.layers()]
    actual = [name for name in self.ws] 
    
    assert len(expected) == len(actual) 

    for name, layer in self.ws.iteritems():
      assert name in expected 
      assert name == layer.name

    assert len([x for x in self.ws.iteritems()]) == len(expected)

  def testAdd(self):
    shp = Shapefile('work/states.shp') 
    l = self.ws.add(shp, 'states2')
 
    assert l
    assert shp.count() == l.count()
