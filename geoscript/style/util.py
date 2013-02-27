from java import awt
from org.geotools.styling import StyleBuilder, PointSymbolizer, LineSymbolizer
from org.geotools.styling import PolygonSymbolizer, TextSymbolizer
from org.geotools.styling import  RasterSymbolizer

_builder = StyleBuilder()

_colors = {}
_colors['red'] = awt.Color(255, 0, 0)
_colors['green'] = awt.Color(0, 255, 0)
_colors['blue'] = awt.Color(0, 0, 255)

_syms = {}
_syms[PointSymbolizer] = lambda x: _builder.createPointSymbolizer()
_syms[LineSymbolizer] = lambda x: _builder.createLineSymbolizer()
_syms[RasterSymbolizer] = lambda x: _builder.createRasterSymbolizer()

def _createPolySymbolizer(x): 
  ps = _builder.createPolygonSymbolizer()
  ps.setStroke(None)
  return ps
_syms[PolygonSymbolizer] = _createPolySymbolizer

_syms[TextSymbolizer] = lambda x: _builder.createTextSymbolizer()

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

def graphic(sym):
  if isinstance(sym, PointSymbolizer):
    if not sym.getGraphic():
      sym.setGraphic(_builder.createGraphic())
    return sym.getGraphic()

  elif isinstance(sym, LineSymbolizer):
    if not sym.getStroke().getGraphicStroke():
      sym.getStroke().setGraphicStroke(_builder.createGraphic())
    return sym.getStroke().getGraphicStroke()

  elif isinstance(sym, PolygonSymbolizer):
    if not sym.getFill().getGraphicFill():    
      sym.getFill().setGraphicFill(_builder.createGraphic())
    return sym.getFill().getGraphicFill()
 
  elif isinstance(sym, TextSymbolizer):
    if not sym.getGraphic():
     sym.setGraphic(_builder.createGraphic())
    return sym.getGraphic()

def stroke(col, width):
  st = _builder.createStroke()
  st.setColor(_builder.filterFactory.literal(color(col)))
  st.setWidth(_builder.filterFactory.literal(width))
  return st

def symbolizers(rule, clazz):
  syms = filter(lambda s: isinstance(s, clazz), rule.symbolizers()) 
  if len(syms) == 0:
    if isinstance(clazz, (list,tuple)):
      clazz = clazz[0]

    sym = _syms[clazz](None)
    rule.symbolizers().add(sym)
    syms.append(sym)

  return syms
