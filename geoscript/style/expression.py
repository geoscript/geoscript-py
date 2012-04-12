from geoscript.style.factory import StyleFactory

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
   
  def value(self, obj=None):
    return self.expr.evaluate(obj)

  def _expr(self, e):
    return self.factory.filter.literal(e)

  def __repr__(self):
    return str(self.expr)
