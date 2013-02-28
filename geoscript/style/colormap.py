from geoscript.style import util
from geoscript.style.color import Color
from geoscript.style.expression import Expression
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import RasterSymbolizer, ColorMap

_type = {}
_type['ramp'] = ColorMap.TYPE_RAMP
_type['interval'] = ColorMap.TYPE_INTERVALS
_type['values'] = ColorMap.TYPE_VALUES

class ColorMap(Symbolizer):
  """
  Symbolizer for raster data that provides a mapping of raster value to 
  color. A color map consists of a set of tuples specifying the value and 
  associated color:

  >>> ColorMap([(0, 'red'), (100, 'blue')])
  ColorMap(values=[(0, 'red'), (100, 'blue')],interpolate=ramp)

  The *interpolate* argument specifies how to apply the entries of the color 
  map to raster data values. The default value, 'ramp' indicates that data 
  values falling between two subsequent entries should be interpolated. 

  The value "intervals" indicates that entries should be considered as intervals
  (first entry inclusive, second exclusive). Data values falling inside an 
  interval are matched to the color of the first/lower entry. 

  The values "values" specifies that data values need be matched exactly to an 
  entry. Those values that do not match are not assigned a color and not 
  rendered.
  """
  def __init__(self, values, interpolate='ramp'):
    Symbolizer.__init__(self)
    self.values = values
    self.interpolate = interpolate

  def _prepare(self, rule):
    syms = util.symbolizers(rule, RasterSymbolizer)
    for sym in syms:
      self._apply(sym)
    
  def _apply(self, sym):
    Symbolizer._apply(self, sym)
    sym.setColorMap(self._colormap())  

  def _colormap(self):
    f = self.factory
    map = f.createColorMap()
    map.setType(_type[self.interpolate])

    for v in self.values:
      entry = f.createColorMapEntry()
      entry.setQuantity(Expression(v[0]).expr)

      col = Color(v[1])
      entry.setColor(col.expr)
      entry.setOpacity(Expression(col._color.alpha/255.0).expr)

      map.addColorMapEntry(entry)

    return map

  def __repr__(self):
    return self._repr('values', 'interpolate')

