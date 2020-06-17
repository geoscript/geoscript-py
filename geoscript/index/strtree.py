from geoscript.index.spatialindex import SpatialIndex
from org.locationtech.jts.index.strtree import STRtree as JtsSTRtree

class STRtree(SpatialIndex):

    def __init__(self):
        SpatialIndex.__init__(self, JtsSTRtree())