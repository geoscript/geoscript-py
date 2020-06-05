from org.geotools.data.collection import ListFeatureCollection
from org.geotools.feature.simple import SimpleFeatureBuilder

def readFeatures(it, type, chunk):
  i = 0
  features = ListFeatureCollection(type)
  while it.hasNext() and i < chunk:
    features.add(it.next()) 
    i = i+1

  return features 

def readFeaturesWithChangedGeometry(it, sourceType, targetType, chunk):
  i = 0
  features = ListFeatureCollection(targetType)
  builder = SimpleFeatureBuilder(targetType)
  while it.hasNext() and i < chunk:
    f = it.next()
    for x in range(0, f.getAttributeCount()):
        name = f.getFeatureType().getDescriptor(x).getLocalName()
        value = f.getAttribute(x)
        if (name == sourceType.getGeometryDescriptor().getLocalName()):
            name = targetType.getGeometryDescriptor().getLocalName()
        builder.set(name, value)
    features.add(builder.buildFeature(f.getID()))
    i = i+1

  return features