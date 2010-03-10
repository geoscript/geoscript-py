import sys
from geoscript import util
from geoscript.proj import Projection
from geoscript.geom import Bounds
from geoscript.raster.band import Band

class Raster(object):

  def __init__(self, reader):
    self.file = file
    self._reader = reader
    self._coverage = reader.read(None)

  def getformat(self):
    return str(self._reader.getFormat().getName())

  format = property(getformat, None)

  def getproj(self):
    crs = self._coverage.getCoordinateReferenceSystem2D()
    if crs:
      return Projection(crs) 

  proj = property(getproj, None)

  def getbounds(self):
    env = self._coverage.getEnvelope()
    crs = env.getCoordinateReferenceSystem()
    if not crs:
      crs = self.proj 

    return Bounds(env=env, prj=crs)
 
  bounds = property(getbounds, None)

  def getsize(self):
    grid = self._coverage.getGridGeometry().getGridRange2D()
    return (grid.width, grid.height)

  size = property(getsize, None)

  def getbands(self):
    bands = []    
    for i in range(self._coverage.getNumSampleDimensions()):
      bands.append(Band(self._coverage.getSampleDimension(i)))

    return bands

  bands = property(getbands, None)

  def getblocksize(self):
    return tuple(self._coverage.getOptimalDataBlockSizes())

  blocksize = property(getblocksize, None)

  def getpixelsize(self):
    b = self.bounds
    s = self.size
    return (b.width/s[0], b.height/s[1])

  pixelsize = property(getpixelsize, None)

  def render(self):
    self._coverage.show()

   
