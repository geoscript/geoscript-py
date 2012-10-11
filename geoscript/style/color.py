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
      return val.expr
    else:
      # transform val to color
      if isinstance(val, awt.Color):
         # try direct awt color 
         col = val
      elif _colors.has_key(val):
         # try well known
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
    return "(%d,%d,%d)" % self.rgb

  def _getcolor(self):
    return self.expr.evaluate(awt.Color)
  _color = property(_getcolor)

  def getrgb(self):
    col = self._color
    return (col.red, col.green, col.blue)
  rgb = property(getrgb,None,None,"The RGB value of the color")

  def gethsl(self): 
    r,g,b = [x/255.0 for x in self.rgb]
    lo, hi = min(r,g,b), max(r,g,b)
    h = s = l = (lo+hi)/2.0

    if lo == hi:
      h = s = 0 # achromatic
    else:
      d = float(hi - lo);
      s = d / (2-hi-lo) if l > 0.5 else d / (hi+lo)
      h = {
        r: lambda x: (g - b) / d + (6 if g < b else 0),
        g: lambda x: (b - r) / d + 2,
        b: lambda x: (r - g) / d + 4
      }[hi](-1)

      h /= 6.0;

    return [x for x in [h, s, l]];        
  hsl = property(gethsl,None,None,"The HSL/HLS value of the color")

  def interpolate(self, color, n=10):
    """  
    Interpolates a set of color values beteen this color and the specified
    *color*. 

    The *n* parameter specifies how many values to interpolate, specifically the
    number of classes resulting from the interpolation. The interpolation is 
    inclusive of this and the specified color and returns a list of *n*+1 
    values.
    """  
    hsl1,hsl2 = self.hsl, color.hsl 
    dhsl = map(lambda x: x[1]-x[0], zip(hsl1,hsl2)) 

    return [Color.fromHSL(map(lambda x,y: x + (r/float(n))*y,hsl1,dhsl)) 
      for r in range(0,n+1)]

  @classmethod
  def fromHSL(cls, hsl):
    """
    Creates a color object from the HSL/HLS value.
    """
    h,s,l = hsl

    if s == 0:
      r = g = b = l # achromatic
    else:
      q = l * (1+s) if l < 0.5 else  l + s - l * s;
      p = 2 * l - q
      #var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      #var p = 2 * l - q;
      r = Color._hue2rgb(p, q, h + 1/3.0)
      g = Color._hue2rgb(p, q, h);
      b = Color._hue2rgb(p, q, h - 1/3.0);

    return Color(tuple([int(round(255*x)) for x in [r,g,b]]))

  @classmethod
  def _hue2rgb(cls, p, q, t):
    if t < 0: 
      t += 1;
    if t > 1: 
      t -= 1;
    if t < 1/6.0: 
      return p + (q - p) * 6 * t;
    if t < 1/2.0: 
      return q;
    if t < 2/3.0: 
       return p + (q - p) * (2/3.0 - t) * 6;
    return p;
 
