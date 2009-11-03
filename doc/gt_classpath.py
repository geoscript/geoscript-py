import sys, os

if len(sys.argv) < 2:
  print "Usage: gt_classpath.py <GeoTools Directory>"
  sys.exit(-1)

base = sys.argv[1]
if not os.path.exists(base):
  print "Error: No such directory %s" % base
  sys.exit(-1)

cp=[os.path.abspath(f) for f in os.listdir(base)]
print os.pathsep.join(cp)
