from geoscript.plot import *
from geoscript.layer.shapefile import Shapefile
from geoscript.processing.sampledata import sampledata

if __name__ == '__main__':  
    
    #layer = Shapefile('/home/myuser/points.shp')
    #===========================================================================
    # layer = sampledata.get('heights')
    # x = y = ifeat = 0
    # for feature in layer.features():        
    #    pt = feature.geom.centroid
    #    x += pt.x
    #    y += pt.y
    #    ifeat += 1
    # x /= float(ifeat)
    # y /= float(ifeat)
    # chart = xybars(frequency(disttopoint(layer, x, y), 10))
    # chart.show()
    #===========================================================================
    
    #the same thing using the xy function to calculate the mean center
    layer = sampledata.get('heights')
    x = y = ifeat = 0
    xy = xy(layer)
    for px,py in xy:                
        x += px
        y += py
        ifeat += 1
    x /= float(ifeat)
    y /= float(ifeat)
    chart = xybars(frequency(disttopoint(layer, x, y), 10))
    chart.show()
        
        
    
