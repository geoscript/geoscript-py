from java import awt
from geoscript.render.base import RendererBase

class Window(RendererBase):
   """
   Renderer that produces a window containing the rendered image.
   """

   def _encode(self, img, g, size, **options):
      p = Panel(img, size)

      def onWindowClose(e):
        e.getWindow().dispose()
        self.dispose()

      self.window = awt.Frame(windowClosing=onWindowClose)
      if options.has_key('title'):
        self.window.setTitle(options['title'])
      self.window.add(p)
      self.window.pack()
      self.window.setVisible(True)

class Panel(awt.Panel):

   def __init__(self, img, size):
      self.setPreferredSize(awt.Dimension(*size))
      self.img = img

   def paint(self, g):
      g.drawImage(self.img, 0, 0, self)

