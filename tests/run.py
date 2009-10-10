import sys

try:
  import nose
except ImportError:
  print "The nose library required for testing."
  sys.exit(1)

# run all regular tests
nose.run()

# run doc tests
nose.run(argv=['nosetests', '--with-doctest', '../geoscript'])
