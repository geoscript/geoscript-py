from geoscript.filter import Filter
from org.geotools.data import DefaultQuery, Query

class Stats(object):

  def __init__(self, layer, filter=None):
    self.layer = layer
    self.filter = None if filter is None else Filter(filter)

  def values(self, fields, filter=None):
    fil = self._filter(filter)
    if isinstance(fields, (list,tuple)):
      for f in self.layer.features(fil):
        yield tuple(f.get(fld) for fld in fields)
    else:
      for f in self.layer.features(fil):
        yield f.get(fields)

  def valueTable(self, fields, filter=None): 
    fil = self._filter(filter)
    ret = dict(zip(fields, [[] for f in fields]))
    for f in self.layer.features(fil):
      for fld in fields:
        ret[fld].append(f.get(fld))  
    return ret

  def x(self, filter=None):
    # TODO: handle no geometry case
    fil = self._filter(filter)
    for f in self.layer.features(fil):
      yield f.geom.centroid.x

  def y(self, filter=None):
    # TODO: handle no geometry case
    fil = self._filter(filter)
    for f in self.layer.features(fil):
      yield f.geom.centroid.y

  def xy(self, filter=None):
    # TODO: handle no geometry case
    fil = self._filter(filter)
    for f in self.layer.features(fil):
      yield (f.geom.centroid.x, f.geom.centroid.y)

  def extrema(self, field, low=None, high=None, filter=None):
    # build a filter based on specified min/max values
    fil = ['%s >= %s' % (field, low)] if low != None else []
    fil += ['%s <= %s' % (field, high)] if high != None else []
    fil = ' AND '.join(fil)
    fil = Filter(fil) if len(fil) > 0 else Filter.PASS

    # concatenate with one passed in
    fil += self._filter(filter)

    q = DefaultQuery(self.layer.name)
    q.setFilter(fil._filter)

    min, max = None, None
    fit = self.layer._source.getFeatures(q).features()
    try:
      while fit.hasNext():
        f = fit.next() 
        val = f.getAttribute(field)
        min = val if min == None or val < min else min
        max = val if max == None or val > max else max
    finally:
      fit.close()

    return (min,max)

  def frequency(self, field, filter=None):
    pass

  def histogram(self, field, nbins=10, low=None, high=None, filter=None):
    if low is None or high is None:  
      minmax = self.extrema(field)
      low = minmax[0] if low is None else low
      high = minmax[1] if high is None else high

    rnge = high - low
    dx = rnge/float(nbins)
    values = [0]*nbins

    # should optimize this, we don't need a filter if a low,high is not 
    # specified
    fil = Filter('%s BETWEEN %s AND %s' % (field, low, high))
    
    # concatenate with one specified
    fil += self._filter(filter)

    fit = self.layer._source.getFeatures(fil._filter).features()
    try:
      while fit.hasNext():
        f = fit.next()
        val = f.getAttribute(field)
        values[min(nbins-1, int( (val-low)/float(rnge)*nbins ))] += 1
    finally:
      fit.close()

    keys = [round(low + x * dx, 2) for x in range(0,nbins+1)]
    return zip([(keys[i-1],keys[i]) for i in range(1,len(keys))], values)
  
  def _filter(self, filter):
    if filter is None:
      return self.filter

    if self.filter is None:
      return filter

    return self.filter + Filter(filter)
