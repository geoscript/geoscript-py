from geoscript.processing.sampledata import sampledata
from geoscript.plot import *

if __name__ == '__main__':       
    layer = sampledata.get('landcover')                  
    chart = pie(uniquecounts(layer, 'LANDCOVER'))
    chart.show()