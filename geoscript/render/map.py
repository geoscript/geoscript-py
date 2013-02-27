from geoscript import geom, proj
from geoscript.layer import Raster
from geoscript.style import Stroke, Shape, Opacity
from geoscript.render.window import Window
from geoscript.render.mapwindow import MapWindow
from geoscript.render.png import PNG
from geoscript.render.jpeg import JPEG
from geoscript.render.gif import GIF

_renderers = {
  'window': Window, 'mapwindow': MapWindow, 'png': PNG, 'jpeg': JPEG,
  'gif': GIF
}

class Map:

   def __init__(self, layers, styles=[], title=None):
     self.layers = layers if isinstance(layers, list) else [layers]
     self.styles = styles if isinstance(styles, list) else [styles]

     for i in range(len(self.layers)):
       if i < len(self.styles):
         self.styles.append(self.styles[i])
       else:
         l = self.layers[i]
         if hasattr(l, 'style'):
           style = l.style
         else:
           if isinstance(l, Raster):
               style = Opacity()
           else:
             if l.schema.geom.typ.__name__ in ['Point', 'MultiPoint']:
               style = Shape()
             else:
               style = Stroke()
         self.styles.append(style)

     self.title = title if title else layers[0].name

   def render(self, format=None, bounds=None, size=None, **options):
     if not bounds:
       # calulate bounds for layers, merge all bounds together
       bounds = reduce(lambda x,y:x+y, map(lambda x:x.bounds(), self.layers))
     else:
       # bounds may be a "raw" envelope
       if not isinstance(bounds, geom.Bounds):
         bounds = geom.Bounds(env=bounds)

     # handle the case of a 0 width/height bounds, might happen if rendering
     # a single point, or a single verticle/horizontal line
     if bounds.width == 0 or bounds.height == 0:
       if bounds.height > 0:
         h = bounds.height/2.0
         bounds = geom.Bounds(bounds.west-h, bounds.south, bounds.east+h, 
           bounds.north, bounds.proj)
       elif bounds.width > 0:
         w = bounds.width/2.0
         bounds = geom.Bounds(bounds.west, bounds.south-w, bounds.east, 
           bounds.south+w, bounds.proj)
       else: 
         e = geom.Point(bounds.west, bounds.south).buffer(0.1).getEnvelopeInternal()
         bounds = geom.Bounds(env=e, prj=bounds.proj)

     # try to ensure the bounds has a projection
     if not bounds.proj and self.layers[0].proj:
       # use the layer projection
       bounds = geom.Bounds(env=bounds, prj=self.layers[0].proj) 


     if not size:
         size = (500, int(500 * bounds.height / bounds.width))

     format = format if format else 'window'

     # look up the render based on format
     renderer = _renderers[format]
     if not renderer:
       raise Exception("Unrecognized format '%s'" % format)

     # instantiate it 
     renderer = renderer()

     # set some options
     if self.title and not options.has_key('title'):
       options['title'] = self.title

     obj = renderer.render(self.layers, self.styles, bounds, size, **options)

     self.renderer = renderer
     return obj if obj else renderer

   def dispose(self):
     if self.renderer and self.renderer.dispose:
       self.renderer.dispose()

