"""
The :mod:`layer.shapefile` module provides support for Shapefile access.
"""

from os import path
from java import net
from geoscript import util
from geoscript.layer import Layer

class Shapefile(Layer):
  """
  A subclass of :class:`geoscript.layer.layer.Layer` for the Shapefile format.

  A Shapefile layer is constructed by specifing the *file* path as a ``str``.
  """
  def __init__(self, file):
    f = util.toFile(file) 
    name = path.splitext(path.basename(file))[0]

    from geoscript.workspace import Directory
    Layer.__init__(self, name, Directory(f.canonicalFile.parent))

  def getfile(self):
    return self.fs.dataStore.info.source.toURL().file

  file = property(getfile, None, None, 'Returns the file path to the Shapefile')

