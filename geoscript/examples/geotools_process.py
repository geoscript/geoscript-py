from  geoscript.processing import getprocess
from geoscript.processing.sampledata import sampledata

'''An example that show how to use a geotools process'''

if __name__ == '__main__':   
    #run a GeoTools process using a Layer object as input 
    layer = sampledata.get('landcover')
    proc = getprocess('gs:Unique')
    out = proc.run(features=layer, attribute='LANDCOVER')
    print str(out['result'].aslayer().count())
    
    #and now run it using a filename as input
    filename = layer.shapefile
    out = proc.run(features=filename, attribute='LANDCOVER')
    print str(out['result'].aslayer().count())