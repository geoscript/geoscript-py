from org.geotools.data.collection import ListFeatureCollection
def readFeatures(it, type, chunk):
  i = 0
  features = ListFeatureCollection(type)
  while it.hasNext() and i < chunk:
    features.add(it.next()) 
    i = i+1

  return features 
