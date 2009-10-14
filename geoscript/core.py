from org.python.core.adapter import ClassAdapter

class ProxyRenamer(ClassAdapter):

  def __init__(self, cls):
    self.name = cls.__name__
    ClassAdapter.__init__(self, cls)

  def rename(self):
    self.adaptedClass.__name__ = self.name

def register(t):
   ProxyRenamer(t).rename()
