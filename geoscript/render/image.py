from java.io import ByteArrayOutputStream
from java.lang import String
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
      file = opts['file'] if opts.has_key('file') else None
      if file:
        # write out to file
        ImageIO.write(img, self.format, util.toFile(file))
      else:
        # write to byte array
        out = ByteArrayOutputStream()
        ImageIO.write(img, self.format, out)
        bytes = out.toByteArray()

        # check for strencode flag to check whether to return result as raw 
        # bytes or as string
        if opts.has_key('strencode'):
          return str(String(bytes, 0, 0, len(bytes)))
        return out.toByteArray()
     
