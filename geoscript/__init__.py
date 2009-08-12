from java.lang import System
from org.geotools.factory import Hints

# by default the geotools referenceing Systemtem assumes yx or lat/lon 
if not System.getProperty("org.geotools.referencing.forceXY"):
  System.setProperty("org.geotools.referencing.forceXY", "true")

if Hints.getSystemDefault(Hints.FORCE_LONGITUDE_FIRST_AXIS_ORDER):
  Hints.putSystemDefault(Hints.FORCE_AXIS_ORDER_HONORING, "http")
