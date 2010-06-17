
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

  def __eq__(self, other):
    return other and self.name == other.name \
      and self.typ == other.typ and self.proj == other.proj
