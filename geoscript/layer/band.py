class Band(object):

  def __init__(self, dim):
    self._dim = dim

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
