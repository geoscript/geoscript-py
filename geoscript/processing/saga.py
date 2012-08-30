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

def sagaDescriptionPath():
    return os.path.join(os.path.dirname(__file__),"saga_descriptions")

def createSagaBatchJobFileFromSagaCommands(commands):

    fout = open(sagaBatchJobFilename(), "w")

    for command in commands:
        fout.write("saga_cmd " + command + "\n")

    fout.write("exit")
    fout.close()


def executeSaga(progress):
    if isWindows():
        command = ["cmd.exe", "/C ", sagaBatchJobFilename()]
    else:
        os.chmod(sagaBatchJobFilename(), stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        command = [sagaBatchJobFilename()]
    loglines = []
    loglines.append("SAGA execution console output")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True).stdout
    for line in iter(proc.readline, ""):
        #=======================================================================
        # if "%" in line:
        #    s = "".join([x for x in line if x.isdigit()])
        #    progress.setPercentage(int(s))
        # else:
        #    line = line.strip()
        #    if line!="/" and line!="-" and line !="\\" and line!="|":
        #        loglines.append(line)
        #        progress.setConsoleInfo(line)
        #=======================================================================
        pass
    

class SagaProvider(ProcessProvider):

    def __init__(self):
        ProcessProvider.__init__(self)        
        
    def loadprocesses(self):
        self._processes = []
        folder = sagaDescriptionPath()
        print folder
        for descriptionFile in os.listdir(folder):
            if descriptionFile.endswith("txt"):
                try:
                    alg = SagaProcess(os.path.join(folder, descriptionFile))
                    if alg.name.strip() != "":
                        self._processes.append(alg)                    
                except Exception,e:
                    print e#do nothing by now if an algorithm cannot be loaded
                    pass

    def name(self):
        return "SAGA"

#============================================


class SagaProcess(Process):

    OUTPUT_EXTENT = "outputextent"

    def __init__(self, descriptionfile):        
        Process.__init__(self)
        self.descriptionFile = descriptionfile
        self.defineCharacteristicsFromFile()        

    def getCopy(self):
        newone = SagaProcess(self.descriptionFile)
        newone.provider = self.provider
        return newone
    
    def defineCharacteristicsFromFile(self):
        self.inputs = {}
        self.outputs = {}
        lines = open(self.descriptionFile)
        line = lines.readline().strip("\n").strip()
        self.fullname = line
        print line
        self.name = "saga:" + ''.join(c for c in line if c not in ':;,. -_()' )
        print self.name        
        self.description = line
        line = lines.readline().strip("\n").strip()
        self.undecoratedGroup = line
        line = lines.readline().strip("\n").strip()        
        while line != "":
            line = line.strip("\n").strip()
            if line.startswith("Parameter"):
                param = getparameterfromstring(line)
                print line
                print param
                self.inputs[param.name] = param
            elif line.startswith("DontResample"):
                pass
                #self.resample = False
            elif line.startswith("Extent"): #An extent parameter that wraps 4 SAGA numerical parameters
                self.extentParamNames = line[6:].strip().split(" ")
                self.addParameter(ParameterExtent(self.OUTPUT_EXTENT, "Output extent", "0,1,0,1"))
            else:
                output = getoutputfromstring(line)
                print line
                print output
                self.outputs[output.name] = output                
            line = lines.readline().strip("\n").strip()
        lines.close()


    def run(self, progress):        
        commands = list()
        self.exportedLayers = {}
 
        #1: Export rasters to sgrd and vectors to shp
        #   Tables must be in dbf format. We check that.    
        for param in self.parameters:
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
                layers = param.value.split(";")
                if layers == None or len(layers) == 0:
                    continue
                if param.datatype == ParameterMultipleInput.TYPE_RASTER:
                    for layer in layers:
                        value = param.asfile()                
                        commands.append(self.exportRasterLayer(value))                        
                elif param.datatype == ParameterMultipleInput.TYPE_VECTOR_ANY:
                    for layer in layers:
                        value = param.asfile()                                    
                        if not layer.endswith("shp"):
                            filename = utils.gettempfilename('shp') 
                            Shapefile.save(param.aslayer(), filename)
                            self.exportedLayers[value]=filename
 
        #2: set parameters and outputs
        if isWindows():
            command = self.undecoratedGroup  + " \"" + self.fullname + "\""
        else:
            command = "lib" + self.undecoratedGroup  + " \"" + self.fullname + "\""
 
        for param in self.parameters:
            if param.value is None:
                continue
            if isinstance(param, (ParameterRaster, ParameterVector)):
                value = param.aslayer()
                if value in self.exportedLayers.keys():
                    command+=(" -" + param.name + " \"" + self.exportedLayers[value] + "\"")
                else:
                    command+=(" -" + param.name + " " + value)
            elif isinstance(param, ParameterMultipleInput):
                s = param.value
                for layer in self.exportedLayers.keys():
                    s = s.replace(layer, self.exportedLayers[layer])
                command+=(" -" + param.name + " \"" + s + "\"");
            elif isinstance(param, ParameterBoolean):
                if param.value:
                    command+=(" -" + param.name);
            elif isinstance(param, ParameterFixedTable):
                tempTableFile  = gettempfilename("txt")
                f = open(tempTableFile, "w")
                f.write('\t'.join([col for col in param.cols]) + "\n")
                values = param.value.split(",")
                for i in range(0, len(values), 3):
                    s = values[i] + "\t" + values[i+1] + "\t" + values[i+2] + "\n"
                    f.write(s)
                f.close()
                command+=( " -" + param.name + " " + tempTableFile)
            elif isinstance(param, ParameterExtent):
                values = param.aslist()
                for i in range(4):
                    command+=(" -" + self.extentParamNames[i] + " " + str(values[i]));
            elif isinstance(param, (ParameterNumber, ParameterSelection)):
                command+=(" -" + param.name + " " + str(param.value));
            else:
                command+=(" -" + param.name + " \"" + str(param.value) + "\"");
 
        for out in self.outputs:
            if isinstance(out, OutputRaster):
                filename = out.value
                if not filename.endswith(".tif"):
                    filename += ".tif"
                    out.value = filename
                filename = tempfolder() + os.sep + os.path.basename(filename) + ".sgrd"
                command+=(" -" + out.name + " \"" + filename + "\"");
            if isinstance(out, OutputVector):
                filename = out.value
                if not filename.endswith(".shp"):
                    filename += ".shp"
                    out.value = filename
                command+=(" -" + out.name + " \"" + filename + "\"");
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
        for out in self.outputs:
            if isinstance(out, OutputRaster):
                filename = out.value
                filename2 = tempfolder() + os.sep + os.path.basename(filename) + ".sgrd"
                if isWindows():
                    commands.append("io_gdal 1 -GRIDS \"" + filename2 + "\" -FORMAT 1 -TYPE 0 -FILE \"" + filename + "\"");
                else:
                    commands.append("libio_gdal 1 -GRIDS \"" + filename2 + "\" -FORMAT 1 -TYPE 0 -FILE \"" + filename + "\"");
 
        #4 Run SAGA
        createSagaBatchJobFileFromSagaCommands(commands)
        
        executeSaga(progress);

    
    def exportRasterLayer(self, layer):
        destFilename = gettempfilename("sgrd")
        self.exportedLayers[layer]= destFilename
        if isWindows():
            return "io_gdal 0 -GRIDS \"" + destFilename + "\" -FILES \"" + layer+"\""
        else:
            return "libio_gdal 0 -GRIDS \"" + destFilename + "\" -FILES \"" + layer + "\""








