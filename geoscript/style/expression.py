from geoscript.style.factory import StyleFactory
from org.opengis.filter.expression import Literal

class Expression(object):
  """
  Base class for all expressions.
  """

  def __init__(self, e): 
    self.factory = StyleFactory()
    if isinstance(e, Expression):
      self.expr = e.expr
    else:
      self.expr = self._expr(e)
   
  def literal(self):
    """
    Returns the literal value of the expression, or None if the expression is
    not a literal.
    """
    if isinstance(self.expr, Literal):
      return self.expr.getValue()

  def _expr(self, e):
    return self.factory.filter.literal(e)

  def __repr__(self):
    return str(self.expr)
