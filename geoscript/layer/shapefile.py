"""
The :mod:`layer.shapefile` module provides support for Shapefile access.
"""

from java import net
from geoscript.layer import Layer
from geoscript import util
from org.geotools.data.shapefile import ShapefileDataStore

class ShapefileLayer(Layer):
  """
  A subclass of :class:`geoscript.layer.layer.Layer` for the Shapefile format.

  A Shapefile layer is constructed by specifing the *file* path as a ``str``.
  """
  def __init__(self,file):
    shp = ShapefileDataStore(util.toURL(file), net.URI('http://geoscript.org'));
    Layer.__init__(self, shp.featureSource)
