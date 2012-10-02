
from geoscript.processing.sampledata import sampledata

'''An example takes a monoband raster layer and applies a convolution kernel filter on it,
generating a new one.

'''
from geoscript.layer.raster import Raster



if __name__ == '__main__':  
    
    #a 3x3 low-pass (smoothing) kernel  
    kernel = [1.0/ 9.0] * 9
    layer = sampledata.get('ortho')            
    width, height = layer.getsize()  
    data = [[0 for x in xrange(width)] for x in xrange(height)]     
    for y in range(height):
        for x in range(width):
            value = layer.getvalueatcell(x,y)
            cellsum = 0
            ikernel = 0                        
            for i in range (-1,2):
                for j in range (-1,2):
                    value = layer.getvalueatcell(x + j, y + i)
                    #value might be equal nodatavalue in the border cells
                    #we, however, assume that no pixel within the image will have a 
                    #nodata value 
                    if not layer.isnodatavalue(value):                                                                                                    
                        cellsum += value * kernel[ikernel]
                ikernel += 1
            data[y][x] = cellsum 
             
    result = Raster.create(data, layer.getextent())
    result.render()
