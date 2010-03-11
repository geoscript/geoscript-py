import sys
from geoscript import util
from geoscript.raster.raster import Raster
from org.geotools.gce.imagemosaic import ImageMosaicReader

class Mosaic(Raster):

  def __init__(self, dir):
    Raster.__init__(self, ImageMosaicReader(util.toFile(dir)))
