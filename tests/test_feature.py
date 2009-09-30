import unittest
from geoscript import geom, proj, feature

class FeatureTest(unittest.TestCase):

  def testFeatureTypeBasic(self):
    atts = [('att1',str),('att2',int),('geom',geom.Point)]
    ft = feature.FeatureType('test',atts)

    self.assertEqual('test',ft.name())
    n = 0
    for att,typ in ft.atts():    
      self.assertEqual(atts[n][0], att)
      self.assertEqual(atts[n][1], typ)
      n = n+1 

    self.assertEqual(len(atts), n)
    self.assertEqual(atts[2],ft.geom())

  def testFeatureTypeGeomSRS(self):
    ft = feature.FeatureType('test',[('att1',str),('att2',int),('geom',geom.Point,'epsg:3005')])
    self.assert_(isinstance(ft.geom()[2], proj.CRS))
    self.assertEqual(proj.crs.decode('epsg:3005'),ft.geom()[2])

  def testBasic(self):
    id = 'fid'
    g = geom.point(-125,50)
    a = {'x': 1, 'y': 1.1, 'z': 'one', 'geom': g}
    f = feature.Feature(a,'fid')
    self.assertEqual(id,f.id())
    self.assertEqual(g,f.geom())
