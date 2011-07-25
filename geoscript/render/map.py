from geoscript import geom, proj
from geoscript.style import Stroke, Shape
from geoscript.render.window import Window
from geoscript.render.mapwindow import MapWindow
from geoscript.render.png import PNG
from geoscript.render.jpeg import JPEG

_renderers = {
  'window': Window, 'mapwindow': MapWindow, 'png': PNG, 'jpeg': JPEG
}

class Map:

   def __init__(self, layers, styles=[], title=None):
     self.layers = layers if isinstance(layers, list) else [layers]
     self.styles = styles if isinstance(styles, list) else [styles]

     for i in range(len(self.layers)):
       if i < len(self.styles):
         self.styles.append(self.styles[i])
       else:
         if self.layers[i].schema.geom.typ.__name__ in ['Point', 'MultiPoint']:
           style = Shape()
         else:
           style = Stroke()
         self.styles.append(style)

     self.title = title if title else layers[0].schema.name

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

     # set some options
     if self.title and not options.has_key('title'):
       options['title'] = self.title

     renderer.render(self.layers, self.styles, bounds, size, **options)

     self.renderer = renderer
     return renderer

   def dispose(self):
     if self.renderer and self.renderer.dispose:
       self.renderer.dispose()

