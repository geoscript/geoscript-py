from org.geotools.factory import CommonFactoryFinder
from org.geotools.styling import StyleFactoryImpl, StyleBuilder

_filter = CommonFactoryFinder.getFilterFactory(None)

class StyleFactory(StyleFactoryImpl):

  def __init__(self):
    self.builder = StyleBuilder()
    self.filter = _filter

  def createStyle(self):
    return self.builder.createStyle()

  def createFill(self):
    return self.builder.createFill()

  def createFont(self, family, italic, bold, size):
    return self.builder.createFont(family, italic, bold, size)

  def createGraphic(self):
    return self.builder.createGraphic()
