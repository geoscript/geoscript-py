import unittest
import threading, time
from geoscript.style import *
from geoscript.render import Map
from geoscript.layer import Shapefile
from geoscript.layer import GeoTIFF

def points():
   return Shapefile('work/point.shp')

def lines():
   return Shapefile('work/line.shp')

def polygons():
   return Shapefile('work/polygon.shp')

def raster():
   return GeoTIFF('data/sfdem.tif')

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

def render(style, layer, title):
   w = Worker(layers=layer, styles=style, title=title)
   w.start()
   time.sleep(2)
   w.dispose()

tests = [
  (Stroke(), lines, "simple stroke"), 
  (Stroke()+Stroke().hatch('vertline').zindex(1), lines, "stroke with hatch"), 
  (Stroke()+Label('name'), lines, "simple label"),
  (Stroke()+Label('name').linear(), lines, "simple linear label"),
  (Stroke()+Label('name').linear(25), lines,"simple label with line placement"),
  (Stroke()+Label('name').linear(follow=True), lines, "curved label"),
  (Stroke()+Label('name').linear(offset=25, follow=True), lines, "curved label with offset"),
  (Stroke()+Label('name').font('bold 16px "Times New Roman"'), lines, "label with font"), 
  (Fill(), polygons, "simple polygon"),
  (Stroke(), polygons, "polygon no fill"),
  (Fill()+Label('name'), polygons, "polygon with label"),
  #  (Fill() + Label('name').font('16px "Times New Roman"').halo(), polygons,  "polygon label with halo") ,
  (Fill().hatch('backslash'), polygons, "polygon with hatch"),
  (Icon('data/hospital16.png'), points, 'simple icon'),
  (ColorMap(zip([0,1000,2000],['red','green','blue'])), raster, 'color map')
]

def test():
   from java.lang import System 
   if not System.getProperty("java.awt.headless"):
     for t in tests:
       yield render, t[0], t[1](), t[2]

