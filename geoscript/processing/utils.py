import os
import java
import tempfile

def isWindows():
    name = java.lang.System.getProperty( "os.name" )
    return "windows" in name.lower()

def isMac():
    name = java.lang.System.getProperty( "os.name" )
    return "mac" in name.lower()

def userFolder():
    userfolder = os.path.expanduser("~") + os.sep + "geoscript"
    mkdir(userfolder)

    return userfolder

def mkdir(newdir):
    if os.path.isdir(newdir):
        pass
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        if tail:
            os.mkdir(newdir)

def tempfolder():
    tempfolder = os.path.expanduser("~") + os.sep + "geoscript" + os.sep + "tempdata"
    mkdir(tempfolder)

    return tempfolder
    

NUM_LAYERS_SAVED = 1

def gettempfilename(ext=None, path=None):
    if path is None:
        path = tempfolder()    
    if ext is None:
        suffix = None
    else:
        suffix = "." + ext
    filename = tempfile.NamedTemporaryFile(suffix=suffix, dir=path).name
    return filename
