from geoscript.layer.raster import Raster
from org.geotools.gce.imagemosaic import ImageMosaicFormat

class Mosaic(Raster):

  def __init__(self, dir, proj=None):
    Raster.__init__(self, ImageMosaicFormat(), dir,proj)
