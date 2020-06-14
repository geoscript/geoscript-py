
from geoscript.index.spatialindex import SpatialIndex
from org.locationtech.jts.index.quadtree import Quadtree as JtsQuadtree

class QuadTree(SpatialIndex):

    def __init__(self):
        SpatialIndex.__init__(self, JtsQuadtree())

    def queryAll(self):
        return self.index.queryAll()

    def remove(self, bounds, item):
        return self.index.remove(bounds, item)