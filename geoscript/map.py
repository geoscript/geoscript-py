from java import awt
from java.awt import image
from javax import swing
from geoscript import geom, proj, style 
from org.geotools.geometry.jts import ReferencedEnvelope
from org.geotools.swing import JMapPane,StatusBar
from org.geotools.swing.action import PanAction, ZoomInAction, ZoomOutAction, ResetAction
from org.geotools.map import DefaultMapContext, DefaultMapLayer
from org.geotools.renderer.lite import StreamingRenderer

class Map:

   def __init__(self, name=None, srs=None):
      self.layers = []
      self.name = name
      self.crs = proj.crs.decode(srs) if srs else None

   def add(self,layer):
 
      if not layer.style:
         gtype = layer.ftype.geom()[1]
         if issubclass(gtype,(geom.Polygon, geom.MultiPolygon)):
           layer.style = style.polygon()
         elif issubclass(gtype,(geom.LineString, geom.MultiLineString)):
            layer.style = style.line()
         elif issubclass(gtype,(geom.Point, geom.MultiPoint)):
            layer.style = style.polygon()
         else:
            raise Exception('Could not determine style for layer, specify a style explicitily')

      self.layers.append(layer)

   def render(self, bounds=None, size=None, antialias=True):
      if self.crs:
         mc = DefaultMapContext(self.crs) 
      else:
         mc = DefaultMapContext() 

      if bounds:
         mc.setAreaOfInterest(ReferencedEnvelope(bounds[0],bounds[2],bounds[1],bounds[3],self.crs))

      for l in self.layers:
         ml = DefaultMapLayer(l.fs,l.style.style)
         mc.addLayer(ml)

      w,h = (size[0], size[1]) if size else (500,500)

      hints = {}
      if antialias:
        hints [awt.RenderingHints.KEY_ANTIALIASING] = awt.RenderingHints.VALUE_ANTIALIAS_ON
      
      renderer = StreamingRenderer()
      renderer.java2DHints = awt.RenderingHints(hints)

      mappane = JMapPane(renderer,mc)
      mappane.size = (w,h) 
      mappane.visible = True

      f = MapFrame(mappane)
      f.setSize(w,h)
      f.setVisible(True)

class MapFrame(swing.JFrame):

   def __init__(self, mappane):
      self.init(mappane)

   def init(self,mappane):
      self.add(mappane,awt.BorderLayout.CENTER)
      self.add(StatusBar(mappane), awt.BorderLayout.SOUTH)
            
      toolBar = swing.JToolBar()
      toolBar.setOrientation(swing.JToolBar.HORIZONTAL)
      toolBar.setFloatable(False)

      cursorToolGrp = swing.ButtonGroup()
      zoomInBtn = swing.JButton(ZoomInAction(mappane))
      toolBar.add(zoomInBtn)
      cursorToolGrp.add(zoomInBtn)

      zoomOutBtn = swing.JButton(ZoomOutAction(mappane))
      toolBar.add(zoomOutBtn)
      cursorToolGrp.add(zoomOutBtn)

      toolBar.addSeparator()

      panBtn = swing.JButton(PanAction(mappane))
      toolBar.add(panBtn)
      cursorToolGrp.add(panBtn)

      toolBar.addSeparator()

      resetBtn = swing.JButton(ResetAction(mappane))
      toolBar.add(resetBtn)

      self.add( toolBar, awt.BorderLayout.NORTH )
