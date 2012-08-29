import os
from geoscript.processing.provider import ProcessProvider
from geoscript.processing.utils import isWindows, userFolder, gettempfilename,\
    tempfolder, asrasterlayer
import stat
import subprocess
from geoscript.process import Process
from geoscript.processing.parameters import *
from geoscript.processing.output import getoutputfromstring

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


@staticmethod
def sagaDescriptionPath():
    return os.path.join(os.path.dirname(__file__),"description")

@staticmethod
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
        self.preloadedAlgs = []
        folder = sagaDescriptionPath()
        for descriptionFile in os.listdir(folder):
            if descriptionFile.endswith("txt"):
                try:
                    alg = SagaProcess(os.path.join(folder, descriptionFile))
                    if alg.name.strip() != "":
                        self.preloadedAlgs.append(alg)                    
                except Exception,e:
                    #do nothing by now if an algorithm cannot be loaded
                    pass

    def name(self):
        return "SAGA"

#============================================


import os
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SagaProcess(Process):

    OUTPUT_EXTENT = "OUTPUT_EXTENT"

    def __init__(self, descriptionfile):
        self.resample = True #True if it should resample
                             #in case several non-matching raster layers are used as input
        Process.__init__(self)
        self.descriptionFile = descriptionfile
        self.defineCharacteristicsFromFile()
        if self.resample:
            #reconsider resampling policy now that we know the input parameters
            self.resample = self.setResamplingPolicy()

    def getCopy(self):
        newone = SagaProcess(self.descriptionFile)
        newone.provider = self.provider
        return newone


    def setResamplingPolicy(self):
        count = 0
        for param in self.parameters:
            if isinstance(param, ParameterRaster):
                count += 1
            if isinstance(param, ParameterMultipleInput):
                if param.datatype == ParameterMultipleInput.TYPE_RASTER:
                    return True

        return count > 1
    

    def defineCharacteristicsFromFile(self):
        lines = open(self.descriptionFile)
        line = lines.readline().strip("\n").strip()
        self.name = line
        line = lines.readline().strip("\n").strip()
        self.undecoratedGroup = line        
        while line != "":
            line = line.strip("\n").strip()
            if line.startswith("Parameter"):
                self.addParameter(getparameterfromstring(line))
            elif line.startswith("DontResample"):
                self.resample = False
            elif line.startswith("Extent"): #An extent parameter that wraps 4 SAGA numerical parameters
                self.extentParamNames = line[6:].strip().split(" ")
                self.addParameter(ParameterExtent(self.OUTPUT_EXTENT, "Output extent", "0,1,0,1"))
            else:
                self.addOutput(getoutputfromstring(line))
            line = lines.readline().strip("\n").strip()
        lines.close()


    def calculateResamplingExtent(self):
        '''this method calculates the resampling extent, but it might set self.resample
        to false if, with the current layers, there is no need to resample'''                
        first = True;
        self.inputExtentsCount = 0
        for param in self.parameters:
            if param.value:
                if isinstance(param, ParameterRaster):                        
                    layer = asrasterlayer(param.value)
                    self.addToResamplingExtent(layer, first)
                    first = False
                if isinstance(param, ParameterMultipleInput):
                    if param.datatype == ParameterMultipleInput.TYPE_RASTER:
                        layers = param.value
                        for layer in layers:
                            layer = asrasterlayer(layer)
                            self.addToResamplingExtent(layer, first)
                            first = False
            if self.inputExtentsCount < 2:
                self.resample = False        


    def addToResamplingExtent(self, layer, first):
        if first:
            self.inputExtentsCount = 1
            self.xmin = layer.extent().xMinimum()
            self.xmax = layer.extent().xMaximum()
            self.ymin = layer.extent().yMinimum()
            self.ymax = layer.extent().yMaximum()
            self.cellsize = (layer.extent().xMaximum() - layer.extent().xMinimum())/layer.width()
        else:
            cellsize = (layer.extent().xMaximum() - layer.extent().xMinimum())/layer.width()
            if self.xmin != layer.extent().xMinimum() \
                    or self.xmax != layer.extent().xMaximum() \
                    or self.ymin != layer.extent().yMinimum() \
                    or self.ymax != layer.extent().yMaximum() \
                    or self.cellsize != cellsize:
                self.xmin = min(self.xmin, layer.extent().xMinimum())
                self.xmax = max(self.xmax, layer.extent().xMaximum())
                self.ymin = min(self.ymin, layer.extent().yMinimum())
                self.ymax = max(self.ymax, layer.extent().yMaximum())
                self.cellsize = max(self.cellsize, cellsize)
                self.inputExtentsCount += 1


    def run(self, progress):        
        commands = list()
        self.exportedLayers = {}

        #1: Export rasters to sgrd and vectors to shp
        #   Tables must be in dbf format. We check that.
        if self.resample:
            self.calculateResamplingExtent()
        for param in self.parameters:
            if isinstance(param, ParameterRaster):
                if param.value == None:
                    continue
                value = param.value
                if not value.endswith("sgrd"):
                    commands.append(self.exportRasterLayer(value))
                if self.resample:
                    commands.append(self.resampleRasterLayer(value));
            if isinstance(param, ParameterVector):
                if param.value == None:
                    continue
                layer = QGisLayers.getObjectFromUri(param.value, False)
                if layer:
                    filename = LayerExporter.exportVectorLayer(layer)
                    self.exportedLayers[param.value]=filename
                elif not param.value.endswith("shp"):
                        raise GeoAlgorithmExecutionException("Unsupported file format")
            if isinstance(param, ParameterTable):
                if param.value == None:
                    continue
                value = param.value
                if not value.endswith("dbf"):
                    raise GeoAlgorithmExecutionException("Unsupported file format")
            if isinstance(param, ParameterMultipleInput):
                if param.value == None:
                    continue
                layers = param.value.split(";")
                if layers == None or len(layers) == 0:
                    continue
                if param.datatype == ParameterMultipleInput.TYPE_RASTER:
                    for layerfile in layers:
                        if not layerfile.endswith("sgrd"):
                            commands.append(self.exportRasterLayer(layerfile))
                        if self.resample:
                            commands.append(self.resampleRasterLayer(layerfile));
                elif param.datatype == ParameterMultipleInput.TYPE_VECTOR_ANY:
                    for layerfile in layers:
                        layer = QGisLayers.getObjectFromUri(layerfile, False)
                        if layer:
                            filename = LayerExporter.exportVectorLayer(layer)
                            self.exportedLayers[layerfile]=filename
                        elif (not value.endswith("shp")):
                            raise GeoAlgorithmExecutionException("Unsupported file format")

        #2: set parameters and outputs
        if isWindows():
            command = self.undecoratedGroup  + " \"" + self.name + "\""
        else:
            command = "lib" + self.undecoratedGroup  + " \"" + self.name + "\""

        for param in self.parameters:
            if param.value is None:
                continue
            if isinstance(param, (ParameterRaster, ParameterVector)):
                value = param.value
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
                values = param.value.split(",")
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
            if isinstance(out, OutputTable):
                filename = out.value
                if not filename.endswith(".dbf"):
                    filename += ".dbf"
                    out.value = filename
                command+=(" -" + out.name + " \"" + filename + "\"");

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
        #=======================================================================
        # loglines = []
        # loglines.append("SAGA execution commands")
        # for line in commands:
        #    progress.setCommand(line)
        #    loglines.append(line)
        # if SextanteConfig.getSetting(SagaUtils.SAGA_LOG_COMMANDS):
        #    SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)
        #=======================================================================
        executeSaga(progress);


    def resampleRasterLayer(self,layer):
        '''this is supposed to be run after having exported all raster layers'''
        if layer in self.exportedLayers.keys():
            inputFilename = self.exportedLayers[layer]
        else:
            inputFilename = layer
        destFilename = gettempfilename("sgrd")
        self.exportedLayers[layer]= destFilename
        if isWindows():
            s = "grid_tools \"Resampling\" -INPUT \"" + inputFilename + "\" -TARGET 0 -SCALE_UP_METHOD 4 -SCALE_DOWN_METHOD 4 -USER_XMIN " +\
                str(self.xmin) + " -USER_XMAX " + str(self.xmax) + " -USER_YMIN " + str(self.ymin) + " -USER_YMAX "  + str(self.ymax) +\
                " -USER_SIZE " + str(self.cellsize) + " -USER_GRID \"" + destFilename + "\""
        else:
            s = "libgrid_tools \"Resampling\" -INPUT \"" + inputFilename + "\" -TARGET 0 -SCALE_UP_METHOD 4 -SCALE_DOWN_METHOD 4 -USER_XMIN " +\
                str(self.xmin) + " -USER_XMAX " + str(self.xmax) + " -USER_YMIN " + str(self.ymin) + " -USER_YMAX "  + str(self.ymax) +\
                " -USER_SIZE " + str(self.cellsize) + " -USER_GRID \"" + destFilename + "\""
        return s


    def exportRasterLayer(self, layer):
        destFilename = gettempfilename("sgrd")
        self.exportedLayers[layer]= destFilename
        if isWindows():
            return "io_gdal 0 -GRIDS \"" + destFilename + "\" -FILES \"" + layer+"\""
        else:
            return "libio_gdal 0 -GRIDS \"" + destFilename + "\" -FILES \"" + layer + "\""








