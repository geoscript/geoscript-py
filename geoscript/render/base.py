from java import awt
from java.awt import image
from geoscript import geom, proj, style 
from geoscript.layer import Raster
from org.geotools.geometry.jts import ReferencedEnvelope
from org.geotools.map import MapContent, FeatureLayer, GridCoverageLayer
from org.geotools.renderer.lite import StreamingRenderer

class RendererBase:
   """
   Base class for renderers that make use of StreamingRenderer.
   """

   def render(self, layers, styles, bounds, size, **options):
      self.map = MapContent()
      self.map.getViewport().setCoordinateReferenceSystem(bounds.proj._crs)
      self.map.getViewport().setBounds(bounds)

      for i in range(len(layers)): 
        l = layers[i]

        data = l._coverage if isinstance(l,Raster) else l._source
        mapLayer = GridCoverageLayer(data, styles[i]._style()) if isinstance(l,Raster) else FeatureLayer(data, styles[i]._style())
        self.map.addLayer(mapLayer)

      w,h = (size[0], size[1]) 

      hints = {}
      hints [awt.RenderingHints.KEY_ANTIALIASING] = awt.RenderingHints.VALUE_ANTIALIAS_ON
      
      renderer = StreamingRenderer()
      renderer.setJava2DHints(awt.RenderingHints(hints))
      renderer.setMapContent(self.map)

      img = image.BufferedImage(w, h, image.BufferedImage.TYPE_INT_ARGB)
      g = img.getGraphics()
      g.setColor(style.Color(options["bgcolor"]).expr.value if options.has_key("bgcolor") else awt.Color.white)
      g.fillRect(0, 0, w, h)
      
      renderer.paint(g, awt.Rectangle(w,h), bounds)
      return self._encode(img, g, size, **options)   

   def _encode(self, img, g, size, **options):
      pass

   def dispose(self):
      if self.map:
        self.map.dispose()

