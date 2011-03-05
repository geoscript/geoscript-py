from geoscript import geom, proj, style 
from geoscript.render.window import Window
from geoscript.render.mapwindow import MapWindow

_renderers = {
  'window': Window, 'mapwindow': MapWindow
}

class Map:

   def __init__(self):
     pass

   def render(self, layer, style=None, format='window', bounds=None, size=None, **options):
     if not bounds:
       bounds = layer.bounds()
     if not size:
       size = (500,500)

     # look up the render based on format
     renderer = _renderers[format]
     if not renderer:
       raise Exception("Unrecognized format '%s'" % format)

     # instantiate it 
     renderer = renderer()
     renderer.render(layer, style, bounds, size, **options)

     self.renderer = renderer
     return renderer

   def dispose(self):
     if self.renderer and self.renderer.dispose:
       self.renderer.dispose()
