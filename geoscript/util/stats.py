import math

def interpolate(low, high, classes=10, method='linear'):
  """
  Generates a set of interpolated values for an attribute of the layer.

  *low* and *high* specify the interval over which to interpolate values.

  *classes* specifies the number of values to interpolate.

  The *method* parameter specifies the interpolation method. By default
  a linear method is used. The values 'exp' (exponential) and 'log' 
  (logarithmic) methods are also supported.
 
  """
  rnge = high-low
  if method == 'linear':
    fx = lambda x: rnge * x
  elif method == 'exp':
    fx = lambda x: math.exp(x * math.log(1+rnge)) - 1
  elif method == 'log':
    fx = lambda x: rnge * math.log((x+1))/math.log(2)
  else:
    raise Exception('Interpolation method %s not supported' % method)
    
  fy = lambda x : low + fx(x)
  delta = 1/float(classes)
  return map(fy, [x*delta for x in range(0,classes+1)])

