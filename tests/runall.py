import sys
from os import path

sys.path.insert(0,path.join(path.dirname(__file__),path.pardir))

import unittest
import geom

loader = unittest.TestLoader()
runner = unittest.TextTestRunner(verbosity=2)

runner.run(loader.loadTestsFromTestCase(geom.GeomTest))
