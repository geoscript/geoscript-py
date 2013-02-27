from cursor import Cursor
from layer import Layer
from shapefile import Shapefile
from io.gml import writeGML, readGML
from io.json import writeJSON, readJSON
from raster import Raster
from geotiff import GeoTIFF
from worldimage import WorldImage
from worldfile import WorldFile

def _import(mod, clas):
  try:
    m = __import__(mod, globals(), locals(), [clas])
    return getattr(m, clas)
  except ImportError, (errmsg):
    print 'Error importing %s module: %s' % (mod, errmsg)

Mosaic = _import('mosaic', 'Mosaic')
MrSID = _import('mrsid', 'MrSID')

