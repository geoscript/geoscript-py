import sys
from java.lang import System

try:
   import org.geotools
   from org.geotools.util.factory import Hints

   # by default the geotools referenceing Systemtem assumes yx or lat/lon 
   if not System.getProperty("org.geotools.referencing.forceXY"):
      System.setProperty("org.geotools.referencing.forceXY", "true")

   if Hints.getSystemDefault(Hints.FORCE_LONGITUDE_FIRST_AXIS_ORDER):
      Hints.putSystemDefault(Hints.FORCE_AXIS_ORDER_HONORING, "http")

   # set the matching tolerance in the referencing model, this makes it easier
   # to match projection definitions that don't have epsg codes to an existing
   # code
   Hints.putSystemDefault(Hints.COMPARISON_TOLERANCE, 1e-9);

except ImportError:
   if not System.getProperty("geoscript.bootstrap"):
      print "Error: Could not find GeoTools libraries on classpath."
      sys.exit(1)

