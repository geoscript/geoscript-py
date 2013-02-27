from geoscript.layer.raster import Raster
from org.geotools.gce.geotiff import GeoTiffFormat

class GeoTIFF(Raster):

  def __init__(self, file, proj=None, mode='r'):
    Raster.__init__(self, GeoTiffFormat(), file, proj, mode=mode)

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
