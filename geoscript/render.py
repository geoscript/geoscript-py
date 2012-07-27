"""
The :mod:`render` module provides rendering and visualization utilities.
"""
from java import awt, io
from java.awt import image
from javax import imageio
from geoscript import style as st
from geoscript.layer import Layer
from geoscript.raster import Raster
from com.vividsolutions.jts import geom
from org.geotools.map import DefaultMapContext, DefaultMapLayer
from org.geotools.renderer.lite import StreamingRenderer
from org.geotools.renderer.lite.gridcoverage2d import GridCoverageRenderer
from org.geotools.swing import JMapFrame

def render(data, style=None, bbox=None, size=None, file=None, format='png'):
   """
   Renders data to an image.

   *data* is the object being rendered. An instance of :class:`geoscript.layer.layer.Layer` or ...

   *bbox* is the optional :class:`geoscript.geom.Bounds` filter. It defaults to the bounds of the entire layer.

   *size* is the optional size of the of the resulting image. 

   *file* is the optional name of a file to render to. If left unspecified this method will instead return an array of bytes representing the image.

   *format* is the optional image format to render to. It defaults to "png".
   """

   mc = _prepareContext(data, style, bbox)
   return _renderContext(mc, size, file, format)

def view(data, bbox=None, size=(500,500)):
   mc = _prepareContext(data) 

   frame = JMapFrame(mc)
   frame.setDefaultCloseOperation(JMapFrame.DISPOSE_ON_CLOSE)
   frame.enableToolBar(True)
   frame.enableStatusBar(True)
   frame.enableTool([JMapFrame.Tool.ZOOM, JMapFrame.Tool.PAN])
   frame.size = size
   frame.setVisible(True)

def _prepareContext(data, style=None, bbox=None):
   if not bbox:
     bbox = data.extent

   if bbox.proj:
      mc = DefaultMapContext(bbox.proj._crs)
   elif data.proj:
      mc = DefaultMapContext(data.proj._crs)
   else:
      mc = DefaultMapContext() 

   mc.setAreaOfInterest(bbox)

   if not style:
     style = _computeStyle(data)

   if isinstance(data, Layer):
     mc.addLayer(DefaultMapLayer(data._source, style.style))
   elif isinstance(data, Raster):
     mc.addLayer(DefaultMapLayer(data._reader, style.style))
   else:
     raise Exception('Unable to render %s' % str(data))

   return mc

def _renderContext(mc, size, file, format):
   bbox = mc.getAreaOfInterest()

   if not size:
     size = _computeSize(bbox)

   w,h = int(size[0]), int(size[1])

   hints = {}
   hints [awt.RenderingHints.KEY_ANTIALIASING] = awt.RenderingHints.VALUE_ANTIALIAS_ON
   
   renderer = StreamingRenderer()
   renderer.java2DHints = awt.RenderingHints(hints)
   renderer.context = mc

   img = image.BufferedImage(w, h, image.BufferedImage.TYPE_4BYTE_ABGR);
   gc = img.createGraphics()
   renderer.paint(gc, awt.Rectangle(w, h), bbox)

   return _encodeImage(file, format, img) 

def _computeStyle(data):
   if isinstance(data, Layer):
      gtype = data.schema.geom.typ
      if issubclass(gtype, (geom.Point, geom.MultiPoint)):
        style = st.point()
      elif issubclass(gtype, (geom.LineString, geom.MultiLineString)):
        style = st.line()
      elif issubclass(gtype, (geom.Polygon, geom.MultiPolygon)):
        style = st.polygon()
      else:
        raise Exception('Unable to infer style for layer, please specify')
   elif isinstance(data, Raster):
      style = st.raster()

   return style

def _computeSize(bbox):
   aspect = bbox.width / bbox.height
   return (500, 500/aspect) if aspect > 1 else (500*aspect, 500)

def _encodeImage(file, format, img):
   if file:
     out = io.FileOutputStream(file)
     imageio.ImageIO.write(img, "png", out)
     out.flush() 
     out.close()
   else:
     out = io.ByteArrayOutputStream()
     imageio.ImageIO.write(img, "png", out)
     return out.toByteArray()
