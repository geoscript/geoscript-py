from raster import Raster
from geotiff import GeoTIFF
from worldimage import WorldImage

def _import(mod, clas):
  try:
    m = __import__(mod, globals(), locals(), [clas])
    return getattr(m, clas)
  except ImportError, (errmsg):
    print 'Error importing %s module: %s' % (mod, errmsg)

MrSID = _import('mrsid', 'MrSID')
