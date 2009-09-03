"""
layer/shapefile module -- Shapefile implementation of Layer.

A shapefile layer is created from a path to a shapefile.

   shp = ShapefileLayer('path/to/file.shp')
"""

from java import net
from geoscript.layer import Layer
from geoscript import util
from org.geotools.data.shapefile import ShapefileDataStore

class ShapefileLayer(Layer):
  def __init__(self,file):
    shp = ShapefileDataStore(util.toURL(file), net.URI('http://geoscript.org'));
    Layer.__init__(self, shp.featureSource)
