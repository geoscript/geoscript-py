import sys

try:
  import nose
except ImportError:
  print "The nose library required for testing."
  sys.exit(1)

# run all regular tests
passed = nose.run()
if passed:
  # run doc tests
  passed = nose.run(argv=['nosetests', '--with-doctest', '--ignore-files=spatialite.py', '--ignore-files=oracle.py', '../geoscript'])

sys.exit(0 if passed else 1)
