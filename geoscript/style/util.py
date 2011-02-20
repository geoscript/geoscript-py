from java import awt
from org.geotools.styling import StyleBuilder

_builder = StyleBuilder()

_colors = {}
_colors['red'] = awt.Color(255, 0, 0)
_colors['green'] = awt.Color(0, 255, 0)
_colors['blue'] = awt.Color(0, 0, 255)

def color(val):
  # first try well known
  if _colors.has_key(val):
     return _colors[val]
 
  # try as tuple
  if isinstance(val,(list,tuple)):
     return awt.Color(*val)

  # try as hex string
  if isinstance(val, str):
     val = val[1:] if val[0] == "#" else val
     return awt.Color(*[int('0x'+x,0) for x in val[0:2],val[2:4],val[4:6]])

def stroke(col, width):
  st = _builder.createStroke()
  st.setColor(_builder.filterFactory.literal(color(col)))
  st.setWidth(_builder.filterFactory.literal(width))
  return st

def lineSymbolizer(col, width):
  line = _builder.createLineSymbolizer() 
  line.setStroke(stroke(col, width))
  return line
