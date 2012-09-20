from geoscript.plot import *
from geoscript.processing.sampledata import sampledata

'''An example that plots a semivariogram cloud'''
import math
import random

if __name__ == '__main__':      
    layer = sampledata.get('heights') 
    semivar = []
    i= 0
    for feature in layer.features():
        pt1 = feature.geom.getCoordinates()[0]
        value1 = feature.get('VALUE')
        i2 = 0         
        for feature2 in layer.features():
            if i2 > i:
                pt2 = feature2.geom.getCoordinates()[0]
                value2 = feature2.get('VALUE')
                semivar.append((pt1.distance(pt2), math.pow(value2-value1,2.)))
            i2 += 1
        i+=1               
    # we do not plot all points, as that would mean a large                                     
    chart = scatterplot(semivar)
    chart.show()
        