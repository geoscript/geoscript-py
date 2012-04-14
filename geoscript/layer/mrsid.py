from geoscript.layer.raster import Raster
from org.geotools.coverageio.gdal.mrsid import MrSIDFormat

class MrSID(Raster):

  def __init__(self, file, proj=None):
    Raster.__init__(self, MrSIDFormat(), file, proj)
