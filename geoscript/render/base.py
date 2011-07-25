from java import awt
from java.awt import image
from geoscript import geom, proj, style 
from org.geotools.geometry.jts import ReferencedEnvelope
from org.geotools.map import DefaultMapContext, DefaultMapLayer
from org.geotools.renderer.lite import StreamingRenderer

class RendererBase:
   """
   Base class for renderers that make use of StreamingRenderer.
   """

   def render(self, layers, styles, bounds, size, **options):
      self.map = DefaultMapContext(bounds.proj._crs)
      self.map.setAreaOfInterest(bounds)

      for i in range(len(layers)): 
        self.map.addLayer(DefaultMapLayer(layers[i]._source,styles[i]._style()))

      w,h = (size[0], size[1]) 

      hints = {}
      hints [awt.RenderingHints.KEY_ANTIALIASING] = awt.RenderingHints.VALUE_ANTIALIAS_ON
      
      renderer = StreamingRenderer()
      renderer.setJava2DHints(awt.RenderingHints(hints))
      renderer.setContext(self.map)

      img = image.BufferedImage(w, h, image.BufferedImage.TYPE_INT_ARGB)
      g = img.getGraphics()
      g.setColor(awt.Color.white)
      g.fillRect(0, 0, w, h)
      
      renderer.paint(g, awt.Rectangle(w,h), bounds)
      self._encode(img, g, size, **options)   

   def _encode(self, img, g, size, **options):
      pass

   def dispose(self):
      if self.map:
        self.map.dispose()

