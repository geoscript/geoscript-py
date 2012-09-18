
from geoscript.processing.sampledata import sampledata
from geoscript.workspace.memory import Memory
from geoscript.feature.field import Field

'''An example that shows how to take values from a raster layer 
and put them into a points layer. For each point in the layer, 
the raster layer is queried, and the value at that point added to a
new attribute field.

'''

if __name__ == '__main__':       

    #open the origin layers
    points = sampledata.get('heights')
    raster = sampledata.get('dem')
    
    #create the output schema based on the input one
    fields = points.schema.fields
    fields.append(Field(raster.name, float))
    
    #create the output layer with the above schema
    ws = Memory()
    result = ws.create('result', fields)
    
    #add features with sampled values
    i = 0
    for feature in points.features():        
        pt = feature.geom.getCoordinates()[0]            
        value = raster.getvalueatcoord(pt.x, pt.y, 0)
        values = feature.values()
        values.append(value)
        result.add(values)

    