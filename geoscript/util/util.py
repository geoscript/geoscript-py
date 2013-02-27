"""
util module -- Various utility functions
"""

import math, warnings
from java import io, lang, net, util
from java.lang.String import format
from javax.xml.bind import DatatypeConverter

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
      try:
        return net.URL('file:%s' % o)
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
  if isinstance(o, (io.OutputStream, io.Writer, file)):
    return o
  else:
    o = toFile(o)
    if isinstance(o,io.File):
      return io.FileOutputStream(o)

def toInputStream(o):
  if isinstance(o, (io.InputStream, io.Reader, file)):
    return o

  f = toFile(o)
  if isinstance(f,io.File) and f.exists():
    return io.FileInputStream(f)

  if isinstance(o, (str,unicode)):
    return io.ByteArrayInputStream(lang.String(o).getBytes())

  if type(o).__name__ == 'array':
    return io.ByteArrayInputStream(o)

def doOutput(fn, out):
  os = toOutputStream(out)
  try:  
    return fn(os)
  finally:
    if os != out:
      os.close()

def doInput(fn, input):
  instream = toInputStream(input)
  try:
    return fn(instream)
  finally:
    if instream != input:
      instream.close()

def deprecated(f):
  def wrapper(*args, **kwargs):
    warnings.warn("Function %s is deprecated. %s"% (f.__name__, f.__doc__),
        DeprecationWarning, 2)
    return f(*args, **kwargs)
    
  wrapper.__name__ = f.__name__ 
  wrapper.__doc__ = f.__doc__
  wrapper.__dict__.update(f.__dict__)
  return wrapper

def interpolate(low, high, n, method):
  """
  Interpolates between two numeric values.

  The *n* parameter specifies the number of values to interpoluate. 
  Specifically the number of classes that will result from  the interpolated
  values.

  The *method* parameter specifies the interpolation method. By default
  a linear method is used. The values 'exp' (exponential) and 'log' 
  (logarithmic) methods are also supported.

  This function returns n+1 values.
  """
  delta = high - low
  if method == 'linear':
    fx = lambda x: delta * x
  elif method == 'exp':
    fx = lambda x: math.exp(x * math.log(1+delta)) - 1
  elif method == 'log':
    fx = lambda x: delta * math.log((x+1))/math.log(2)
  else:
    raise Exception('Interpolation method %s not supported' % method)
      
  fy = lambda x : low + fx(x)
  return map(fy, [x/float(n) for x in range(0,n+1)])

def catch(f):
  """
  Utility function to run some code and catch the java exception.
  Used to get around jython not printing source exceptions to console.
  """
  try: 
    return f()
  except lang.Exception, e:
    return e

def dateToStr(obj):
  """
  Encodes a java.util.Date or java.util.Calendar object to an ISO8601 
  formatted datetime string.
  """
  cal = None
  if isinstance(obj, util.Calendar):
    cal = obj
  elif isinstance(obj, util.Date):
    cal = util.Calendar.getInstance()
    cal.setTime(obj)
  else:
    raise Exception('Unable to turn %s into date' % obj)

  return DatatypeConverter.printDateTime(cal)
  
def strToDate(s):
  """
  Parses a ISO8601 formatted datetime string into a java.util.Calendar object.
  """
  return DatatypeConverter.parseDateTime(s)
