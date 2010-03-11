"""
The :mod:`render` module provides rendering and visualization utilities.
"""

from java import awt, io
from java.awt import image
from javax import imageio
from geoscript import style as st
from com.vividsolutions.jts import geom
from org.geotools.map import DefaultMapContext, DefaultMapLayer
from org.geotools.renderer.lite import StreamingRenderer

def render(layer, style=None, bbox=None, size=None, file=None, format='png'):
   """
   Renders a layer.

   *layer* is the :class:`geoscript.layer.layer.Layer` to render.

   *bbox* is the optional :class:`geoscript.geom.Bounds` filter. It defaults to the bounds of the entire layer.

   *size* is the optional size of the of the resulting image. 

   *file* is the optional name of a file to render to. If left unspecified this method will instead return an array of bytes representing the image.

   *format* is the optional image format to render to. It defaults to "png".
   """

   if not style:
      gtype = layer.schema.geom.typ
      if issubclass(gtype, (geom.Point, geom.MultiPoint)):
        style = st.point()
      elif issubclass(gtype, (geom.LineString, geom.MultiLineString)):
        style = st.line()
      elif issubclass(gtype, (geom.Polygon, geom.MultiPolygon)):
        style = st.polygon()
      else:
        raise Exception('Unable to infer style for layer, please specify')
   if not bbox:
      bbox = layer.bounds() 

   if bbox.proj:
      mc = DefaultMapContext(bbox.proj._crs)
   elif layer.proj:
      mc = DefaultMapContext(layer.proj._crs)
   else:
      mc = DefaultMapContext() 

   mc.setAreaOfInterest(bbox)
   mc.addLayer(DefaultMapLayer(layer.fs, style.style))

   aspect = bbox.width / bbox.height
   if not size:
     size = (500, 500/aspect) if aspect > 1 else (500*aspect, 500)
   w,h = int(size[0]), int(size[1])

   hints = {}
   hints [awt.RenderingHints.KEY_ANTIALIASING] = awt.RenderingHints.VALUE_ANTIALIAS_ON
   
   renderer = StreamingRenderer()
   renderer.java2DHints = awt.RenderingHints(hints)
   renderer.context = mc

   img = image.BufferedImage(w, h, image.BufferedImage.TYPE_4BYTE_ABGR);
   gc = img.createGraphics()
   renderer.paint(gc, awt.Rectangle(w, h), bbox)

   if file:
     out = io.FileOutputStream(file)
     imageio.ImageIO.write(img, "png", out)
     out.flush() 
     out.close()
   else:
     out = io.ByteArrayOutputStream()
     imageio.ImageIO.write(img, "png", out)
     return out.toByteArray()
