import zipfile
import urllib2
import os
from geoscript.processing.utils import mkdir
from geoscript.layer.raster import Raster
from geoscript.layer.shapefile import Shapefile
from geoscript.layer.geotiff import GeoTIFF

def downloadAndUnzipSampleData():
    folder = os.path.expanduser('~') + os.sep + 'geoscript' \
        + os.sep + 'sampledata'
    if os.path.exists(folder):
        return
    mkdir(folder)
    downloadAndUnzip("http://geomorphometry.org/system/files/BaranjaHill.zip", folder)
    downloadAndUnzip("http://geomorphometry.org/system/files/BaranjaHill_photo.zip", folder)
    
def downloadAndUnzip(url, folder):
    zf = urllib2.urlopen(url)    
    filename = os.path.join(folder,'downloaded.zip')    
    output = open(filename,'wb')    
    output.write(zf.read())
    output.close()
    z = zipfile.ZipFile(filename)
    for n in z.namelist():
        dest = os.path.join(folder, n)        
        data = z.read(n)
        f = open(dest, 'wb')
        f.write(data)
        f.close()
    z.close()
    os.unlink(filename)

class sampledata():
    
    raster = {'dem' : "DEM25.asc",
              'ortho' : 'orthophoto.asc'}
    
    vector = { 'landcover' : 'landcover.shp',
               'elevation_points' : 'elevations.shp',
               'heights' : 'heights'}
    
    @staticmethod
    def get(name):
        folder = os.path.expanduser('~') + os.sep + 'geoscript'  + os.sep + 'sampledata'
        if name.lower() not in sampledata.raster.keys() and name.lower() not in sampledata.vector.keys():
            return None        
        downloadAndUnzipSampleData()        
        if name.lower() in sampledata.raster.keys():
            return Raster(file=os.path.join(folder, sampledata.raster[name.lower()]))
        else:
            return Shapefile(os.path.join(folder, sampledata.vector[name.lower()]))
            