from geoscript.processing.sampledata import sampledata
from geoscript.plot import attribute
from geoscript.plot.regression import linearregression

if __name__ == '__main__':       
    layer = sampledata.get('heights')
    chart = linearregression(attribute(layer, 'VALUE'), attribute(layer, 'VALUE'))
    chart.show()