from geoscript.filter import Filter
from geoscript.util import interpolate
from geoscript.style import util
from geoscript.style.color import Color
from geoscript.style.expression import Expression
from geoscript.style.hatch import Hatch
from geoscript.style.icon import Icon
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import LineSymbolizer

class Stroke(Symbolizer):
  """
  Symbolizer for linear geometries that consists of a ``color`` and a ``width``.

  >>> Stroke('#00ff00', 4)
  Stroke(color=(0,255,0),width=4)

  The ``color`` argument may also be specified as a well known name or as an rgb tuple.

  >>> stroke = Stroke('green', 4)
  >>> stroke = Stroke((0,255,0), 4)

  The ``dash`` argument specifies a dashed stroke pattern as a list of values. Oddly 
  positioned elements specify the length in pixels of the dash. Evenly positioned 
  elements specify the spaces.

  >>> stroke = Stroke('green', 4, [2,1,3,2])

  The ``dash`` argument may also be specified as a tuple in which the first element is
  specifies the dash pattern described above, and the second element is an offset into
  the array which specifies where to begin the pattern from.
  
  >>> stroke = Stroke('green', 4, ([2,1,3,2], 2))
  
  The ``cap`` argument specifies how lines should be capped. Supported values include 
  "butt", "round", and "square". The ``join``argument specifies how two lines should be
  joined. Supported values include "miter", "round", and "bevel".

  The ``opacity`` argument is a float between 0 and 1 specifying the opaqueness of 
  the stroke.
  """

  def __init__(self, color='#000000', width=1, dash=None, cap=None, join=None,
               opacity=1.0):
    Symbolizer.__init__(self)
    self.color = Color(color)
    self.width = Expression(width)
    self.opacity = Expression(opacity)
    self.dash = dash
    self.cap = Expression(cap) if cap else None
    self.join = Expression(join) if join else None
    self._hatch = None
    self._icon = None

  def hatch(self, name, stroke=None, size=None):
    """
    Composes the stroke with a hatched pattern.

    The ``name`` argument is the well known name of the hatch pattern. See 
    :class:`Hatch <geoscript.style.hatch.Hatch>` for the list of supported names. 

    The ``stroke`` and ``size`` argument specify the 
    :class:`Stroke <geoscript.style.stroke.Stroke>` and size to use for the hatch 
    pattern respectively.

    >>> stroke = Stroke().hatch('vertline')
    """
    self._hatch = Hatch(name, stroke, size)
    return self

  def icon(self, url, format=None, size=None):
    """
    Composes this stroke as an :class:`Icon <geoscript.style.icon.Icon>`.

    The ``url`` argument is the url/file containing the image. The ``format`` argument
    is the format or mime type of the image.
    """
    self._icon = Icon(url, format, size)
    return self

  def interpolate(self, stroke, n=10, method='linear'):
    colors = self.color.interpolate(stroke.color, n, method)
    w1 = self.width.literal()
    w2 = stroke.width.literal()

    if w1 != None and w2 != None:
      widths = interpolate(w1, w2, n, method) 
    else:
      widths = [self.width] * n

    return map(lambda x: Stroke(x[0], x[1]), zip(colors, widths))

  def _prepare(self, rule):
    sym = self.factory.createLineSymbolizer()
    self._apply(sym) 
    rule.addSymbolizer(sym)
    
  def _apply(self, sym):
    Symbolizer._apply(self, sym)
    sym.setStroke(self._stroke())

    if self._icon:
      self._icon._apply(sym)
    
  def _stroke(self):
    f = self.factory
    stroke = f.createStroke(self.color.expr, self.width.expr, self.opacity.expr)
    #stroke = f.createStroke(f.filter.literal(util.color(self.color)), 
    #  f.filter.literal(self.width))

    if self.dash:
      if isinstance(self.dash, tuple): 
        stroke.setDashArray(self.dash[0])
        stroke.setDashOffset(f.filter.literal(self.dash[1]))
      else:
        stroke.setDashArray(self.dash)

    if self.cap:
      #stroke.setLineCap(f.filter.literal(self.cap))
      stroke.setLineCap(self.cap.expr)
    if self.join:
      stroke.setLineJoin(self.join.expr)
      #stroke.setLineJoin(f.filter.literal(self.join))
   
    if self._hatch:
      stroke.setGraphicStroke(self._hatch._hatch())

    return stroke

  def __repr__(self):
    return self._repr('color', 'width')

