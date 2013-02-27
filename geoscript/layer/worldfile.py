from java.awt.geom import AffineTransform
from org.geotools.referencing.operation.matrix import AffineTransform2D
from org.geotools.data import WorldFileReader, WorldFileWriter
from geoscript import util

class WorldFile(object):
   """
   World file reader and writer.
   """

   def __init__(self, file):
     self.file = file

   def read(self):
     f = util.toFile(self.file)
     if f is None or not f.exists():
       raise Exception('No such file %s' % self.file)

     return WorldFileReader(f)

   def pixelSize(self):
     wf = self.read()
     return (wf.getXPixelSize(), wf.getYPixelSize())

   def rotation(self):
     wf = self.read()
     return (wf.getRotationX(), wf.getRotationY())

   def ulc(self):
     wf = self.read()
     return (wf.getXULC(), wf.getYULC())

   def write(self, bbox, size): 
     scx, scy = bbox.width / size[0], -1*bbox.height / size[1]
     at = AffineTransform(scx, 0, 0, scy, bbox.west+scx/2.0, bbox.north+scy/2.0)
     
     f = util.toFile(self.file)
     WorldFileWriter(f, at)
      
