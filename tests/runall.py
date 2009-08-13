import sys
from os import path

sys.path.insert(0,path.join(path.dirname(__file__),path.pardir))

import unittest
import doctest
import geomtest
from geoscript import geom

loader = unittest.TestLoader()
runner = unittest.TextTestRunner(verbosity=2)

runner.run(doctest.DocTestSuite(geom))
runner.run(loader.loadTestsFromTestCase(geomtest.GeomTest))
