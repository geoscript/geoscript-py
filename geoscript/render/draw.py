from geoscript.layer import Layer
from geoscript.render import Map
from geoscript.style import Stroke
from geoscript.workspace import Memory

def draw(obj, style=None, size=None, format=None):
  """
  Draws an object onto a canvas.

  *obj* can be a geometry, list of geometries, or a :class:`Layer <geoscript.layer.layer.Layer>`.

  *style* is a :class:`geoscript.style.symbolizer.Symbolizer` that specifies how to render the object.

  *size* is a tuple that specifies the dimensions of the canvas the object will drawn upon. 

  *format* is the format or renderer to use for rendering.
  """

  if isinstance(obj, Layer):
    layer = obj
  else:
    obj = obj if isinstance(obj, list) else [obj]

    # wrap up the geometries features
    mem = Memory()
    layer = mem.create("feature")
    for geom in g:
      layer.add([geom])

  # create a map and render
  map = Map([layer], [style] if style else [])
  map.render(format=format, bounds=layer.bounds().scale(1.1), size=size) 
