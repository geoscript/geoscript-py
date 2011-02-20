from geoscript.style.symbolizer import Symbolizer

class Label(Symbolizer):

  def __init__(self):
    Symbolizer.__init__(self)

  def __repr__(self):
    return 'Label()[%s]' % (self.filter)
