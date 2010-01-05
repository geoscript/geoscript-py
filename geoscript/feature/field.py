
class Field(object):
  """
  A schema field composed of a name and a type. A geometric attribute also contains a :class:`Projection <geoscript.proj.Projection>`.
  """

  def __init__(self, name, typ, proj=None):
    self.name = name
    self.typ = typ
    self.proj = proj

  def __repr__(self):
    return '%s: %s' % (self.name, self.typ.__name__)

