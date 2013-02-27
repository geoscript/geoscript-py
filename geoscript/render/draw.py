from geoscript.feature import Feature
from geoscript.layer import Layer, Raster
from geoscript.render import Map
from geoscript.style import Stroke
from geoscript.workspace import Memory

def draw(obj, style=None, bounds=None, size=None, format=None, **options):
  """
  Draws an object onto a canvas.

  *obj* can be a geometry, list of geometries, or a :class:`Layer <geoscript.layer.layer.Layer>`.

  *style* is a :class:`Symbolizer <geoscript.style.symbolizer.Symbolizer>` that specifies how to render the object.

  *size* is a tuple that specifies the dimensions of the canvas the object will drawn upon. 

  *format* is the format or renderer to use for rendering.
  """

  if isinstance(obj, (Layer,Raster)):
    layer = obj
  else:
    obj = obj if isinstance(obj, list) else [obj]

    # wrap up geometries/features in a layer for rendering
    mem = Memory()

    if isinstance(obj[0], Feature):
      layer = mem.create(schema=obj[0].schema)
    else:
      layer = mem.create("feature")

    for o in obj:
      layer.add(o if isinstance(o, Feature) else [o])

  # create a map and render
  if not bounds:
    bounds = layer.bounds().scale(1.1)

  map = Map([layer], [style] if style else [])
  return map.render(format=format, bounds=bounds, size=size, **options) 
