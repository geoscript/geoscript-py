import string
from java import awt
from geoscript.style.expression import Expression

_colors = {}
_colors['red'] = awt.Color(255, 0, 0)
_colors['green'] = awt.Color(0, 255, 0)
_colors['blue'] = awt.Color(0, 0, 255)

class Color(Expression):
  """
  Expression that evaluates to a color object.

  The `val` argument may be specified as an rgba tuple:    

  >>> Color((255, 0, 255))
  (255,0,255)

  Or as a hex color string:

  >>> Color('ff00ff')
  (255,0,255)

  Or as a well known color name:

  >>> Color('magenta')
  (255,0,255)
  
  """

  def __init__(self, val):
    Expression.__init__(self, val)

  def _expr(self, val):
    if isinstance(val, Expression):
      # direct expression specified
      self.expr = val
    else:
      # transform val to color
      if _colors.has_key(val):
         # first try well known
         col = _colors[val]
      elif isinstance(val,(list,tuple)):
         # try as tuple
         col = awt.Color(*val)
      elif isinstance(val, str):
         # look up wellknown
         if hasattr(awt.Color, string.upper(val)):
           col = getattr(awt.Color, string.upper(val))
         else:
           # try as hex string
           val = val[1:] if val[0] == "#" else val
           col = awt.Color(*[int('0x'+x,0) for x in val[0:2],val[2:4],val[4:6]])
      else:
         # default
         col = awt.Color(0,0,0)
      return self.factory.filter.literal(col)

  def __repr__(self):
    col = self.expr.evaluate(awt.Color)
    return "(%d,%d,%d)" % (col.red, col.green, col.blue)
