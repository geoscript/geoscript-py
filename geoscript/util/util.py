"""
util module -- Various utility functions
"""

import warnings
from java import io, net

def toURL(o):
  """
  Transforms an object to a URL if possible. This method can take a file, 
  string, uri, or url object.
  """

  if isinstance(o,net.URL):
    return o
  elif isinstance(o,(net.URI,io.File)):
    return o.toURL()
  elif isinstance(o, (str, unicode)):
    try:
      return net.URL(o)
    except net.MalformedURLException:
      return io.File(o).toURL()

def toFile(o):
  """
  Transforms an object to a File if possible. This method can take a file, 
  string, uri, or url object.
  """
  if isinstance(o, (io.File, file)):
    return o
  elif isinstance(o, net.URI):
    return toFile(o.toURL())
  elif isinstance(o, net.URL):
    return toFile(o.getFile())
  elif isinstance(o, (str, unicode)):
    return io.File(o)

def toOutputStream(o):
  """
  """
  if isinstance(o, (io.InputStream, io.Reader, file)):
    return o
  else:
    o = toFile(o)
    if isinstance(o,io.File):
      return io.FileOutputStream(o)

def deprecated(f):
  def wrapper(*args, **kwargs):
    warnings.warn("Function %s is deprecated. %s"% (f.__name__, f.__doc__),
        DeprecationWarning, 2)
    return f(*args, **kwargs)
    
  wrapper.__name__ = f.__name__ 
  wrapper.__doc__ = f.__doc__
  wrapper.__dict__.update(f.__dict__)
  return wrapper
