
from  geoscript.processing import getprocess
from geoscript.layer.raster import Raster

'''An example that show how to use external algorithms'''

if __name__ == '__main__':   
    dem = Raster(file="d:\\gisdata\\dempart1.tif")
    #Calculate slope calling a external GRASS process
    proc = getprocess('grass:r.slope')
    out = proc.run(elevation=dem)
    slope_grass = out['slope'].aslayer()
    
    #Calculate slope calling a external SAGA process
    proc = getprocess('saga:slopeaspectcurvature')
    out = proc.run(elevation=dem)
    slope_saga = out['slope'].aslayer()
       
    # Calculate difference between the two slope layers   
    nx, ny = slope_saga.getsize()
    data = [[x for x in xrange(nx)] for y in xrange(ny)]
    for x in range(1,nx-1):
       for y in range(1,ny-1):
           data[y][x] = abs(slope_saga.getvalueatcell(x,y) - slope_grass.getvalueatcell(x,y))
    diff = Raster.create(data, slope_saga.getextent())  
    diff.render()  
 

 
        
