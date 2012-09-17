
'''
An example that creates a cone shaped elevation raster.
It uses the :class:`WritableRaster` class instead of
creating a data array and the constructing a Raster obejct

'''
from geoscript.processing import *
from geoscript.layer.writableraster import WritableRaster
from geoscript.geom.bounds import Bounds
import math

if __name__ == '__main__':  
    
    SIZE = 100
    CENTER = SIZE / 2;
    MAX_ELEVATION = math.sqrt(CENTER * CENTER + CENTER * CENTER);
    wr = WritableRaster(Bounds(0,0,SIZE,SIZE), 1, 1)
    width, height = wr.getsize()     
    for y in range(height):
        for x in range(width):
            dx = math.fabs(CENTER - x);
            dy = math.fabs(CENTER - y);
            dist = math.sqrt(dx * dx + dy * dy);
            elevation = MAX_ELEVATION - dist;      
            wr.setvalueatcell(x, y, 0 , elevation)
             
    result = wr.getraster()
    result.render()
