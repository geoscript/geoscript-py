from geoscript.render.image import Image

class PNG(Image):
   """
   Renderer that produces a PNG image.
   """
   def __init__(self):
     Image.__init__(self, 'png')
