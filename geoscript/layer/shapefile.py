"""
The :mod:`layer.shapefile` module provides support for Shapefile access.
"""

from os import path
from java import net
from geoscript import util
from geoscript.layer import Layer

class Shapefile(Layer):
  """
  A subclass of :class:`Layer <geoscript.layer.layer.Layer>` for the Shapefile format.

  *file* is the path to the Shapefile as a ``str``.

  *schema* is optional and only relevent when creating a new Shapefile. It 
  specifies the schema for the new file.
  """
  def __init__(self, file, schema=None):
    f = util.toFile(file) 
    name = path.splitext(path.basename(file))[0]

    from geoscript.workspace import Directory
    Layer.__init__(self, name, Directory(f.canonicalFile.parent), schema=schema)

  def getfile(self):
    return self._source.dataStore.info.source.toURL().file

  file = property(getfile, None, None, 'Returns the file path to the Shapefile')

