from geoscript import geom, proj
from geoscript.style import Stroke, Shape
from geoscript.render.window import Window
from geoscript.render.mapwindow import MapWindow

_renderers = {
  'window': Window, 'mapwindow': MapWindow
}

class Map:

   def __init__(self, layers, styles=[]):
     self.layers = layers if isinstance(layers, (list)) else [layers]
     self.styles = []
     for i in range(len(layers)):
       if i < len(styles):
         self.styles.append(styles[i])
       else:
         if layers[i].schema.geom.typ.__name__ in ['Point', 'MultiPoint']:
           style = Shape()
         else:
           style = Stroke()
         self.styles.append(style)

   def render(self, format='window', bounds=None, size=None, **options):
     if not bounds:
       # calulate bounds for layers, merge all bounds together
       bounds = reduce(lambda x,y:x+y, map(lambda x:x.bounds(), self.layers))
     if not size:
       size = (500, int(500 * bounds.height / bounds.width))

     # look up the render based on format
     renderer = _renderers[format]
     if not renderer:
       raise Exception("Unrecognized format '%s'" % format)

     # instantiate it 
     renderer = renderer()
     renderer.render(self.layers, self.styles, bounds, size, **options)

     self.renderer = renderer
     return renderer

   def dispose(self):
     if self.renderer and self.renderer.dispose:
       self.renderer.dispose()
