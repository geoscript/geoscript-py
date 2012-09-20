from geoscript.plot import *
from geoscript.processing.sampledata import sampledata

if __name__ == '__main__':  
    
    layer = sampledata.get('heights')    
    chart = scatterplot(xy(layer))
    chart.show()
        