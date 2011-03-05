from java import awt
from java.awt import image
from javax import swing
from geoscript import geom, proj, style 
from org.geotools.geometry.jts import ReferencedEnvelope
from org.geotools.map import DefaultMapContext, DefaultMapLayer
from org.geotools.renderer.lite import StreamingRenderer

class Window:

   def render(self, layer, style, bounds, size, **options):
      self.map = DefaultMapContext(layer.proj._crs)
      self.map.setAreaOfInterest(bounds)

      self.map.addLayer(DefaultMapLayer(layer._source, style._style()))

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
      
      p = Panel(img, size)
      self.window = awt.Frame(windowClosing=lambda e: e.getWindow().dispose())
      if options.has_key('title'):
        self.window.setTitle(options['title'])
      self.window.add(p)
      self.window.pack()
      self.window.setVisible(True)

   def dispose(self):
      if self.map:
        self.map.dispose()

class Panel(awt.Panel):

   def __init__(self, img, size):
      self.setPreferredSize(awt.Dimension(*size))
      self.img = img

   def paint(self, g):
      g.drawImage(self.img, 0, 0, self)

