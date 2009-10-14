# first thing to do is ensure that the geotools libs are on the classpath
try:
  import org.geotools
except ImportError:
  # try to find them
  import sys, os
  libs = os.path.abspath(os.path.join(__file__, '../../geotools'))
  if os.path.exists(libs): 
     # round up all the libs and add them to the classpath
     for lib in os.listdir(libs):
       sys.path.append(os.path.join(libs,lib))

  try:
     import org.geotools
  except ImportError:
     print "Error: Could not find GeoTools libraries on classpath."
     sys.exit(1)

from java.lang import System
from org.geotools.factory import Hints

# by default the geotools referenceing Systemtem assumes yx or lat/lon 
if not System.getProperty("org.geotools.referencing.forceXY"):
  System.setProperty("org.geotools.referencing.forceXY", "true")

if Hints.getSystemDefault(Hints.FORCE_LONGITUDE_FIRST_AXIS_ORDER):
  Hints.putSystemDefault(Hints.FORCE_AXIS_ORDER_HONORING, "http")
