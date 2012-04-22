from os import path
from java import net
from geoscript import util
from geoscript.layer import Layer

class GML(Layer):
  """
  A subclass of :class:`Layer <geoscript.layer.layer.Layer>` for the GML format.

  *file* is the path to the GML file as a ``str``.
  """
  def __init__(self, file):
    name = path.splitext(path.basename(file))[0]

    from geoscript.workspace.ogr import OGR
    Layer.__init__(self, name, OGR(file))


