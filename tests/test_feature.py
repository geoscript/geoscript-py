import unittest
from geoscript import geom, proj, feature

class Feature_Test:

  def testSchemaBasic(self):
    atts = [('att1',str),('att2',int),('geom',geom.Point)]
    s = feature.Schema('test',atts)

    assert 'test' == s.name
    n = 0
    for att in s.fields:    
      assert atts[n][0] == att.name
      assert atts[n][1] == att.typ
      n = n+1 

    assert len(atts) == n
    assert atts[2][0] == s.geom.name
    assert atts[2][1] == s.geom.typ

  def testSchemaGeomProj(self):
    prj = proj.Projection('epsg:3005')
    s = feature.Schema('test',[('att1',str),('att2',int),('geom', geom.Point,'epsg:3005')])
    assert s.geom.proj
    assert prj == s.geom.proj

  def testSchemaReproject(self):
    prj1 = proj.Projection('epsg:4326')
    prj2 = proj.Projection('epsg:3005')

    s = feature.Schema('test',[('geom', geom.Point,'epsg:4326')])
    assert s.fields[0].proj == prj1

    s = s.reproject(prj2, 'reprojected')
    assert 'reprojected' == s.name
    assert s.fields[0].proj == prj2

  def testSchemaAsContainer(self):
    s = feature.Schema('test',[('att1',str),('att2',int),('geom', geom.Point,'epsg:3005')])
    assert s['att1'] 
    assert s['att1'].typ == str

    expected = [f.name for f in s.fields]
    assert [name for name in s] == expected

    expected = [f for f in s.fields]
    print expected
    print [f for name, f in s.iteritems()]
    assert [f for name, f in s.iteritems()] == expected

    try:
      s['foo']
      assert False
    except KeyError:
      pass

  def testSchemaEquals(self):
    s1 = feature.Schema('test',[('att1',str),('att2',int),('geom', geom.Point,'epsg:3005')])
    s2 = feature.Schema('test',[('att1',str),('att2',int),('geom', geom.Point,'epsg:3005')])
    assert s1 == s2

  def testBasic(self):
    id = 'fid'
    g = geom.Point(-125, 50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    f = feature.Feature(a,'fid')
    assert id == f.id
    assert g == f.geom

  def testAsContainer(self):
    id = 'fid'
    g = geom.Point(-125, 50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    f = feature.Feature(a,'fid')

    assert 1 == f['x']
    try:
      f['foo'] 
      assert False
    except KeyError:
      pass

    assert [x for x in f.schema] == [y for y in f]
    expected = [(x,y) for x,y in f.attributes.iteritems()]
    assert [(x,y) for x,y in f.iteritems()] == expected
   
  def testEquals(self):
    id = 'fid'
    g = geom.Point(-125, 50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    f1 = feature.Feature(a,'fid')
    f2 = feature.Feature(a,'fid')
    assert f1 == f2

