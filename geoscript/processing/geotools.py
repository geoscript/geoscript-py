from org.geotools.process import Processors
from geoscript import core
from geoscript.layer import Layer
from geoscript.processing.process import Process
from geoscript.processing.provider import ProcessProvider
from geoscript.processing.parameters import ParameterRaster


def getgeoscriptoutputs(outputs):
    return outputs

def getgeoscriptinputs(inputs):
    m = {}
    for inp in inputs:
        if isinstance()


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
    
          paraminfo = pf.getParameterInfo(n)
          inputs = _params(paraminfo)
          p.inputs = getgeoscriptinputs(inputs)
          
          
          resultinfo = pf.getResultInfo(n, paraminfo)
          outputs = _params(resultinfo)
          p.outputs = getgeoscriptoutputs(outputs)
          
          self._processes.append(p)         
 
  def name(self):
      return "GeoTools"
  
class GeotoolsProcess(Process):
    
  def __init__(self, process=None):
    self._process = process  
  
  def _run(self):                        
        # map the inputs to java.
        m = {}
        for inp in self.input:                       
            if isinstance(inp, ParameterRaster):
                m[inp.name] = core.unmap(inp.aslayer())
            elif isinstance(inp, ParameterRaster):            
                m[inp.name] = core.unmap(inp.aslayer().cursor())
            else:
                m[inp.name] = core.unmap(inp.value)
        
        # run the process
        result = self._process.execute(m, None)
    
        # reverse map the outputs back 
        r = {}
        for k, v in dict(result).iteritems():
          self.outputs[k].value = core.map(v)
          r[k] = self.outputs[k]          
    
        return r        

def _params(m):
  d = {}
  for k,v in dict(m).iteritems():
     d[k] = (v.name, core.map(v.type), v.description)
  return d 

