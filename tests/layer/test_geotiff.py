import sys, java, unittest
from geoscript.layer import GeoTIFF

class GeoTIFF_Test:

  def setUp(self):
    self.tif = GeoTIFF('data/sfdem.tif')

  def testBounds(self):
    assert self.tif.bounds() is not None
    assert self.tif.bounds().west == 589980.0
    assert self.tif.bounds().south == 4913700.0
    assert self.tif.bounds().east == 609000.0
    assert self.tif.bounds().north == 4928010.0
    assert self.tif.bounds().proj.id == 'EPSG:26713'
    
  def testBands(self):
    bands = self.tif.bands
    assert 1 == len(bands)
    assert 'GRAY_INDEX' == bands[0].name
