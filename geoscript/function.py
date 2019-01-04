"""
The :mod:`function` module integrates functions into the GeoTools filter 
function system. Such functions are executed against feature objects and can be
used in styles or for custom filter processing.
"""

import java
import weakref
import inspect
from org.geotools.factory import CommonFactoryFinder
from org.geotools.util.factory import FactoryIteratorProvider, GeoTools
from org.geotools.filter import FunctionFactory, FunctionExpressionImpl

_factory = CommonFactoryFinder.getFilterFactory(None)
_functions = []

class Factory(FunctionFactory):

  def __init__(self):
    pass

  def getFunctionNames(self):
    names = []
    for f in _functions:
      f = f()      
      if f:
        names.append(_factory.functionName(f.getName(), f.getArgCount())) 
    return names

  def function(self, name, args, fallback):
    for f in _functions:
      f = f()
      if f and f.getName() == name:
        return f

class Function(FunctionExpressionImpl):
  """
  A function to be executed against a feature. The ``fn`` is the function to
  execute. The arguments of ``fn`` are feature attributes.

  >>> def foo(the_geom):
  ...    return the_geom.buffer(10)
  >>> f = Function(foo)
  """

  def __init__(self, fn):
    FunctionExpressionImpl.__init__(self, fn.__name__)
    self.fn = fn

    args = inspect.getargspec(fn)[0]
    for arg in args:
      self.getParameters().add(_factory.property(arg))

    _functions.append(weakref.ref(self))

  def getArgCount(self):
    return self.getParameters().size()

  def evaluate(self, obj, clazz):
    args = [arg.evaluate(obj) for arg in self.getParameters()]
    return self.fn(*args)

  def __repr__(self):
    return "Function(%s)" % (self.fn.__name__)

class Provider(FactoryIteratorProvider):

  def __init__(self):
    pass

  def iterator(self, clazz):
    if FunctionFactory == clazz:
      return java.util.ArrayList([Factory()]).iterator()

_provider = Provider()
GeoTools.addClassLoader(_provider.getClass().getClassLoader())
GeoTools.addFactoryIteratorProvider(_provider)
