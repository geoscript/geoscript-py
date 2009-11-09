"""
util module -- Various utility functions
"""

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
    return io.File(o).toURL()

def toFile(o):
  """
  Transforms an object to a File if possible. This method can take a file, 
  string, uri, or url object.
  """
  if isinstance(o, io.File):
    return o
  elif isinstance(o, net.URI):
    return toFile(o.toURL())
  elif isinstance(o, net.URL):
    return toFile(o.getFile())
  elif isinstance(o, (str, unicode)):
    return io.File(o)
