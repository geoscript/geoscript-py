from geoscript.plot import *
from geoscript.processing.sampledata import sampledata

if __name__ == '__main__':  
    
    layer = sampledata.get('heights') 
    x, y = zip(*xy(layer))       
    chart = scatterplot(list(x), list(y))
    chart.show()
        