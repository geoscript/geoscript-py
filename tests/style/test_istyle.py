import unittest
import threading, time
from geoscript.style import *
from geoscript.render import Map
from geoscript.layer import Shapefile

class InteractiveStyle_Test:

  def testStrokeSimple(self):
    self.render(Stroke(), self.lines(), "simple stroke") 

  def testStrokeHatch(self):
    self.render(Stroke() + Stroke().hatch('vertline').zindex(1), self.lines(), "stroke with hatch") 

  def testLabelSimple(self):
    self.render(Stroke() + Label('name'), self.lines(), "simple label") 

  def testLabelLinear(self):
    self.render(Stroke() + Label('name').linear(), self.lines(), "simple linear label")

  def testLabelLinearOffset(self):
    self.render(Stroke() + Label('name').linear(25), self.lines(), "simple label with line placement") 

  def testLabelCurved(self):
    self.render(Stroke() + Label('name').linear(follow=True), self.lines(), "curved label") 

  def testLabelCurvedOffset(self):
    self.render(Stroke() + Label('name').linear(offset=25, follow=True), self.lines(), "curved label with offset") 

  def testLabelFont(self):
    self.render(Stroke() + Label('name').font('bold 16px "Times New Roman"'), self.lines(), "label with font") 

  def testPolySimple(self):
    self.render(Fill(), self.polygons(), "simple polygon")

  def testPolyWithNoFill(self):
    self.render(Stroke(), self.polygons(), "polygon no fill")

  def testPolyLabel(self):
    self.render(Fill() + Label('name'), self.polygons(), "polygon with label")

  """
  def testPolyLabelWithHalo(self):
    self.render(Fill() + Label('name').font('16px "Times New Roman"').halo(), self.polygons(),  "polygon label with halo") 

  """

  def testPolyHatch(self):
    self.render(Fill().hatch('backslash'), self.polygons(), "polygon with hatch")
  def testIcon(self):
    self.render(Icon('data/hospital16.png'), self.points(), 'simple icon')

  def render(self, style, layer, title):
    w = Worker(layers=layer, styles=style, title=title)
    w.start()
    time.sleep(2)
    w.dispose()
    
  def points(self):
    return Shapefile('work/point.shp')

  def lines(self):
    return Shapefile('work/line.shp')

  def polygons(self):
    return Shapefile('work/polygon.shp')

class Worker(threading.Thread):

   def __init__(self, **kwargs):
     threading.Thread.__init__(self)
     self.args = kwargs

   def run(self):
     self.map = Map(**self.args)
     self.renderer = self.map.render()

   def dispose(self):
     self.renderer.window.dispose()
     self.map.dispose()
