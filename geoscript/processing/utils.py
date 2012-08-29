''' the :mod:`utils` module contains methods to easily convert between several ways 
of representing a given type of input. These methods should be used by processes to provide
a transparent access to them , so users can call their run() method transparently without
having to worry about the format of the input object to use.

It also contains method for handling outputs and managing temporary files'''  

import os
import time
import sys

def asvectorlayer(obj):
    pass

def asrasterlayer(obj):
    pass

def asnumber(obj):
    pass

def asboolean(obj):
    pass

def asstring(obj):
    pass

def asfile(obj):
    pass

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
