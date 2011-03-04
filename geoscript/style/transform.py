from geoscript.style import util
from geoscript.function import Function
from geoscript.style.symbolizer import Symbolizer

class Transform(Symbolizer):
  """
  Symbolizer for transforming a geometry before rendering.

  The ``fn`` argument is the function to execute against each feature being
  rendered. This function is wrapped in a 
  :class:`Function <geoscript.function.Function>`
  """
  def __init__(self, fn):
    Symbolizer.__init__(self)
    self.function = Function(fn)

  def _prepare(self, rule):
    for sym in rule.getSymbolizers():
      self._apply(sym)
      
  def _apply(self, sym):
    sym.setGeometry(self.function)

  
