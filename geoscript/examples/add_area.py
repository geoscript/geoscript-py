
from geoscript.processing.sampledata import sampledata

'''An example that show how to add a new attribute containing area measurements
to a polygon vector layer'''

from geoscript.feature.field import Field
from geoscript.workspace.memory import Memory

if __name__ == '__main__':       
    #open the origin layer
    layer = sampledata.get('landcover')
    
    #create the output schema based on the input one
    fields = layer.schema.fields
    fields.append(Field('area,', float))
    
    #create the output layer with the above schema
    ws = Memory()
    result = ws.create('result', fields)
    
    #add features with additional area field
    for feature in layer.features():
        area = feature.geom.area
        values = feature.values()
        values.append(area)
        result.add(values)
        print str(values)
        
    
