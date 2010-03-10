import sys
from geoscript import util
from geoscript.raster.raster import Raster
from org.geotools.coverageio.gdal.mrsid import MrSIDReader

class MrSID(Raster):

  def __init__(self, file):
    Raster.__init__(self, MrSIDReader(util.toFile(file)))

