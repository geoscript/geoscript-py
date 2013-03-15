import string
from java import awt, lang
from geoscript.style.expression import Expression
from geoscript import util

_colors = {}
_colors['aliceblue'] = awt.Color(240,248,255)
_colors['antiquewhite'] = awt.Color(250,235,215)
_colors['aqua'] = awt.Color(0,255,255)
_colors['aquamarine'] = awt.Color(127,255,212)
_colors['azure'] = awt.Color(240,255,255)
_colors['beige'] = awt.Color(245,245,220)
_colors['bisque'] = awt.Color(255,228,196)
_colors['black'] = awt.Color(0,0,0)
_colors['blanchedalmond'] = awt.Color(255,235,205)
_colors['blue'] = awt.Color(0,0,255)
_colors['blueviolet'] = awt.Color(138,43,226)
_colors['brown'] = awt.Color(165,42,42)
_colors['burlywood'] = awt.Color(222,184,135)
_colors['cadetblue'] = awt.Color(95,158,160)
_colors['chartreuse'] = awt.Color(127,255,0)
_colors['chocolate'] = awt.Color(210,105,30)
_colors['coral'] = awt.Color(255,127,80)
_colors['cornflowerblue'] = awt.Color(100,149,237)
_colors['cornsilk'] = awt.Color(255,248,220)
_colors['crimson'] = awt.Color(220,20,60)
_colors['cyan'] = awt.Color(0,255,255)
_colors['darkblue'] = awt.Color(0,0,139)
_colors['darkcyan'] = awt.Color(0,139,139)
_colors['darkgoldenrod'] = awt.Color(184,134,11)
_colors['darkgray'] = awt.Color(169,169,169)
_colors['darkgreen'] = awt.Color(0,100,0)
_colors['darkkhaki'] = awt.Color(189,183,107)
_colors['darkmagenta'] = awt.Color(139,0,139)
_colors['darkolivegreen'] = awt.Color(85,107,47)
_colors['darkorange'] = awt.Color(255,140,0)
_colors['darkorchid'] = awt.Color(153,50,204)
_colors['darkred'] = awt.Color(139,0,0)
_colors['darksalmon'] = awt.Color(233,150,122)
_colors['darkseagreen'] = awt.Color(143,188,143)
_colors['darkslateblue'] = awt.Color(72,61,139)
_colors['darkslategray'] = awt.Color(47,79,79)
_colors['darkturquoise'] = awt.Color(0,206,209)
_colors['darkviolet'] = awt.Color(148,0,211)
_colors['deeppink'] = awt.Color(255,20,147)
_colors['deepskyblue'] = awt.Color(0,191,255)
_colors['dimgray'] = awt.Color(105,105,105)
_colors['dodgerblue'] = awt.Color(30,144,255)
_colors['firebrick'] = awt.Color(178,34,34)
_colors['floralwhite'] = awt.Color(255,250,240)
_colors['forestgreen'] = awt.Color(34,139,34)
_colors['fuchsia'] = awt.Color(255,0,255)
_colors['gainsboro'] = awt.Color(220,220,220)
_colors['ghostwhite'] = awt.Color(248,248,255)
_colors['gold'] = awt.Color(255,215,0)
_colors['goldenrod'] = awt.Color(218,165,32)
_colors['gray'] = awt.Color(128,128,128)
_colors['green'] = awt.Color(0,128,0)
_colors['greenyellow'] = awt.Color(173,255,47)
_colors['grey'] = awt.Color(84,84,84)
_colors['honeydew'] = awt.Color(240,255,240)
_colors['hotpink'] = awt.Color(255,105,180)
_colors['indianred'] = awt.Color(205,92,92)
_colors['indigo'] = awt.Color(75,0,130)
_colors['ivory'] = awt.Color(255,255,240)
_colors['khaki'] = awt.Color(240,230,140)
_colors['lavender'] = awt.Color(230,230,250)
_colors['lavenderblush'] = awt.Color(255,240,245)
_colors['lawngreen'] = awt.Color(124,252,0)
_colors['lemonchiffon'] = awt.Color(255,250,205)
_colors['lightblue'] = awt.Color(173,216,230)
_colors['lightcoral'] = awt.Color(240,128,128)
_colors['lightcyan'] = awt.Color(224,255,255)
_colors['lightgoldenrodyellow'] = awt.Color(250,250,210)
_colors['lightgrey'] = awt.Color(211,211,211)
_colors['lightgreen'] = awt.Color(144,238,144)
_colors['lightpink'] = awt.Color(255,182,193)
_colors['lightsalmon'] = awt.Color(255,160,122)
_colors['lightseagreen'] = awt.Color(32,178,170)
_colors['lightskyblue'] = awt.Color(135,206,250)
_colors['lightslategray'] = awt.Color(119,136,153)
_colors['lightsteelblue'] = awt.Color(176,196,222)
_colors['lightyellow'] = awt.Color(255,255,224)
_colors['lime'] = awt.Color(0,255,0)
_colors['limegreen'] = awt.Color(50,205,50)
_colors['linen'] = awt.Color(250,240,230)
_colors['magenta'] = awt.Color(255,0,255)
_colors['maroon'] = awt.Color(128,0,0)
_colors['mediumaquamarine'] = awt.Color(102,205,170)
_colors['mediumblue'] = awt.Color(0,0,205)
_colors['mediumorchid'] = awt.Color(186,85,211)
_colors['mediumpurple'] = awt.Color(147,112,216)
_colors['mediumseagreen'] = awt.Color(60,179,113)
_colors['mediumslateblue'] = awt.Color(123,104,238)
_colors['mediumspringgreen'] = awt.Color(0,250,154)
_colors['mediumturquoise'] = awt.Color(72,209,204)
_colors['mediumvioletred'] = awt.Color(199,21,133)
_colors['midnightblue'] = awt.Color(25,25,112)
_colors['mintcream'] = awt.Color(245,255,250)
_colors['mistyrose'] = awt.Color(255,228,225)
_colors['moccasin'] = awt.Color(255,228,181)
_colors['navajowhite'] = awt.Color(255,222,173)
_colors['navy'] = awt.Color(0,0,128)
_colors['oldlace'] = awt.Color(253,245,230)
_colors['olive'] = awt.Color(128,128,0)
_colors['olivedrab'] = awt.Color(107,142,35)
_colors['orange'] = awt.Color(255,165,0)
_colors['orangered'] = awt.Color(255,69,0)
_colors['orchid'] = awt.Color(218,112,214)
_colors['palegoldenrod'] = awt.Color(238,232,170)
_colors['palegreen'] = awt.Color(152,251,152)
_colors['paleturquoise'] = awt.Color(175,238,238)
_colors['palevioletred'] = awt.Color(216,112,147)
_colors['papayawhip'] = awt.Color(255,239,213)
_colors['peachpuff'] = awt.Color(255,218,185)
_colors['peru'] = awt.Color(205,133,63)
_colors['pink'] = awt.Color(255,192,203)
_colors['plum'] = awt.Color(221,160,221)
_colors['powderblue'] = awt.Color(176,224,230)
_colors['purple'] = awt.Color(128,0,128)
_colors['red'] = awt.Color(255,0,0)
_colors['rosybrown'] = awt.Color(188,143,143)
_colors['royalblue'] = awt.Color(65,105,225)
_colors['saddlebrown'] = awt.Color(139,69,19)
_colors['salmon'] = awt.Color(250,128,114)
_colors['sandybrown'] = awt.Color(244,164,96)
_colors['seagreen'] = awt.Color(46,139,87)
_colors['seashell'] = awt.Color(255,245,238)
_colors['sienna'] = awt.Color(160,82,45)
_colors['silver'] = awt.Color(192,192,192)
_colors['skyblue'] = awt.Color(135,206,235)
_colors['slateblue'] = awt.Color(106,90,205)
_colors['slategray'] = awt.Color(112,128,144)
_colors['snow'] = awt.Color(255,250,250)
_colors['springgreen'] = awt.Color(0,255,127)
_colors['steelblue'] = awt.Color(70,130,180)
_colors['tan'] = awt.Color(210,180,140)
_colors['teal'] = awt.Color(0,128,128)
_colors['thistle'] = awt.Color(216,191,216)
_colors['tomato'] = awt.Color(255,99,71)
_colors['turquoise'] = awt.Color(64,224,208)
_colors['violet'] = awt.Color(238,130,238)
_colors['wheat'] = awt.Color(245,222,179)
_colors['white'] = awt.Color(255,255,255)
_colors['whitesmoke'] = awt.Color(245,245,245)
_colors['yellow'] = awt.Color(255,255,0)
_colors['yellowgreen'] = awt.Color(154,205,50)

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
      elif isinstance(val, (str,unicode)):
         # look up wellknown
         if hasattr(awt.Color, string.upper(val)):
           col = getattr(awt.Color, string.upper(val))
         else:
           # try as hex string
           val = val[1:] if val[0] == "#" else val

           # convert 3 digit to 6
           if len(val) == 3:
             val = ''.join([val[i]+val[i] for i in range(0,3)])

           # support 8 and 6 digit
           if len(val) == 8:
             # move alpha to end
             val = val[2:] + val[:2]

           col = awt.Color(*[int('0x'+x,0) 
             for x in [val[i:i+2] for i in range(0, len(val), 2)]])
             #for x in val[0:2],val[2:4],val[4:6]])
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

  def getrgba(self):
    col = self._color
    return (col.red, col.green, col.blue, col.alpha)
  rgba = property(getrgba,None,None,"The RGBA value of the color")
   
  def getargb(self):
    col = self._color
    return (col.alpha, col.red, col.green, col.blue)
  argb = property(getrgba,None,None,"The ARGB value of the color")

  def gethex(self):
    return self._tohex(self.rgb)
  hex = property(gethex,None,None,"The hex value of the color")

  def getahex(self):
    return self._hex(self.argb)
  ahex = property(gethex,None,None,"The hex value, with alpha, of the color")

  def _tohex(self, vals):
    return ''.join([lang.String.format('%02x', x) for x in vals])

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

  def opacity(self, o):
    return self.alpha(int(255*o))

  def alpha(self, a):
    return Color(tuple(list(self.rgb) + [a]))

  def interpolate(self, color, n=10, method='linear'):
    """  
    Interpolates a set of color values beteen this color and the specified
    *color*. 

    The *n* parameter specifies how many values to interpolate, specifically the
    number of classes resulting from the interpolation. The interpolation is 
    inclusive of this and the specified color and returns a list of *n*+1 
    values.
    """  
    color = Color(color)
    hsl1,hsl2 = self.hsl, color.hsl 
    dhsl = map(lambda x: x[1]-x[0], zip(hsl1,hsl2)) 

    colors = [Color.fromHSL(map(lambda x,y: x + (r/float(n))*y,hsl1,dhsl)) 
      for r in util.interpolate(0, n, n, method)]
    if self._color.alpha != color._color.alpha:
      alphas = util.interpolate(self._color.alpha,color._color.alpha,n,method)
      colors = map(lambda (c,a): c.alpha(int(a)), zip(colors, alphas))      

    return colors

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
  def random(cls, n):
    """
    Returns a generator of random colors.

    *n* is the number of colors to generate.
    """
    colors = _colors.values()
    from random import randint
    for i in range(n):
      yield Color(colors[randint(0,len(colors)-1)])

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
 
