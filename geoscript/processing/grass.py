import os
from geoscript.processing.process import Process
from geoscript.processing.provider import ProcessProvider
import subprocess
import stat
import shutil
from geoscript.processing.utils import userFolder, mkdir, isWindows, isMac
from geoscript.processing.outputs import getoutputfromstring, OutputFile,\
    OutputRaster, OutputVector
from geoscript.processing.parameters import getparameterfromstring,\
    ParameterExtent, ParameterNumber, ParameterRaster, ParameterVector,\
    ParameterTable, ParameterMultipleInput, ParameterBoolean, ParameterSelection
import time

def grassBatchJobFilename():
    '''This is used in linux. This is the batch job that we assign to
    GRASS_BATCH_JOB and then call GRASS and let it do the work'''
    filename = "grass_batch_job.sh";
    batchfile = userFolder() + os.sep + filename
    return batchfile

def grassScriptFilename():
    '''this is used in windows. We create a script that initializes
    GRASS and then uses grass commands'''
    filename = "grass_script.bat";
    filename = userFolder() + os.sep + filename
    return filename

def grassDescriptionsFile():
    return os.path.join(os.path.dirname(__file__), "..", "..", "data", "grass_descriptions.txt")
   
def grassPath():
    return os.environ['GRASS_BIN_PATH']

def grassWinShellPath():
    return os.environ['GRASS_SHELL_PATH']

def isLatLon():
    ##TODO: change this!!!
    return False

def createGrassScript(commands):
    folder = grassPath()
    shell = grassWinShellPath()

    script = grassScriptFilename()
    gisrc =  userFolder() + os.sep + "sextante.gisrc"

    #temporary gisrc file
    output = open(gisrc, "w")
    location = "temp_location"
    mapset = "user"
    gisdbase = os.path.join(os.path.expanduser("~"), "sextante", "tempdata", "grassdata")
    output.write("GISDBASE: " + gisdbase + "\n");
    output.write("LOCATION_NAME: " + location + "\n");
    output.write("MAPSET: " + mapset + "\n");
    output.write("GRASS_GUI: text\n");
    output.close();

    output=open(script, "w")
    output.write("set HOME=" + os.path.expanduser("~") + "\n");
    output.write("set GISRC=" + gisrc + "\n")
    output.write("set GRASS_SH=" + shell + "\\bin\\sh.exe\n")
    output.write("set PATH=" + shell + os.sep + "bin;" + shell + os.sep + "lib;" + "%PATH%\n")
    output.write("set WINGISBASE=" + folder + "\n")
    output.write("set GISBASE=" + folder + "\n");
    output.write("set GRASS_PROJSHARE=" + folder + os.sep + "share" + os.sep + "proj" + "\n")
    output.write("set GRASS_MESSAGE_FORMAT=gui\n")
    #Replacement code for etc/Init.bat
    output.write("if \"%GRASS_ADDON_PATH%\"==\"\" set PATH=%WINGISBASE%\\bin;%WINGISBASE%\\lib;%PATH%\n")
    output.write("if not \"%GRASS_ADDON_PATH%\"==\"\" set PATH=%WINGISBASE%\\bin;%WINGISBASE%\\lib;%GRASS_ADDON_PATH%;%PATH%\n")
    output.write("\n")
    output.write("set GRASS_VERSION=" + getGrassVersion() + "\n");
    output.write("if not \"%LANG%\"==\"\" goto langset\n");
    output.write("FOR /F \"usebackq delims==\" %%i IN (`\"%WINGISBASE%\\etc\\winlocale\"`) DO @set LANG=%%i\n");
    output.write(":langset\n")
    output.write("\n")
    output.write("set PATHEXT=%PATHEXT%;.PY\n")
    output.write("set PYTHONPATH=%PYTHONPATH%;%WINGISBASE%\\etc\\python;%WINGISBASE%\\etc\\wxpython\\n");
    output.write("\n")
    output.write("g.gisenv.exe set=\"MAPSET=" + mapset + "\"\n")
    output.write("g.gisenv.exe set=\"LOCATION=" + location + "\"\n")
    output.write("g.gisenv.exe set=\"LOCATION_NAME=" + location + "\"\n")
    output.write("g.gisenv.exe set=\"GISDBASE=" + gisdbase + "\"\n")
    output.write("g.gisenv.exe set=\"GRASS_GUI=text\"\n")
    for command in commands:
        output.write(command + "\n")
    output.write("\n");
    output.write("exit\n");
    output.close();


def createGrassBatchJobFileFromGrassCommands(commands):
    fout = open(grassBatchJobFilename(), "w")
    for command in commands:
        fout.write(command + "\n")
    fout.write("exit")
    fout.close()

def grassMapsetFolder():
    tempfolder = os.path.join(os.path.expanduser("~"), "sextante", "tempdata", "grassdata", "temp_location")
    mkdir(tempfolder)
    return tempfolder

def createTempMapset(latlon):
    '''Creates a temporary location and mapset(s) for GRASS data processing. A minimal set of folders and files is created in the
     system's default temporary directory. The settings files are written with sane defaults, so GRASS can do its work. File
    structure and content will vary slightly depending on whether the user wants to process lat/lon or x/y data.'''

    folder = grassMapsetFolder()
    mkdir(os.path.join(folder, "PERMANENT"))
    mkdir(os.path.join(folder, "user"))
    mkdir(os.path.join(folder, "PERMANENT", ".tmp"))
    writeGrassWindow(os.path.join(folder, "PERMANENT", "DEFAULT_WIND"));
    outfile = open(os.path.join(folder, "PERMANENT", "MYNAME"), "w")
    if not latlon:
        outfile.write("SEXTANTE GRASS interface: temporary x/y data processing location.\n");
    else:
        outfile.write("SEXTANTE GRASS interface: temporary lat/lon data processing location.\n");
    outfile.close();
    if latlon:
        outfile = open(os.path.join(folder, "PERMANENT", "PROJ_INFO"), "w")
        outfile.write("name: Latitude-Longitude\n")
        outfile.write("proj: ll\n")
        outfile.write("ellps: wgs84\n")
        outfile.close()
        outfile = open(os.path.join(folder, "PERMANENT", "PROJ_UNITS"), "w")
        outfile.write("unit: degree\n");
        outfile.write("units: degrees\n");
        outfile.write("meters: 1.0\n");
        outfile.close();
    writeGrassWindow(os.path.join(folder, "PERMANENT", "WIND"));
    mkdir(os.path.join(folder, "user", "dbf"))
    mkdir(os.path.join(folder, "user", ".tmp"))
    outfile = open(os.path.join(folder, "user", "VAR"), "w")
    outfile.write("DB_DRIVER: dbf\n");
    outfile.write("DB_DATABASE: $GISDBASE/$LOCATION_NAME/$MAPSET/dbf/\n");
    outfile.close()
    writeGrassWindow(os.path.join(folder, "user", "WIND"), latlon);

def writeGrassWindow(filename, latlon):
    out = open(filename, "w")       
    if not latlon:
        out.write("proj:       0\n");
        out.write("zone:       0\n");
        out.write("north:      1\n");
        out.write("south:      0\n");
        out.write("east:       1\n");
        out.write("west:       0\n");
        out.write("cols:       1\n");
        out.write("rows:       1\n");
        out.write("e-w resol:  1\n");
        out.write("n-s resol:  1\n");
        out.write("top:        1\n");
        out.write("bottom:     0\n");
        out.write("cols3:      1\n");
        out.write("rows3:      1\n");
        out.write("depths:     1\n");
        out.write("e-w resol3: 1\n");
        out.write("n-s resol3: 1\n");
        out.write("t-b resol:  1\n");
    else:
        out.write("proj:       3\n");
        out.write("zone:       0\n");
        out.write("north:      1N\n");
        out.write("south:      0\n");
        out.write("east:       1E\n");
        out.write("west:       0\n");
        out.write("cols:       1\n");
        out.write("rows:       1\n");
        out.write("e-w resol:  1\n");
        out.write("n-s resol:  1\n");
        out.write("top:        1\n");
        out.write("bottom:     0\n");
        out.write("cols3:      1\n");
        out.write("rows3:      1\n");
        out.write("depths:     1\n");
        out.write("e-w resol3: 1\n");
        out.write("n-s resol3: 1\n");
        out.write("t-b resol:  1\n");
    out.close()


def executeGrass(commands):
    if isWindows():
        createGrassScript(commands)
        command = ["cmd.exe", "/C ", grassScriptFilename()]
    else:
        gisrc =  userFolder() + os.sep + "sextante.gisrc"
        os.putenv("GISRC", gisrc)
        os.putenv("GRASS_MESSAGE_FORMAT", "gui")
        os.putenv("GRASS_BATCH_JOB", grassBatchJobFilename())
        createGrassBatchJobFileFromGrassCommands(commands)
        os.chmod(grassBatchJobFilename(), stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        if isMac():
            command = grassPath() + os.sep + "grass.sh " + grassMapsetFolder() + "/user"
        else:
            command = "grass64 " + grassMapsetFolder() + "/user"
    loglines = []
    loglines.append("GRASS execution console output")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True).stdout
    for line in iter(proc.readline, ""):
        if "GRASS_INFO_PERCENT" in line:
            try:
                percentage = int(line[len("GRASS_INFO_PERCENT")+ 2:])
            except:
                pass
        else:
            pass        
    shutil.rmtree(grassMapsetFolder(), True)

def getGrassVersion():
    #I do not know if this should be removed or let the user enter it
    #or something like that... This is just a temporary thing
    return "6.4.0"


class GrassProvider(ProcessProvider):

    def __init__(self):
        ProcessProvider.__init__(self)


    def loadprocesses(self):
        file = grassDescriptionsFile()
        lines = open(file)   
        s = ""     
        for line in lines:            
            if not line.startswith("----"):
                s += line
            else:                
                alg = GrassProcess(s)
                if alg.name.strip() != "":
                    self._processes.append(alg)                    
                s = ""
    
    def name(self):
        return "GRASS"





class GrassProcess(Process):
    
    ExportedLayers = 0;

    GRASS_REGION_EXTENT_PARAMETER = "region"
    GRASS_REGION_CELLSIZE_PARAMETER = "regioncellsize"

    def __init__(self, text):
        Process.__init__(self)        
        self.defineCharacteristicsFromText(text)        

    def defineCharacteristicsFromText(self, text):
        self.inputs = {}
        self.outputs = {}    
        lines = text.split("\n")            
        self.name = "grass:" +  lines[0].strip("\n").strip()
        desc =  lines[1].strip("\n").strip()
        self.grassname = desc[:desc.find(" ")]         
        self.description = desc[desc.find(" ") + 2:]      
        for i in range(3,len(lines)):                
            line = lines[i].strip("\n").strip()
            if line.startswith("Parameter"):
                param = getparameterfromstring(line)
                self.inputs[param.name] = param
            elif line == "":
                break
            else:
                output = getoutputfromstring(line)
                self.outputs[output.name] = output   
        
        param = ParameterExtent(self.GRASS_REGION_EXTENT_PARAMETER, "Region extent", "0,1,0,1")
        self.inputs[param.name] = param
        param = ParameterNumber(self.GRASS_REGION_CELLSIZE_PARAMETER, "Region cellsize", 0, None, 1.0)
        self.inputs[param.name] = param  


    def _run(self):
        if isWindows():
            path = grassPath()
            if path == "":
                raise Exception("GRASS folder is not configured.\nPlease configure it before running GRASS algorithms.")

        commands = []
        self.exportedLayers = {}
        
        region = str(self.getParameterValue(self.GRASS_REGION_EXTENT_PARAMETER))
        regionCoords = region.split(",")
        createTempMapset(isLatLon());

        command = "g.region"
        command += " n=" + str(regionCoords[3])
        command +=" s=" + str(regionCoords[2])
        command +=" e=" + str(regionCoords[1])
        command +=" w=" + str(regionCoords[0])
        command +=" res=" + str(self.inputs[self.GRASS_REGION_CELLSIZE_PARAMETER].value)
        commands.append(command)

        #1: Export layer to grass mapset
        for param in self.inputs.values():
            if isinstance(param, ParameterRaster):
                if param.value == None:
                    continue
                value = param.value
                commands.append(self.exportRasterLayer(param.asfile()))
            if isinstance(param, ParameterVector):
                if param.value == None:
                    continue
                value = param.value
                commands.append(self.exportVectorLayer(param.asfile()))
            if isinstance(param, ParameterTable):
                pass
            if isinstance(param, ParameterMultipleInput):
                if param.value == None:
                    continue
                layers = param.asfiles()
                if layers == None or len(layers) == 0:
                    continue
                if param.datatype == ParameterMultipleInput.TYPE_RASTER:
                    for layer in layers:
                        commands.append(self.exportRasterLayer(layer))
                elif param.datatype == ParameterMultipleInput.TYPE_VECTOR_ANY:
                    for layer in layers:
                        commands.append(self.exportVectorLayer(layer))

        #2: set parameters and outputs
        command = self.grassname
        for param in self.inputs.values():
            if param.value == None:
                continue
            if param.name == self.GRASS_REGION_CELLSIZE_PARAMETER or param.name == self.GRASS_REGION_EXTENT_PARAMETER:
                continue
            if isinstance(param, (ParameterRaster, ParameterVector)):
                value = param.value
                if value in self.exportedLayers.keys():
                    command+=(" " + param.name + "=" + self.exportedLayers[value])
                else:
                    command+=(" " + param.name + "=" + value)
            elif isinstance(param, ParameterMultipleInput):
                s = param.value
                for layer in self.exportedLayers.keys():
                    s = s.replace(layer, self.exportedLayers[layer])
                s = s.replace(";",",")
                command+=(" " + param.name + "=" + s);
            elif isinstance(param, ParameterBoolean):
                if param.value:
                    command += (" " + param.name)
            elif isinstance(param, ParameterSelection):
                idx = int(param.value)
                command+=(" " + param.name + "=" + str(param.options[idx]));
            else:
                command+=(" " + param.name + "=" + str(param.value));

        for out in self.outputs.values():
            if isinstance(out, OutputFile):
                command+=(" " + out.name + "=\"" + out.value + "\"");
            else:
                command+=(" " + out.name + "=" + out.name);

        command += " --overwrite"
        commands.append(command)

        #3:Export resulting layers to a format that qgis can read
        for out in self.outputs.values():
            if isinstance(out, OutputRaster):
                filename = out.value
                #Raster layer output: adjust region to layer before exporting
                commands.append("g.region rast=" + out.name)
                command = "r.out.gdal -c createopt=\"TFW=YES,COMPRESS=LZW\""
                command += " input="
                command += out.name
                command += " output=\"" + filename + "\""
                commands.append(command)
            if isinstance(out, OutputVector):
                command = "v.out.ogr -ce input=" + out.name
                command += " dsn=\"" + os.path.dirname(out.value) + "\""
                command += " format=ESRI_Shapefile"
                command += " olayer=" + os.path.basename(out.value)[:-4]
                command += " type=auto"
                commands.append(command)

        #4 Run GRASS)
        executeGrass(commands);


    def exportVectorLayer(self, orgFilename):
        destFilename = self.getTempFilename()
        self.exportedLayers[orgFilename]= destFilename
        command = "v.in.ogr"
        command += " min_area=-1"
        command +=" dsn=\"" + os.path.dirname(orgFilename) + "\""
        command +=" layer=" + os.path.basename(orgFilename)[:-4]
        command +=" output=" + destFilename;
        command +=" --overwrite -o"
        return command


    def exportRasterLayer(self, layer):
        destFilename = self.getTempFilename()
        self.exportedLayers[layer]= destFilename
        command = "r.in.gdal"
        command +=" input=\"" + layer + "\""
        command +=" band=1"
        command +=" out=" + destFilename;
        command +=" --overwrite -o"
        return command


    def getTempFilename(self):
        filename =  "tmp" + str(time.time()).replace(".","") + str(self.ExportedLayers)
        self.ExportedLayers += 1
        return filename

