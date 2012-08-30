from org.geotools.process import Processors
from geoscript import core
from geoscript.processing.process import Process
from geoscript.processing.provider import ProcessProvider
from geoscript.processing.parameters import ParameterRaster, ParameterVector,\
    ParameterBoolean, ParameterNumber, ParameterString, ParameterObject,\
    ParameterSelection, ParameterCrs, ParameterExtent
from geoscript.processing.outputs import OutputRaster, OutputVector,\
    OutputNumber, OutputObject
import java
from org.geotools.coverage.grid import GridCoverage2D
from org.geotools.feature import FeatureCollection
from org.geotools.referencing import CRS
from org.opengis.referencing.crs import CoordinateReferenceSystem
from com.vividsolutions.jts.geom import Envelope



def getgeoscriptoutputs(outputs):
    
    m = {}
    for k,v in dict(outputs).iteritems():
        if v.type == GridCoverage2D:
            m[v.name] = OutputRaster(v.name, v.description)
        elif issubclass(v.type, FeatureCollection) :
            m[v.name] = OutputVector(v.name, v.description)        
        elif issubclass(v.type, java.lang.Number):
            m[v.name] = OutputNumber(v.name, v.description)
        #TODO: add other types
        else:
            m[v.name] = OutputObject(v.name, v.description)
        
    return m

def getgeoscriptinputs(inputs):
    m = {}
    for k,v in dict(inputs).iteritems():        
        t = v.type
        if t == GridCoverage2D:
            m[v.name] = ParameterRaster(v.name, v.description)
        elif issubclass(t,FeatureCollection):
            m[v.name] = ParameterVector(v.name, v.description)
        elif t == java.lang.Boolean:
            m[v.name] = ParameterBoolean(v.name, v.description)
        elif issubclass(v.type, java.lang.Number):
            m[v.name] = ParameterNumber(v.name, v.description)
        elif t == CRS or t == CoordinateReferenceSystem:
            m[v.name] = ParameterCrs(v.name, v.description)            
        elif issubclass(t, Envelope):
            m[v.name] = ParameterExtent(v.name, v.description)    
        elif t == java.lang.String:
            m[v.name] = ParameterString(v.name, v.description)
        elif hasattr(t, "values"): #is Enum            
            #I cannot get the enum consts names, so by now I am getting them from the str
            #representation of the array.array it returns, while I find a cleaner solution
            s = str(t.values())
            s = s[s.find("[")+1:-2]
            options = s.split(",")                        
            m[v.name] = ParameterSelection(v.name, v.description, options)
        #TODO: add other types
        else:
            m[v.name] = ParameterObject(v.name, v.description, v.type)
    
    return m


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
                p.inputs = getgeoscriptinputs(paraminfo)                
                resultinfo = pf.getResultInfo(n, paraminfo)          
                p.outputs = getgeoscriptoutputs(resultinfo)
                
                self._processes.append(p)         
 
    def name(self):
        return "GeoTools"
  
class GeotoolsProcess(Process):
    
  def __init__(self, process=None):
    Process.__init__(self)  
    self._process = process  
  
  def _run(self):                        
        # map the inputs to java.
        m = {}
        for inp in self.input:                       
            if isinstance(inp, ParameterRaster):
                m[inp.name] = core.unmap(inp.aslayer())
            elif isinstance(inp, ParameterVector):            
                m[inp.name] = core.unmap(inp.aslayer().cursor())
            elif isinstance(inp, ParameterSelection):
                ##TODO: do this            
                #m[inp.name] = core.unmap(inp.aslayer().cursor())
                pass
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


