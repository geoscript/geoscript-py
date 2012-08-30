import os
import time
import sys

def isWindows():
    return os.name =="nt"

def isMac():
    return sys.platform == "darwin"

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

def gettempfilename(ext):
    path = tempfolder()
    filename = path + os.sep + str(time.time()) + str(NUM_LAYERS_SAVED) + "." + ext
    NUM_LAYERS_SAVED += 1
    return filename
