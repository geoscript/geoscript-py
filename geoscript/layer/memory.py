"""
layer.memory module -- Layer in which features are stored in memory.

A memory layer can be created with a name and a list of attribute names:
  
>>> from geoscript import geom
>>> l = MemoryLayer('widgets', [ ('geom',geom.Point), ('name',str)])
>>> l.add( [geom.Point(1,1), 'one'] )
>>> l.add( [geom.Point(2,2), 'two'] )
>>> l.count()
2
"""

from geoscript.layer import Layer
from geoscript import geom, feature
from org.geotools.data.memory import MemoryDataStore

class MemoryLayer(Layer):

  def __init__(self,name,atts=[('geom', geom.Geometry)]):
    ftype = feature.Schema(name, atts) 
    ds = MemoryDataStore(ftype.ft)
    Layer.__init__(self,ds.getFeatureSource(name))
