import os, sys
from jarray import array
from geoscript import util
from geoscript.proj import Projection
from geoscript.geom import Bounds
from geoscript.layer.band import Band
from org.geotools.factory import Hints
from org.geotools.coverage import CoverageFactoryFinder
from org.geotools.coverage.processing import CoverageProcessor
from org.geotools.process.raster.gs import ScaleCoverage, CropCoverage
from org.geotools.process.raster.gs import AddCoveragesProcess

class Raster(object):

  @staticmethod
  def create(data, bounds):
    factory = CoverageFactoryFinder.getGridCoverageFactory(None)
    coverage = factory.create('raster', data, bounds)
    return Raster(None, coverage=coverage)

  def __init__(self, format, file=None, proj=None, coverage=None, reader=None):
    self.file = file
    self._format = format
    self._coverage = coverage
    self._reader = reader

    if not coverage:
      if not reader:
        hints = Hints()
        if proj:
          proj = Projection(proj)
          hints.put(Hints.DEFAULT_COORDINATE_REFERENCE_SYSTEM, proj._crs) 

        self._reader = format.getReader(util.toFile(file), hints)
      self._coverage = self._reader.read(None)

  def getname(self):
    return os.path.basename(self.file) if self.file else 'raster'

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

  def scale(self, x, y, interp='nearest'):
    sc = ScaleCoverage()
    i = util.jai.interpolation(interp) 
    result = sc.execute(self._coverage, x, y, 0, 0, i)
    return Raster(self._format, coverage=result, reader=self._reader)

  def crop(self, geom):
    cc = CropCoverage()
    result = cc.execute(self._coverage, geom, None)
    return Raster(self._format, coverage=result, reader=self._reader)

  def __add__(self, other):
    if isinstance(other, Raster):
      result = self._op('Add', Source0=self._coverage, Source1=other._coverage)
    else:
      result = self._op('AddConst', Source=self._coverage, constants=
        array(other if isinstance(other, (list,tuple)) else [other], 'd'))

    return Raster(self._format, coverage=result)
   
  def __sub__(self, other):
    if isinstance(other, Raster):
      return self.__add__(-other)
    else:
      result = self._op('SubtractConst', Source=self._coverage, constants=
        array(other if isinstance(other, (list,tuple)) else [other], 'd'))
      return Raster(self._format, coverage=result)

  def __mul__(self, other):
    if isinstance(other, Raster):
      result = self._op('Multiply', Source0=self._coverage, 
        Source1=other._coverage)
    else:
      result = self._op('MultiplyConst', Source=self._coverage, constants=
        array(other if isinstance(other, (list,tuple)) else [other], 'd'))

    return Raster(self._format, coverage=result)

  def __div__(self, other):
    if isinstance(other, Raster):
      result = self._op('DivideIntoConst', Source=other._coverage, constants=
        array([1], 'd'))
      return self.__mul__(Raster(other._format, coverage=result))
    else:
      result = self._op('DivideByConst', Source=self._coverage, constants=
        array(other if isinstance(other, (list,tuple)) else [other], 'd'))
    return Raster(self._format, coverage=result)

  def __neg__(self): 
    result = self._op('Invert', Source=self._coverage)
    return Raster(self._format, coverage=result, reader=self._reader)
    
  def __invert__(self):
    pass

  def _op(self, name, **params):
    op = CoverageProcessor.getInstance().getOperation(name)
    p = op.getParameters()
    for k,v in params.iteritems():
      p.parameter(k).setValue(v)

    return op.doOperation(p, None)
