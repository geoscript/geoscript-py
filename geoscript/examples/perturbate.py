
from geoscript.processing.sampledata import sampledata
from geoscript.workspace.memory import Memory
import math
from geoscript.geom.point import Point
import random
from geoscript.render import draw

'''An example that shows how to randomly perturbate a points layer.
The resulting layer contains the same attributes but displaced geometries
instead of the original ones.

Displacement angles are random. Displacement distances follow a normal distribution
with a given mean and stddev
'''

if __name__ == '__main__':       
    MEAN = 10
    STD = 5
    #open the origin layer
    layer = sampledata.get('heights')
    
    #create the output layer with the same schema as the input
    ws = Memory()
    result = ws.create('result', layer.schema.fields)
        
    #add features with displaced geometries
    i = 0
    for feature in layer.features():        
        pt = feature.geom.getCoordinates()[0]
        dist = random.normalvariate(MEAN, STD)
        angle = random.random() * math.pi * 2.
        displaced = Point(pt.x + math.sin(angle) * dist, pt.y + math.cos(angle) * dist)        
        feature.setgeom(displaced)        
        result.add(feature)
        
    draw(result)
    
