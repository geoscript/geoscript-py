from geoscript.style import util
from geoscript.style.expression import Expression
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import LineSymbolizer, PolygonSymbolizer

class Hatch(Symbolizer):
  """
  Symbolizer that repeats a pattern. A hatch can be applied to linear and area 
  geometries. 

  A hatch is composed of a well known ``name`` that describes the pattern, and a 
  :class:`Stroke <geoscript.style.stroke.Stroke>` that specifies how the pattern is
  stroked.
  
  >>> from geoscript.style import Stroke
  >>> Hatch('slash', Stroke('#333333'))
  Hatch(name=slash,stroke=Stroke(color=(51,51,51),width=1),size=8)

  A hatch also accepts a ``size`` argument. When applied to a linear geometry the size
  specifies both the length of the hatch and the distance between repeated instances of
  it. When applied to a polygon the size specifies the dimensions of the square tile in
  which the pattern is repeated.
  """

  def __init__(self, name, stroke=None, size=None):
    Symbolizer.__init__(self)
    self.name = name
    if not stroke:
      from geoscript.style.stroke import Stroke
      stroke = Stroke()

    self.stroke = stroke 
    self.size = Expression(size if size else 8)

  def _prepare(self, syms):
    raise Exception('not implemented')

  def _apply(self, sym):
    raise Exception('not implemented')

  def _hatch(self):
    f = self.factory
    mark = f.createMark()
    mark.setWellKnownName('shape://%s' % self.name)
    mark.setStroke(self.stroke._stroke())

    graphic = self.factory.createGraphic()    
    graphic.graphicalSymbols().clear()
    graphic.graphicalSymbols().add(mark)
    graphic.setSize(self.size.expr)

    return graphic

  def __repr__(self):
    return self._repr('name', 'stroke', 'size')
