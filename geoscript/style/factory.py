from org.geotools.factory import CommonFactoryFinder

_style = CommonFactoryFinder.getStyleFactory(None)
_filter = CommonFactoryFinder.getFilterFactory(None)

class Factory(object):

  def __init__(self):
    self.style = _style
    self.filter = _filter
    
