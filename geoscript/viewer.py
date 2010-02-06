from java import awt
from javax import swing
from java.awt.geom import AffineTransform
from com.vividsolutions.jts.geom import GeometryFactory
from com.vividsolutions.jts.geom import Polygon, MultiPolygon
from org.geotools.geometry.jts import LiteShape

_fac = GeometryFactory()

def draw(g, size=(500,500)):
  """
  Draws a geometry onto a canvas.

  *size* is a tuple that specifies the dimensions of the canvas the geometry will drawn upon. 
  """
  buf = 50.0

  if not isinstance(g, list):
    g = [g]

  e = _fac.createGeometryCollection(g).getEnvelopeInternal()
  scale = size[0] / e.width if e.width > 0 else sys.maxint
  scale = min(scale, size[1] / e.height) if e.height > 0 else 1 

  tx = -1*e.minX
  ty = -1*e.minY
       
  at = AffineTransform()
  
  # scale to size of canvas (inverting the y axis)
  at.scale(scale,-1*scale)
  
  # translate to the origin
  at.translate(tx,ty)

  # translate to account for invert
  at.translate(0,-1*size[1]/scale)

  # buffer
  at.translate(buf/scale,-1*buf/scale)
        
  class Panel(swing.JPanel):

    def __init__(self, geoms, atx):
      self.geoms = geoms
      self.atx = atx

    def paintComponent(self, gc):
      opaque = gc.getComposite()      
      gc.setRenderingHint(awt.RenderingHints.KEY_ANTIALIASING, 
        awt.RenderingHints.VALUE_ANTIALIAS_ON)
      gc.setStroke(awt.BasicStroke(2))

      i = 0
      for g in self.geoms:
        shp = LiteShape(g, self.atx, False)

        if isinstance(g, (Polygon, MultiPolygon)):
          i = i + 1
          gc.setColor(awt.Color.WHITE)
          gc.setComposite(awt.AlphaComposite.getInstance(awt.AlphaComposite.SRC_OVER, 0.5))
          gc.fill(shp)

        gc.setComposite(opaque)
        gc.setColor(awt.Color.BLACK)
        gc.draw(shp)

  panel = Panel(g, at)
  s = tuple([int(size[x]+2*buf) for x in range(2)])
  panel.preferredSize = s
  frame = swing.JFrame()
  frame.contentPane = panel
  frame.pack()
  frame.visible = True

