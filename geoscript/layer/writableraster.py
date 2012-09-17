from geoscript.layer.raster import Raster
import math
from javax.media.jai import RasterFactory
from geoscript.layer.band import Band
from org.geotools.coverage import CoverageFactoryFinder
from geoscript.geom.bounds import Bounds

class WritableRaster(Raster):
     
    def __init__(self, bounds, cellsize, nband=1, dataType=Raster.DATA_TYPE_FLOAT):
        '''
        Creates a new writable raster layer, with all cells set to zero. Cells are supposed to be filled
        by using the methods in this class.
        
        Using this class is preferred to directly creating and array and using the create method 
        in the :class:`Raster` class, as it will ensure better handling of data, specially in 
        the case or large layers.
        
        *cellsize* is used as both vertical and horizontal cellsize. This method does not support creation
        of layers with different cellsizes.
        
        *bounds* might be extended in case east-west or north-south span is not a multiple of cellsize 
        
        Use *nbands* to set the number of bands. 
        
        the *dataType* parameter defines the type of data to use for the layer to create, which
        is represented as a constant DATA_TYPE_XXX from this same class
        
        Note that not all operations available for a Raster object are available when it is created this
        way. You are supposed to fill the values and then call the :meth:`getraster` method to create a Raster
        object that support querying and other operations. While it is being edited, most of them will result
        in an exception being raised.
        
        In particular, only the getvalueatcell method is implemented, and should be the only one used, apart 
        form the ones used to set cell values.
        '''
          
        self.width = w = int(math.ceil((bounds.geteast() - bounds.getwest()) / cellsize))
        self.height = h = int(math.ceil((bounds.getnorth() - bounds.getsouth()) / cellsize))          
        self.writable = RasterFactory.createBandedRaster(dataType, w, h, nband, None)                   
        bands = [Band('band%d' % i) for i in range(nband)]
        self.bounds = Bounds(bounds.getwest(), bounds.getsouth(), 
                             bounds.getwest() + w * cellsize,
                             bounds.getsouth() + h * cellsize, 
                             bounds.getproj())
        self.nodatavalue = Raster.DEFAULT_NO_DATA
        self._bands = bands
        
    def getextent(self):
        return self.bounds
     
    def getsize(self):    
        return (self.width, self.height)
    
    def getraster(self):
        factory = CoverageFactoryFinder.getGridCoverageFactory(None)
        if len(self._bands) > 1:
            coverage = factory.create('raster', self.writable, self.bounds, [b._dim for b in self._bands])
        else:
            coverage = factory.create('raster', self.writable, self.bounds)

        return Raster(coverage=coverage)
    
    def getvalueatcell(self, x, y, band=0):
        try:      
            if self.isinwindow(x, y): 
                return self.writable.getSampleDouble(x, y, band)
            else:
                return self.nodatavalue
        except:      
            return self.nodatavalue

    def setvalueatcell(self, x, y, band, value):    
        if self.isinwindow(x, y): 
            return self.writable.setSample(x, y, band, value)
    