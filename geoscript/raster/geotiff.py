import sys
from geoscript import util
from geoscript.raster.raster import Raster
from org.geotools.gce.geotiff import GeoTiffReader

class GeoTIFF(Raster):

  def __init__(self, file):
    Raster.__init__(self, GeoTiffReader(util.toFile(file)))

  def getpixelsize(self):
    md = self._reader.getMetadata()
    if md.hasPixelScales():
      ps = md.getModelPixelScales()
      return tuple(ps.getValues())  

    return Raster.getpixelsize(self)

  pixelsize = property(getpixelsize, None)

  def dump(self):
    from org.geotools.coverage.grid.io.imageio import IIOMetadataDumper
    md = self._reader.getMetadata()
    dump = IIOMetadataDumper(md.rootNode).getMetadata().split('\n')
    for s in dump:
      print s
