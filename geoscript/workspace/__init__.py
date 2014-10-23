from workspace import Workspace
from memory import Memory

def _import(mod, clas):
  try:
    m = __import__(mod, globals(), locals(), [clas])
    return getattr(m, clas)
  except ImportError, (errmsg):
    print 'Error import module %s: %s' % (mod, errmsg)

PostGIS = _import('postgis', 'PostGIS')
H2 = _import('h2', 'H2')
Directory = _import('directory', 'Directory')
SpatiaLite = _import('spatialite', 'SpatiaLite')
MySQL = _import('mysql', 'MySQL')
Teradata = _import('teradata', 'Teradata')
Property = _import('property', 'Property')
Oracle = _import('oracle', 'Oracle')
GeoPackage = _import('geopackage', 'GeoPackage')

