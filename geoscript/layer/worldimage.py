from geoscript.layer.raster import Raster
from org.geotools.gce.image import WorldImageFormat

class WorldImage(Raster):

  def __init__(self, file, proj=None):
    Raster.__init__(self, WorldImageFormat(), file, proj)

  def getformat(self):
    return str(Raster.getformat(self) + ' (%s)' % self._reader.getExtension())

  format = property(getformat, None)
