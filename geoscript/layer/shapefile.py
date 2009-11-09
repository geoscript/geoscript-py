"""
The :mod:`layer.shapefile` module provides support for Shapefile access.
"""

import os
from java import net
from geoscript.layer import Layer
from geoscript import util
from org.geotools.data.shapefile import ShapefileDataStore

class ShapefileLayer(Layer):
  """
  A subclass of :class:`geoscript.layer.layer.Layer` for the Shapefile format.

  A Shapefile layer is constructed by specifing the *file* path as a ``str``.
  """
  def __init__(self, file, fs=None):
    if not fs:
      shp = ShapefileDataStore(util.toURL(file), net.URI('http://geoscript.org'));
      fs = shp.featureSource

    Layer.__init__(self, fs)

  def getfile(self):
    return self.fs.dataStore.info.source.toURL().file

  file = property(getfile, None, None, 'Returns the file path to the Shapefile')

  def _newLayer(self, schema, **options):
    if options.has_key('file'):
      file = options['file']
    else:
      file = os.path.join(os.path.dirname(self.file), '%s.shp' % schema.name)

    shp = ShapefileDataStore(util.toURL(file), net.URI('http://geoscript.org'));
    shp.createSchema(schema.ft) 
    return ShapefileLayer(None, shp.featureSource) 
