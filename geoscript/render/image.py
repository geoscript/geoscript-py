from javax.imageio import ImageIO
from geoscript import util
from geoscript.render.base import RendererBase

class Image(RendererBase):
   """
   Base class for image based renderers.
   """

   def __init__(self, format):
     self.format = format

   def _encode(self, img, g, size, **opts):
      file = opts['file'] if opts.has_key('file') else '%s.%s' % (opts['title'],
         self.format)
      ImageIO.write(img, self.format, util.toFile(file))
