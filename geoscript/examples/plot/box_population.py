from geoscript.plot.functions import  attributesasdict
from geoscript.layer.shapefile import Shapefile
from geoscript.plot.box import box
from geoscript.filter import Filter

if __name__ == '__main__':       
    layer = Shapefile('D:/gisdata/denver_shapefiles/census_boundaries.shp')    
    chart = box(attributesasdict(layer, ['BLACK', 'AMERI_ES', 'ASIAN', 'OTHER', 'HISPANIC'], Filter("COUNTYNAME = 'DENVER'")))
    chart.show()
    