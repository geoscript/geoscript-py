from geoscript.render.image import Image

class JPEG(Image):
   """
   Renderer that produces a JPEG image.
   """

   def __init__(self):
     Image.__init__(self, 'jpeg')
