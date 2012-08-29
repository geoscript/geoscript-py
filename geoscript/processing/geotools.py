from org.geotools.process import Processors
from geoscript import core
from geoscript.layer import Layer
from geoscript.processing.process import Process
from geoscript.processing.provider import ProcessProvider

class GeotoolsProvider(ProcessProvider):
  """
  A provider for Geotools algorithms
  """
  def __init__(self):
      ProcessProvider.__init__(self)
  
  def loadprocesses(self):    
    for pf in Processors.getProcessFactories():
      for n in pf.getNames():
          p = GeotoolsProcess(pf.create(n))
          p.name = str(":".join((n.namespaceURI, n.localPart)))
          p.title = str(pf.getTitle(n))
          p.description = str(pf.getDescription(n))
    
          params = pf.getParameterInfo(n)
          p.inputs = _params(params)
          p.outputs = _params(pf.getResultInfo(n, params))
          
          self._processes.append(p)         
 
  def name(self):
      return "GeoTools"
  
class GeotoolsProcess(Process):
    
  def __init__(self, process=None):
    self._process = process

  def run(self, **args):
    """
    Executes the process with set of named inputs. The input argument names are
    specified by the :attr:`inputs` property. The output arguments names are 
    specified by the :attr:`outputs` property. 

    >>> p = Process.lookup('gs:Reproject')

    >>> from geoscript import geom, proj
    >>> l = Layer()
    >>> l.add([geom.Point(-125, 50)])
    >>> r = p.run(features=l, targetCRS=proj.Projection('epsg:3005'))
    >>> [f.geom.round() for f in r['result']]
    [POINT (1071693 554290)]
    """
    # map the inputs to java
    m = {}
    for k,v in args.iteritems(): 
      # special case for layer
      if isinstance(v, Layer):
        v = v.cursor()

      m[k] = core.unmap(v)
    
    # run the process
    result = self._process.execute(m, None)

    # reverse map the outputs back 
    r = {}
    for k, v in dict(result).iteritems():
      r[k] = core.map(v)

    return r

def _params(m):
  d = {}
  for k,v in dict(m).iteritems():
     d[k] = (v.name, core.map(v.type), v.description)
  return d 

