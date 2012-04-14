import os, sys
from geoscript import util
from geoscript.proj import Projection
from geoscript.geom import Bounds
from geoscript.layer.band import Band
from org.geotools.factory import Hints

class Raster(object):

  def __init__(self, format, file, proj):
    self.file = file
    self._format = format

    hints = Hints()
    if proj:
      proj = Projection(proj)
      
      hints.put(Hints.DEFAULT_COORDINATE_REFERENCE_SYSTEM, proj._crs) 

    self._reader = format.getReader(util.toFile(file), hints)
    self._coverage = self._reader.read(None)

  def getname(self):
     return os.path.basename(self.file)

  name = property(getname, None)

  def getformat(self):
    return str(self._format.getName())

  format = property(getformat, None)

  def getproj(self):
    crs = self._coverage.getCoordinateReferenceSystem2D()
    if crs:
      return Projection(crs) 

  proj = property(getproj, None)

  def getextent(self):
    env = self._coverage.getEnvelope()
    crs = env.getCoordinateReferenceSystem()
    if not crs:
      crs = self.proj 

    return Bounds(env=env, prj=crs)
 
  extent = property(getextent, None)

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
    b = self.extent
    s = self.size
    return (b.width/s[0], b.height/s[1])

  pixelsize = property(getpixelsize, None)

  def render(self):
    self._coverage.show()

