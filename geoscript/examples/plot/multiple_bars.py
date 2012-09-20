from geoscript.plot import *
from geoscript.layer.shapefile import Shapefile

if __name__ == '__main__':       
    layer = Shapefile('D:/gisdata/denver_shapefiles/census_boundaries.shp')    
    chart = categorybars(summarize(layer, 'BLKGRP', ['BLACK', 'ASIAN', 'HISPANIC']), stacked=True)
    chart.show()
    