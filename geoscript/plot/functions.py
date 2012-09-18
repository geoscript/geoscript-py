'''
Functions in this class returns generators than can be used as input for 
any of the method in the plot package that create chart.

This functions should simplify the creation of dataset when the data to
plot comes from a GeoScript layer or can be derived from it

Although most functions return generators, some might returns other data structure
like dicts or lists, depending on the kind of data being created
'''  

from geoscript.geom.point import Point
from com.vividsolutions.jts.operation.distance import DistanceOp
import math

def attribute(layer, attr):
    '''returns a generator with values of a given attribute of a given vector layer'''
    for feature in layer.features():
        yield  float(feature.get(attr))
        
def x(layer):
    '''returns a generator with x coordinates of features in a vector layer. 
    If the layer contains lines or polygons, the x coordinate of the centroid is used'''
    for feature in layer.features():
        yield  feature.geom.centroid.x
        
def y(layer):
    '''returns a generator with x coordinates of features in a vector layer. 
    If the layer contains lines or polygons, the x coordinate of the centroid is used'''
    for feature in layer.features():
        yield  feature.geom.centroid.x
        

def disttopoint(layer, x, y):
    '''returns a generator with distances from features in a vector layer to a given point'''
    pt = Point(x,y)
    for feature in layer.features():
        yield DistanceOp(pt, feature.geom).distance()    

def uniquecounts(layer, attr):
    '''returns a map with unique values as keys, and counts(number of times that unique value appears
    in the passed layer) as values''' 
    categories = {}
    for feature in layer.features():
        value = feature.get(attr)
        if value not in categories.keys():
            categories[value] = 1
        categories[value] += 1
    return categories
         
        
def frequency(data, nbins):  
    '''returns a frequency distribution of a data serie, divided in a given number of bins'''      
    datalist = list(data)
    lo = min(datalist)
    hi = max(datalist)
    binsize = (hi-lo)/(float(nbins))
    freq = [0] * nbins
    for d in datalist:
        bin = math.ceil((d - lo)/binsize) - 1
        freq[bin] += 1
    return freq

def histogram(layer, attr, nbins):
    
                                  