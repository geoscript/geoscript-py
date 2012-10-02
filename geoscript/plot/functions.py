'''
Functions in this class returns iterables than can be used as input for 
any of the method in the plot package that create chart.

This functions should simplify the creation of dataset when the data to
plot comes from a GeoScript layer or can be derived from it

For now, all this functions work with vector layers, althought they might be adapted
to use also raster ones
'''  

from geoscript.geom.point import Point
from com.vividsolutions.jts.operation.distance import DistanceOp
import math

def attribute(layer, attr, filter=None):
    '''returns a generator with values of a given attribute of a given vector layer'''
    for feature in layer.features(filter):
        yield  float(feature.get(attr))
        
def attributes(layer, attrs, filter=None):
    '''returns a generator with values of a given set of attribute of a given vector layer.
    The generator contain tuples with as many values as attribute names were passed'''
    for feature in layer.features(filter):
        yield tuple(float(feature.get(attr)) for attr in attrs)   

def attributesasdict(layer, attrs, filter=None):
    '''returns a dict with attribute names as keys and lists of values for each parameter as values'''
    ret = {}
    for attr in attrs:
        ret[attr] = []
    for feature in layer.features(filter):
        for attr in attrs:
            ret[attr].append(feature.get(attr))               
    return ret

def x(layer, filter=None):
    '''returns a generator with x coordinates of features in a vector layer. 
    If the layer contains lines or polygons, the x coordinate of the centroid is used'''
    for feature in layer.features(filter):
        yield  feature.geom.centroid.x
        
def y(layer, filter=None):
    '''returns a generator with y coordinates of features in a vector layer. 
    If the layer contains lines or polygons, the y coordinate of the centroid is used'''
    for feature in layer.features(filter):
        yield  feature.geom.centroid.x
        
def xy(layer, filter=None):
    '''returns a generator with x coordinates of features in a vector layer. 
    If the layer contains lines or polygons, the x coordinate of the centroid is used'''
    for feature in layer.features(filter):
        centroid = feature.geom.centroid 
        yield  (centroid.x, centroid.y)        
        

def disttopoint(layer, x, y, filter=None):
    '''returns a generator with distances from features in a vector layer to a given point'''
    pt = Point(x,y)
    for feature in layer.features(filter):
        yield DistanceOp(pt, feature.geom).distance()    

def uniquecounts(layer, attr, filter=None):
    '''returns a dict with unique values as keys, and counts(number of times that unique value appears
    in the passed layer) as values''' 
    categories = {}
    for feature in layer.features(filter):
        value = feature.get(attr)
        if value not in categories.keys():
            categories[value] = 1
        categories[value] += 1
    return categories
         
        
def frequency(data, nbins):  
    '''returns a frequency distribution of a data series, divided in a given number of bins.
    the distribution is returned as a list of tuples in the form (bin_center, frequency)'''      
    datalist = list(data)
    lo = min(datalist)
    hi = max(datalist)
    binsize = (hi-lo)/(float(nbins))
    freq = [0] * nbins
    for d in datalist:
        bin = int(math.ceil((d - lo)/binsize) - 1)
        freq[bin] += 1
    ret = []
    i = 0
    for f in freq:
        center = binsize / 2 + binsize * i
        ret.append((center,f))
        i += 1
    return ret


def summarize(layer, keyattr, attrs, op='sum',  filter=None):
    '''Summarizes a layer according to the classes defined by a given attribute.
    Operation to performed has to be selected from 'sum', 'max, 'min', 'avg'
    Attributes to compute the selected operation on are passed as a list with attribute names.
    Returns a dict with category values as keys, and another dict as values. This second dict
    has attribute names as keys and the selected statistical value fr each attribute as values'''
    categories = {}
    count = 0
    for feature in layer.features(filter):
        cat = feature.get(keyattr)        
        if cat not in categories.keys():
            categories[cat] = {} 
            for attr in attrs:
                categories[cat][attr] = 0
        for attr in attrs:
            value = feature.get(attr)
            if op == 'sum' or op == 'mean':
                categories[cat][attr] += value
            if op == 'min':
                categories[cat][attr] = min(value, categories[cat][attr])                
            if op == 'max':
                categories[cat][attr] = max(value, categories[cat][attr])
        count += 1                
            
    if op == 'mean':
        for cat in categories.keys():
            for attr in categories[cat].keys():
                categories[cat][attr] = categories[cat][attr]/float(count)  
    
    return categories
    