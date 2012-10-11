from geoscript.processing.sampledata import sampledata
from geoscript.plot import linearregression
from geoscript.plot import attribute
from geoscript.plot import disttopoint

if __name__ == '__main__':       
    layer = sampledata.get('heights')    
    pt = layer.features().next().geom.centroid            
    chart = linearregression(disttopoint(layer, pt.x, pt.y), attribute(layer, 'VALUE'))
    chart.savepng("d:\\chart.png")
    chart.show()