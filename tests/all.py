import sys
from os import path

sys.path.insert(0,path.join(path.dirname(__file__),path.pardir))

import unittest
import doctest
import geomtest
import projtest
import featuretest
import workspace
from layer import MemoryLayerTest, ShapefileLayerTest, PostgisLayerTest, H2LayerTest
from workspace import MemoryWorkspaceTest, PostgisWorkspaceTest, H2WorkspaceTest
from geoscript import geom, proj, feature, layer, workspace

loader = unittest.TestLoader()
runner = unittest.TextTestRunner(verbosity=1)

runner.run(doctest.DocTestSuite(geom))
runner.run(loader.loadTestsFromTestCase(geomtest.GeomTest))

runner.run(doctest.DocTestSuite(proj))
runner.run(loader.loadTestsFromTestCase(projtest.ProjTest))

runner.run(doctest.DocTestSuite(feature))
runner.run(loader.loadTestsFromTestCase(featuretest.FeatureTest))

runner.run(doctest.DocTestSuite(layer.layer))
runner.run(loader.loadTestsFromTestCase(MemoryLayerTest))
runner.run(doctest.DocTestSuite(layer.memory))
runner.run(loader.loadTestsFromTestCase(ShapefileLayerTest))
runner.run(loader.loadTestsFromTestCase(PostgisLayerTest))
runner.run(loader.loadTestsFromTestCase(H2LayerTest))

runner.run(doctest.DocTestSuite(workspace.workspace))
runner.run(loader.loadTestsFromTestCase(MemoryWorkspaceTest))
runner.run(loader.loadTestsFromTestCase(PostgisWorkspaceTest))
runner.run(loader.loadTestsFromTestCase(H2WorkspaceTest))
