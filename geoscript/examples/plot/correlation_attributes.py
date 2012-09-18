from geoscript.processing.sampledata import sampledata
from geoscript.plot import correlation
from geoscript.plot import attribute

if __name__ == '__main__':       
    layer = sampledata.get('heights')
    chart = correlation(attribute(layer, 'VALUE'), attribute(layer, 'VALUE'))
    chart.show()