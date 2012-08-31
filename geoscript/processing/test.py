'''
Created on 25/08/2012

@author: volaya
'''
import time
from  geoscript.processing import processes, getprocess



if __name__ == '__main__':
    #===========================================================================
    # from geoscript.layer.geotiff import GeoTIFF
    # r = GeoTIFF("d:\\gisdata\\dempart2.tif")
    # w, h = r.getsize()
    # 
    # 
    # print "Starting scanning with getvalueatcell"
    # t1 = time.clock()        
    # for x in range(w):
    #    for y in range(h):
    #        print r.getvalueatcell(x, y, 0)
    # t2 = time.clock()
    # print t2-t1
    # 
    # print "Starting scanning with eval"
    # r.getnodatavalue()
    # t1 = time.clock()
    # for x in range(w):
    #    for y in range(h):
    #        print r.eval(pixel = (x, y))
    # t2 = time.clock()
    # print t2-t1
    #===========================================================================
    
    
   p = getprocess('saga:slopeaspectcurvature')
   p.run (elevation = 'd:\gisdata\dempart1.tif')    