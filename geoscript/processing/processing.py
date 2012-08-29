from geoscript.processing.geotools import GeotoolsProvider

'''This module is the entry point to geoprocessing capabilities in GeoScript.
Ideally, a user should be able to perform geodata analysis just calling methods
from this module from a geoscript console'''
    
#The list of providers whose processes are available to be run or queried
providers = [GeotoolsProvider()];
    

def processes(text=None):
    '''
    Prints a list of all available processes, with name and description. 
    
    If the *text* parameter is used, it will only print those processes that
    include the passed text in either their name or their description.
    '''

    for provider in providers:
        sortedlist = sorted(provider.processes(), key= lambda process: process.name)
        for process in sortedlist:
            if text == None or text.lower() in process.name.lower() or text.lower() in process.description.lower():
                print (process.name.ljust(30, "-") + "--->" + process.description)


def processhelp(name):
    '''
    Prints information about parameters needed by a process and the outputs
    it generates.
    '''
    process = getprocess(name)
    if process is not None:
        print(str(process))
    else:
        print "ERROR: Process not found"

def getprocess(name):
    '''
    Returns a process based on its name.
    
    The *name* parameter is as a colon delimited string in the form namespace:name
        
    Returns None if there is not a process with that name
    '''
    for provider in providers:        
        process = provider.lookup(name)
        if process is not None: 
            return process
        