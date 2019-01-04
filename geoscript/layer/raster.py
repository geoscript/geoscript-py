import os, sys
from jarray import array
from java.awt.image import DataBuffer
from javax.media.jai import RasterFactory
from geoscript import core, util
from geoscript.proj import Projection
from geoscript.geom import Bounds, Point
from geoscript.feature import Feature
from geoscript.layer.band import Band
from org.opengis.parameter import GeneralParameterValue
from org.opengis.referencing.datum import PixelInCell
from org.geotools.util.factory import Hints
from org.geotools.geometry import DirectPosition2D
from org.geotools.parameter import Parameter
from org.geotools.coverage import CoverageFactoryFinder, GridSampleDimension
from org.geotools.coverage.grid import GridCoverage2D, GridGeometry2D
from org.geotools.coverage.grid import GridEnvelope2D, GridCoordinates2D
from org.geotools.coverage.grid.io import AbstractGridFormat
from org.geotools.coverage.processing import CoverageProcessor
from org.geotools.process.raster import ScaleCoverage, CropCoverage
from org.geotools.process.raster import AddCoveragesProcess
from org.geotools.process.raster import RasterAsPointCollectionProcess

class Raster(object):

  @staticmethod
  def create(data, bounds, nband=1, bands=None, dataType=DataBuffer.TYPE_FLOAT):
    """
    Creates a new Raster. *data* may be specified as a two dimensional list or
    array. It may be also specified as 
    """
    factory = CoverageFactoryFinder.getGridCoverageFactory(None)

    if not bands:
      bands = [Band('band%d' % i) for i in range(nband)]
      
    nband = len(bands)

    if isinstance(data, list):
      # copy the data into a writeable raster
      h, w = len(data), len(data[0])
      wr = RasterFactory.createBandedRaster(dataType, w, h, nband, None)

      for j in range(len(data)):
        for i in range(len(data[j])):
          if nband > 1:
            for b in range(nband):
              wr.setSample(i, j, b, data[j][i][b])
          else:
            wr.setSample(i, j, 0, data[j][i])

      data = wr

    if nband > 1:
      coverage = factory.create('raster', data, bounds, [b._dim for b in bands])
    else:
      coverage = factory.create('raster', data, bounds)

    return Raster(None, coverage=coverage)

  def __init__(self, format, file=None, proj=None, coverage=None, reader=None,
               mode='r'):
    self.file = file
    self._format = format
    self._coverage = coverage
    self._reader = reader
    self.mode = mode

    if mode == 'r': 
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

  def bounds(self):
    env = self._coverage.getEnvelope()
    crs = env.getCoordinateReferenceSystem()
    if not crs:
      crs = self.proj 

    return Bounds(env=env, prj=crs)
 
  def getsize(self):
    grid = self._coverage.getGridGeometry().getGridRange2D()
    return (grid.width, grid.height)

  size = property(getsize, None)

  def getbands(self):
    bands = []    
    for i in range(self._coverage.getNumSampleDimensions()):
      bands.append(Band(dim=self._coverage.getSampleDimension(i)))

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

  def getdata(self):
     return self._coverage.getRenderedImage().getData() 

  data = property(getdata, None)

  def eval(self, point=None, pixel=None):
     """
     Returns the value of the raster at the specified location.
  
     The location can be specified with the *point* parameter (world space) or
     with the *pixel* parameter (image space).
     """
     if point:
       p = Point(point)
     elif pixel:
       p = self.point(pixel)
     else:
       p = self.point((0,0))

     return list(self._coverage.evaluate(DirectPosition2D(p.x, p.y)))

  def write(self, raster):
     """
     Replaces the content of this raster. 

     The *raster* parameter is a :class:`Raster` to write out.
     """
     if self.mode != 'w':
       raise Exception('Raster not created in write mode')

     w = self._format.getWriter(util.toFile(self.file))
     w.write(raster._coverage, None)
     w.dispose()

  def point(self, pixel):
     """
     Maps a coordinate from world space to pixel space returning the result as a
     :class:`Point <geoscript.geom.point.Point>` object.

     The *pixel* parameter may be specified as an x/y ``tuple`` or ``list`` or
     as a :class:`Point <geoscript.geom.point.Point>` object.
     """
     p = Point(pixel)
     gg = self._coverage.getGridGeometry()
     dp = gg.gridToWorld(GridCoordinates2D(int(p.x), int(p.y)))
     return Point(dp.x, dp.y)
  
  def pixel(self, point):
     """
     Maps a coordinate from pixel space to world space returning the result as a
     :class:`Point <geoscript.geom.point.Point>` object.

     The *point* parameter may be specified as an x/y ``tuple`` or ``list`` or
     as a :class:`Point <geoscript.geom.point.Point>` object.
     """
     p = Point(point)
     gg = self._coverage.getGridGeometry()
     dp = gg.worldToGrid(DirectPosition2D(p.x, p.y))
     return (dp.x, dp.y)
    
  def resample(self, bbox=None, rect=None, size=None):
     """
     Resamples this raster returning a new raster. The *bbox* argument specifies
     the subset in model/world space to resample. Alternatively the *rect*
     argument can be used to specify the subset in pixel space.

     The *size* argument defines the size of the resulting raster. If not 
     specified the resulting size will be calculated proportionally to the 
     the *bbox* or *rect* arguments.
     """
     if not bbox:
       if rect:
         # compute bounds from rectangle in pixel space
         dx, dy = self.pixelsize
         #dx = rect[2] / float(self.size[0])
         #dy = rect[3] / float(self.size[1])

         e = self.extent
         bbox = Bounds(e.west + rect[0]*dx, e.south + rect[1]*dy, 
          e.west + (rect[0]+rect[2])*dx, e.south + (rect[1]+rect[3])*dy, e.proj)
       else:
         # no bbox or rectangle, use full extent
         bbox = self.extent

     if not size:
       if not rect:
         # auto compute size based on bounding box ratio
         e = self.extent
         w = int(self.size[0] * bbox.width / e.width)
         size = (w, int(w * e.aspect))
       else:
         size = rect[2], rect[3]

     gg = GridGeometry2D(GridEnvelope2D(0,0,*size), bbox)
     result =  self._op('Resample', Source=self._coverage, 
       CoordinateReferenceSystem=self.proj._crs, GridGeometry=gg)

     return Raster(self._format, coverage=result, reader=self._reader)

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

  def histogram(self, low=None, high=None, nbins=None):
    """
    Computes a histogram for the raster.  

    *low* specifies the lowest (inclusive) pixel value to include and *high* 
    specifies the highest (exclusive) pixel value to include.

    *nbins* specifies the number of bins/buckets of the resulting histogram.

    This method returns a :class:`Histogram <geoscript.layer.raster.Histogram>`
    instance.
    """
    nb = len(self.bands)

    params = {'Source': self._coverage}
    if low: 
      low = low if isinstance(low, (tuple, list)) else [low]*nb
      params['lowValue'] = array(low, 'd')
    if high:
      high = high if isinstance(high, (tuple, list)) else [high]*nb
      params['highValue'] = array(high, 'd')
    if nbins:
      nbins = nbins if isinstance(nbins, (tuple, list)) else [nbins]*nb
      params['numBins'] = array(nbins, 'i')

    h = self._op('Histogram', **params).getProperty('histogram') 
    return Histogram(h)

  def extrema(self):
    """
    Computes the min and max values of each band in the raster.

    This method returns a (min,max) ``tuple`` in which each element is a 
    ``list`` consisting of the min or max value corresponding to each band. 
    """
    result = self._op('Extrema', Source=self._coverage).getProperty('extrema')
    return tuple([list(x) for x in result])

  def features(self):
    """
    Returns the contents of the raster as a 
    :class:`Feature <geoscript.feature.Feature>` generator by converting each
    cell/pixel into a feature object.
 
    Each returned feature has a :class:`Point <geoscript.geom.Point>` geometry 
    corresponding to the location of the center of the pixel. The feature also
    contains attributes corresponding to the bands of the raster, which values
    corresponding to the band value for the pixel.
    """
    pcp = RasterAsPointCollectionProcess()
    result = pcp.execute(self._coverage)
    
    it = result.features()
    while it.hasNext(): 
      f = it.next()
      yield Feature(f=f)

    it.close()
 
  def dispose(self):
    if self._reader:
      self._reader.dispose()

    if self._coverage:
      self._coverage.dispose(False)

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

core.registerTypeMapping(GridCoverage2D, Raster, lambda x: Raster(None, coverage=x))
core.registerTypeUnmapping(Raster, GridCoverage2D, lambda x: x._coverage)

class Histogram(object):

  def __init__(self, histo):
    self._histo = histo

  def bin(self, i, band=0):
    h = self._histo
    if i < h.getNumBins(band):
      return (h.getBinLowValue(band, i), h.getBinLowValue(band, i+1))

  def bins(self, band=0):
    return [self.bin(i, band) for i in range(len(self))]

  def count(self, i, band=0):
    return self._histo.getBinSize(band, i)

  def counts(self, band=0):
    return [self.count(i, band) for i in range(len(self))]

  def __len__(self):
    return self._histo.getNumBins(0)

  def __getitem__(self, key):
    return self.count(key)
