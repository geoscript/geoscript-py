
from geoscript.processing.sampledata import sampledata

'''An example that takes a vector layer and creates a set of n new vector layers in a given folder,
each of them containing only features with the the same value for a selected field.
n is the number of unique values for the selected field'''


from geoscript.feature.field import Field
from geoscript.workspace.memory import Memory
import os
from geoscript.workspace.directory import Directory

if __name__ == '__main__':
    
    # set the output folder and create it if it does not exist
    FOLDER = os.path.expanduser('~') + os.sep + 'geoscript' \
        + os.sep + 'explode_to_files'
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
        
    #set the field to use
    FIELD = 'LANDCOVER'
        
    #open the origin layer
    layer = sampledata.get('landcover')
    
    fields = layer.schema.fields
    
    #create the output layer with the above schema
    ws = Directory(FOLDER)    

    #the input layers to create. keys are classnames (the unique values in the selected field)    
    layers = {}
    
    for feature in layer.features():
        classname = feature.get(FIELD)
        if not classname in layers.keys():
            #NOTE: we assume the classname is ok for creating a valid filename, but a robust solution
            #should check for non-ascii chars and similar elements that might not be suitable
            #and cause problems
            layers[classname] = ws.create(str(classname), layer.schema.fields)
        layers[classname].add(feature.values()) 

    
