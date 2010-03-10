import sys
from geoscript import util
from geoscript.raster.raster import Raster
from org.geotools.gce.image import WorldImageReader

class WorldImage(Raster):

  def __init__(self, file):
    Raster.__init__(self, WorldImageReader(util.toFile(file)))

  def getformat(self):
    return str(Raster.getformat(self) + ' (%s)' % self._reader.getExtension())

  format = property(getformat, None)
