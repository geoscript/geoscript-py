import sys
from os import path

sys.path.insert(0,path.join(path.dirname(__file__),path.pardir))

import unittest
import doctest

if len(sys.argv) == 1:
  import all
  exit()

loader = unittest.TestLoader()
runner = unittest.TextTestRunner(verbosity=2)

test = sys.argv[1]
if 'Test' == test[-4:]:
  (mod,testclass) = test.rsplit('.',1)  
  exec "import %s" % (mod) 
  exec "runner.run(loader.loadTestsFromTestCase(%s))" % (test)
else:
  exec "import geoscript.%s" % (test)
  exec "runner.run(doctest.DocTestSuite(geoscript.%s))" % (test)

