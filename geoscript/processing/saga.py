import os
from geoscript.processing.provider import ProcessProvider
from geoscript.processing.utils import isWindows, userFolder, gettempfilename,\
    tempfolder
import stat
import subprocess
from geoscript.processing.parameters import *
from geoscript.processing.process import Process
from geoscript.processing.outputs import getoutputfromstring, OutputRaster,\
    OutputVector
from geoscript.layer.shapefile import Shapefile

''' 
The :mod:`saga` module contains provider and process classes to call algorithms 
from SAGA (System for Automated Geospatial Analysis)
'''
def sagaBatchJobFilename():

    if isWindows():
        filename = "saga_batch_job.bat";
    else:
        filename = "saga_batch_job.sh";

    batchfile = userFolder() + os.sep + filename

    return batchfile

def sagaDescriptionsFile():
    return os.path.join(os.path.dirname(__file__), "..", "..", "data", "saga_descriptions.txt")

def createSagaBatchJobFileFromSagaCommands(commands):

    fout = open(sagaBatchJobFilename(), "w")

    for command in commands:
        fout.write("saga_cmd " + command + "\n")

    fout.write("exit")
    fout.close()


def executeSaga():
    if isWindows():
        command = ["cmd.exe", "/C ", sagaBatchJobFilename()]
    else:
        os.chmod(sagaBatchJobFilename(), stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        command = [sagaBatchJobFilename()]
    loglines = []
    loglines.append("SAGA execution console output")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True).stdout
    for line in iter(proc.readline, ""):
        pass
    

class SagaProvider(ProcessProvider):

    def __init__(self):
        ProcessProvider.__init__(self)        
        
    def loadprocesses(self):
        file = sagaDescriptionsFile()
        lines = open(file)   
        s = ""     
        for line in lines:            
            if not line.startswith("----"):
                s += line
            else:                
                alg = SagaProcess(s)
                if alg.name.strip() != "":
                    self._processes.append(alg)                    
                s = ""
    
    def name(self):
        return "SAGA"

#============================================


class SagaProcess(Process):

    OUTPUT_EXTENT = "outputextent"

    def __init__(self, text):        
        Process.__init__(self)        
        self.defineCharacteristicsFromText(text)        
    
    
    def defineCharacteristicsFromText(self, text):
        self.inputs = {}
        self.outputs = {}    
        lines = text.split("\n")    
        line = lines[0].strip("\n").strip()
        self.fullname = lines[0].strip("\n").strip()      
        self.name = "saga:" + ''.join(c for c in self.fullname if c not in ':;,. -_()[]' ).lower()        
        self.description = self.fullname
        line = lines[1].strip("\n").strip()
        self.undecoratedGroup = line        
        for i in range(2,len(lines)):                
            line = lines[i].strip("\n").strip()
            if line.startswith("Parameter"):
                param = getparameterfromstring(line)
                self.inputs[param.name] = param
            elif line.startswith("DontResample"):
                pass
                #self.resample = False
            elif line.startswith("Extent"): #An extent parameter that wraps 4 SAGA numerical parameters
                self.extentParamNames = line[6:].strip().split(" ")
                self.addParameter(ParameterExtent(self.OUTPUT_EXTENT, "Output extent", "0,1,0,1"))
            elif line == "":
                break
            else:
                output = getoutputfromstring(line)
                self.outputs[output.name] = output                                   

    def _run(self):        
        commands = list()
        self.exportedLayers = {}
 
        #1: Export rasters to sgrd and vectors to shp
        #   Tables must be in dbf format. We check that.    
        for param in self.inputs.values():
            if isinstance(param, ParameterRaster):
                if param.value == None:
                    continue
                value = param.asfile()                
                commands.append(self.exportRasterLayer(value))                
            if isinstance(param, ParameterVector):
                if param.value == None:
                    continue
                layer = param.asfile()                                    
                if not layer.endswith("shp"):
                    filename = utils.gettempfilename('shp') 
                    Shapefile.save(param.aslayer(), filename)
                    self.exportedLayers[layer]=filename
            if isinstance(param, ParameterTable):
                #TODO: this is unsupported by now
                pass
            if isinstance(param, ParameterMultipleInput):
                if param.value == None:
                    continue
                value = param.asfiles() 
                layers = value.split(";")
                if layers == None or len(layers) == 0:
                    continue
                if param.datatype == ParameterMultipleInput.TYPE_RASTER:                    
                    for layer in layers:               
                        commands.append(self.exportRasterLayer(value))                        
                elif param.datatype == ParameterMultipleInput.TYPE_VECTOR_ANY:
                    for layer in layers:                                  
                        if not layer.endswith("shp"):
                            filename = utils.gettempfilename('shp') 
                            Shapefile.save(layer, filename)
                            self.exportedLayers[value]=filename
 
        #2: set parameters and outputs
        if isWindows():
            command = self.undecoratedGroup  + " \"" + self.fullname + "\""
        else:
            command = "lib" + self.undecoratedGroup  + " \"" + self.fullname + "\""
 
        for param in self.inputs.values():
            paramname = param.name.upper()
            if param.value is None:
                continue
            if isinstance(param, (ParameterRaster, ParameterVector)):
                value = param.asfile()
                if value in self.exportedLayers.keys():
                    command+=(" -" + paramname + " \"" + self.exportedLayers[value] + "\"")
                else:
                    command+=(" -" + paramname + " " + value)
            elif isinstance(param, ParameterMultipleInput):
                s = param.value
                for layer in self.exportedLayers.keys():
                    s = s.replace(layer, self.exportedLayers[layer])
                command+=(" -" + paramname + " \"" + s + "\"");
            elif isinstance(param, ParameterBoolean):
                if param.value:
                    command+=(" -" + paramname);
            elif isinstance(param, ParameterFixedTable):
                tempTableFile  = gettempfilename("txt")
                f = open(tempTableFile, "w")
                f.write('\t'.join([col for col in param.cols]) + "\n")
                values = param.value.split(",")
                for i in range(0, len(values), 3):
                    s = values[i] + "\t" + values[i+1] + "\t" + values[i+2] + "\n"
                    f.write(s)
                f.close()
                command+=( " -" + paramname + " " + tempTableFile)
            elif isinstance(param, ParameterExtent):
                values = param.aslist()
                for i in range(4):
                    command+=(" -" + self.extentParamNames[i] + " " + str(values[i]));
            elif isinstance(param, (ParameterNumber, ParameterSelection)):
                command+=(" -" + paramname + " " + str(param.value));
            else:
                command+=(" -" + paramname + " \"" + str(param.value) + "\"");
 
        for out in self.outputs.values():
            if isinstance(out, OutputRaster): 
                outname = out.name.upper()               
                filename = out.value
                if not filename.endswith(".tif"):
                    filename += ".tif"
                    out.value = filename
                filename = tempfolder() + os.sep + os.path.basename(filename) + ".sgrd"
                command+=(" -" + outname + " \"" + filename + "\"");
            if isinstance(out, OutputVector):
                filename = out.value
                if not filename.endswith(".shp"):
                    filename += ".shp"
                    out.value = filename
                command+=(" -" + outname + " \"" + filename + "\"");
            #===================================================================
            # if isinstance(out, OutputTable):
            #    filename = out.value
            #    if not filename.endswith(".dbf"):
            #        filename += ".dbf"
            #        out.value = filename
            #    command+=(" -" + out.name + " \"" + filename + "\"");
            #===================================================================
 
        commands.append(command)
 
        #3:Export resulting raster layers
        for out in self.outputs.values():
            if isinstance(out, OutputRaster):
                filename = out.value
                filename2 = tempfolder() + os.sep + os.path.basename(filename) + ".sgrd"
                if isWindows():
                    commands.append("io_gdal 1 -GRIDS \"" + filename2 + "\" -FORMAT 1 -TYPE 0 -FILE \"" + filename + "\"");
                else:
                    commands.append("libio_gdal 1 -GRIDS \"" + filename2 + "\" -FORMAT 1 -TYPE 0 -FILE \"" + filename + "\"");
 
        #4 Run SAGA
        createSagaBatchJobFileFromSagaCommands(commands)
        
        executeSaga();

    
    def exportRasterLayer(self, layer):
        destFilename = gettempfilename("sgrd")
        self.exportedLayers[layer]= destFilename
        if isWindows():
            return "io_gdal 0 -GRIDS \"" + destFilename + "\" -FILES \"" + layer+"\""
        else:
            return "libio_gdal 0 -GRIDS \"" + destFilename + "\" -FILES \"" + layer + "\""








