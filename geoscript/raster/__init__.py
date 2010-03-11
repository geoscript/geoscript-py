from raster import Raster
from geotiff import GeoTIFF
from worldimage import WorldImage

def _import(mod, clas):
  try:
    m = __import__(mod, globals(), locals(), [clas])
    return getattr(m, clas)
  except ImportError, (errmsg):
    print 'Error importing %s module: %s' % (mod, errmsg)

Mosaic = _import('mosaic', 'Mosaic')
MrSID = _import('mrsid', 'MrSID')
