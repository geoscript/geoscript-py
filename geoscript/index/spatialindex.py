class SpatialIndex:
    
    def __init__(self, index):
        self.index = index

    def size(self):
        return self.index.size()

    def insert(self, bounds, item):
        self.index.insert(bounds, item)

    def query(self, bounds):
        return self.index.query(bounds)