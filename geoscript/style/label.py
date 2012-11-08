from geoscript.util import deprecated
from geoscript.style import util
from geoscript.style.expression import Expression
from geoscript.style.font import Font
from geoscript.style.fill import Fill
from geoscript.style.halo import Halo
from geoscript.style.color import Color
from geoscript.style.icon import Icon
from geoscript.style.property import Property
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import TextSymbolizer

class Label(Symbolizer):
  """
  Symbolizer for labelling a geometry. 

  The ``property`` argument specifies the field or attribute with which to generate labels from.
 
  The ``font`` and ``color`` arguments specify the label font and color
  respectively. 

  >>> Label('foo')
  Label(property=foo)
  """

  def __init__(self, property, font=None, color=None, priority=None, 
               options=None):
    Symbolizer.__init__(self)
    self.property = Property(property)
    self.color = Color(color) if color else None
    self.priority = Property(priority) if priority else None
    self.options = options if options else {}
    self._font = Font(font) if font else None
    self._halo = None
    self._icon = None
    self._placement = None

  def font(self, font):
    """
    Sets the font for this label. The ``font`` argument is a string describing the
    font attributes. See :class:`Font <geoscript.style.font.Font>` for supported 
    syntax.

    >>> label = Label('foo').font('italic bold 12px "Times New Roman"')
    """

    self._font = Font(font)
    return self

  def halo(self, fill=None, radius=None):
    """
    Generates a halo for this label.  

    The ``fill`` and ``radius`` arguments specify the :class:`Fill` and radius to 
    use for the halo.
   
    >>> from geoscript.style import Fill
    >>> label = Label('foo').halo(Fill('#ffffff'), 2)
    """
    self._halo = Halo(fill, radius)
    return self

  def point(self, anchor=(0.5,0.5), displace=(0,0), rotate=0):
    """
    Sets the label placement relative to a point. 

    The ``anchor`` argument is a tuple that specifies how the label should be 
    anchored along an xy axis relative to the geometry being labeled. Allowable
    values range from (0,0) to (1,1) ordered from the bottom left corner to the top
    right corner of the label. 

    The ``displacement`` argument is a tuple that specifies how the label should be
    displaced along an xy axis. 

    The ``rotate`` argument specifies in degrees the angle at which to rotate the 
    label. 

    >>> label = Label('foo').point((0.5,0), (0,5))
    """
    self._placement = self._pointPlacement(anchor, displace, rotate)
    return self

  def icon(self, url, format=None, size=None):
    """
    Composes this label as an :class:`Icon <geoscript.style.icon.Icon>`.

    The ``url`` argument is the url/file containing the image. The ``format`` argument
    is the format or mime type of the image.
    """
    self._icon = Icon(url, format, size)
    return self

  @deprecated
  def linear(self, offset=0, gap=None, igap=None, align=False, follow=False, 
             group=False, displace=None, repeat=None):
    """Use :func:`geoscript.style.Label.line`"""

    return self.line(offset, gap, igap, align, follow, group, displace, repeat)

  def line(self, offset=0, gap=None, igap=None, align=False, follow=False, 
             group=False, displace=None, repeat=None):
    """
    Sets the label placement relative to a line. 

    The ``offset`` argument specifies the perpindicular distance from the line at
    which to position the label. 

    The ``align`` argument specifies whether to align the label along the line. The
    ``follow`` argument specifies whether to curve the label in order to force it
    to follow the line. 
    
    >>> label = Label('foo').linear(align=True, follow=True)
    """
    f = self.factory
    lp = f.createLinePlacement(Expression(offset).expr)
    lp.setAligned(align)
    #lp.setRepeated(repeat)
    if gap:   
      lp.setGap(Expression(gap).expr)
    if igap:
      lp.setInitialGap(Expression(igap).expr)
    self._placement = lp

    self.options['followLine'] = follow
    self.options['group'] = group
    if displace:
      self.options['maxDisplacement'] = displace
    if repeat:
      self.options['repeat'] = repeat
    return self

  def polygon(self, anchor=(0.5,0.5), displace=(0,0), rotate=0, wrap=None):
    self._placement = self._pointPlacement(anchor, displace, rotate)
    if wrap:
      self.options['autoWrap'] = wrap
    return self

  def _pointPlacement(self, anchor, displace, rotate):
    f = self.factory
    ap = f.createAnchorPoint(
      Expression(anchor[0]).expr,Expression(anchor[1]).expr)
    dp = f.createDisplacement(
      Expression(displace[0]).expr, Expression(displace[1]).expr)
    return f.createPointPlacement(ap, dp, Expression(rotate).expr)

  def _prepare(self, rule):
    syms = util.symbolizers(rule, TextSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    Symbolizer._apply(self, sym)
    sym.setLabel(self.property.expr)

    if self._font:
      self._font._apply(sym)
    if self._halo:
      self._halo._apply(sym)
    if self._icon:
      self._icon._apply(sym)

    if self.color:
      sym.setFill(Fill(self.color)._fill())

    if self.priority:
      sym.setPriority(self.priority.expr)

    if self._placement:
      sym.setLabelPlacement(self._placement)
    else:
      sym.setLabelPlacement(None)

  def __repr__(self):
    return self._repr('property')
