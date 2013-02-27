from org.geotools.util import NumberRange
from org.geotools.coverage import Category, GridSampleDimension

class Band(object):

  def __init__(self, name=None, min=0, max=255, dim=None):
    if dim:
      self._dim = dim
    else:
      cat = Category(name, None, NumberRange.create(min, max))
      self._dim = GridSampleDimension(name, [cat], None)

  def getname(self):
    return self._dim.getDescription().toString()
  
  name = property(getname, None)

  def getmin(self):
    return self._dim.getMinimumValue()

  min = property(getmin, None)

  def getmax(self):
    return self._dim.getMaximumValue()
 
  max = property(getmax, None)

  def getnodata(self):
    return self._dim.getNoDataValues()

  nodata = property(getnodata, None)

  def getunit(self):
    return self._dim.getUnits()

  unit = property(getunit, None)

  def getscale(self):
    return self._dim.scale

  scale = property(getscale, None)

  def getoffset(self):
    return self._dim.getOffset()

  offset = property(getoffset, None)
  
  def __repr__(self):
    return self._dim.getDescription().toString()
