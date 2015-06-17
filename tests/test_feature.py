import sys, java, unittest
import xpath
from xml.dom import minidom as dom
from geoscript import geom, proj, feature
try:
  import json
except ImportError:
  import simplejson as json

class Feature_Test:

  @classmethod
  def setUpClass(cls):
    cls.xpathctx = xpath.XPathContext()    
    cls.xpathctx.namespaces['gml'] = 'http://www.opengis.net/gml' 
    cls.xpathctx.namespaces['gsf'] = 'http://geoscript.org/feature'

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
    assert [f for name, f in s.iteritems()] == expected

    try:
      s['foo']
      assert False
    except KeyError:
      pass

    assert s.values() == s.fields 
    assert s.keys() == [f.name for f in s.fields]

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
   
    assert sorted(f.attributes.keys()) == sorted(f.keys())
    assert sorted(f.attributes.values()) == sorted(f.values())

  def testEquals(self):
    id = 'fid'
    g = geom.Point(-125, 50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    f1 = feature.Feature(a,'fid')
    f2 = feature.Feature(a,'fid')
    assert f1 == f2

  def testBounds(self):
    g = geom.LineString((1,1), (10,10))
    f = feature.Feature({'geom': g}, 'fid')
   
    assert 1 == f.bounds.west 
    assert 1 == f.bounds.south 
    assert 10 == f.bounds.east
    assert 10 == f.bounds.north

  def testBoundsNoGeom(self):
    f = feature.Feature({'x': 1}, 'fid')
    assert None == f.bounds

  def testWriteJSON(self):
    g = geom.Point(-125, 50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    f1 = feature.Feature(a,'fid')
    st = feature.writeJSON(f1)    
    assert st

    obj = json.loads(st) 
    assert obj['type'] == 'Feature'
    assert obj['properties']['x'] == 1
    assert obj['properties']['y'] == 1.1
    assert obj['geometry']['type'] == 'Point'
    assert obj['geometry']['coordinates'] == [-125, 50] 

  def testReadJSON(self):
    st = '{"type": "Feature", "properties": {"x": 1, "y": 1.1 }, "id": "fid"}'
    f = feature.readJSON(st) 
    assert f

    assert 1 == f['x']
    assert 1.1 == f['y']
    assert 'fid' == f.id

  def testWriteGML(self):
    g = geom.Point(-125, 50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    xml = feature.writeGML(feature.Feature(a,'fid'))
    doc = dom.parseString(xml)
    assert "gsf:feature" == doc.documentElement.nodeName

    xp = Feature_Test.xpathctx
    assert u'1' in xp.findvalues('//gsf:x', doc) 
    assert u'1.1' in xp.findvalues('//gsf:y', doc) 
    assert u'one' in xp.findvalues('//gsf:z', doc) 
    assert -125.0 == float(xp.findvalues('//gsf:geom/gml:Point/gml:coord/gml:X', doc)[0] )
    assert 50.0 == float(xp.findvalues('//gsf:geom/gml:Point/gml:coord/gml:Y', doc)[0] )

  def testReadGML(self):
    xml = u'<gsf:feature fid="fid" xmlns:gml="http://www.opengis.net/gml" xmlns:gsf="http://geoscript.org/feature"><gsf:geom><gml:Point><gml:coord><gml:X>-125.0</gml:X><gml:Y>50.0</gml:Y></gml:coord></gml:Point></gsf:geom><gsf:x>1</gsf:x><gsf:z>one</gsf:z><gsf:y>1.1</gsf:y></gsf:feature>'
    f = feature.readGML(xml)
    assert f

    assert u'1' == f['x']
    assert u'1.1' == f['y']
    assert u'fid' == f.id
    assert -125.0 == f.geom.x and 50.0 == f.geom.y
    
    xml = '<gsf:feature gml:id="fid" xmlns:gml="http://www.opengis.net/gml" xmlns:gsf="http://geoscript.org/feature"><gsf:geom><gml:Point><gml:pos>-125.0 50.0</gml:pos></gml:Point></gsf:geom><gsf:x>1</gsf:x><gsf:z>one</gsf:z><gsf:y>1.1</gsf:y></gsf:feature>'
    f = feature.readGML(xml,ver=3)
    assert f

    assert u'1' == f['x']
    assert u'1.1' == f['y']
    assert u'fid' == f.id
    assert -125.0 == f.geom.x and 50.0 == f.geom.y

    xml = '<gsf:feature gml:id="fid" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gsf="http://geoscript.org/feature"><gsf:geom><gml:Point><gml:pos>-125.0 50.0</gml:pos></gml:Point></gsf:geom><gsf:x>1</gsf:x><gsf:z>one</gsf:z><gsf:y>1.1</gsf:y></gsf:feature>'
    f = feature.readGML(xml,ver=3.2)
    assert f

    assert u'1' == f['x']
    assert u'1.1' == f['y']
    assert u'fid' == f.id
    assert -125.0 == f.geom.x and 50.0 == f.geom.y

  def testWriteGML3(self):
    g = geom.Point(-125, 50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    xml = feature.writeGML(feature.Feature(a,'fid'), ver=3)
    doc = dom.parseString(xml)
    assert "gsf:feature" == doc.documentElement.nodeName

    xp = Feature_Test.xpathctx
    assert u'1' in xp.findvalues('//gsf:x', doc) 
    assert u'1.1' in xp.findvalues('//gsf:y', doc) 
    assert u'one' in xp.findvalues('//gsf:z', doc) 
    assert u'-125.0 50.0' in xp.findvalues('//gsf:geom/gml:Point/gml:pos', doc)

  def testWriteGML32(self):
    g = geom.Point(-125, 50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    xml = feature.writeGML(feature.Feature(a,'fid'), ver=3.2)
    doc = dom.parseString(xml)
    assert "gsf:feature" == doc.documentElement.nodeName

    xp = Feature_Test.xpathctx
    xp.namespaces['gml'] = 'http://www.opengis.net/gml/3.2'
    assert u'1' in xp.findvalues('//gsf:x', doc) 
    assert u'1.1' in xp.findvalues('//gsf:y', doc) 
    assert u'one' in xp.findvalues('//gsf:z', doc) 
    assert u'-125.0 50.0' in xp.findvalues('//gsf:geom/gml:Point/gml:pos', doc)

