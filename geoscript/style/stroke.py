from geoscript.filter import Filter
from geoscript.style import util
from geoscript.util import stats
from geoscript.style.color import Color
from geoscript.style.expression import Expression
from geoscript.style.hatch import Hatch
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
  """

  def __init__(self, color='#000000', width=1, dash=None, cap=None, join=None):
    Symbolizer.__init__(self)
    self.color = Color(color)
    self.width = Expression(width)
    self.dash = dash
    self.cap = Expression(cap) if cap else None
    self.join = Expression(join) if join else None
    self._hatch = None

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

  def interpolate(self, stroke, n=10, method='linear'):
    """
    Creates a set of stroke objects by interpolating between the color/width of
    this stroke and the specified stroke.

    The *n* parameter specifies how many values to interpolate. The 
    interpolation is inclusive of this and the specified stroke. 

    The *method* parameter specifies the interpolation method. By default
    a linear method is used. The values 'exp' (exponential) and 'log' 
    (logarithmic) methods are also supported.
    """
    def _stroke(col, width):
      s = Stroke(col, width, self.dash, self.cap, self.join)
      s._hatch = self._hatch
      return s 

    cols = self.color.interpolate(stroke.color, n, method)
    widths = stats.interpolate(self.width.value(), stroke.width.value(), n,
      method)
    return map(lambda col, width: _stroke(col, width), cols, widths)

  def _prepare(self, rule):
    syms = util.symbolizers(rule, LineSymbolizer)
    for sym in syms:
      self._apply(sym)
    
  def _apply(self, sym):
    Symbolizer._apply(self, sym)
    sym.setStroke(self._stroke())

  def _stroke(self):
    f = self.factory
    stroke = f.createStroke(self.color.expr, self.width.expr)
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

