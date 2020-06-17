import unittest
from geoscript.index import STRtree, QuadTree
from geoscript.geom import Bounds, Point

class IndexTest(unittest.TestCase):

    def testQuadTree(self):
        index = QuadTree()
        index.insert(Bounds(0,0,10,10), Point(5,5))
        index.insert(Bounds(2,2,6,6),  Point(4,4))
        index.insert(Bounds(20,20,60,60), Point(30,30))
        index.insert(Bounds(22,22,44,44), Point(32,32))
        self.assertEqual(4, index.size())

        results = index.query(Bounds(1,1,5,5))
        self.assertEquals(4, len(results))

        allResults = index.queryAll()
        self.assertEquals(4, len(allResults))

        isRemoved = index.remove(Bounds(22,22,44,44), Point(32,32))
        self.assertTrue(isRemoved)

        allResults = index.queryAll()
        self.assertEquals(3, len(allResults))

    def testSTRtree(self):
        index = STRtree()
        index.insert(Bounds(0,0,10,10), Point(5,5))
        index.insert(Bounds(2,2,6,6),  Point(4,4))
        index.insert(Bounds(20,20,60,60), Point(30,30))
        index.insert(Bounds(22,22,44,44), Point(32,32))
        self.assertEqual(4, index.size())

        results = index.query(Bounds(1,1,5,5))
        self.assertEquals(2, len(results))

