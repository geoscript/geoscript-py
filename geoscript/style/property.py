from geoscript.style.expression import Expression

class Property(Expression):
  """
  Expression that evaluates to the field value of a feature.

  The ``name`` argument is the name of the feature field.
  """

  def __init__(self, name):
    Expression.__init__(self, name)

  def _expr(self, e):
    return self.factory.filter.property(e)
